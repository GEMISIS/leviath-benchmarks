"""Score a CRS run's artifact against its task's held-out verification.

Ported from the July harness's scripts/validate-run.sh (kept at
recovered/validate-run.sh): copy the task's validation/ suite into the
run's workdir, install its requirements into a fresh venv, run pytest
with --json-report, and parse the summary. Differences from the shell
original, all deliberate:

- suite_hash is a sha256 manifest over the validation files themselves
  (the old `git rev-parse HEAD:...` breaks in a worktree and says
  nothing once files move);
- "no tests ran" is a recorded failure with a reason, never a refusal
  that loses the run;
- record writing belongs to the quality runner, not this module.

Non-coding tasks verify against an answer key instead: a task directory
with answers.json (or the loganalysis-style salted heldout hashes) is
scored by exact match of the run's submitted answer.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

VENV_TIMEOUT_SECS = 600
PYTEST_TIMEOUT_SECS = 900


def suite_hash(validation_dir: Path) -> str:
    """sha256 over (relative path, bytes) of every validation file."""
    digest = hashlib.sha256()
    for path in sorted(validation_dir.rglob("*")):
        if path.is_file():
            digest.update(str(path.relative_to(validation_dir)).encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def run_pytest(task_dir: Path, workdir: Path,
               artifacts_dir: Path) -> dict:
    """The held-out pytest suite against the run's workdir."""
    validation_src = task_dir / "validation"
    if not validation_src.is_dir():
        return {"passed": 0, "failed": 0, "errors": 0, "total": 0,
                "failures": [], "suite_hash": None,
                "detail": "task has no validation suite"}

    validation = workdir / "validation"
    if validation.exists():
        # A run that wrote into validation/ does not get to grade itself.
        subprocess.run(["rm", "-rf", str(validation)], check=True)
    subprocess.run(["cp", "-R", str(validation_src), str(validation)],
                   check=True)

    venv = workdir / ".crs-venv"
    py = venv / "bin" / "python3"
    report_path = artifacts_dir / "pytest-report.json"
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv)],
                       check=True, capture_output=True,
                       timeout=VENV_TIMEOUT_SECS)
        subprocess.run([str(py), "-m", "pip", "install", "-q", "-r",
                        str(validation / "requirements.txt")],
                       check=True, capture_output=True,
                       timeout=VENV_TIMEOUT_SECS)
        workdir_reqs = workdir / "requirements.txt"
        if workdir_reqs.is_file():
            # The agent's own dependencies; failure to install them is
            # the run's failure, not the harness's.
            subprocess.run([str(py), "-m", "pip", "install", "-q", "-r",
                            str(workdir_reqs)],
                           capture_output=True, timeout=VENV_TIMEOUT_SECS)
        proc = subprocess.run(
            [str(py), "-m", "pytest", str(validation), "--tb=line",
             "--json-report", f"--json-report-file={report_path}"],
            cwd=workdir, capture_output=True, timeout=PYTEST_TIMEOUT_SECS)
        # pytest's own words, kept beside the report: when the JSON is
        # missing or empty, this log is the diagnosis.
        (artifacts_dir / "pytest-output.txt").write_bytes(
            proc.stdout + b"\n--- stderr ---\n" + proc.stderr)
    except subprocess.TimeoutExpired as exc:
        return {"passed": 0, "failed": 0, "errors": 1, "total": 1,
                "failures": [f"timeout: {exc.cmd[0]}"],
                "suite_hash": suite_hash(validation_src),
                "detail": "validation timed out"}
    except subprocess.CalledProcessError as exc:
        return {"passed": 0, "failed": 0, "errors": 1, "total": 1,
                "failures": [f"setup failed: {exc.cmd[:2]}"],
                "suite_hash": suite_hash(validation_src),
                "detail": "validation environment setup failed"}

    try:
        report = json.loads(report_path.read_text())
    except (OSError, json.JSONDecodeError):
        return {"passed": 0, "failed": 0, "errors": 1, "total": 1,
                "failures": ["pytest wrote no report"],
                "suite_hash": suite_hash(validation_src),
                "detail": "no pytest report produced"}

    summary = report.get("summary", {})
    passed = int(summary.get("passed", 0))
    failed = int(summary.get("failed", 0))
    errors = int(summary.get("error", 0))
    total = passed + failed + errors
    failures = [t["nodeid"].split("::")[-1]
                for t in report.get("tests", [])
                if t.get("outcome") in ("failed", "error")]
    out = {"passed": passed, "failed": failed, "errors": errors,
           "total": total, "failures": failures,
           "suite_hash": suite_hash(validation_src)}
    if total == 0:
        out["detail"] = "no tests ran"
    return out


def run_answer_key(task_dir: Path, answer: str | None) -> dict:
    """Non-coding tasks: keyed answers, one expected value per line.

    answers.json: {"answers": ["...", ...]} - the task's generator
    writes it (or a salted-hash variant revealed at publish time). The
    submitted answer is compared line-by-line after whitespace
    normalization; every expected line counts, matched or not.
    """
    key_path = task_dir / "answers.json"
    if not key_path.is_file():
        return {"passed": 0, "failed": 0, "errors": 1, "total": 1,
                "failures": ["no answer key"], "suite_hash": None,
                "detail": "task has no answers.json"}
    key = json.loads(key_path.read_text())
    expected = [str(a).strip() for a in key["answers"]]
    got = [line.strip() for line in (answer or "").splitlines()
           if line.strip()]
    failures = [f"line {i + 1}: expected {e!r}"
                for i, e in enumerate(expected)
                if i >= len(got) or got[i] != e]
    total = len(expected)
    matched = total - len(failures)
    return {"passed": matched, "failed": len(failures), "errors": 0,
            "total": total, "failures": failures[:20],
            "suite_hash": hashlib.sha256(
                key_path.read_bytes()).hexdigest()}
