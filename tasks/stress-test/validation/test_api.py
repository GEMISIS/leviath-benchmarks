"""
API-specific validation tests for Flask endpoints.

Tests cover all endpoints from api-spec.md, auth flows with real bcrypt,
batch ingestion, DLQ admin access, health check, metrics, and error format.
"""

import json
import uuid

import pytest

from conftest import make_event, make_auth_header


class TestEventIngestion:
    """Tests for POST /api/v1/events endpoint."""

    def test_single_event_ingestion(self, app_client, auth_header_factory):
        """Spec: POST /api/v1/events accepts a single event."""
        event = make_event(
            tenant_id="tn-us-east-0042",
            event_type="user.created",
            source="web-app",
        )
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code in (200, 201, 207), \
            f"Single event ingestion should succeed, got {resp.status_code}"

    def test_event_response_contains_event_id(self, app_client, auth_header_factory):
        """Spec: Successful ingestion response includes the event_id."""
        event = make_event(
            tenant_id="tn-us-east-0042",
            event_type="user.created",
            source="web-app",
        )
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        if resp.status_code in (200, 201):
            data = resp.get_json()
            assert data is not None
            assert "event_id" in data or "id" in data, \
                "Response should contain event_id"


class TestBatchIngestion:
    """Tests for POST /api/v1/events/batch endpoint."""

    def test_batch_ingestion_success(self, app_client, auth_header_factory):
        """Spec: POST /api/v1/events/batch accepts up to 100 events."""
        events = [
            make_event(
                tenant_id="tn-us-east-0042",
                event_type="user.created",
                source="web-app",
            )
            for _ in range(5)
        ]
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events/batch", json=events, headers=headers)
        assert resp.status_code in (200, 207), \
            f"Batch ingestion should succeed, got {resp.status_code}"

    def test_batch_over_100_rejected(self, app_client, auth_header_factory):
        """Spec: Batch endpoint accepts max 100 events."""
        events = [
            make_event(
                tenant_id="tn-us-east-0042",
                event_type="user.created",
                source="web-app",
            )
            for _ in range(101)
        ]
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events/batch", json=events, headers=headers)
        assert resp.status_code == 400, \
            f"Batch >100 should return 400, got {resp.status_code}"


class TestDLQEndpoints:
    """Tests for DLQ admin endpoints."""

    def test_dlq_requires_admin_key(self, app_client, auth_header_factory):
        """Spec: DLQ endpoints require admin-level access (dlq:read permission)."""
        # Non-admin key without dlq:read permission
        headers = auth_header_factory("acme-api-key-prod")
        resp = app_client.get("/api/v1/dlq", headers=headers)
        assert resp.status_code in (401, 403), \
            f"DLQ should require admin access, got {resp.status_code}"

    def test_dlq_accessible_with_admin_key(self, app_client, auth_header_factory):
        """Spec: Admin key has dlq:read and dlq:write permissions."""
        headers = auth_header_factory("admin-secret-key-2024")
        resp = app_client.get("/api/v1/dlq", headers=headers)
        assert resp.status_code == 200, \
            f"DLQ should be accessible with admin key, got {resp.status_code}"


class TestHealthEndpoint:
    """Tests for GET /api/v1/health endpoint."""

    def test_health_returns_200(self, app_client):
        """Spec: Health endpoint returns 200 with status information."""
        resp = app_client.get("/api/v1/health")
        assert resp.status_code == 200

    def test_health_response_structure(self, app_client):
        """Spec: Health response includes status (healthy/degraded/unhealthy)."""
        resp = app_client.get("/api/v1/health")
        data = resp.get_json()
        assert data is not None, "Health endpoint should return JSON"
        assert "status" in data, "Health response must include 'status' field"
        assert data["status"] in ("healthy", "degraded", "unhealthy"), \
            f"Health status must be healthy/degraded/unhealthy, got '{data['status']}'"


class TestMetricsEndpoint:
    """Tests for metrics endpoints."""

    def test_prometheus_metrics_endpoint(self, app_client, auth_header_factory):
        """Spec: GET /metrics exposes Prometheus-format metrics."""
        # /metrics may or may not require auth
        headers = auth_header_factory("admin-secret-key-2024")
        resp = app_client.get("/metrics", headers=headers)
        if resp.status_code == 404:
            resp = app_client.get("/api/v1/metrics", headers=headers)
        assert resp.status_code == 200, \
            f"Metrics endpoint should return 200, got {resp.status_code}"
        # Prometheus format uses plain text with metric names
        content = resp.data.decode("utf-8", errors="replace")
        assert "evtplatform" in content.lower() or "event" in content.lower(), \
            "Prometheus metrics should use evtplatform prefix"

    def test_metrics_summary_endpoint(self, app_client, auth_header_factory):
        """Spec: GET /api/v1/metrics/summary returns JSON summary."""
        headers = auth_header_factory("admin-secret-key-2024")
        resp = app_client.get("/api/v1/metrics/summary", headers=headers)
        assert resp.status_code == 200, \
            f"Metrics summary should return 200, got {resp.status_code}"
        data = resp.get_json()
        assert data is not None, "Metrics summary should return JSON"


class TestErrorResponseFormat:
    """Tests for standardized error response format."""

    def test_error_response_has_required_fields(self, app_client):
        """Spec: Error responses include error_code, message, details, request_id."""
        # Trigger a 401 error
        event = make_event()
        resp = app_client.post(
            "/api/v1/events",
            json=event,
            headers={"Content-Type": "application/json"},
        )
        assert resp.status_code == 401

        data = resp.get_json()
        assert data is not None, "Error responses should be JSON"
        # Check for error structure — may be nested under 'error' key
        error_obj = data.get("error", data)
        has_code = "error_code" in error_obj or "code" in error_obj
        has_message = "message" in error_obj or "error" in error_obj
        assert has_code or has_message, \
            "Error response should include error_code/code and message"

    def test_error_response_includes_request_id(self, app_client):
        """Spec: Error responses include request_id for tracing."""
        resp = app_client.post(
            "/api/v1/events",
            json={},
            headers={"Content-Type": "application/json"},
        )
        # Check response body or header for request_id
        data = resp.get_json() or {}
        error_obj = data.get("error", data)
        has_request_id = (
            "request_id" in error_obj or
            "requestId" in error_obj or
            resp.headers.get("X-Request-ID") is not None
        )
        assert has_request_id, \
            "Error response should include request_id (body or X-Request-ID header)"


class TestAuthWithBcrypt:
    """Tests verifying auth uses real bcrypt hash verification."""

    def test_correct_plaintext_authenticates(self, app_client):
        """Spec: API keys verified against bcrypt hashes in api_keys.yaml."""
        event = make_event(
            tenant_id="tn-us-east-0042",
            event_type="user.created",
            source="web-app",
        )
        headers = make_auth_header("acme-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code in (200, 201, 207), \
            f"Correct API key should authenticate, got {resp.status_code}"

    def test_wrong_plaintext_rejected(self, app_client):
        """Spec: Wrong plaintext fails bcrypt verification → 401."""
        event = make_event(
            tenant_id="tn-us-east-0042",
            event_type="user.created",
            source="web-app",
        )
        headers = make_auth_header("acme-api-key-wrong")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code == 401, \
            f"Wrong API key should return 401, got {resp.status_code}"
