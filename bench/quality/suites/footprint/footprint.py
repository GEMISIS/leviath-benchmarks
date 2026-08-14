"""Per-request context footprint, folded from a run's own journal.

The suite's thesis lives here: what each architecture SENDS per request,
over the life of the run. A flat window grows without bound as work
accumulates; structured regions hold the per-request footprint roughly
constant. Stability is what makes small-window models - cheap tiers,
local models with 8k-32k windows - viable at all, so the summary keys
are chosen to answer "would this run fit on a small window?" directly.

Input tokens per request are deltas of the journal's cumulative
provider-billed counters (prompt + cache reads + cache writes): that is
what the provider actually received each call, cache-honest by
construction. Latency per request comes from the journal's own
timestamps (second resolution).
"""
from __future__ import annotations

import statistics
import sys
from pathlib import Path

_CORE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_CORE))

from core import lvr  # noqa: E402

MAX_CURVE_POINTS = 500


def _meta_int(meta: dict, key: str) -> int:
    return int(meta.get(key, 0) or 0)


def _openai_stages(archive: Path) -> set[str]:
    """Stages served by an OpenAI model, whose prompt_tokens INCLUDE
    cached tokens (Anthropic's exclude them) - summing prompt+cached
    for those stages double-counts. The runner writes the stage map
    beside the journal; absent (single-model runs), empty set."""
    import json
    path = Path(archive).parent / "stage_models.json"
    try:
        mapping = json.loads(path.read_text())
    except (OSError, ValueError):
        return set()
    return {stage for stage, model in mapping.items()
            if str(model).startswith("openai/")}


def from_archive(archive: Path) -> dict | None:
    """Fold run.lvr(.gz) into the request-footprint block, or None."""
    points = lvr.fold(archive)
    if not points:
        return None
    openai_stages = _openai_stages(archive)

    requests = []
    prev = None
    prev_ts = None
    prev_out = None
    for p in points:
        meta = p.meta if isinstance(p.meta, dict) else {}
        cur = {k: _meta_int(meta, k) for k in
               ("prompt_tokens", "cached_tokens", "cache_write_tokens")}
        cum_out = _meta_int(meta, "completion_tokens")
        ts = meta.get("updated_at")
        if prev is None:
            prev, prev_out, prev_ts = cur, cum_out, ts
            continue
        deltas = {k: cur[k] - prev[k] for k in cur}
        # Per-counter deltas attribute the cached share to THIS
        # request, so the provider correction works even though the
        # journal counters are cumulative across stages.
        d_in = sum(deltas.values())
        d_cached = deltas["cached_tokens"]
        if meta.get("current_stage") in openai_stages:
            d_in -= d_cached
        d_out = cum_out - prev_out
        if d_in <= 0 and d_out <= 0:
            continue  # persistence tick with no inference behind it
        entry = {
            "iteration": _meta_int(meta, "iteration"),
            "tool_calls": _meta_int(meta, "tool_calls"),
            "input_tokens": max(d_in, 0),
            "cached_tokens": max(d_cached, 0),
            "output_tokens": max(d_out, 0),
        }
        stage = meta.get("current_stage")
        if stage:
            entry["stage"] = stage
        if isinstance(ts, (int, float)) and isinstance(prev_ts,
                                                       (int, float)):
            entry["secs"] = max(int(ts - prev_ts), 0)
        requests.append(entry)
        prev, prev_out, prev_ts = cur, cum_out, ts

    if not requests:
        return None
    if len(requests) > MAX_CURVE_POINTS:
        # Keep the shape without unbounded records: every Nth point,
        # first and last always included.
        step = len(requests) // MAX_CURVE_POINTS + 1
        requests = requests[::step] + [requests[-1]]

    inputs = [r["input_tokens"] for r in requests]
    outputs = [r["output_tokens"] for r in requests]
    secs = [r["secs"] for r in requests if "secs" in r]
    n = len(requests)
    head = inputs[: max(n // 4, 1)]
    tail = inputs[-max(n // 4, 1):]
    head_mean = sum(head) / len(head)
    tail_mean = sum(tail) / len(tail)
    return {
        "n_requests": n,
        "input_p50": int(statistics.median(inputs)),
        "input_max": max(inputs),
        "input_head_mean": int(head_mean),
        "input_tail_mean": int(tail_mean),
        # >1 means the footprint grows over the run; ~1 means stable.
        # This single number is the local-viability verdict.
        "input_growth": round(tail_mean / head_mean, 2) if head_mean
        else None,
        "output_p50": int(statistics.median(outputs)),
        "secs_p50": int(statistics.median(secs)) if secs else None,
        "requests": requests,
    }
