#!/usr/bin/env python3
"""Classify every run's ending into a failure mode, mechanically.

The white-paper measurement: flat agents near their window don't
degrade smoothly, they collapse - and the collapse has recognizable
shapes. This walks run records + journals and labels each run:

  clean            complete with a substantive deliverable
  degenerate-output  complete, but the deliverable is a token/stub
                     (the leviath#446 plumbing flake)
  malformed-death  errored after emitting a tool call with empty or
                   unparseable arguments (thrash collapse endpoint)
  reread-loop      capped/timed out with a high duplicate-read ratio
                   (the window evicts what was just read, forever)
  fixation-spiral  errored/capped with many near-identical probing
                   calls that are not corpus reads
  early-stop       errored with no deliverable and none of the above -
                   the model simply stopped calling tools
  infra            provider/runtime error (529s, credits, spawn)

Labels land in a JSON table beside the runs and print as a matrix.
Usage: classify_failures.py <runs_dir_or_results_dir> [...]
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from core import lvr  # noqa: E402


def _batches(archive: Path) -> list[dict]:
    try:
        _, recs, _ = lvr.read_archive(archive)
    except Exception:
        return []
    return [r["ToolBatch"] for r in recs if "ToolBatch" in r]


def classify(record: dict, artifacts: Path) -> str:
    status = record.get("status")
    meta_err = ""
    meta_path = artifacts / "run" / "meta.json"
    if meta_path.is_file():
        try:
            meta_err = str(json.loads(
                meta_path.read_text()).get("error") or "")
        except (OSError, ValueError):
            pass
    if "API error" in meta_err or "credits" in meta_err.lower() \
            or "overloaded" in meta_err.lower():
        return "infra"

    if status == "complete":
        answer = artifacts / "answer.txt"
        text = answer.read_text().strip() if answer.is_file() else ""
        if len(text) < 40 or len(text.split()) < 4:
            return "degenerate-output"
        return "clean"

    archive = None
    for name in ("run.lvr.gz", "run.lvr"):
        if (artifacts / "run" / name).is_file():
            archive = artifacts / "run" / name
            break
    if archive is None:
        return "infra"
    batches = _batches(archive)
    if not batches:
        return "infra"

    calls = [c for b in batches for c in b.get("calls", [])]
    # Malformed endpoint: the last turn's call has empty/blank args.
    last_calls = batches[-1].get("calls", [])
    for c in last_calls:
        args = c.get("arguments")
        if args in (None, "", "{}") or args == "null":
            return "malformed-death"

    read_paths = []
    probe_like = 0
    for c in calls:
        try:
            args = json.loads(c.get("arguments") or "{}")
        except ValueError:
            args = {}
        if c.get("name") in ("read_file", "read_files"):
            read_paths.append(json.dumps(args, sort_keys=True))
        elif c.get("name") in ("shell", "bash"):
            cmd = str(args.get("command", ""))
            if any(t in cmd for t in ("--version", "which ", "import ",
                                      "cd /tmp", "cd /home", "pwd")):
                probe_like += 1
    dup_reads = (len(read_paths) - len(set(read_paths))) \
        / len(read_paths) if read_paths else 0.0
    if status in ("cap", "timeout") and dup_reads > 0.25:
        return "reread-loop"
    if probe_like >= 6:
        return "fixation-spiral"
    if status in ("cap", "timeout"):
        return "reread-loop" if dup_reads > 0.1 else "early-stop"
    return "early-stop"


def main() -> int:
    rows = []
    for root in sys.argv[1:]:
        runs_dir = Path(root)
        if runs_dir.name != "runs":
            hits = sorted(runs_dir.glob("quality/*/runs"))
            if hits:
                runs_dir = hits[0]
        for f in sorted(runs_dir.glob("*.json")):
            if ".err" in f.name:
                continue
            rec = json.loads(f.read_text())
            art = f.with_name(f.name[:-5] + ".artifacts")
            mode = classify(rec, art)
            rows.append({
                "task": rec["task_id"], "arm": rec["arm"],
                "window": rec.get("window_tokens"),
                "status": rec.get("status"), "mode": mode,
            })
            print(f"{rec['task_id'][:18]:18} {rec['arm'][:24]:24} "
                  f"@{(rec.get('window_tokens') or 0) // 1000:3}k "
                  f"{rec.get('status', '?'):8} -> {mode}")
        # Beside runs/, never inside it - the runs dir is records-only.
        out = runs_dir.parent / "failure_modes.json"
        out.write_text(json.dumps(rows, indent=1) + "\n")
    print("\nmode counts by arm kind:")
    tally: Counter = Counter()
    for r in rows:
        kind = "flagship" if "flagship" in r["arm"] else "flat"
        tally[(kind, r["mode"])] += 1
    for (kind, mode), n in sorted(tally.items()):
        print(f"  {kind:9} {mode:18} {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
