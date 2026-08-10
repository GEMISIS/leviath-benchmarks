"""Harbor "installed agent" adapter: run leviath inside a task container.

Harbor (the framework behind Terminal-Bench 2.x and Frontier-Bench)
drives agents through a BaseAgent subclass: setup() provisions the task
container, run() executes the task, and the AgentContext carries token
accounting back to Harbor's results. This adapter installs a Linux lev
binary plus the frozen benchmark blueprints into the container and runs
one headless `lev run`.

Environment contract (set these before `harbor run`):
- LEV_LINUX_BIN: host path to a Linux lev binary matching the task
  container's architecture (the release tarballs work).
- LEVIATH_BLUEPRINT: which installed blueprint to run (default
  coder-bench; flat-coder for the flat arm).
- Provider API keys (ANTHROPIC_API_KEY, ...) must be passed through to
  the agent's exec environment via Harbor's extra_env mechanism; they
  are read by lev inside the container and never written to disk here.

Model selection: Harbor's --model value (provider/model) is passed
straight to `lev run -m`, which overrides every stage - the pinned-arm
contract. Without --model the blueprint's native stage mix runs.

Token accounting: harvested from the run's meta.json (cat over exec,
sentinel-delimited), which carries provider-reported prompt, completion,
cache-read, and cache-write token counts. n_input_tokens is reported
cache-inclusive, matching Harbor's field description.

Usage:
    harbor run -d terminal-bench@2.1 \
        --agent bench.quality.suites.terminalbench.harbor_agent:LeviathAgent \
        --model anthropic/<pinned>
"""
from __future__ import annotations

import json
import os
import re
import shlex
import time
from pathlib import Path

_ANSI = re.compile(r"\x1b\[[0-9;]*m")


def _json_payload(text: str):
    """Parse JSON from CLI stdout that may carry an ANSI-colored log
    line ahead of the payload (TTY-less containers log to stdout)."""
    clean = _ANSI.sub("", text)
    start = min((i for i in (clean.find("{"), clean.find("["))
                 if i >= 0), default=0)
    return json.loads(clean[start:])

# Pier (the deep-swe runner) is a Harbor fork with the identical
# BaseAgent/BaseEnvironment/AgentContext interface, so one adapter file
# serves terminal-bench/frontier-bench (harbor) and deep-swe (pier).
# When both packages are installed, LEVIATH_ADAPTER_RUNTIME=pier forces
# the pier base classes (a pier-driven run must subclass pier's
# BaseAgent, not harbor's).
if os.environ.get("LEVIATH_ADAPTER_RUNTIME") == "pier":
    from pier.agents.base import AgentContext, BaseAgent
    from pier.environments.base import BaseEnvironment
else:
    try:
        from harbor.agents.base import AgentContext, BaseAgent
        from harbor.environments.base import BaseEnvironment
    except ImportError:  # pragma: no cover - pier-only installs
        from pier.agents.base import AgentContext, BaseAgent
        from pier.environments.base import BaseEnvironment

QUALITY_DIR = Path(__file__).resolve().parents[2]
HOME = "/opt/levbench"
TERMINAL = {"complete", "error", "cancelled", "complete_interactive"}
META_BEGIN, META_END = "LEVMETA_BEGIN", "LEVMETA_END"


class LeviathAgent(BaseAgent):
    SUPPORTS_ATIF = False

    @staticmethod
    def name() -> str:
        return "leviath"

    def version(self) -> str | None:
        return os.environ.get("LEV_VERSION", "0.2.0")

    def _blueprint(self) -> str:
        return os.environ.get("LEVIATH_BLUEPRINT", "coder-bench")

    async def _sh(self, environment: BaseEnvironment, cmd: str,
                  timeout: int = 300) -> str:
        result = await environment.exec(cmd, timeout_sec=timeout)
        if result.return_code != 0:
            self.logger.warning("exec rc=%s stderr=%s", result.return_code,
                                (result.stderr or "")[:400])
        return result.stdout or ""

    async def setup(self, environment: BaseEnvironment) -> None:
        # Pick the binary by the CONTAINER's architecture - task images
        # may be x86_64 under emulation on an arm host.
        arch_out = await environment.exec("uname -m")
        arch = (arch_out.stdout or "").strip()
        env_var = ("LEV_LINUX_ARM64" if arch in ("aarch64", "arm64")
                   else "LEV_LINUX_X64")
        lev_bin = os.environ.get(env_var) or os.environ.get("LEV_LINUX_BIN")
        if not lev_bin or not Path(lev_bin).is_file():
            raise RuntimeError(
                f"{env_var} (or LEV_LINUX_BIN) must point at a Linux "
                f"lev binary for container arch {arch!r}")
        blueprint = self._blueprint()
        # Parent directories must exist before any upload lands.
        await self._sh(environment,
                       f"mkdir -p {HOME}/.leviath/agents/{blueprint}")
        await environment.upload_file(Path(lev_bin), "/opt/lev")
        await environment.upload_dir(
            QUALITY_DIR / "blueprints" / blueprint,
            f"{HOME}/.leviath/agents/{blueprint}")
        await self._sh(environment, "chmod +x /opt/lev")
        # Provider keys travel as an uploaded config file, never inside
        # shell command lines (which containers log).
        import tempfile
        keys = {
            "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY"),
            "openai_api_key": os.environ.get("OPENAI_API_KEY"),
            "google_api_key": os.environ.get("GOOGLE_API_KEY"),
        }
        lines = ["[providers]"]
        lines += [f'{k} = "{v}"' for k, v in keys.items() if v]
        openrouter = os.environ.get("OPENROUTER_API_KEY")
        if openrouter:
            lines.insert(0, f'openrouter_api_key = "{openrouter}"')
        with tempfile.NamedTemporaryFile("w", suffix=".toml",
                                         delete=False) as fh:
            fh.write("\n".join(lines) + "\n")
            tmp = fh.name
        try:
            await environment.upload_file(
                Path(tmp), f"{HOME}/.leviath/config.toml")
        finally:
            os.unlink(tmp)
        # The provider HTTP client refuses to build without system CA
        # certificates; minimal images ship none.
        await self._sh(environment, (
            "if [ ! -e /etc/ssl/certs/ca-certificates.crt ]; then "
            "apt-get update -qq && "
            "apt-get install -y -qq ca-certificates >/dev/null; fi"),
            timeout=600)

    async def run(self, instruction: str, environment: BaseEnvironment,
                  context: AgentContext) -> None:
        blueprint = self._blueprint()
        model_flag = f"-m {shlex.quote(self.model_name)}" if self.model_name else ""
        env_prefix = f"LEVIATH_HOME={HOME} LEVIATH_SKIP_DOTENV=1"

        launch_cmd = (
            f"{env_prefix} /opt/lev run {shlex.quote(blueprint)} "
            f"{model_flag} --yolo --json --workdir \"$PWD\" "
            f"--task {shlex.quote(instruction)}")
        result = await environment.exec(launch_cmd, timeout_sec=300)
        launch = result.stdout or ""
        if not launch.strip():
            raise RuntimeError(
                f"lev run produced no output (rc={result.return_code}); "
                f"stderr: {(result.stderr or '')[-500:]}")
        try:
            payload = _json_payload(launch)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"lev run stdout was not JSON (rc={result.return_code}): "
                f"stdout[:400]={launch[:400]!r} "
                f"stderr[-400:]={(result.stderr or '')[-400:]!r}") from exc
        if isinstance(payload, list):
            payload = payload[0]
        run_id = payload["run_id"]
        meta_path = f"{HOME}/.leviath/runs/{run_id}/meta.json"

        deadline = time.time() + float(
            os.environ.get("LEVIATH_TASK_TIMEOUT_SECS", "3600"))
        # Same runaway protection as the local runner: cancel mid-run
        # past a billed-token ceiling (0 disables).
        max_tokens = int(os.environ.get("LEVIATH_MAX_BILLED_TOKENS",
                                        "10000000"))
        meta: dict = {}
        while time.time() < deadline:
            text = await self._sh(environment, (
                f"echo {META_BEGIN}; cat {shlex.quote(meta_path)} "
                f"2>/dev/null; echo; echo {META_END}"))
            meta = _between(text) or {}
            # Populate the context every poll, not just at the end, so
            # a harness-side timeout still reports the tokens spent
            # (per the BaseAgent contract's own guidance).
            self._report(context, meta, run_id, blueprint)
            if meta.get("status") in TERMINAL:
                break
            billed = sum(int(meta.get(k, 0) or 0) for k in
                         ("prompt_tokens", "completion_tokens",
                          "cached_tokens", "cache_write_tokens"))
            if max_tokens and billed > max_tokens:
                await self._sh(environment,
                               f"{env_prefix} /opt/lev cancel {run_id} "
                               "|| true")
                break
            time.sleep(5.0)
        else:
            await self._sh(environment,
                           f"{env_prefix} /opt/lev cancel {run_id} || true")

        # deep-swe's verifier extracts the agent's work as the commits it
        # made; commit whatever the run left in the task workdir. Inert
        # when the workdir is not a git checkout (terminal-bench tasks).
        await self._sh(environment, (
            'if git -C "$PWD" rev-parse --is-inside-work-tree '
            ">/dev/null 2>&1; then "
            'git -C "$PWD" add -A && '
            'git -C "$PWD" -c user.email=agent@localhost '
            '-c user.name=agent commit -m "agent work" || true; fi'))

        self._report(context, meta, run_id, blueprint)

    def _report(self, context: AgentContext, meta: dict, run_id: str,
                blueprint: str) -> None:
        prompt = int(meta.get("prompt_tokens", 0) or 0)
        cached = int(meta.get("cached_tokens", 0) or 0)
        cache_write = int(meta.get("cache_write_tokens", 0) or 0)
        context.n_input_tokens = prompt + cached + cache_write
        context.n_cache_tokens = cached
        context.n_output_tokens = int(meta.get("completion_tokens", 0) or 0)
        context.metadata = {
            "run_id": run_id,
            "status": meta.get("status", "unknown"),
            "final_stage": meta.get("current_stage"),
            "tool_calls": meta.get("tool_calls"),
            "iterations": meta.get("iteration"),
            "blueprint": blueprint,
            "model_override": self.model_name,
            "usage": {"prompt_tokens": prompt, "cached_tokens": cached,
                      "cache_write_tokens": cache_write,
                      "completion_tokens": context.n_output_tokens},
        }


def _between(text: str) -> dict | None:
    try:
        body = text.split(META_BEGIN, 1)[1].split(META_END, 1)[0].strip()
        return _json_payload(body) if body else None
    except (IndexError, json.JSONDecodeError):
        return None
