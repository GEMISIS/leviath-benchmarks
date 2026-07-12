"""
Shared fixtures for stress-test validation.

These fixtures dynamically import from the implementation under test,
so they work with ANY correct implementation — not tied to a specific coding style.
"""

import importlib
import json
import os
import sys
import time
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
# Dynamic module loaders
# ---------------------------------------------------------------------------

def _import_module(name):
    """Try importing 'src.<name>' then '<name>'."""
    for qualified in [f"src.{name}", name]:
        try:
            return importlib.import_module(qualified)
        except ImportError:
            continue
    pytest.skip(f"Cannot import module '{name}'")


@pytest.fixture(scope="session")
def pipeline_module(project_root):
    return _import_module("pipeline")


@pytest.fixture(scope="session")
def api_module(project_root):
    return _import_module("api")


@pytest.fixture(scope="session")
def storage_module(project_root):
    return _import_module("storage")


@pytest.fixture(scope="session")
def dlq_module(project_root):
    return _import_module("dlq")


@pytest.fixture(scope="session")
def rate_limiter_module(project_root):
    return _import_module("rate_limiter")


@pytest.fixture(scope="session")
def metrics_module(project_root):
    return _import_module("metrics")


@pytest.fixture(scope="session")
def audit_module(project_root):
    return _import_module("audit")


@pytest.fixture(scope="session")
def transformer_module(project_root):
    return _import_module("transformer")


@pytest.fixture(scope="session")
def router_module(project_root):
    return _import_module("router")


@pytest.fixture(scope="session")
def schema_validator_module(project_root):
    return _import_module("schema_validator")


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
# Pipeline fixture — creates a fresh instance for each test
# ---------------------------------------------------------------------------

def _find_pipeline_class(mod):
    """Find the Pipeline class (or equivalent callable) in the module."""
    for attr_name in ["Pipeline", "EventPipeline", "ProcessingPipeline"]:
        cls = getattr(mod, attr_name, None)
        if cls is not None:
            return cls
    # Fallback: find any class with 'pipeline' in its name
    for name in dir(mod):
        obj = getattr(mod, name)
        if isinstance(obj, type) and "pipeline" in name.lower():
            return obj
    pytest.skip("No Pipeline class found in pipeline module")


class _PipelineAdapter:
    """Wraps a pipeline instance to normalize method names across implementations.

    Different implementations may use ``process()``, ``process_event()``,
    ``handle()``, or ``ingest()`` — this adapter exposes a canonical
    ``.process(event)`` regardless of what the underlying class calls it.
    Similarly, storage/DLQ/metrics accessors are normalised.
    """

    _PROCESS_NAMES = ["process", "process_event", "handle", "handle_event", "ingest", "ingest_event"]

    def __init__(self, inner):
        self._inner = inner
        self._process_fn = None
        for name in self._PROCESS_NAMES:
            fn = getattr(inner, name, None)
            if callable(fn):
                self._process_fn = fn
                break
        if self._process_fn is None:
            raise AttributeError(
                f"Pipeline class {type(inner).__name__} has no process method "
                f"(tried: {self._PROCESS_NAMES})"
            )

    # Canonical entry point
    def process(self, event):
        return self._process_fn(event)

    # Transparent proxy for everything else (storage, dlq, metrics, etc.)
    def __getattr__(self, name):
        return getattr(self._inner, name)


@pytest.fixture
def pipeline(pipeline_module, project_root):
    """Create a fresh Pipeline instance for each test."""
    cls = _find_pipeline_class(pipeline_module)
    os.chdir(project_root)
    try:
        instance = cls()
    except TypeError:
        # Maybe it needs a config path
        try:
            instance = cls(config_dir=str(project_root / "config"))
        except TypeError:
            instance = cls(str(project_root / "config"))
    return _PipelineAdapter(instance)


# ---------------------------------------------------------------------------
# Flask test client
# ---------------------------------------------------------------------------

def _find_flask_app(mod):
    """Find the Flask app in the api module."""
    import flask
    # Direct 'app' attribute
    for attr_name in ["app", "application", "create_app"]:
        obj = getattr(mod, attr_name, None)
        if obj is None:
            continue
        if isinstance(obj, flask.Flask):
            return obj
        if callable(obj):
            result = obj()
            if isinstance(result, flask.Flask):
                return result
    # Fallback: scan module for Flask instances
    for name in dir(mod):
        obj = getattr(mod, name)
        if isinstance(obj, flask.Flask):
            return obj
    pytest.skip("No Flask app found in api module")


@pytest.fixture
def app_client(api_module, project_root):
    """Create a Flask test client for each test."""
    os.chdir(project_root)
    app = _find_flask_app(api_module)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


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
