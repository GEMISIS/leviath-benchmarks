"""Input validation tests."""
import pytest

from conftest import auth_header, create_test_user, make_token


class TestValidation:
    """Tests for request input validation on user creation."""

    def test_invalid_email_format(self, client, admin_token):
        """Creating a user with an invalid email returns 400."""
        resp = create_test_user(
            client, admin_token,
            email="not-an-email",
        )
        assert resp.status_code == 400

    def test_password_too_short(self, client, admin_token):
        """Password shorter than 8 characters returns 400."""
        resp = create_test_user(
            client, admin_token,
            email="short@example.com",
            password="Ab1!",
        )
        assert resp.status_code == 400

    def test_password_missing_uppercase(self, client, admin_token):
        """Password without uppercase letter returns 400."""
        resp = create_test_user(
            client, admin_token,
            email="noupper@example.com",
            password="alllower1!",
        )
        assert resp.status_code == 400

    def test_password_missing_number(self, client, admin_token):
        """Password without a digit returns 400."""
        resp = create_test_user(
            client, admin_token,
            email="nodigit@example.com",
            password="NoDigitHere!",
        )
        assert resp.status_code == 400

    def test_duplicate_email(self, client, admin_token):
        """Creating a user with an existing email returns 409 or 400."""
        # admin@example.com already exists from seed data
        resp = create_test_user(
            client, admin_token,
            email="admin@example.com",
        )
        assert resp.status_code in (400, 409)

    def test_empty_full_name(self, client, admin_token):
        """Empty full_name returns 400."""
        resp = create_test_user(
            client, admin_token,
            email="emptyname@example.com",
            full_name="",
        )
        assert resp.status_code == 400

    def test_full_name_too_long(self, client, admin_token):
        """full_name over 100 characters returns 400."""
        resp = create_test_user(
            client, admin_token,
            email="longname@example.com",
            full_name="A" * 101,
        )
        assert resp.status_code == 400
