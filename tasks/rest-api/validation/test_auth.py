"""Authentication and JWT tests."""
import datetime
import time

import jwt as pyjwt
import pytest

from conftest import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    PUBLIC_KEY,
    PRIVATE_KEY,
    auth_header,
    login,
    make_token,
)


class TestAuth:
    """Tests for POST /api/auth/login and JWT handling."""

    def test_login_success(self, client):
        """POST /api/auth/login with valid admin credentials returns 200."""
        resp = login(client)
        assert resp.status_code == 200

    def test_login_returns_jwt_token(self, client):
        """Successful login response contains a token field."""
        resp = login(client)
        data = resp.get_json()
        assert data is not None
        token = data.get("token") or data.get("access_token")
        assert token is not None, (
            "Expected 'token' or 'access_token' in response body"
        )

    def test_login_wrong_password(self, client):
        """Login with wrong password returns 401."""
        resp = login(client, password="WrongPassword1!")
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Login with unknown email returns 401."""
        resp = login(client, email="nobody@example.com", password="Nope1234!")
        assert resp.status_code == 401

    def test_login_missing_fields(self, client):
        """Login without required fields returns 400."""
        resp = client.post("/api/auth/login", json={})
        assert resp.status_code == 400

    def test_jwt_token_is_valid_rs256(self, client):
        """Returned JWT can be decoded with the public key using RS256."""
        resp = login(client)
        data = resp.get_json()
        token = data.get("token") or data.get("access_token")
        decoded = pyjwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        assert decoded is not None

    def test_jwt_contains_user_info(self, client):
        """Decoded JWT contains user identifier and role."""
        resp = login(client)
        data = resp.get_json()
        token = data.get("token") or data.get("access_token")
        decoded = pyjwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])

        # The token should contain a user identifier (sub or user_id)
        user_id = decoded.get("sub") or decoded.get("user_id")
        assert user_id is not None, "Token must contain 'sub' or 'user_id'"

        # Should also contain role info
        role = decoded.get("role")
        assert role is not None, "Token must contain 'role'"

    def test_jwt_has_expiry(self, client):
        """JWT has an exp claim set roughly 24 hours in the future."""
        resp = login(client)
        data = resp.get_json()
        token = data.get("token") or data.get("access_token")
        decoded = pyjwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])

        assert "exp" in decoded, "Token must have 'exp' claim"
        exp_dt = datetime.datetime.utcfromtimestamp(decoded["exp"])
        now = datetime.datetime.utcnow()
        delta = exp_dt - now
        # Should be between 23 and 25 hours
        assert datetime.timedelta(hours=23) < delta < datetime.timedelta(hours=25), (
            f"Token expiry should be ~24h from now, got {delta}"
        )

    def test_expired_token_rejected(self, client):
        """A request with an expired JWT returns 401."""
        expired_token = make_token(expired=True)
        resp = client.get("/api/users/1", headers=auth_header(expired_token))
        assert resp.status_code == 401
