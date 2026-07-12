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

def _try_import_module(name):
    """Try importing 'src.<name>' then '<name>'. Returns None on failure.

    Handles both absolute imports (``import pipeline``) and relative
    imports (``from .audit import ...``) by ensuring the ``src`` package
    is initialised before attempting ``src.<name>``.
    """
    root = _project_root()
    src_init = root / "src" / "__init__.py"
    if (root / "src").is_dir() and not src_init.exists():
        src_init.touch()

    for qualified in [f"src.{name}", name]:
        try:
            return importlib.import_module(qualified)
        except ImportError:
            continue
    return None


def _import_module(name):
    """Import a module, skipping the test if not found."""
    mod = _try_import_module(name)
    if mod is None:
        pytest.skip(f"Cannot import module '{name}'")
    return mod


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
        result = self._process_fn(event)
        # Normalize result to dict if it's a custom object
        if result is not None and not isinstance(result, dict):
            d = {}
            for attr in ["status_code", "http_status", "body", "headers",
                         "event", "processed_event", "handler_results",
                         "event_id", "tenant_id", "status", "message",
                         "error", "degraded"]:
                val = getattr(result, attr, None)
                if val is not None:
                    d[attr] = val
            # Also try converting via vars() or __dict__
            if not d:
                try:
                    d = vars(result)
                except TypeError:
                    pass
            if d:
                return d
        return result

    # Transparent proxy for everything else (storage, dlq, metrics, etc.)
    def __getattr__(self, name):
        return getattr(self._inner, name)


def _try_instantiate_class(cls, project_root):
    """Try multiple strategies to instantiate a class.

    Strategy order:
    1. No-arg constructor
    2. config_dir keyword
    3. config_dir positional
    4. Introspect __init__ params and auto-resolve dependencies from src/
    """
    import inspect

    # Strategy 1: no-arg
    try:
        return cls()
    except TypeError:
        pass

    config_dir = str(project_root / "config")

    # Strategy 2: config_dir keyword
    try:
        return cls(config_dir=config_dir)
    except TypeError:
        pass

    # Strategy 3: config_dir positional
    try:
        return cls(config_dir)
    except TypeError:
        pass

    # Strategy 4: introspect __init__ and auto-resolve dependencies
    try:
        sig = inspect.signature(cls.__init__)
        params = [p for p in sig.parameters.values() if p.name != "self"]
    except (ValueError, TypeError):
        raise TypeError(
            f"Cannot instantiate {cls.__name__}: no working constructor pattern found"
        )

    # All known module files in src/
    _ALL_MODULES = [
        "schema_validator", "transformer", "router", "handlers",
        "storage", "metrics", "dlq", "rate_limiter", "audit",
        "pipeline", "tenant", "tenant_registry", "errors",
    ]

    # Map param names to candidate module names (most specific first)
    _PARAM_MODULE_CANDIDATES = {
        "schema_validator": ["schema_validator"],
        "validator": ["schema_validator"],
        "transformer": ["transformer"],
        "transform_engine": ["transformer"],
        "router": ["router"],
        "event_router": ["router"],
        "handler_registry": ["handlers"],
        "handlers": ["handlers"],
        "handler": ["handlers"],
        "storage": ["storage"],
        "store": ["storage"],
        "storage_layer": ["storage"],
        "metrics": ["metrics"],
        "metrics_collector": ["metrics"],
        "dlq": ["dlq"],
        "dead_letter_queue": ["dlq"],
        "rate_limiter": ["rate_limiter"],
        "limiter": ["rate_limiter"],
        "audit": ["audit"],
        "audit_logger": ["audit"],
        "auditor": ["audit"],
        "tenant_registry": ["tenant_registry", "tenant"],
        "tenants": ["tenant_registry", "tenant"],
    }

    def _resolve_class_by_annotation(param, modules_cache):
        """Use the type annotation to find the exact class."""
        ann = param.annotation
        if ann is inspect.Parameter.empty:
            return None, None
        # Get the class name from the annotation
        if isinstance(ann, type):
            target_name = ann.__name__
        elif isinstance(ann, str):
            target_name = ann
        else:
            return None, None
        # Search all loaded modules for this class name
        for mod in modules_cache.values():
            cls_candidate = getattr(mod, target_name, None)
            if cls_candidate is not None and isinstance(cls_candidate, type):
                return mod, cls_candidate
        return None, None

    def _find_class_in_module(mod, hint_name):
        """Find a class in a module, using multiple strategies."""
        # 1. Exact CamelCase of hint
        parts = hint_name.split("_")
        camel = "".join(p.capitalize() for p in parts)
        cls_candidate = getattr(mod, camel, None)
        if cls_candidate and isinstance(cls_candidate, type):
            return cls_candidate
        # 2. Any class whose name matches case-insensitively
        hint_lower = hint_name.lower().replace("_", "")
        for name in dir(mod):
            obj = getattr(mod, name)
            if isinstance(obj, type) and name.lower().replace("_", "") == hint_lower:
                return obj
        # 3. Any class containing a significant word from the hint
        significant = [p for p in parts if len(p) > 2]
        for name in dir(mod):
            obj = getattr(mod, name)
            if isinstance(obj, type) and not name.startswith("_"):
                name_lower = name.lower()
                if any(p in name_lower for p in significant):
                    return obj
        return None

    # Cache for resolved dependency instances (avoids re-instantiation)
    _dep_cache = {}

    def _instantiate_dependency(dep_cls, dep_project_root, depth=0):
        """Try to instantiate a dependency class, recursively resolving its own deps."""
        if dep_cls in _dep_cache:
            return _dep_cache[dep_cls]
        if depth > 5:
            return None

        config_dir_val = str(dep_project_root / "config")

        # Strategy 1: no-arg
        try:
            inst = dep_cls()
            _dep_cache[dep_cls] = inst
            return inst
        except TypeError:
            pass

        # Strategy 2: recursive introspection (same as parent)
        try:
            dep_sig = inspect.signature(dep_cls.__init__)
            dep_params = [p for p in dep_sig.parameters.values() if p.name != "self"]
        except (ValueError, TypeError):
            dep_params = []

        if dep_params:
            dep_kwargs = {}
            dep_resolved = True
            for dp in dep_params:
                if dp.default is not inspect.Parameter.empty:
                    continue  # has default, skip
                dp_name = dp.name.lower()
                if dp_name in ("config", "config_dir", "config_path"):
                    dep_kwargs[dp.name] = config_dir_val
                    continue

                # Try annotation-based resolution
                inner_cls = None
                ann = dp.annotation
                if ann is not inspect.Parameter.empty:
                    target_name = ann.__name__ if isinstance(ann, type) else str(ann)
                    # Strip Optional wrapper
                    if target_name.startswith("Optional["):
                        continue  # optional, skip
                    for m in modules_cache.values():
                        c = getattr(m, target_name, None)
                        if c is not None and isinstance(c, type):
                            inner_cls = c
                            break

                # Fallback: name-based resolution
                if inner_cls is None:
                    candidates = _PARAM_MODULE_CANDIDATES.get(dp_name, [dp_name])
                    for mod_name in candidates:
                        mod = modules_cache.get(mod_name)
                        if mod is None:
                            continue
                        inner_cls = _find_class_in_module(mod, dp_name)
                        if inner_cls is not None:
                            break

                if inner_cls is None:
                    # Brute-force search
                    for m in modules_cache.values():
                        inner_cls = _find_class_in_module(m, dp_name)
                        if inner_cls is not None:
                            break

                if inner_cls is None:
                    dep_resolved = False
                    break

                inner_inst = _instantiate_dependency(inner_cls, dep_project_root, depth + 1)
                if inner_inst is None:
                    dep_resolved = False
                    break
                dep_kwargs[dp.name] = inner_inst

            if dep_resolved:
                try:
                    inst = dep_cls(**dep_kwargs)
                    _dep_cache[dep_cls] = inst
                    return inst
                except TypeError:
                    pass

        # Strategy 3: config_dir fallback (only if no recursive resolution)
        for strategy in [
            lambda: dep_cls(config_dir=config_dir_val),
            lambda: dep_cls(config_dir_val),
        ]:
            try:
                inst = strategy()
                _dep_cache[dep_cls] = inst
                return inst
            except (TypeError, Exception):
                continue

        return None

    # Pre-load all available modules (non-skipping)
    modules_cache = {}
    for mod_name in _ALL_MODULES:
        mod = _try_import_module(mod_name)
        if mod is not None:
            modules_cache[mod_name] = mod

    kwargs = {}
    resolved_all = True

    for param in params:
        name = param.name.lower()

        # Config-related params
        if name in ("config", "config_dir", "config_path"):
            kwargs[param.name] = config_dir
            continue

        dep_cls = None
        dep_mod = None

        # Strategy A: use type annotation to find the exact class
        dep_mod, dep_cls = _resolve_class_by_annotation(param, modules_cache)

        # Strategy B: use param name → module mapping
        if dep_cls is None:
            candidates = _PARAM_MODULE_CANDIDATES.get(name, [name])
            for mod_name in candidates:
                mod = modules_cache.get(mod_name)
                if mod is None:
                    continue
                dep_cls = _find_class_in_module(mod, name)
                if dep_cls is not None:
                    dep_mod = mod
                    break

        # Strategy C: brute-force search all modules
        if dep_cls is None:
            for mod in modules_cache.values():
                dep_cls = _find_class_in_module(mod, name)
                if dep_cls is not None:
                    dep_mod = mod
                    break

        if dep_cls is None:
            resolved_all = False
            break

        val = _instantiate_dependency(dep_cls, project_root)
        if val is None:
            resolved_all = False
            break
        kwargs[param.name] = val

    if resolved_all:
        try:
            return cls(**kwargs)
        except TypeError:
            pass
        # Try positional
        try:
            return cls(*kwargs.values())
        except TypeError:
            pass

    raise TypeError(
        f"Cannot instantiate {cls.__name__}: tried no-arg, config_dir, "
        f"and dependency injection (params: {[p.name for p in params]})"
    )


@pytest.fixture
def pipeline(pipeline_module, project_root):
    """Create a fresh Pipeline instance for each test."""
    cls = _find_pipeline_class(pipeline_module)
    os.chdir(project_root)
    instance = _try_instantiate_class(cls, project_root)
    return _PipelineAdapter(instance)


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


@pytest.fixture
def app_client(api_module, project_root):
    """Create a test client for the API (Flask or FastAPI)."""
    os.chdir(project_root)
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
