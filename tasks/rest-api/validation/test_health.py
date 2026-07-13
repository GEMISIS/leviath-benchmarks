"""Health check endpoint tests."""
import pytest


class TestHealth:
    """Tests for GET /api/health."""

    def test_health_returns_200(self, client):
        """GET /api/health returns 200."""
        resp = client.get("/api/health")
        assert resp.status_code == 200

    def test_health_no_auth_required(self, client):
        """Health endpoint works without any authorization header."""
        resp = client.get("/api/health")
        assert resp.status_code == 200

    def test_health_returns_json(self, client):
        """Health response is JSON and contains a status field."""
        resp = client.get("/api/health")
        assert resp.content_type is not None
        assert "application/json" in resp.content_type
        data = resp.get_json()
        assert data is not None
        # Should have a "status" key (common convention)
        assert "status" in data
