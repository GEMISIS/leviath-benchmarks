"""How fast a round drained, and what the limit actually was.

Wall-clock per task says something about an agent. Wall-clock per
*round* says something about the runtime: how much agent work one
machine kept in flight at once. Both are worth publishing, and they are
different claims - this module computes the second from the timestamps
every record already carries.

The number that keeps it honest is `utilisation`: the parallelism
actually achieved divided by the parallelism asked for. High means the
host was the thing doing the work. Low means the round spent its time
waiting - on provider pacing, on the daemon's shared tool lane, or on a
few long runs with nothing left to overlap them with - and the drain
time is a fact about the provider rather than a fact about leviath.
"""
from __future__ import annotations

from datetime import datetime

__all__ = ["throughput"]

_FMT = "%Y-%m-%dT%H:%M:%SZ"


def _ts(value: str | None) -> float | None:
    try:
        return datetime.strptime(str(value), _FMT).timestamp()
    except (TypeError, ValueError):
        return None


def throughput(records: list[dict], declared_concurrency: int = 1) -> dict:
    """Drain time, agent-seconds, and how much overlap was achieved."""
    spans = []
    for r in records:
        start, end = _ts(r.get("started_utc")), _ts(r.get("ended_utc"))
        if start is None or end is None or end < start:
            continue
        spans.append((start, end))
    if not spans:
        return {"runs_timed": 0}

    agent_seconds = sum(
        float(r.get("wall_clock_secs") or 0.0) for r in records)
    round_start = min(s for s, _ in spans)
    round_end = max(e for _, e in spans)
    span = max(1.0, round_end - round_start)

    # Peak overlap, from the start/end events themselves.
    events = sorted([(s, 1) for s, _ in spans] + [(e, -1) for _, e in spans])
    in_flight = peak = 0
    for _, delta in events:
        in_flight += delta
        peak = max(peak, in_flight)

    effective = agent_seconds / span
    return {
        "runs_timed": len(spans),
        "declared_concurrency": declared_concurrency,
        "round_span_secs": round(span, 1),
        "agent_seconds": round(agent_seconds, 1),
        "serial_equivalent_hours": round(agent_seconds / 3600.0, 2),
        "effective_parallelism": round(effective, 2),
        "peak_in_flight": peak,
        "utilisation": (round(effective / declared_concurrency, 2)
                        if declared_concurrency else None),
        "note": ("agent_seconds is the work this round would have taken "
                 "serially; round_span_secs is what it took. utilisation "
                 "below ~0.6 means the round was waiting on something "
                 "other than the host - provider pacing, the daemon's "
                 "shared tool lane, or too few cells left to overlap."),
    }
