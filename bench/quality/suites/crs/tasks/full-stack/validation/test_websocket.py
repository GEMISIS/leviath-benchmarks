"""Tests for WebSocket message format and schema validation.

These tests validate the structure of WebSocket messages without
requiring a running server. They construct messages matching the
expected schema and validate them via the conftest helpers.
"""

import datetime


class TestWebSocketMessageFormat:
    """Validate WebSocket message schemas."""

    def _make_timestamp(self) -> str:
        return datetime.datetime.now(datetime.timezone.utc).isoformat()

    def test_websocket_message_format_notification(self, ws_message_validator):
        """A notification message must have type, payload, and timestamp."""
        msg = {
            "type": "notification",
            "payload": {
                "id": "notif-001",
                "user_id": 1,
                "type": "comment",
                "priority": "medium",
                "title": "New comment",
                "message": "Someone commented on your post",
                "read": False,
                "created_at": self._make_timestamp(),
            },
            "timestamp": self._make_timestamp(),
        }
        errors = ws_message_validator(msg)
        assert errors == [], f"Validation errors: {errors}"

    def test_websocket_message_format_ping_pong(self, ws_message_validator):
        """Ping and pong messages must have correct type field."""
        for msg_type in ("ping", "pong"):
            msg = {
                "type": msg_type,
                "payload": {},
                "timestamp": self._make_timestamp(),
            }
            errors = ws_message_validator(msg)
            assert errors == [], (
                f"Validation errors for {msg_type}: {errors}"
            )

    def test_notification_payload_fields(
        self, ws_message_validator, notification_payload_validator
    ):
        """Notification payload must contain all required Notification fields."""
        payload = {
            "id": "notif-002",
            "user_id": 42,
            "type": "mention",
            "priority": "high",
            "title": "You were mentioned",
            "message": "@user mentioned you in a discussion",
            "read": False,
            "created_at": self._make_timestamp(),
        }
        msg = {
            "type": "notification",
            "payload": payload,
            "timestamp": self._make_timestamp(),
        }
        ws_errors = ws_message_validator(msg)
        assert ws_errors == [], f"WebSocket message errors: {ws_errors}"

        payload_errors = notification_payload_validator(payload)
        assert payload_errors == [], f"Payload errors: {payload_errors}"

    def test_websocket_message_types_valid(self, ws_message_validator):
        """Only notification, notification_read, ping, pong are valid types."""
        valid_types = ["notification", "notification_read", "ping", "pong"]
        for t in valid_types:
            msg = {
                "type": t,
                "payload": {},
                "timestamp": self._make_timestamp(),
            }
            errors = ws_message_validator(msg)
            assert errors == [], f"Type '{t}' should be valid but got: {errors}"

        # An invalid type should produce an error.
        msg = {
            "type": "invalid_type",
            "payload": {},
            "timestamp": self._make_timestamp(),
        }
        errors = ws_message_validator(msg)
        assert len(errors) > 0, "Invalid type should produce validation errors"

    def test_notification_read_message_format(self, ws_message_validator):
        """notification_read messages should include notification_id in payload."""
        msg = {
            "type": "notification_read",
            "payload": {"notification_id": "notif-003"},
            "timestamp": self._make_timestamp(),
        }
        errors = ws_message_validator(msg)
        assert errors == [], f"Validation errors: {errors}"
        assert "notification_id" in msg["payload"], (
            "notification_read payload must contain 'notification_id'"
        )

    def test_message_missing_fields_rejected(self, ws_message_validator):
        """Messages missing required fields should fail validation."""
        # Missing type
        errors = ws_message_validator({"payload": {}, "timestamp": "t"})
        assert len(errors) > 0, "Missing 'type' should produce error"

        # Missing payload
        errors = ws_message_validator({"type": "ping", "timestamp": "t"})
        assert len(errors) > 0, "Missing 'payload' should produce error"

        # Missing timestamp
        errors = ws_message_validator({"type": "ping", "payload": {}})
        assert len(errors) > 0, "Missing 'timestamp' should produce error"
