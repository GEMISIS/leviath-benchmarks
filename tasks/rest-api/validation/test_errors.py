"""Error handling and security tests."""
import sqlite3

import pytest

from conftest import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    auth_header,
    create_test_user,
    login,
)


class TestErrors:
    """Tests for error responses and security properties."""

    def test_404_returns_json(self, client, admin_token):
        """Request to an unknown endpoint returns a JSON error body."""
        resp = client.get(
            "/api/nonexistent-endpoint",
            headers=auth_header(admin_token),
        )
        assert resp.status_code == 404
        data = resp.get_json()
        assert data is not None, "404 response should be JSON"

    def test_method_not_allowed(self, client):
        """Using an unsupported HTTP method returns 405."""
        resp = client.patch("/api/health")
        assert resp.status_code == 405

    def test_error_response_format(self, client):
        """Error responses contain an error/message field."""
        resp = client.post("/api/auth/login", json={})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data is not None
        # Should have some kind of error description
        has_error = (
            "error" in data
            or "message" in data
            or "msg" in data
            or "detail" in data
        )
        assert has_error, (
            f"Error response should contain an error/message field, got: {data}"
        )

    def test_bcrypt_password_storage(self, client, admin_token, _fresh_db):
        """Newly created user has a bcrypt hash (starts with $2b$)."""
        create_test_user(client, admin_token, email="hashcheck@example.com")

        conn = sqlite3.connect(_fresh_db)
        row = conn.execute(
            "SELECT password_hash FROM users WHERE email = ?",
            ("hashcheck@example.com",),
        ).fetchone()
        conn.close()

        assert row is not None, "User should exist in the database"
        password_hash = row[0]
        assert password_hash.startswith("$2b$") or password_hash.startswith("$2a$"), (
            f"Password hash should be bcrypt, got: {password_hash[:20]}..."
        )

    def test_password_not_stored_plaintext(self, client, admin_token):
        """User detail responses do not include the raw password."""
        resp = create_test_user(client, admin_token, email="nopass@example.com")
        data = resp.get_json()

        # Flatten: check top-level and nested 'user' dict
        fields_to_check = dict(data)
        if isinstance(data.get("user"), dict):
            fields_to_check.update(data["user"])

        assert "password" not in fields_to_check, (
            "Response should not include 'password' field"
        )
        assert "password_hash" not in fields_to_check, (
            "Response should not include 'password_hash' field"
        )
