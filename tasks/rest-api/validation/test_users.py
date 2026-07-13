"""User CRUD endpoint tests."""
import pytest

from conftest import (
    auth_header,
    create_test_user,
    login,
    make_token,
)


class TestUsers:
    """Tests for /api/users endpoints."""

    def test_create_user_as_admin(self, client, admin_token):
        """POST /api/users with admin JWT and valid data returns 201."""
        resp = create_test_user(client, admin_token)
        assert resp.status_code == 201

    def test_create_user_without_auth(self, client):
        """POST /api/users without auth returns 401."""
        resp = client.post(
            "/api/users",
            json={
                "email": "noauth@example.com",
                "password": "Test1234!",
                "full_name": "No Auth",
                "role": "user",
            },
        )
        assert resp.status_code == 401

    def test_create_user_as_regular_user(self, client, admin_token):
        """Non-admin cannot create users (403)."""
        # First create a regular user
        create_test_user(client, admin_token, email="regular@example.com")

        # Login as regular user to get a valid token from the API, or use fixture
        user_token = make_token(user_id=2, email="regular@example.com", role="user")

        resp = client.post(
            "/api/users",
            json={
                "email": "another@example.com",
                "password": "Test1234!",
                "full_name": "Another User",
                "role": "user",
            },
            headers=auth_header(user_token),
        )
        assert resp.status_code == 403

    def test_get_user_by_id(self, client, admin_token):
        """GET /api/users/1 returns the admin user."""
        resp = client.get("/api/users/1", headers=auth_header(admin_token))
        assert resp.status_code == 200
        data = resp.get_json()
        assert data is not None
        # Should contain user information
        email = data.get("email") or (data.get("user", {}) or {}).get("email")
        assert email == "admin@example.com"

    def test_update_own_profile(self, client, admin_token):
        """PUT /api/users/:id as the owner succeeds."""
        # Create a user first
        create_resp = create_test_user(client, admin_token, email="owner@example.com")
        create_data = create_resp.get_json()
        # Try to extract the user id from the response
        user_id = (
            create_data.get("id")
            or create_data.get("user_id")
            or (create_data.get("user", {}) or {}).get("id")
            or 2
        )

        owner_token = make_token(user_id=user_id, email="owner@example.com", role="user")
        resp = client.put(
            f"/api/users/{user_id}",
            json={"full_name": "Updated Name"},
            headers=auth_header(owner_token),
        )
        assert resp.status_code in (200, 204)

    def test_update_other_user_as_non_admin(self, client, admin_token):
        """PUT /api/users/:id on another user's profile as non-admin returns 403."""
        # Try to update user 1 (admin) as a regular user
        user_token = make_token(user_id=999, email="rando@example.com", role="user")
        resp = client.put(
            "/api/users/1",
            json={"full_name": "Hacked Name"},
            headers=auth_header(user_token),
        )
        assert resp.status_code == 403

    def test_delete_user_as_admin(self, client, admin_token):
        """DELETE /api/users/:id as admin succeeds."""
        # Create a user to delete
        create_resp = create_test_user(client, admin_token, email="deleteme@example.com")
        create_data = create_resp.get_json()
        user_id = (
            create_data.get("id")
            or create_data.get("user_id")
            or (create_data.get("user", {}) or {}).get("id")
            or 2
        )

        resp = client.delete(
            f"/api/users/{user_id}",
            headers=auth_header(admin_token),
        )
        assert resp.status_code in (200, 204)

    def test_delete_user_as_non_admin(self, client, admin_token):
        """DELETE /api/users/:id as non-admin returns 403."""
        user_token = make_token(user_id=2, email="user@example.com", role="user")
        resp = client.delete(
            "/api/users/1",
            headers=auth_header(user_token),
        )
        assert resp.status_code == 403

    def test_get_nonexistent_user(self, client, admin_token):
        """GET /api/users/99999 returns 404."""
        resp = client.get("/api/users/99999", headers=auth_header(admin_token))
        assert resp.status_code == 404
