#!/usr/bin/env python3
"""Import a BASE for the benchmark agents from upstream leviath.

The blueprints in this directory are this repo's own agents (see
AGENTS.md). Upstream's bundled agents are their starting point, not
their definition: this script copies those bytes in, and from there the
agents evolve here by ordinary reviewed commits.

Because of that, importing OVERWRITES local evolution. The script
refuses to clobber an existing blueprint unless --overwrite is passed;
the intended flow is to import into a scratch tree, diff, and fold
upstream's changes into the evolved agent by hand. Never import
mid-round: any change here means a new freeze tag.

Usage:
    python3 import_base.py /path/to/leviath [--overwrite]
    python3 import_base.py --github <commit-sha> [--overwrite]

The --github form fetches the exact bytes GitHub serves at a commit -
use it to import from the commit a release was cut from, which may not
exist in any local checkout.

Afterwards: apply_bench_policy.py, then make_flat.py, then
check_pairs.py.
"""
from __future__ import annotations

import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

PAIRS = {
    "coder": "coder-bench",
    "data-analyst": "analyst-bench",
    "researcher": "researcher-bench",
    "log-analyzer": "loganalyzer-bench",
}
_RAW = "https://raw.githubusercontent.com/GEMISIS/leviath"
_API = "https://api.github.com/repos/GEMISIS/leviath"


def main() -> int:
    argv = [a for a in sys.argv[1:] if a != "--overwrite"]
    overwrite = "--overwrite" in sys.argv[1:]
    if len(argv) != 1 and not (len(argv) == 2 and argv[0] == "--github"):
        print(__doc__, file=sys.stderr)
        return 2

    if argv[0] == "--github":
        commit = argv[1]

        def read(name: str) -> str:
            url = (f"{_RAW}/{commit}/crates/leviath-cli/agents/"
                   f"{name}/agent.leviath")
            return urllib.request.urlopen(url, timeout=60).read().decode()

        def tools(name: str) -> dict[str, str]:
            """The agent's own tools/*.rhai - it is invalid without them."""
            url = (f"{_API}/contents/crates/leviath-cli/agents/{name}"
                   f"/tools?ref={commit}")
            req = urllib.request.Request(
                url, headers={"accept": "application/vnd.github+json"})
            try:
                listing = json.loads(
                    urllib.request.urlopen(req, timeout=60).read())
            except urllib.error.HTTPError as exc:
                if exc.code == 404:
                    return {}      # this agent ships no tools
                raise
            out = {}
            for entry in listing:
                if entry["type"] != "file":
                    continue
                out[entry["name"]] = urllib.request.urlopen(
                    entry["download_url"], timeout=60).read().decode()
            return out
        commit_label = commit[:12]
    else:
        repo = Path(argv[0])
        agents = repo / "crates" / "leviath-cli" / "agents"
        commit_label = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()

        def read(name: str) -> str:
            return (agents / name / "agent.leviath").read_text()

        def tools(name: str) -> dict[str, str]:
            d = agents / name / "tools"
            return {p.name: p.read_text()
                    for p in sorted(d.glob("*")) if p.is_file()} \
                if d.is_dir() else {}

    here = Path(__file__).resolve().parent
    existing = [d for d in PAIRS.values() if (here / d / "agent.leviath").exists()]
    if existing and not overwrite:
        print("These blueprints already exist and may carry local "
              "evolution:", file=sys.stderr)
        for d in existing:
            print(f"  {d}", file=sys.stderr)
        print("Import into a scratch tree and diff, or pass --overwrite "
              "to replace them.", file=sys.stderr)
        return 1

    for name, dest in PAIRS.items():
        out = here / dest
        out.mkdir(parents=True, exist_ok=True)
        header = (
            f"# Benchmark agent, based on the bundled {name} agent "
            f"(leviath commit {commit_label}).\n"
            "# Evolved in this repo under blueprints/AGENTS.md; frozen "
            "per round, sha256 recorded in every run record.\n\n")
        text = read(name)
        (out / "agent.leviath").write_text(header + text)
        agent_tools = tools(name)
        if agent_tools:
            (out / "tools").mkdir(exist_ok=True)
            for fname, body in agent_tools.items():
                (out / "tools" / fname).write_text(body)
        print(f"{dest}: {len(text.splitlines())} upstream lines, "
              f"{len(agent_tools)} tool script(s) @ {commit_label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
