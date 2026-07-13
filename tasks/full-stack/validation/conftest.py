import sys
import os
import json
import glob as globmod
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

WORKDIR = os.path.join(os.path.dirname(__file__), "..")

# Try importing the FastAPI app from multiple possible module paths.
app = None
for mod_path in [
    "backend.app",
    "backend.main",
    "backend.src.app",
    "backend.src.main",
]:
    try:
        mod = __import__(mod_path, fromlist=["app", "create_app"])
        if hasattr(mod, "create_app"):
            app = mod.create_app()
        elif hasattr(mod, "app"):
            app = mod.app
        if app:
            break
    except (ImportError, Exception):
        continue


@pytest.fixture
def workdir():
    """Return the root working directory of the task."""
    return WORKDIR


@pytest.fixture
def fastapi_app():
    """Return the discovered FastAPI app instance, or None."""
    return app


@pytest.fixture
def async_client():
    """Provide an httpx async test client bound to the FastAPI app."""
    if app is None:
        pytest.skip("FastAPI app could not be imported")
    try:
        from httpx import ASGITransport, AsyncClient
    except ImportError:
        pytest.skip("httpx not installed")

    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://testserver")


@pytest.fixture
def ws_message_validator():
    """Return a helper that validates a WebSocket message dict."""

    def _validate(msg: dict) -> list[str]:
        errors = []
        if "type" not in msg:
            errors.append("missing 'type' field")
        elif msg["type"] not in (
            "notification",
            "notification_read",
            "ping",
            "pong",
        ):
            errors.append(f"invalid type: {msg['type']}")
        if "payload" not in msg:
            errors.append("missing 'payload' field")
        if "timestamp" not in msg:
            errors.append("missing 'timestamp' field")
        return errors

    return _validate


@pytest.fixture
def notification_payload_validator():
    """Return a helper that validates a notification payload dict."""
    required_fields = [
        "id",
        "user_id",
        "type",
        "priority",
        "title",
        "message",
        "read",
        "created_at",
    ]

    def _validate(payload: dict) -> list[str]:
        errors = []
        for field in required_fields:
            if field not in payload:
                errors.append(f"missing field: {field}")
        valid_types = ["comment", "mention", "system", "security"]
        if payload.get("type") and payload["type"] not in valid_types:
            errors.append(f"invalid notification type: {payload['type']}")
        valid_priorities = ["low", "medium", "high", "urgent"]
        if payload.get("priority") and payload["priority"] not in valid_priorities:
            errors.append(f"invalid priority: {payload['priority']}")
        return errors

    return _validate


def find_files(base_dir: str, pattern: str) -> list[str]:
    """Recursively find files matching a glob pattern under base_dir."""
    return globmod.glob(os.path.join(base_dir, "**", pattern), recursive=True)


@pytest.fixture
def find_project_files():
    """Return a helper to find files in the project by glob pattern."""

    def _find(pattern: str) -> list[str]:
        return find_files(WORKDIR, pattern)

    return _find
