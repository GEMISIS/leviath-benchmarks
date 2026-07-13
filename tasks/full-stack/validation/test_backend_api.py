"""Tests for backend REST API endpoints."""

import os
import pytest

from conftest import WORKDIR, app


class TestBackendStructure:
    """Verify the backend directory and app are present."""

    def test_backend_directory_exists(self, workdir):
        """The backend/ directory must exist."""
        backend_dir = os.path.join(workdir, "backend")
        assert os.path.isdir(backend_dir), (
            f"Expected backend/ directory at {backend_dir}"
        )

    def test_backend_app_importable(self):
        """The FastAPI app must be importable from the backend package."""
        assert app is not None, (
            "Could not import FastAPI app from backend.app, backend.main, "
            "backend.src.app, or backend.src.main"
        )


@pytest.mark.asyncio
class TestBackendEndpoints:
    """Verify key REST endpoints exist and respond."""

    async def test_health_endpoint(self, async_client):
        """A health or status endpoint should return HTTP 200."""
        possible_paths = ["/health", "/api/health", "/status", "/api/status", "/"]
        found = False
        for path in possible_paths:
            resp = await async_client.get(path)
            if resp.status_code == 200:
                found = True
                break
        assert found, (
            "No health/status endpoint found returning 200 at any of: "
            + ", ".join(possible_paths)
        )

    async def test_preferences_endpoint_exists(self, async_client):
        """A notification preferences endpoint should exist."""
        possible_paths = [
            "/api/preferences",
            "/api/notification-preferences",
            "/api/notifications/preferences",
            "/preferences",
            "/api/users/1/preferences",
        ]
        found = False
        for path in possible_paths:
            resp = await async_client.get(path)
            # Accept any response that is not 404 (the endpoint exists even
            # if it returns 401/403/422 because of missing auth/params).
            if resp.status_code != 404:
                found = True
                break
        assert found, (
            "No preferences endpoint found (all returned 404) at: "
            + ", ".join(possible_paths)
        )

    async def test_notifications_endpoint_exists(self, async_client):
        """A notifications listing endpoint should exist."""
        possible_paths = [
            "/api/notifications",
            "/notifications",
            "/api/notifications/",
        ]
        found = False
        for path in possible_paths:
            resp = await async_client.get(path)
            if resp.status_code != 404:
                found = True
                break
        assert found, (
            "No notifications endpoint found (all returned 404) at: "
            + ", ".join(possible_paths)
        )

    async def test_create_notification_endpoint(self, async_client):
        """POST to the notifications endpoint should accept a notification."""
        possible_paths = [
            "/api/notifications",
            "/notifications",
            "/api/notifications/",
        ]
        payload = {
            "user_id": 1,
            "type": "comment",
            "priority": "medium",
            "title": "Test notification",
            "message": "This is a test notification",
        }
        found = False
        for path in possible_paths:
            resp = await async_client.post(path, json=payload)
            # Accept 200, 201, or 422 (validation error means endpoint exists
            # but expects different shape -- still counts as existing).
            if resp.status_code in (200, 201, 422):
                found = True
                if resp.status_code in (200, 201):
                    data = resp.json()
                    # Verify the response contains key fields.
                    assert "id" in data or "notification" in data, (
                        "Created notification response should contain 'id'"
                    )
                break
        assert found, (
            "No create-notification endpoint found at: "
            + ", ".join(possible_paths)
        )
