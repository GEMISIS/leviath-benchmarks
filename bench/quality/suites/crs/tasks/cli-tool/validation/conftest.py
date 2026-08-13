import os
import subprocess
import tempfile
import textwrap

import pytest


SAMPLE_LOG_LINES = textwrap.dedent("""\
[2024-01-15 10:30:45] [INFO] [http-server] Request received GET /api/users
[2024-01-15 10:30:46] [DEBUG] [database] Query executed: SELECT * FROM users
[2024-01-15 10:30:47] [INFO] [http-server] Response sent 200 OK
[2024-01-15 10:30:48] [WARN] [auth] Token expiring soon for user=42
[2024-01-15 10:30:49] [ERROR] [database] Connection timeout (database)
[2024-01-15 10:30:50] [INFO] [http-server] Request received POST /api/login
[2024-01-15 10:30:51] [DEBUG] [cache] Cache miss for key=session_42
[2024-01-15 10:30:52] [ERROR] [database] Connection timeout (database)
[2024-01-15 10:30:53] [FATAL] [database] Connection pool exhausted
[2024-01-15 10:30:54] [INFO] [http-server] Request received GET /api/health
[2024-01-15 10:30:55] [INFO] [scheduler] Cron job started: cleanup
[2024-01-15 10:30:56] [WARN] [http-server] Slow response time: 2340ms
[2024-01-15 10:30:57] [INFO] [http-server] Request received GET /api/users/1
[2024-01-15 10:30:58] [DEBUG] [database] Query executed: SELECT * FROM users WHERE id=1
[2024-01-15 10:30:59] [INFO] [http-server] Response sent 200 OK
""").strip()


SAMPLE_LOG_WITH_MALFORMED = SAMPLE_LOG_LINES + "\n" + textwrap.dedent("""\
this line is malformed and has no proper format
another bad line without brackets
[2024-01-15 10:31:00] [INFO] [http-server] Final valid line
""").strip()


@pytest.fixture
def tmp_dir():
    """Create a temporary directory that is cleaned up after the test."""
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def sample_log_file(tmp_dir):
    """Create a sample log file with known valid content."""
    path = os.path.join(tmp_dir, "application.log")
    with open(path, "w") as f:
        f.write(SAMPLE_LOG_LINES + "\n")
    return path


@pytest.fixture
def sample_log_with_malformed(tmp_dir):
    """Create a sample log file that includes malformed lines."""
    path = os.path.join(tmp_dir, "malformed.log")
    with open(path, "w") as f:
        f.write(SAMPLE_LOG_WITH_MALFORMED + "\n")
    return path


@pytest.fixture
def empty_log_file(tmp_dir):
    """Create an empty log file."""
    path = os.path.join(tmp_dir, "empty.log")
    with open(path, "w") as f:
        pass
    return path


@pytest.fixture
def multi_level_log_file(tmp_dir):
    """Create a log file with a controlled distribution of levels and components."""
    lines = []
    base = "2024-01-15 10:30:{sec:02d}"
    sec = 0
    # 3 DEBUG
    for _ in range(3):
        lines.append(f"[{base.format(sec=sec)}] [DEBUG] [database] Debug message {sec}")
        sec += 1
    # 5 INFO
    for _ in range(5):
        lines.append(f"[{base.format(sec=sec)}] [INFO] [http-server] Info message {sec}")
        sec += 1
    # 2 WARN
    for _ in range(2):
        lines.append(f"[{base.format(sec=sec)}] [WARN] [auth] Warn message {sec}")
        sec += 1
    # 4 ERROR  (2 distinct messages)
    for i in range(4):
        comp = "database" if i < 2 else "http-server"
        msg = "Connection timeout (database)" if i < 2 else "Request failed (http-server)"
        lines.append(f"[{base.format(sec=sec)}] [ERROR] [{comp}] {msg}")
        sec += 1
    # 1 FATAL
    lines.append(f"[{base.format(sec=sec)}] [FATAL] [database] Connection pool exhausted")
    sec += 1

    path = os.path.join(tmp_dir, "multi.log")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path


@pytest.fixture
def config_file(tmp_dir):
    """Create a sample config file."""
    config_dir = os.path.join(tmp_dir, ".logviz")
    os.makedirs(config_dir, exist_ok=True)
    path = os.path.join(config_dir, "config.yaml")
    with open(path, "w") as f:
        f.write(textwrap.dedent("""\
            default_export_format: json
            colors:
              DEBUG: cyan
              INFO: green
              WARN: yellow
              ERROR: red
              FATAL: magenta_bold
            date_format: "%Y-%m-%d %H:%M:%S"
            timezone: UTC
            tail_buffer_size: 1000
            streaming:
              chunk_size: 8192
              auto_stream_threshold_mb: 100
        """))
    return path


def run_logviz(*args, cwd=None):
    """Run the logviz CLI tool as a subprocess and return the CompletedProcess.

    The tool is invoked via ``python3 -m logviz`` so that the agent's
    ``logviz/`` package is picked up from the working directory.
    """
    # Resolve the directory that contains the agent's logviz/ package.
    # The deliverable lives at tasks/cli-tool/logviz/ (sibling of validation/).
    task_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
    work_dir = cwd or task_dir

    cmd = ["python3", "-m", "logviz"] + list(args)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=work_dir,
        timeout=30,
    )
    return result


@pytest.fixture
def cli():
    """Provide the ``run_logviz`` helper as a fixture."""
    return run_logviz
