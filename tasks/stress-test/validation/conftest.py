"""
Shared fixtures for stress-test validation.

These fixtures support API-based behavioral testing and algorithm unit testing.
No pipeline auto-discovery or dynamic class instantiation — tests go through
HTTP endpoints or import specific functions by name.
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml


# ---------------------------------------------------------------------------
# Path helpers — the working directory is the root of the implementation
# ---------------------------------------------------------------------------

def _project_root():
    """Return the project root (cwd or the directory containing src/)."""
    cwd = Path.cwd()
    if (cwd / "src").is_dir():
        return cwd
    # Walk up at most 2 levels
    for parent in [cwd.parent, cwd.parent.parent]:
        if (parent / "src").is_dir():
            return parent
    return cwd


@pytest.fixture(scope="session")
def project_root():
    root = _project_root()
    # Ensure src/ is importable
    src_dir = str(root / "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return root


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def tenants_config(project_root):
    path = project_root / "config" / "tenants.yaml"
    with open(path) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def api_keys_config(project_root):
    path = project_root / "config" / "api_keys.yaml"
    with open(path) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def routing_config(project_root):
    path = project_root / "config" / "routing.yaml"
    with open(path) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def transforms_config(project_root):
    path = project_root / "config" / "transforms.yaml"
    with open(path) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# HTTP test client (Flask or FastAPI)
# ---------------------------------------------------------------------------

def _find_app(mod):
    """Find a Flask or FastAPI app in the api module.

    Returns (app, framework) where framework is 'flask' or 'fastapi'.
    """
    # Try Flask first
    try:
        import flask
        for attr_name in ["app", "application", "create_app"]:
            obj = getattr(mod, attr_name, None)
            if obj is None:
                continue
            if isinstance(obj, flask.Flask):
                return obj, "flask"
            if callable(obj) and attr_name == "create_app":
                try:
                    result = obj()
                    if isinstance(result, flask.Flask):
                        return result, "flask"
                except Exception:
                    pass
        for name in dir(mod):
            obj = getattr(mod, name)
            if isinstance(obj, flask.Flask):
                return obj, "flask"
    except ImportError:
        pass

    # Try FastAPI
    try:
        import fastapi
        for attr_name in ["app", "application", "create_app"]:
            obj = getattr(mod, attr_name, None)
            if obj is None:
                continue
            if isinstance(obj, fastapi.FastAPI):
                return obj, "fastapi"
            if callable(obj) and attr_name == "create_app":
                try:
                    result = obj()
                    if isinstance(result, fastapi.FastAPI):
                        return result, "fastapi"
                except Exception:
                    pass
        for name in dir(mod):
            obj = getattr(mod, name)
            if isinstance(obj, fastapi.FastAPI):
                return obj, "fastapi"
    except ImportError:
        pass

    pytest.skip("No Flask or FastAPI app found in api module")


class _FlaskClientAdapter:
    """Thin wrapper so Flask test client matches our expected interface."""
    def __init__(self, client):
        self._client = client

    def __getattr__(self, name):
        return getattr(self._client, name)


class _FastAPIClientAdapter:
    """Wraps FastAPI TestClient to behave like Flask's test client.

    Flask's test client returns response objects with `status_code` and
    `get_json()`, while Starlette's returns `status_code` and `.json()`.
    This adapter normalises the differences so tests work unchanged.
    """
    def __init__(self, client):
        self._client = client

    def _wrap_response(self, resp):
        """Add Flask-compatible methods to a Starlette response."""
        if not hasattr(resp, "get_json"):
            resp.get_json = lambda: resp.json()
        if not hasattr(resp, "get_data"):
            resp.get_data = lambda as_text=False: resp.text if as_text else resp.content
        return resp

    def get(self, *args, **kwargs):
        return self._wrap_response(self._client.get(*args, **kwargs))

    def post(self, *args, **kwargs):
        return self._wrap_response(self._client.post(*args, **kwargs))

    def put(self, *args, **kwargs):
        return self._wrap_response(self._client.put(*args, **kwargs))

    def delete(self, *args, **kwargs):
        return self._wrap_response(self._client.delete(*args, **kwargs))

    def patch(self, *args, **kwargs):
        return self._wrap_response(self._client.patch(*args, **kwargs))

    def __getattr__(self, name):
        return getattr(self._client, name)


def _try_import_module(name):
    """Try importing 'src.<name>' then '<name>'. Returns None on failure."""
    root = _project_root()
    src_init = root / "src" / "__init__.py"
    if (root / "src").is_dir() and not src_init.exists():
        src_init.touch()

    for qualified in [f"src.{name}", name]:
        try:
            return __import__(qualified, fromlist=[""])
        except ImportError:
            continue
    return None


def _import_module(name):
    """Import a module, skipping the test if not found."""
    mod = _try_import_module(name)
    if mod is None:
        pytest.skip(f"Cannot import module '{name}'")
    return mod


@pytest.fixture
def app_client(project_root):
    """Create a test client for the API (Flask or FastAPI)."""
    os.chdir(project_root)
    api_module = _import_module("api")
    app, framework = _find_app(api_module)

    if framework == "flask":
        app.config["TESTING"] = True
        with app.test_client() as client:
            yield _FlaskClientAdapter(client)
    else:
        from starlette.testclient import TestClient
        with TestClient(app) as client:
            yield _FastAPIClientAdapter(client)


# ---------------------------------------------------------------------------
# Event helpers
# ---------------------------------------------------------------------------

def make_event(
    tenant_id="tn-us-east-0042",
    event_type="user.created",
    source="web-app",
    payload=None,
    correlation_id=None,
    sdk_version="2.3.0",
    idempotency_key=None,
    timestamp=None,
    event_id=None,
):
    """Create a valid event envelope matching the event-schema-spec."""
    if payload is None:
        payload = {"user_id": "u_12345", "action": "signup"}
    if idempotency_key is None:
        idempotency_key = str(uuid.uuid4())
    if timestamp is None:
        timestamp = datetime.now(timezone.utc).isoformat()
    # Ensure timestamp uses +00:00 not Z
    if timestamp.endswith("Z"):
        timestamp = timestamp[:-1] + "+00:00"
    if event_id is None:
        # Format: evt_<first 2 chars of region>_<ulid-like>
        region = tenant_id.split("-")[1] if "-" in tenant_id else "us"
        region_prefix = region[:2]
        event_id = f"evt_{region_prefix}_{uuid.uuid4().hex[:12].upper()}"
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    return {
        "event_id": event_id,
        "tenant_id": tenant_id,
        "event_type": event_type,
        "version": "2.3",
        "timestamp": timestamp,
        "source": source,
        "correlation_id": correlation_id,
        "payload": payload,
        "metadata": {
            "sdk_version": sdk_version,
            "retry_count": 0,
            "idempotency_key": idempotency_key,
        },
    }


def make_auth_header(api_key="acme-api-key-prod"):
    """Create an Authorization header for API requests."""
    return {"Authorization": f"Bearer {api_key}"}


# Make helpers available to tests via conftest
@pytest.fixture
def event_factory():
    """Returns the make_event helper function."""
    return make_event


@pytest.fixture
def auth_header_factory():
    """Returns the make_auth_header helper function."""
    return make_auth_header
