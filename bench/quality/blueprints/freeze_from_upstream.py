#!/usr/bin/env python3
"""Re-freeze the structured benchmark blueprints from upstream leviath.

Copies the bundled agents byte-for-byte, prepending a provenance header
with the upstream commit. Run deliberately, review the diff, and re-run
make_flat.py afterwards so every flat counterpart is regenerated from
the same bytes. Never run mid-round: any change here means a new freeze
tag.

Usage:
    python3 freeze_from_upstream.py /path/to/leviath
    python3 freeze_from_upstream.py --github <commit-sha>

The --github form fetches the exact bytes GitHub serves at a commit -
use it to freeze from the commit a release was cut from, which may not
exist in any local checkout.
"""
from __future__ import annotations

import subprocess
import sys
import urllib.request
from pathlib import Path

PAIRS = {
    "coder": "coder-bench",
    "data-analyst": "analyst-bench",
    "researcher": "researcher-bench",
    "log-analyzer": "loganalyzer-bench",
}
_RAW = "https://raw.githubusercontent.com/GEMISIS/leviath"


def main() -> int:
    if len(sys.argv) != 2 and not (len(sys.argv) == 3
                                   and sys.argv[1] == "--github"):
        print(__doc__, file=sys.stderr)
        return 2

    if sys.argv[1] == "--github":
        commit = sys.argv[2]
        def read(name: str) -> str:
            url = (f"{_RAW}/{commit}/crates/leviath-cli/agents/"
                   f"{name}/agent.leviath")
            return urllib.request.urlopen(url, timeout=60).read().decode()
        commit_label = commit[:12]
    else:
        repo = Path(sys.argv[1])
        agents = repo / "crates" / "leviath-cli" / "agents"
        commit_label = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True).stdout.strip()
        def read(name: str) -> str:
            return (agents / name / "agent.leviath").read_text()

    here = Path(__file__).resolve().parent
    for name, dest in PAIRS.items():
        out = here / dest
        out.mkdir(parents=True, exist_ok=True)
        header = (
            f"# Frozen benchmark copy of the bundled {name} agent "
            f"(leviath commit {commit_label}).\n"
            "# Byte-frozen for the quality track; its sha256 is recorded "
            "in every run record.\n\n")
        text = read(name)
        (out / "agent.leviath").write_text(header + text)
        print(f"{dest}: {len(text.splitlines())} upstream lines "
              f"@ {commit_label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
