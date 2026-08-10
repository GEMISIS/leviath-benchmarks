"""quality-run-v1 raw records and their aggregation.

One JSON file per run, always - failures, timeouts, and budget cap-outs
included. The committed records are the API a downstream consumer reads;
the schema version is bumped, never mutated.
"""
from __future__ import annotations

import json
from pathlib import Path

from . import stats

__all__ = ["SCHEMA", "REQUIRED_KEYS", "STATUSES", "record_filename",
           "validate", "write_record", "load_records", "aggregate"]

SCHEMA = "quality-run-v1"
STATUSES = {"complete", "error", "timeout", "no_answer", "cap"}
REQUIRED_KEYS = {
    "schema", "freeze_tag", "suite", "task_id", "arm", "model_label",
    "model_policy", "rep", "blueprint", "lev", "status", "started_utc",
    "ended_utc", "wall_clock_secs", "usage", "tool_calls", "cost_usd",
    "rates_sha256", "score",
}
_AGG_FIELDS = ("billed_tokens", "cost_usd", "wall_clock_secs", "tool_calls")


def record_filename(task_id: str, arm: str, model_label: str,
                    rep: int) -> str:
    safe = [s.replace("/", "-").replace(" ", "-")
            for s in (task_id, arm, model_label or "native")]
    return f"{safe[0]}__{safe[1]}__{safe[2]}__rep{rep}.json"


def validate(record: dict) -> None:
    missing = REQUIRED_KEYS - set(record)
    if missing:
        raise ValueError(f"record missing keys: {sorted(missing)}")
    if record["schema"] != SCHEMA:
        raise ValueError(f"unexpected schema {record['schema']!r}")
    if record["status"] not in STATUSES:
        raise ValueError(f"unexpected status {record['status']!r}")


def write_record(runs_dir: Path, record: dict) -> Path:
    validate(record)
    runs_dir.mkdir(parents=True, exist_ok=True)
    path = runs_dir / record_filename(record["task_id"], record["arm"],
                                      record["model_label"], record["rep"])
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    return path


def load_records(runs_dir: Path) -> list[dict]:
    records = []
    for path in sorted(Path(runs_dir).glob("*.json")):
        record = json.loads(path.read_text())
        validate(record)
        records.append(record)
    return records


def aggregate(records: list[dict]) -> dict:
    """Per (arm, model) aggregates: pass rate + the standard spreads.

    A non-complete run counts against the pass rate (its score is a
    fail) but is excluded from token/cost spreads only when the counter
    is absent, never because the number looks wrong.
    """
    cells: dict[tuple[str, str], list[dict]] = {}
    for r in records:
        cells.setdefault((r["arm"], r["model_label"]), []).append(r)

    out = []
    for (arm, model_label), rs in sorted(cells.items()):
        passes = [bool(r["score"] and r["score"].get("passed")) for r in rs]
        cell = {
            "arm": arm,
            "model_label": model_label,
            "runs": len(rs),
            "passes": sum(passes),
            "pass_rate": round(sum(passes) / len(rs), 4),
            "statuses": _count(r["status"] for r in rs),
        }
        for field in _AGG_FIELDS:
            values = [r[field] for r in rs
                      if isinstance(r.get(field), (int, float))]
            cell[field] = stats.summary_stats([float(v) for v in values])
        hit_rates = [r["cache_hit_rate"] for r in rs
                     if isinstance(r.get("cache_hit_rate"), (int, float))]
        cell["cache_hit_rate"] = stats.summary_stats(hit_rates)
        out.append(cell)
    return {"cells": out}


def _count(values) -> dict:
    counts: dict = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    return counts
