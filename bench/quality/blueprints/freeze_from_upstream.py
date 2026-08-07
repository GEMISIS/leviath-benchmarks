#!/usr/bin/env python3
"""Re-freeze the structured benchmark blueprints from a leviath checkout.

Copies the bundled agents byte-for-byte, prepending a provenance header
with the upstream commit. Run deliberately, review the diff, and re-run
make_flat.py afterwards so every flat counterpart is regenerated from
the same bytes. Never run mid-round: any change here means a new freeze
tag.

Usage:
    python3 freeze_from_upstream.py /path/to/leviath
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PAIRS = {
    "coder": "coder-bench",
    "data-analyst": "analyst-bench",
    "researcher": "researcher-bench",
    "log-analyzer": "loganalyzer-bench",
}


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    repo = Path(sys.argv[1])
    agents = repo / "crates" / "leviath-cli" / "agents"
    commit = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    here = Path(__file__).resolve().parent
    for name, dest in PAIRS.items():
        out = here / dest
        out.mkdir(parents=True, exist_ok=True)
        header = (
            f"# Frozen benchmark copy of the bundled {name} agent "
            f"(leviath commit {commit}).\n"
            "# Byte-frozen for the quality track; its sha256 is recorded "
            "in every run record.\n\n")
        text = (agents / name / "agent.leviath").read_text()
        (out / "agent.leviath").write_text(header + text)
        print(f"{dest}: {len(text.splitlines())} upstream lines "
              f"@ {commit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
