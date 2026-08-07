"""Everything the quality track says to lev goes through this module.

Mirrors the performance runner's conventions: an isolated home (so the
user's real ~/.leviath is never touched), a short path (Unix socket
SUN_LEN cap), daemon lifecycle by pidfile, readiness by `lev ps --json`,
and per-run truth read from the run's meta.json on disk.

The quality track uses its own home (/tmp/levqual) so a perf run and a
quality run can never contaminate each other.
"""
from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import time
from pathlib import Path

__all__ = ["QualityHome", "TERMINAL"]

TERMINAL = {"complete", "error", "cancelled", "complete_interactive"}
_READY_TIMEOUT = 30.0


class QualityHome:
    """One isolated LEVIATH_HOME plus the lev calls the runner needs."""

    def __init__(self, lev: str, home: Path = Path("/tmp/levqual")):
        self.lev = lev
        self.home = home
        self.runs_dir = home / ".leviath" / "runs"
        self._daemon: subprocess.Popen | None = None

    # -- home ---------------------------------------------------------
    def install(self, blueprints_dir: Path, config_text: str,
                providers_dir: Path | None = None) -> None:
        """Fresh home with the frozen blueprints and the given config."""
        shutil.rmtree(self.home, ignore_errors=True)
        (self.home / ".leviath").mkdir(parents=True)
        (self.home / "work").mkdir()
        agents_dir = self.home / ".leviath" / "agents"
        agents_dir.mkdir()
        for blueprint in sorted(Path(blueprints_dir).iterdir()):
            if (blueprint / "agent.leviath").is_file():
                shutil.copytree(blueprint, agents_dir / blueprint.name)
        if providers_dir is not None:
            shutil.copytree(providers_dir,
                            self.home / ".leviath" / "providers")
        (self.home / ".leviath" / "config.toml").write_text(config_text)

    def env(self, extra: dict | None = None) -> dict:
        env = dict(os.environ, LEVIATH_HOME=str(self.home),
                   LEVIATH_SKIP_DOTENV="1")
        env.pop("LEVIATH_RUNS_DIR", None)
        env.update(extra or {})
        return env

    # -- daemon -------------------------------------------------------
    def start_daemon(self, extra_env: dict | None = None) -> None:
        self._daemon = subprocess.Popen(
            [self.lev, "daemon"], env=self.env(extra_env),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True)
        deadline = time.time() + _READY_TIMEOUT
        while time.time() < deadline:
            probe = subprocess.run([self.lev, "ps", "--json"],
                                   env=self.env(extra_env),
                                   capture_output=True, text=True)
            if probe.returncode == 0:
                return
            time.sleep(0.05)
        raise RuntimeError("daemon did not become ready "
                           f"within {_READY_TIMEOUT}s")

    def stop_daemon(self) -> None:
        pidfile = self.home / ".leviath" / "daemon.pid"
        pid = None
        try:
            pid = int(pidfile.read_text().strip())
        except (OSError, ValueError):
            if self._daemon is not None:
                pid = self._daemon.pid
        if pid is not None:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        if self._daemon is not None:
            try:
                self._daemon.wait(timeout=30)
            except subprocess.TimeoutExpired:
                self._daemon.kill()
            self._daemon = None

    # -- runs ---------------------------------------------------------
    def launch(self, agent: str, task_text: str, workdir: Path,
               model: str | None = None, extra_args: list[str] | None = None,
               extra_env: dict | None = None) -> str:
        cmd = [self.lev, "run", agent, "--task", task_text, "--yolo",
               "--json", "--workdir", str(workdir)]
        if model:
            cmd += ["-m", model]
        cmd += extra_args or []
        out = subprocess.run(cmd, env=self.env(extra_env),
                             capture_output=True, text=True, timeout=120)
        if out.returncode != 0:
            raise RuntimeError(f"lev run failed: {out.stderr.strip()[:400]}")
        # Without a TTY the runtime's INFO log line can land on stdout
        # ahead of the JSON payload, ANSI-colored - strip escapes, then
        # parse from the first JSON character.
        import re
        text = re.sub(r"\x1b\[[0-9;]*m", "", out.stdout)
        start = min((i for i in (text.find("{"), text.find("["))
                     if i >= 0), default=0)
        payload = json.loads(text[start:])
        if isinstance(payload, list):
            payload = payload[0]
        return payload["run_id"]

    def stages(self, run_id: str) -> list[dict]:
        """Per-stage ledger (name + token counts) from stages.json."""
        path = self.runs_dir / run_id / "stages.json"
        try:
            return json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            return []

    def meta(self, run_id: str) -> dict | None:
        path = self.runs_dir / run_id / "meta.json"
        try:
            return json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            return None

    def wait(self, run_id: str, timeout_secs: float,
             poll_secs: float = 1.0,
             should_cancel=None) -> tuple[str, dict | None]:
        """Poll meta.json until terminal. Returns (status, meta).

        On timeout the run is cancelled and status "timeout" returned.
        ``should_cancel(meta)`` is checked each poll; returning True
        cancels the run with status "cap" - the per-run spend ceiling,
        enforced mid-run because a single runaway run can otherwise
        blow through a whole round budget before the next between-run
        check. Either way the captured meta still carries the tokens
        spent.
        """
        deadline = time.time() + timeout_secs
        meta = None
        while time.time() < deadline:
            meta = self.meta(run_id)
            if meta and meta.get("status") in TERMINAL:
                return meta["status"], meta
            if meta and should_cancel is not None and should_cancel(meta):
                subprocess.run([self.lev, "cancel", run_id],
                               env=self.env(), capture_output=True,
                               text=True)
                time.sleep(2.0)
                return "cap", self.meta(run_id) or meta
            time.sleep(poll_secs)
        subprocess.run([self.lev, "cancel", run_id], env=self.env(),
                       capture_output=True, text=True)
        time.sleep(2.0)
        return "timeout", self.meta(run_id) or meta

    def result(self, run_id: str,
               extra_env: dict | None = None) -> str | None:
        """Final answer text, or None when the run produced no answer.

        One short retry: the answer sidecar is written by an async
        persistence lane and can trail the terminal status by a moment.
        """
        out = subprocess.run([self.lev, "result", run_id, "--json"],
                             env=self.env(extra_env), capture_output=True,
                             text=True)
        if out.returncode != 0:
            time.sleep(2.0)
            out = subprocess.run([self.lev, "result", run_id, "--json"],
                                 env=self.env(extra_env),
                                 capture_output=True, text=True)
        if out.returncode != 0:
            return None
        try:
            payload = json.loads(out.stdout)
        except json.JSONDecodeError:
            return out.stdout.strip() or None
        if isinstance(payload, dict):
            for key in ("answer", "result", "output", "content"):
                if isinstance(payload.get(key), str):
                    return payload[key]
            return json.dumps(payload)
        return str(payload)

    def context_dump(self, run_id: str) -> str | None:
        out = subprocess.run(
            [self.lev, "context", run_id, "--json", "--full"],
            env=self.env(), capture_output=True, text=True)
        return out.stdout if out.returncode == 0 else None

    def version(self) -> str:
        out = subprocess.run([self.lev, "--version"], capture_output=True,
                             text=True)
        return out.stdout.strip()
