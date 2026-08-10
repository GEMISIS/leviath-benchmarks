#!/usr/bin/env python3
"""Spike: prove lev runs headless inside a Linux task container.

This is the de-risking step for every container-hosted coding suite:
the daemon must boot as an ordinary background process (no systemd),
the control socket must fit the SUN_LEN path cap, a run must reach a
terminal status, and meta.json must come back over the container's
stdout between sentinels - the same extraction path the real adapter
uses when the harness offers no file copy.

Uses the deterministic mock provider so the spike needs no API keys and
no egress. Requires a local Docker daemon and a Linux lev binary.

Usage:
    python3 spike_container.py --lev-linux /path/to/linux/lev \
        [--image ubuntu:24.04]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

QUALITY_DIR = Path(__file__).resolve().parents[2]
BENCH_DIR = QUALITY_DIR.parent

IN_CONTAINER = r"""
set -eu
export LEVIATH_HOME=/opt/levbench
export LEVIATH_SKIP_DOTENV=1
# The provider layer's HTTP client refuses to build without system CA
# certificates, and minimal images ship none. The real adapter's install
# step must make the same guarantee.
if [ ! -e /etc/ssl/certs/ca-certificates.crt ]; then
    apt-get update -qq && apt-get install -y -qq ca-certificates >/dev/null
fi
mkdir -p /opt/levbench /work
cd /work
echo spike-log-line-1 > log.txt
echo spike-log-line-2 >> log.txt

RUN_JSON=$(/opt/lev run flat-loganalyzer -m mockx/sim-1 \
    --task "How many lines are in log.txt? Reply with only the number." \
    --yolo --json --workdir /work)
RUN_ID=$(printf '%s' "$RUN_JSON" | sed -n 's/.*"run_id"[: ]*"\([^"]*\)".*/\1/p')
echo "spike: run_id=$RUN_ID"

for i in $(seq 1 120); do
    STATUS=$(sed -n 's/.*"status"[: ]*"\([^"]*\)".*/\1/p' \
        "/opt/levbench/.leviath/runs/$RUN_ID/meta.json" 2>/dev/null | head -1)
    case "$STATUS" in
        complete|error|cancelled|complete_interactive) break ;;
    esac
    sleep 1
done

echo LEVMETA_BEGIN
cat "/opt/levbench/.leviath/runs/$RUN_ID/meta.json"
echo
echo LEVMETA_END
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lev-linux", required=True,
                        help="path to a Linux lev binary matching the "
                             "docker daemon's architecture")
    parser.add_argument("--image", default="ubuntu:24.04")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp) / "home"
        providers = home / ".leviath" / "providers"
        agents = home / ".leviath" / "agents"
        providers.mkdir(parents=True)
        agents.mkdir(parents=True)
        (home / ".leviath" / "config.toml").write_text(
            '[model_providers.mockx]\nscript = "mockx"\n')
        (providers / "mockx.rhai").write_bytes(
            (BENCH_DIR / "providers" / "mockx.rhai").read_bytes())
        blueprint = QUALITY_DIR / "blueprints" / "flat-loganalyzer"
        dest = agents / "flat-loganalyzer"
        dest.mkdir()
        (dest / "agent.leviath").write_bytes(
            (blueprint / "agent.leviath").read_bytes())

        out = subprocess.run(
            ["docker", "run", "--rm",
             "-v", f"{args.lev_linux}:/opt/lev:ro",
             "-v", f"{home}:/opt/levbench",
             "-e", "LEVMOCK_LATENCY_MS=",
             args.image, "bash", "-lc", IN_CONTAINER],
            capture_output=True, text=True, timeout=600)

    sys.stderr.write(out.stderr[-2000:])
    print(out.stdout[-400:] if "LEVMETA_BEGIN" not in out.stdout else "")
    if out.returncode != 0:
        print(f"spike FAILED rc={out.returncode}", file=sys.stderr)
        return 1
    try:
        meta_text = out.stdout.split("LEVMETA_BEGIN")[1].split(
            "LEVMETA_END")[0]
        meta = json.loads(meta_text)
    except (IndexError, json.JSONDecodeError) as exc:
        print(f"spike FAILED: no meta between sentinels ({exc})",
              file=sys.stderr)
        return 1
    print("spike OK:",
          json.dumps({k: meta.get(k)
                      for k in ("run_id", "status", "current_stage",
                                "prompt_tokens", "completion_tokens",
                                "tool_calls", "error")}, indent=2))
    return 0 if meta.get("status") in ("complete",
                                       "complete_interactive") else 1


if __name__ == "__main__":
    sys.exit(main())
