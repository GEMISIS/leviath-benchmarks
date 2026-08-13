import datetime
import os
import shutil
import sqlite3
import sys
import tempfile

import bcrypt
import jwt
import pytest

# ---------------------------------------------------------------------------
# Path setup – the agent's deliverables live one directory above validation/
# ---------------------------------------------------------------------------
TASK_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SEED_DIR = os.path.join(TASK_DIR, "seed-files")
KEYS_DIR = os.path.join(SEED_DIR, "keys")
SCHEMA_PATH = os.path.join(SEED_DIR, "schema.sql")

# Add the task root to sys.path so we can import the agent's code
sys.path.insert(0, TASK_DIR)
# Also add src/ directly in case the agent structured it as a flat module
sys.path.insert(0, os.path.join(TASK_DIR, "src"))

# ---------------------------------------------------------------------------
# RSA keys (used by helpers to mint / verify JWTs)
# ---------------------------------------------------------------------------
with open(os.path.join(KEYS_DIR, "private.pem"), "r") as _f:
    PRIVATE_KEY = _f.read()

with open(os.path.join(KEYS_DIR, "public.pem"), "r") as _f:
    PUBLIC_KEY = _f.read()

# ---------------------------------------------------------------------------
# Discover the Flask app – try several common import paths
# ---------------------------------------------------------------------------
_app = None
_import_errors = []
for _mod_path in ["src.app", "src.main", "src.server", "src", "app", "main", "server"]:
    try:
        _mod = __import__(_mod_path, fromlist=["app", "create_app"])
        if hasattr(_mod, "create_app"):
            _app = _mod.create_app()
        elif hasattr(_mod, "app"):
            _app = _mod.app
        if _app is not None:
            break
    except Exception as exc:
        _import_errors.append((_mod_path, exc))
        continue

if _app is None:
    raise RuntimeError(
        "Could not import the Flask application. Tried several module paths. "
        f"Errors: {_import_errors}"
    )

# ---------------------------------------------------------------------------
# Seed admin credentials
# ---------------------------------------------------------------------------
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "Admin123!"
ADMIN_NAME = "System Admin"
ADMIN_HASH = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzqJOa/7G6"


def _init_db(db_path: str) -> None:
    """Initialise a fresh SQLite database from the seed schema."""
    conn = sqlite3.connect(db_path)
    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())
    conn.close()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _fresh_db(tmp_path, monkeypatch):
    """Create a temporary database for every test and point the app at it.

    We try several common env-var / config names that the agent might use.
    """
    db_path = str(tmp_path / "test.db")
    _init_db(db_path)

    # Set environment variables the app might read
    monkeypatch.setenv("DATABASE_PATH", db_path)
    monkeypatch.setenv("DATABASE_URL", db_path)
    monkeypatch.setenv("DB_PATH", db_path)
    monkeypatch.setenv("SQLITE_PATH", db_path)
    monkeypatch.setenv("DATABASE", db_path)

    # Also try to set it on the app config directly
    if hasattr(_app, "config"):
        _app.config["DATABASE"] = db_path
        _app.config["DATABASE_PATH"] = db_path
        _app.config["DATABASE_URL"] = db_path
        _app.config["DB_PATH"] = db_path
        _app.config["SQLITE_PATH"] = db_path

    # Point key paths at the seed keys
    monkeypatch.setenv("PRIVATE_KEY_PATH", os.path.join(KEYS_DIR, "private.pem"))
    monkeypatch.setenv("PUBLIC_KEY_PATH", os.path.join(KEYS_DIR, "public.pem"))
    monkeypatch.setenv("PRIVATE_KEY", PRIVATE_KEY)
    monkeypatch.setenv("PUBLIC_KEY", PUBLIC_KEY)
    monkeypatch.setenv("JWT_PRIVATE_KEY", PRIVATE_KEY)
    monkeypatch.setenv("JWT_PUBLIC_KEY", PUBLIC_KEY)
    monkeypatch.setenv("KEYS_DIR", KEYS_DIR)

    # Copy keys into the working directory structure the agent may expect
    app_keys_dir = os.path.join(TASK_DIR, "keys")
    created_keys_dir = False
    if not os.path.isdir(app_keys_dir):
        os.makedirs(app_keys_dir, exist_ok=True)
        shutil.copy2(os.path.join(KEYS_DIR, "private.pem"), app_keys_dir)
        shutil.copy2(os.path.join(KEYS_DIR, "public.pem"), app_keys_dir)
        created_keys_dir = True

    # Also copy into src/keys/ if agent looks there
    src_keys_dir = os.path.join(TASK_DIR, "src", "keys")
    created_src_keys = False
    if not os.path.isdir(src_keys_dir):
        os.makedirs(src_keys_dir, exist_ok=True)
        shutil.copy2(os.path.join(KEYS_DIR, "private.pem"), src_keys_dir)
        shutil.copy2(os.path.join(KEYS_DIR, "public.pem"), src_keys_dir)
        created_src_keys = True

    yield db_path

    # Cleanup copied keys if we created them
    if created_keys_dir:
        shutil.rmtree(app_keys_dir, ignore_errors=True)
    if created_src_keys:
        shutil.rmtree(src_keys_dir, ignore_errors=True)


@pytest.fixture
def client():
    """Flask test client."""
    _app.config["TESTING"] = True
    with _app.test_client() as c:
        yield c


@pytest.fixture
def admin_token():
    """Generate a valid admin JWT token."""
    return make_token(user_id=1, email=ADMIN_EMAIL, role="admin")


@pytest.fixture
def user_token():
    """Generate a valid regular-user JWT token (assumes user id=2 exists)."""
    return make_token(user_id=2, email="testuser@example.com", role="user")


# ---------------------------------------------------------------------------
# Helper functions (available as module-level imports in test files)
# ---------------------------------------------------------------------------

def make_token(user_id=1, email=ADMIN_EMAIL, role="admin", expired=False):
    """Mint a JWT signed with the seed private key."""
    now = datetime.datetime.utcnow()
    if expired:
        exp = now - datetime.timedelta(hours=1)
    else:
        exp = now + datetime.timedelta(hours=24)

    payload = {
        "sub": user_id,
        "user_id": user_id,
        "email": email,
        "role": role,
        "iat": now,
        "exp": exp,
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")


def auth_header(token):
    """Return an Authorization header dict."""
    return {"Authorization": f"Bearer {token}"}


def create_test_user(client, admin_token, email="newuser@example.com",
                     password="Test1234!", full_name="Test User", role="user"):
    """Create a user via the API and return the response."""
    return client.post(
        "/api/users",
        json={
            "email": email,
            "password": password,
            "full_name": full_name,
            "role": role,
        },
        headers=auth_header(admin_token),
    )


def login(client, email=ADMIN_EMAIL, password=ADMIN_PASSWORD):
    """Log in via the API and return the response."""
    return client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
