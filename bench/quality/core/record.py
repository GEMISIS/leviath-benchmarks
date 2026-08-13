"""quality-run-v2 raw records and their aggregation.

One JSON file per run, always - failures, timeouts, and budget cap-outs
included. The committed records are the API a downstream consumer reads;
the schema version is bumped, never mutated. v2 adds four optional
blocks for the Context Retention Suite:

- ``validation``: held-out test results ({passed, failed, errors, total,
  failures, suite_hash}) - how the run's *artifact* scored.
- ``retention``: one entry per probe ({after_tool_calls, at_tool_calls,
  probe_type, reached, score, grade, hallucinated, read_by, graded_by}).
  Probes replayed against a run that died early carry reached=false and
  no score - recorded, never dropped.
- ``retention_summary``: {mean_score, n_probes, n_reached,
  n_hallucinated}; the mean is over reached probes only, on the 0..1
  accuracy scale (hallucination is a separate rate, never a negative
  score in the mean).
- ``probe_overhead``: what the measurement itself cost ({usage,
  cost_usd, reader_model, grader_model, grader_prompt_sha256,
  probe_wrapper_sha256}). Excluded from the run's ``cost_usd`` and from
  every cost comparison: it is measurement, not agent spend.

v1 records remain valid and loadable.
"""
from __future__ import annotations

import json
from pathlib import Path

from . import stats

__all__ = ["SCHEMA", "SCHEMAS", "REQUIRED_KEYS", "STATUSES",
           "record_filename", "validate", "write_record", "load_records",
           "aggregate"]

SCHEMA = "quality-run-v2"
SCHEMAS = {"quality-run-v1", "quality-run-v2"}
STATUSES = {"complete", "error", "timeout", "no_answer", "cap"}
REQUIRED_KEYS = {
    "schema", "freeze_tag", "suite", "task_id", "arm", "model_label",
    "model_policy", "rep", "blueprint", "lev", "status", "started_utc",
    "ended_utc", "wall_clock_secs", "usage", "tool_calls", "cost_usd",
    "rates_sha256", "score",
}
_AGG_FIELDS = ("billed_tokens", "cost_usd", "wall_clock_secs", "tool_calls")

# v2 optional blocks and the keys each must carry when present.
_V2_BLOCKS = {
    "validation": {"passed", "failed", "errors", "total", "suite_hash"},
    "retention_summary": {"mean_score", "n_probes", "n_reached",
                          "n_hallucinated"},
    "probe_overhead": {"usage", "cost_usd", "reader_model", "grader_model"},
}
_RETENTION_KEYS = {"after_tool_calls", "probe_type", "reached"}


def record_filename(task_id: str, arm: str, model_label: str,
                    rep: int) -> str:
    safe = [s.replace("/", "-").replace(" ", "-")
            for s in (task_id, arm, model_label or "native")]
    return f"{safe[0]}__{safe[1]}__{safe[2]}__rep{rep}.json"


def validate(record: dict) -> None:
    missing = REQUIRED_KEYS - set(record)
    if missing:
        raise ValueError(f"record missing keys: {sorted(missing)}")
    if record["schema"] not in SCHEMAS:
        raise ValueError(f"unexpected schema {record['schema']!r}")
    if record["status"] not in STATUSES:
        raise ValueError(f"unexpected status {record['status']!r}")
    for block, keys in _V2_BLOCKS.items():
        if block in record:
            got = record[block]
            if not isinstance(got, dict) or keys - set(got):
                raise ValueError(f"{block} missing keys: "
                                 f"{sorted(keys - set(got or {}))}")
    if "retention" in record:
        if not isinstance(record["retention"], list):
            raise ValueError("retention must be a list")
        for probe in record["retention"]:
            if _RETENTION_KEYS - set(probe):
                raise ValueError(
                    f"retention entry missing keys: "
                    f"{sorted(_RETENTION_KEYS - set(probe))}")
            if probe["reached"] and "score" not in probe:
                raise ValueError("a reached probe must carry a score")


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
        retention = [r["retention_summary"]["mean_score"] for r in rs
                     if isinstance(r.get("retention_summary"), dict)
                     and isinstance(r["retention_summary"].get("mean_score"),
                                    (int, float))]
        if retention:
            cell["retention_mean_score"] = stats.summary_stats(retention)
        out.append(cell)
    return {"cells": out}


def _count(values) -> dict:
    counts: dict = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    return counts
