#!/usr/bin/env python3
"""Re-grade saved probe replays under the current grader prompt.

The reader's answers are frozen on disk (probe_replays/*.json); only
the GRADING is redone, so a grader-prompt change - like the
elaboration-bias fix, where context-supported detail was being labeled
invention - can be applied to an existing round for a fraction of the
replay cost, and the before/after is auditable per probe (.grade.json
files are rewritten in place, the old verdicts recoverable from git).

Usage:
    python3 bench/quality/regrade_probes.py <results_dir> [...]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from core import cost as cost_mod  # noqa: E402
from core import evaluator, record as record_mod  # noqa: E402
from run_probes import KEY_NAMES  # noqa: E402
from run_quality import load_dotenv  # noqa: E402

_NAME = re.compile(r"probe_(\d+)_(\d+)\.json$")


def regrade_record(runs_dir: Path, rec: dict, grader_id: str,
                   rates: dict, keys: dict) -> None:
    stem = record_mod.record_filename(
        rec["task_id"], rec["arm"], rec["model_label"],
        rec["rep"]).removesuffix(".json")
    replay_dir = runs_dir / f"{stem}.artifacts" / "probe_replays"
    if not replay_dir.is_dir():
        return
    verdicts: dict[tuple[int, int], dict] = {}
    extra_cost = 0.0
    for f in sorted(replay_dir.glob("probe_*.json")):
        m = _NAME.search(f.name)
        if not m:
            continue
        saved = json.loads(f.read_text())
        verdict = evaluator.grade_answer(
            saved["probe"], saved.get("answer") or "",
            grader_model_id=grader_id, keys=keys)
        extra_cost += cost_mod.cost_usd(
            verdict["usage"], grader_id, rates) or 0.0
        (replay_dir / f.name.replace(".json", ".grade.json")).write_text(
            json.dumps(verdict, indent=2) + "\n")
        verdicts[(int(m.group(1)), int(m.group(2)))] = verdict

    changed = 0
    for entry in rec.get("retention") or []:
        key = (entry["after_tool_calls"], entry.get("probe_id"))
        v = verdicts.get(key)
        if v is None or not entry.get("reached"):
            continue
        if entry.get("grade") != v["grade"]:
            changed += 1
        entry.update({"score": v["score"], "grade": v["grade"],
                      "hallucinated": v["hallucinated"],
                      "graded_by": grader_id})
    reached = [e for e in rec.get("retention") or [] if e.get("reached")]
    scored = [e["score"] for e in reached
              if isinstance(e.get("score"), (int, float))]
    if reached:
        rec["retention_summary"] = {
            "mean_score": (round(sum(scored) / len(scored), 4)
                           if scored else None),
            "n_probes": len(rec.get("retention") or []),
            "n_reached": len(reached),
            "n_hallucinated": sum(1 for e in reached
                                  if e.get("hallucinated")),
        }
    overhead = rec.get("probe_overhead")
    if overhead:
        overhead["cost_usd"] = round(
            (overhead.get("cost_usd") or 0.0) + extra_cost, 6)
        overhead["regraded_with_sha"] = evaluator.grade_prompt_sha256()
    record_mod.write_record(runs_dir, rec)
    hall = sum(1 for e in reached if e.get("hallucinated"))
    print(f"{rec['task_id']:19} {rec['arm'][:24]:24} regraded "
          f"{len(verdicts):3} probes, {changed:2} verdicts changed, "
          f"hallucinated now {hall} (${extra_cost:.2f})")


def main() -> int:
    import os
    load_dotenv(HERE.parent.parent / ".env")
    arms = json.loads((HERE / "arms.json").read_text())
    grader_label = arms["probes"]["grader_model"]
    grader_id = arms["models"][grader_label]["id"]
    rates = json.loads((HERE / "rates.json").read_text())
    keys = {k: os.environ.get(k, "") for k in KEY_NAMES}
    for root in sys.argv[1:]:
        runs_dir = Path(root)
        if not runs_dir.name == "runs":
            hits = sorted(runs_dir.glob("quality/*/runs"))
            if hits:
                runs_dir = hits[0]
        for f in sorted(runs_dir.glob("*.json")):
            rec = json.loads(f.read_text())
            if rec.get("retention"):
                regrade_record(runs_dir, rec, grader_id, rates, keys)
    return 0


if __name__ == "__main__":
    sys.exit(main())
