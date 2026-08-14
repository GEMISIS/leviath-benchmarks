"""Everything the quality track says to lev goes through this module.

Mirrors the performance runner's conventions: an isolated home (so the
user's real ~/.leviath is never touched), a short path (Unix socket
SUN_LEN cap), daemon lifecycle by pidfile, readiness by `lev ps --json`,
and per-run truth read from the run's meta.json on disk.

The quality track uses its own home (/tmp/levqual) so a perf run and a
quality run can never contaminate each other.
"""
from __future__ import annotations

import gzip
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
    @staticmethod
    def capability_overrides(roster: dict) -> str:
        """`[model_capabilities]` pinning each model's context window.

        Region budgets are percentages of the model's window, so the
        window silently decides how large every region is. Since leviath
        0.3.3 (#360) the runtime primes OpenRouter windows from the
        provider's /models at daemon start, so this pin is no longer a
        bug workaround - it is a freeze: the round runs under the window
        it declared rather than whatever the live lookup returned (or
        failed to return - the priming has a 10s timeout and often lacks
        max_output_tokens). Keys are the model id as the provider sees
        it, without the leading provider segment.

        Only models whose declared window differs from what the runtime
        resolves are overridden, and each entry carries all six fields:
        the capability struct has no serde defaults, so a partial entry
        is silently ignored rather than rejected (verified: a lone
        max_context_tokens leaves the window unchanged).
        """
        lines = []
        for name, entry in sorted(roster.items()):
            caps = entry.get("capability_override")
            if not caps:
                continue
            model = entry["id"].split("/", 1)[1]
            body = "\n".join(
                f"{k} = {json.dumps(v)}" for k, v in caps.items())
            lines.append(f'# {name}: {entry.get("override_reason", "")}\n'
                         f'[model_capabilities."{model}"]\n{body}\n')
        return "\n".join(lines)

    @staticmethod
    def concurrency_config(concurrency: int, rate_limits: dict) -> str:
        """Daemon limits and provider rate limits for a parallel round.

        Two install defaults throttle a round long before the machine
        does: `max_concurrent_inferences` caps in-flight calls per model
        at 8, and `max_concurrent_tools` caps how many *agents* may run
        tools across the whole daemon, also at 8. Every turn of these
        agents runs a tool, so the second is the one that decides
        throughput. Both are raised to the concurrency the round asked
        for, with headroom for the sub-runs an agent may spawn.

        The real ceiling is the provider, not the host, so a round also
        declares the limits it is running under and lets the daemon
        throttle itself rather than discovering them as 429s. Values
        come from arms.json, which is frozen with the round: what we
        promised to stay under is part of what was measured.
        """
        lanes = max(8, int(concurrency) * 2)
        out = ["[limits]",
               f"max_concurrent_inferences = {lanes}",
               f"max_concurrent_tools = {lanes}", ""]
        for provider, limits in sorted(rate_limits.items()):
            rpm = int(limits.get("requests_per_minute", 0) or 0)
            tpm = int(limits.get("tokens_per_minute", 0) or 0)
            if not rpm and not tpm:
                continue
            out += [f"[rate_limits.{provider}]",
                    f"requests_per_minute = {rpm}",
                    f"tokens_per_minute = {tpm}", ""]
        return "\n".join(out)

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
               extra_env: dict | None = None, yolo: bool = True) -> str:
        # yolo=False keeps the ask_user_* tools in the advertised tool
        # set (--yolo strips them before inference); the caller must
        # then answer interactions itself or the run parks until the
        # daemon's interaction timeout.
        cmd = [self.lev, "run", agent, "--task", task_text,
               "--json", "--workdir", str(workdir)]
        if yolo:
            cmd.append("--yolo")
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
             should_cancel=None,
             max_paused_secs: float = 7200.0) -> tuple[str, dict | None]:
        """Poll meta.json until terminal. Returns (status, meta).

        On timeout the run is cancelled and status "timeout" returned.
        ``should_cancel(meta)`` is checked each poll; returning True
        cancels the run with status "cap" - the per-run spend ceiling,
        enforced mid-run because a single runaway run can otherwise
        blow through a whole round budget before the next between-run
        check. Either way the captured meta still carries the tokens
        spent.

        A PAUSED run is waiting on the outside world - leviath pauses
        on provider credit exhaustion, resumable after a top-up - and
        spends nothing, so paused time does not count against the task
        timeout. The harness retries `lev resume` once a minute (a
        resume without credits just re-pauses on the next inference)
        and gives up after ``max_paused_secs`` of accumulated pause.
        """
        deadline = time.time() + timeout_secs
        meta = None
        paused_total = 0.0
        resume_at = 0.0
        while time.time() < deadline:
            meta = self.meta(run_id)
            if meta and meta.get("status") in TERMINAL:
                return meta["status"], meta
            if meta and meta.get("status") == "paused":
                paused_total += poll_secs
                deadline += poll_secs
                if paused_total > max_paused_secs:
                    break  # falls through to cancel/timeout below
                if time.time() >= resume_at:
                    subprocess.run([self.lev, "resume", run_id],
                                   env=self.env(), capture_output=True,
                                   text=True)
                    resume_at = time.time() + 60.0
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

    def archive_run(self, run_id: str, dest: Path,
                    gated: bool = False) -> list[str]:
        """Keep the daemon's own files for a run, next to its record.

        The daemon writes everything needed to reconstruct a run - the
        meta, the per-stage ledger, the final context snapshot, the
        answer, and the full event log - but the isolated home is wiped
        at the start of the next suite, so a round that does not copy
        them cannot be investigated afterwards. The event log is bulky
        and compresses well, so it travels gzipped.

        ``gated`` restricts the archive to the two files that carry no
        dataset content: a gated suite's context snapshot and event log
        embed the question text its terms forbid us from storing.
        """
        src = self.runs_dir / run_id
        if not src.is_dir():
            return []
        keep = ["meta.json", "stages.json"]
        if not gated:
            keep += ["context.json", "final_output"]
        dest.mkdir(parents=True, exist_ok=True)
        written = []
        for name in keep:
            p = src / name
            if p.is_file():
                shutil.copyfile(p, dest / name)
                written.append(name)
        lvr = src / "run.lvr"
        if not gated and lvr.is_file():
            (dest / "run.lvr.gz").write_bytes(gzip.compress(lvr.read_bytes()))
            written.append("run.lvr.gz")
        return written

    def context_dump(self, run_id: str) -> str | None:
        out = subprocess.run(
            [self.lev, "context", run_id, "--json", "--full"],
            env=self.env(), capture_output=True, text=True)
        return out.stdout if out.returncode == 0 else None

    def version(self) -> str:
        out = subprocess.run([self.lev, "--version"], capture_output=True,
                             text=True)
        return out.stdout.strip()
