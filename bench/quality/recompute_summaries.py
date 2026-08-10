#!/usr/bin/env python3
"""Recompute a round's summaries from its recorded runs.

The records are the round; summaries are derived. When the statistics
code changes - as it did when whole-suite comparisons outgrew exact
enumeration - the published summaries can be regenerated from the same
raw records without re-running a single agent, which is the property
that makes results an interface rather than a snapshot.

Reads and rewrites <results-dir>/quality/<suite>/summary.json. Never
touches a run record.

Usage:
    python3 bench/quality/recompute_summaries.py results/<round-dir>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

QUALITY_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(QUALITY_DIR))

from core import record  # noqa: E402
from run_quality import comparisons_block  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    root = Path(sys.argv[1]) / "quality"
    round_meta = json.loads((root / "round.json").read_text())
    seed = int(round_meta.get("seed") or 0)

    for suite_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        runs = sorted((suite_dir / "runs").glob("*.json"))
        if not runs:
            continue
        records = [json.loads(p.read_text()) for p in runs]
        summary_path = suite_dir / "summary.json"
        summary = json.loads(summary_path.read_text())
        summary["aggregate"] = record.aggregate(records)
        summary["comparisons"] = comparisons_block(records, seed=seed)
        summary_path.write_text(json.dumps(summary, indent=2) + "\n")
        print(f"{suite_dir.name}: {len(records)} records, "
              f"{len(summary['comparisons'])} comparisons")
    return 0


if __name__ == "__main__":
    sys.exit(main())
