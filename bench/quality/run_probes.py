#!/usr/bin/env python3
"""Replay retention probes against a finished round's run journals.

Phase B of the Context Retention Suite: the runs already happened,
undisturbed; this tool reconstructs each run's provider-visible context
at every probe depth (core/lvr.py + core/assemble.py), asks the probe
question once against the ONE fixed reader model at temperature 0,
grades the answers with the pinned cross-vendor grader, and amends the
run records with retention / retention_summary / probe_overhead.

Probe and grading spend never enters a record's cost_usd - it is
measurement, not agent spend - but is fully recorded per run.

Usage:
    python3 bench/quality/run_probes.py results/<round-dir> \
        [--grade] [--budget-usd N] [--dry-run] [--force]

--dry-run reconstructs and prints request shapes without any API call
(the fidelity-review tool). Without --force, records that already carry
retention data are skipped, so the tool is idempotent per round.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

QUALITY_DIR = Path(__file__).resolve().parent
REPO_DIR = QUALITY_DIR.parent.parent
sys.path.insert(0, str(QUALITY_DIR))

from core import assemble, cost as cost_mod, evaluator, lvr  # noqa: E402
from core import providers, record as record_mod, scrub  # noqa: E402
from run_quality import load_dotenv  # noqa: E402

sys.path.insert(0, str(QUALITY_DIR / "suites" / "crs"))
import probes as probes_mod  # noqa: E402

# The fixed instruction wrapped around every probe question. Frozen with
# the round: its sha lands in probe_overhead so a change is visible.
PROBE_WRAPPER = (
    "Pause the task for one question. Answer from your memory of the "
    "work and documents so far - do not use tools, do not look anything "
    "up, and keep it brief.\n\nQuestion: {question}")

KEY_NAMES = ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "OPENROUTER_API_KEY")


def wrapper_sha256() -> str:
    return hashlib.sha256(PROBE_WRAPPER.encode()).hexdigest()


def _probe_config(round_meta: dict) -> dict:
    arms_cfg = json.loads((QUALITY_DIR / "arms.json").read_text())
    cfg = round_meta.get("probes") or arms_cfg.get("probes")
    if not cfg:
        raise SystemExit("no probes block in round.json or arms.json")
    roster = round_meta.get("roster") or arms_cfg["models"]
    out = dict(cfg)
    out["reader_id"] = roster[cfg["reader_model"]]["id"]
    out["grader_id"] = roster[cfg["grader_model"]]["id"]
    return out


def _probe_message(question: str) -> dict:
    return {"role": "user", "content": [
        {"type": "text", "text": PROBE_WRAPPER.format(question=question)}]}


def _load_task_probes(task_id: str) -> list[dict]:
    return probes_mod.load_probes(
        QUALITY_DIR / "suites" / "crs" / "tasks" / task_id / "probes.json")


def _archive_path(runs_dir: Path, rec: dict) -> Path | None:
    stem = record_mod.record_filename(
        rec["task_id"], rec["arm"], rec["model_label"],
        rec["rep"]).removesuffix(".json")
    for name in ("run.lvr.gz", "run.lvr"):
        p = runs_dir / f"{stem}.artifacts" / "run" / name
        if p.is_file():
            return p
    return None


def replay_record(rec: dict, runs_dir: Path, cfg: dict, rates: dict,
                  keys: dict, *, grade: bool, dry_run: bool,
                  log=print) -> dict | None:
    """Returns the amended record, or None when nothing was done."""
    archive = _archive_path(runs_dir, rec)
    if archive is None:
        log(f"  {rec['task_id']}/{rec['arm']}: no run.lvr archive")
        return None
    task_probes = _load_task_probes(rec["task_id"])
    points = lvr.fold(archive)
    if not points:
        log(f"  {rec['task_id']}/{rec['arm']}: empty journal")
        return None

    stem = record_mod.record_filename(
        rec["task_id"], rec["arm"], rec["model_label"],
        rec["rep"]).removesuffix(".json")
    replay_dir = runs_dir / f"{stem}.artifacts" / "probe_replays"
    replay_dir.mkdir(parents=True, exist_ok=True)

    retention = []
    overhead = {"prompt_tokens": 0, "completion_tokens": 0,
                "cached_tokens": 0, "cache_write_tokens": 0}
    overhead_cost = 0.0

    for probe in task_probes:
        depth = probe["after_tool_calls"]
        found = lvr.point_at_depth(points, depth)
        entry = {"after_tool_calls": depth,
                 "probe_type": probe["type"],
                 "reached": found is not None}
        if found is None:
            retention.append(entry)
            continue
        point, actual = found
        entry["at_tool_calls"] = actual
        request = assemble.assemble(point)
        request["messages"] = (request["messages"]
                               + [_probe_message(probe["question"])])
        if dry_run:
            log(f"  probe@{depth} (at {actual}): "
                f"{len(request['system'])} system blocks, "
                f"{len(request['messages'])} messages, "
                f"tools {sorted(request['tool_names'])}")
            retention.append(entry)
            continue

        out = providers.call_chat(
            cfg["reader_id"], request["system"], request["messages"],
            request["tool_names"],
            temperature=cfg.get("replay_temperature", 0),
            max_tokens=cfg.get("replay_max_tokens", 1024), keys=keys)
        for k in overhead:
            overhead[k] += out["usage"].get(k, 0)
        overhead_cost += cost_mod.cost_usd(out["usage"], cfg["reader_id"],
                                           rates) or 0.0
        (replay_dir / f"probe_{depth}.json").write_text(json.dumps({
            "probe": probe, "at_tool_calls": actual,
            "system_blocks": len(request["system"]),
            "messages": len(request["messages"]),
            "encoding": out["encoding"],
            "answer": out["text"], "usage": out["usage"],
            "reader_model": cfg["reader_id"],
        }, indent=2) + "\n")
        entry["read_by"] = cfg["reader_id"]

        if grade:
            verdict = evaluator.grade_answer(
                probe, out["text"], grader_model_id=cfg["grader_id"],
                keys=keys)
            for k in overhead:
                overhead[k] += (verdict["usage"] or {}).get(k, 0)
            overhead_cost += cost_mod.cost_usd(
                verdict["usage"], cfg["grader_id"], rates) or 0.0
            (replay_dir / f"probe_{depth}.grade.json").write_text(
                json.dumps(verdict, indent=2) + "\n")
            entry.update({"score": verdict["score"],
                          "grade": verdict["grade"],
                          "hallucinated": verdict["hallucinated"],
                          "graded_by": cfg["grader_id"]})
        retention.append(entry)

    if dry_run:
        unreached = sum(1 for e in retention if not e["reached"])
        log(f"  dry-run: {len(retention) - unreached} probes reachable, "
            f"{unreached} unreached (run made "
            f"{points[-1].meta.get('tool_calls', 0)} tool calls)")
        return None

    rec = dict(rec)
    rec["schema"] = record_mod.SCHEMA
    rec["retention"] = retention
    # Cumulative usage at every tool-call depth, straight from the
    # journal fold: the cost-at-depth chart reads this instead of
    # re-folding archives (charts read committed data only). Components
    # are kept raw so any pricing convention can be applied later.
    curve, last_calls = [], -1
    for point in points:
        meta = point.meta if isinstance(point.meta, dict) else {}
        calls = int(meta.get("tool_calls", 0) or 0)
        if calls <= last_calls:
            continue
        last_calls = calls
        curve.append({
            "tool_calls": calls,
            "prompt_tokens": int(meta.get("prompt_tokens", 0) or 0),
            "completion_tokens": int(meta.get("completion_tokens", 0) or 0),
            "cached_tokens": int(meta.get("cached_tokens", 0) or 0),
            "cache_write_tokens": int(meta.get("cache_write_tokens", 0)
                                      or 0),
        })
    rec["depth_usage_curve"] = curve
    reached = [e for e in retention if e["reached"]]
    scored = [e["score"] for e in reached
              if isinstance(e.get("score"), (int, float))]
    rec["retention_summary"] = {
        "mean_score": (round(sum(scored) / len(scored), 4)
                       if scored else None),
        "n_probes": len(retention),
        "n_reached": len(reached),
        "n_hallucinated": sum(1 for e in reached if e.get("hallucinated")),
    }
    rec["probe_overhead"] = {
        "usage": overhead,
        "cost_usd": round(overhead_cost, 6),
        "reader_model": cfg["reader_id"],
        "grader_model": cfg["grader_id"],
        "grader_prompt_sha256": evaluator.grade_prompt_sha256(),
        "probe_wrapper_sha256": wrapper_sha256(),
    }
    record_mod.write_record(runs_dir, rec)
    return rec


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Replay and grade CRS retention probes.")
    parser.add_argument("results_dir", type=Path)
    parser.add_argument("--grade", action="store_true")
    parser.add_argument("--budget-usd", type=float, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    load_dotenv(REPO_DIR / ".env")
    keys = {k: os.environ.get(k, "") for k in KEY_NAMES}

    quality = args.results_dir / "quality"
    round_meta = json.loads((quality / "round.json").read_text())
    cfg = _probe_config(round_meta)
    rates = cost_mod.load_rates(QUALITY_DIR / "rates.json")
    runs_dir = quality / "crs" / "runs"
    if not runs_dir.is_dir():
        raise SystemExit(f"no crs runs under {quality}")

    spent = 0.0
    amended = 0
    for rec in record_mod.load_records(runs_dir):
        if rec.get("retention") and not args.force:
            continue
        if args.budget_usd is not None and spent >= args.budget_usd:
            print(f"budget cap: ${spent:.2f} >= ${args.budget_usd:.2f}")
            break
        print(f"[{rec['task_id']} {rec['arm']} "
              f"{rec['model_label']} rep{rec['rep']}]")
        out = replay_record(rec, runs_dir, cfg, rates, keys,
                            grade=args.grade, dry_run=args.dry_run)
        if out is not None:
            amended += 1
            spent += out["probe_overhead"]["cost_usd"]

    if amended and not args.dry_run:
        subprocess.run([sys.executable,
                        str(QUALITY_DIR / "recompute_summaries.py"),
                        str(args.results_dir)], check=False)
        leaks = scrub.scan(args.results_dir)
        if leaks:
            print(f"SECRET SCRUB FAILED: {leaks}")
            return 1
    print(f"amended {amended} records, probe spend ~${spent:.2f} "
          "(excluded from arm costs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
