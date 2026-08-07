"""Exact small-sample statistics for the quality track.

Two tests, both exact (full enumeration, no normal approximation),
because run counts here are single digits per cell and t-intervals on
4-point samples are meaningless:

- ``mann_whitney_exact``: one-sided rank-sum for continuous outcomes
  (billed tokens, cost, wall-clock). H1: sample ``a`` tends LOWER than
  sample ``b`` (pre-registered direction: structured bills fewer tokens).
- ``permutation_exact``: one-sided permutation test on the difference in
  pass rates for boolean outcomes (rank-sum is the wrong tool for
  booleans - massive ties). H1: group ``a`` passes MORE than group ``b``.

Both return the exact p-value as a float. Enumeration is capped: above
``_MAX_ENUM`` combinations the caller gets an error rather than a
silently approximate number.
"""
from __future__ import annotations

import itertools
import math
from statistics import median

__all__ = ["mann_whitney_exact", "permutation_exact", "summary_stats"]

_MAX_ENUM = 5_000_000


def _check_enum(n_comb: int) -> None:
    if n_comb > _MAX_ENUM:
        raise ValueError(
            f"exact enumeration would need {n_comb} combinations; "
            "reduce n or pre-register a different test - this module "
            "never switches to an approximation silently")


def mann_whitney_exact(a: list[float], b: list[float]) -> float:
    """Exact one-sided Mann-Whitney p for H1: a stochastically < b.

    U counts, over all cross pairs, how often a-value < b-value (ties
    count half). The p-value is the share of label reassignments with a
    U at least as extreme, enumerated exactly.
    """
    if not a or not b:
        raise ValueError("both samples must be non-empty")

    def u_of(xs: list[float], ys: list[float]) -> float:
        u = 0.0
        for x in xs:
            for y in ys:
                if x < y:
                    u += 1.0
                elif x == y:
                    u += 0.5
        return u

    observed = u_of(a, b)
    pooled = a + b
    n_a = len(a)
    _check_enum(math.comb(len(pooled), n_a))
    at_least = 0
    total = 0
    idx = range(len(pooled))
    for combo in itertools.combinations(idx, n_a):
        chosen = set(combo)
        xs = [pooled[i] for i in idx if i in chosen]
        ys = [pooled[i] for i in idx if i not in chosen]
        if u_of(xs, ys) >= observed:
            at_least += 1
        total += 1
    return at_least / total


def permutation_exact(a: list[bool], b: list[bool]) -> float:
    """Exact one-sided permutation p for H1: pass rate of a > that of b."""
    if not a or not b:
        raise ValueError("both samples must be non-empty")
    observed = sum(a) / len(a) - sum(b) / len(b)
    pooled = [bool(v) for v in a] + [bool(v) for v in b]
    n_a = len(a)
    _check_enum(math.comb(len(pooled), n_a))
    at_least = 0
    total = 0
    idx = range(len(pooled))
    for combo in itertools.combinations(idx, n_a):
        chosen = set(combo)
        pa = sum(pooled[i] for i in chosen) / n_a
        pb = sum(pooled[i] for i in idx if i not in chosen) / (len(pooled) - n_a)
        if pa - pb >= observed - 1e-12:
            at_least += 1
        total += 1
    return at_least / total


def summary_stats(values: list[float]) -> dict:
    """The repo's standard aggregate: median + min/max + every point."""
    if not values:
        return {"median": None, "min": None, "max": None, "n": 0,
                "samples": []}
    return {"median": round(median(values), 3),
            "min": round(min(values), 3),
            "max": round(max(values), 3),
            "n": len(values),
            "samples": [round(v, 3) for v in values]}
