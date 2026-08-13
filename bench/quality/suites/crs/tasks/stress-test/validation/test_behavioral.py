"""
Behavioral validation tests — all tests go through HTTP API.

These tests verify the OBSERVABLE BEHAVIOR of the system through
the REST API endpoints. They do not depend on internal implementation
details or specific class structures.

Tests are organized by category and map to requirements in the spec files.
"""

import json
import time
import uuid
from datetime import datetime, timezone

import pytest

from conftest import make_event, make_auth_header


# ==========================================================================
# Category 1: API Endpoint Behaviors
# ==========================================================================


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
        """Spec: POST /api/v1/events/batch accepts up to 100 events.
        Spec: Request body is {"events": [...]}, always returns 200 at HTTP level."""
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
        resp = app_client.post("/api/v1/events/batch", json={"events": events}, headers=headers)
        assert resp.status_code == 200, \
            f"Batch ingestion should return 200, got {resp.status_code}"
        data = resp.get_json()
        assert data is not None, "Batch response should be JSON"
        assert "results" in data, "Batch response should contain 'results' array"

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
        resp = app_client.post("/api/v1/events/batch", json={"events": events}, headers=headers)
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


# ==========================================================================
# Category 2: Happy Path Event Processing
# ==========================================================================


class TestHappyPath:
    """Tests for successful event processing across all tenant tiers."""

    def test_free_tenant_event_processed(self, app_client, auth_header_factory):
        """Spec: Free tier tenants can process user.* and notification.* events."""
        event = make_event(
            tenant_id="tn-us-west-0099",
            event_type="user.created",
            source="web-app",
        )
        headers = auth_header_factory("startup-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code in (200, 201, 207), \
            f"Expected success for free tenant, got {resp.status_code}"

    def test_premium_tenant_event_processed(self, app_client, auth_header_factory):
        """Spec: Premium tenants can process all event types."""
        event = make_event(
            tenant_id="tn-us-east-0042",
            event_type="order.created",
            source="web-app",
            payload={"order_id": "ord_001", "amount": 99.99, "currency": "usd"},
        )
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code in (200, 201, 207), \
            f"Expected success for premium tenant, got {resp.status_code}"

    def test_pipeline_response_headers(self, app_client, auth_header_factory):
        """Spec: Response must include X-Request-ID, X-Tenant-ID, X-Processing-Time-Ms, X-Pipeline-Version."""
        event = make_event(
            tenant_id="tn-us-east-0042",
            event_type="user.created",
            source="web-app",
        )
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)

        required_headers = [
            "X-Request-ID",
            "X-Tenant-ID",
            "X-Processing-Time-Ms",
            "X-Pipeline-Version",
        ]
        for header in required_headers:
            # Check case-insensitively
            found = any(
                h.lower() == header.lower()
                for h in resp.headers.keys()
            )
            assert found, f"Missing required response header: {header}"

    def test_pipeline_version_header_value(self, app_client, auth_header_factory):
        """Spec: X-Pipeline-Version should be '2.3'."""
        event = make_event(
            tenant_id="tn-us-east-0042",
            event_type="user.created",
            source="web-app",
        )
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)

        version = resp.headers.get("X-Pipeline-Version", "")
        assert version == "2.3", f"Expected X-Pipeline-Version '2.3', got '{version}'"


# ==========================================================================
# Category 3: Schema Validation
# ==========================================================================


class TestSchemaValidation:
    """Tests for event schema validation per event-schema-spec.md."""

    def test_missing_required_fields_returns_400(self, app_client, auth_header_factory):
        """Spec: Missing required fields → 400."""
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"
        # Send event missing event_id and event_type
        resp = app_client.post("/api/v1/events", json={"tenant_id": "tn-us-east-0042"}, headers=headers)
        assert resp.status_code == 400, f"Expected 400 for missing fields, got {resp.status_code}"

    def test_invalid_tenant_id_format_returns_400(self, app_client, auth_header_factory):
        """Spec: Invalid tenant ID format → 400."""
        event = make_event(tenant_id="invalid-tenant-id")
        headers = auth_header_factory("admin-secret-key-2024")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code == 400, f"Expected 400 for invalid tenant_id, got {resp.status_code}"

    def test_unknown_tenant_returns_404(self, app_client, auth_header_factory):
        """Spec: Unknown tenant → 404."""
        event = make_event(tenant_id="tn-us-east-9999")
        headers = auth_header_factory("admin-secret-key-2024")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code == 404, f"Expected 404 for unknown tenant, got {resp.status_code}"

    def test_suspended_tenant_returns_202(self, app_client, auth_header_factory):
        """Spec: Suspended tenant → 202 with queuing."""
        event = make_event(
            tenant_id="tn-ap-south-0777",
            event_type="user.created",
            source="web-app",
        )
        headers = auth_header_factory("admin-secret-key-2024")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code == 202, f"Expected 202 for suspended tenant, got {resp.status_code}"

    def test_payload_too_large_for_free_tier(self, app_client, auth_header_factory):
        """Spec: Free tier payload limit is 64KB."""
        # Create payload > 64KB
        large_payload = {"data": "x" * (65 * 1024)}
        event = make_event(
            tenant_id="tn-us-west-0099",
            event_type="user.created",
            source="web-app",
            payload=large_payload,
        )
        headers = auth_header_factory("startup-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code in (400, 413, 422), \
            f"Expected 400/413/422 for oversized payload, got {resp.status_code}"

    def test_payload_within_premium_limit(self, app_client, auth_header_factory):
        """Spec: Premium tier payload limit is 1MB — 256KB should be fine."""
        medium_payload = {"data": "x" * (200 * 1024)}
        event = make_event(
            tenant_id="tn-us-east-0042",
            event_type="user.created",
            source="web-app",
            payload=medium_payload,
        )
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code in (200, 201, 207), \
            f"Expected success for payload within premium limit, got {resp.status_code}"

    def test_disallowed_event_category_for_free_tier(self, app_client, auth_header_factory):
        """Spec: Free tier only allows user.* and notification.* categories."""
        event = make_event(
            tenant_id="tn-us-west-0099",
            event_type="order.created",
            source="web-app",
        )
        headers = auth_header_factory("startup-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code in (400, 403, 422), \
            f"Expected rejection for disallowed category on free tier, got {resp.status_code}"

    def test_sdk_version_below_2_rejected(self, app_client, auth_header_factory):
        """Spec: sdk_version < 2.0.0 must be rejected."""
        event = make_event(
            tenant_id="tn-us-east-0042",
            event_type="user.created",
            source="web-app",
            sdk_version="1.9.0",
        )
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code in (400, 422), \
            f"Expected 400/422 for old SDK version, got {resp.status_code}"

    def test_invalid_correlation_id_rejected(self, app_client, auth_header_factory):
        """Spec: correlation_id must be valid UUID v4 when present."""
        event = make_event(
            tenant_id="tn-us-east-0042",
            event_type="user.created",
            source="web-app",
            correlation_id="not-a-valid-uuid",
        )
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code in (400, 422), \
            f"Expected 400/422 for invalid correlation_id, got {resp.status_code}"


# ==========================================================================
# Category 4: Idempotency
# ==========================================================================


class TestIdempotency:
    """Tests for idempotency window per pipeline-spec.md."""

    def test_duplicate_event_returns_409(self, app_client, auth_header_factory):
        """Spec: Duplicate idempotency_key within 24h → 409 Conflict."""
        idem_key = str(uuid.uuid4())
        event = make_event(
            tenant_id="tn-us-east-0042",
            event_type="user.created",
            source="web-app",
            idempotency_key=idem_key,
        )
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"

        # First request should succeed
        resp1 = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp1.status_code in (200, 201, 207), \
            f"First request should succeed, got {resp1.status_code}"

        # Second request with same idempotency key should be 409
        event2 = make_event(
            tenant_id="tn-us-east-0042",
            event_type="user.created",
            source="web-app",
            idempotency_key=idem_key,
        )
        resp2 = app_client.post("/api/v1/events", json=event2, headers=headers)
        assert resp2.status_code == 409, \
            f"Duplicate idempotency key should return 409, got {resp2.status_code}"

    def test_different_idempotency_keys_both_succeed(self, app_client, auth_header_factory):
        """Spec: Different idempotency keys are independent events."""
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"

        event1 = make_event(tenant_id="tn-us-east-0042", source="web-app")
        event2 = make_event(tenant_id="tn-us-east-0042", source="web-app")

        resp1 = app_client.post("/api/v1/events", json=event1, headers=headers)
        resp2 = app_client.post("/api/v1/events", json=event2, headers=headers)

        assert resp1.status_code in (200, 201, 207)
        assert resp2.status_code in (200, 201, 207)

    def test_idempotent_header_on_duplicate(self, app_client, auth_header_factory):
        """Spec: Duplicate response includes X-Idempotent: true header."""
        idem_key = str(uuid.uuid4())
        event = make_event(
            tenant_id="tn-us-east-0042",
            event_type="user.created",
            source="web-app",
            idempotency_key=idem_key,
        )
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"

        app_client.post("/api/v1/events", json=event, headers=headers)

        event2 = make_event(
            tenant_id="tn-us-east-0042",
            event_type="user.created",
            source="web-app",
            idempotency_key=idem_key,
        )
        resp2 = app_client.post("/api/v1/events", json=event2, headers=headers)
        idem_header = resp2.headers.get("X-Idempotent", "").lower()
        assert idem_header == "true", \
            f"Expected X-Idempotent: true on duplicate, got '{idem_header}'"


# ==========================================================================
# Category 5: Rate Limiting
# ==========================================================================


class TestRateLimiting:
    """Tests for hybrid token bucket + sliding window per rate-limit-spec.md."""

    def test_free_tenant_rate_limited(self, app_client, auth_header_factory):
        """Spec: Free tier rate limits: 10 events/sec, 500/min, burst capacity 20."""
        headers = auth_header_factory("startup-api-key-prod")
        headers["Content-Type"] = "application/json"

        results = []
        for i in range(25):
            event = make_event(
                tenant_id="tn-us-west-0099",
                event_type="user.created",
                source="web-app",
            )
            resp = app_client.post("/api/v1/events", json=event, headers=headers)
            results.append(resp.status_code)

        assert 429 in results, \
            "Free tier (10 eps, capacity 20) should be rate-limited after 20+ rapid events"

    def test_rate_limit_response_format(self, app_client, auth_header_factory):
        """Spec: Rate limit response includes Retry-After and error body."""
        headers = auth_header_factory("startup-api-key-prod")
        headers["Content-Type"] = "application/json"

        resp_429 = None
        for i in range(30):
            event = make_event(
                tenant_id="tn-us-west-0099",
                event_type="user.created",
                source="web-app",
            )
            resp = app_client.post("/api/v1/events", json=event, headers=headers)
            if resp.status_code == 429:
                resp_429 = resp
                break

        if resp_429 is not None:
            # Check for rate limit headers
            assert resp_429.headers.get("Retry-After") is not None or \
                resp_429.headers.get("X-Rate-Limit-Limit") is not None, \
                "429 response should include rate limit headers"

            body = resp_429.get_json()
            assert body is not None, "429 response should have JSON body"
            # Check for error structure
            assert "error" in body or "error_code" in body or "message" in body, \
                "429 body should contain error information"


# ==========================================================================
# Category 6: API Authentication
# ==========================================================================


class TestAPIAuth:
    """Tests for API authentication per api-spec.md."""

    def test_missing_auth_returns_401(self, app_client):
        """Spec: Missing Authorization header → 401."""
        event = make_event()
        resp = app_client.post(
            "/api/v1/events",
            json=event,
            headers={"Content-Type": "application/json"},
        )
        assert resp.status_code == 401, f"Expected 401 without auth, got {resp.status_code}"

    def test_invalid_key_returns_401(self, app_client):
        """Spec: Invalid API key → 401."""
        event = make_event()
        headers = make_auth_header("totally-wrong-key-12345")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code == 401, f"Expected 401 for invalid key, got {resp.status_code}"

    def test_valid_key_correct_tenant_succeeds(self, app_client, auth_header_factory):
        """Spec: Valid key + matching tenant → 200."""
        event = make_event(
            tenant_id="tn-us-east-0042",
            event_type="user.created",
            source="web-app",
        )
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code in (200, 201, 207), \
            f"Expected success for valid key + tenant, got {resp.status_code}"

    def test_cross_tenant_access_returns_403(self, app_client, auth_header_factory):
        """Spec: Cross-tenant access → 403 (not 404)."""
        # Acme key trying to access EuroTech tenant
        event = make_event(
            tenant_id="tn-eu-central-1337",
            event_type="user.created",
            source="erp-system",
        )
        headers = auth_header_factory("acme-api-key-prod")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code == 403, \
            f"Cross-tenant access should return 403, got {resp.status_code}"

    def test_admin_key_accesses_any_tenant(self, app_client, auth_header_factory):
        """Spec: Admin key (tenant_id='*') can access any tenant."""
        event = make_event(
            tenant_id="tn-eu-central-1337",
            event_type="user.created",
            source="erp-system",
        )
        headers = auth_header_factory("admin-secret-key-2024")
        headers["Content-Type"] = "application/json"
        resp = app_client.post("/api/v1/events", json=event, headers=headers)
        assert resp.status_code in (200, 201, 207), \
            f"Admin key should access any tenant, got {resp.status_code}"

    def test_health_endpoint_no_auth(self, app_client):
        """Spec: Health check endpoint needs no authentication."""
        resp = app_client.get("/api/v1/health")
        assert resp.status_code == 200, \
            f"Health endpoint should return 200 without auth, got {resp.status_code}"
