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

Whole-suite comparisons run past that cap - 36 runs against 36 is
C(72,36), which no machine will enumerate - so ``rank_sum_test`` and
``pass_rate_test`` wrap the pair: exact enumeration when it fits,
otherwise a seeded random-permutation test with a declared number of
resamples. Both return the method, the resample count, and the seed
alongside the p-value, so a published number always says how it was
computed. The Monte-Carlo estimator is (r+1)/(m+1), which is valid
rather than merely close: it never reports a p smaller than one
resample's worth of resolution.
"""
from __future__ import annotations

import itertools
import math
import random
from statistics import median

__all__ = ["mann_whitney_exact", "permutation_exact", "pass_rate_test",
           "rank_sum_test", "summary_stats"]

# Enough resolution to distinguish p = 0.001 from p = 0.01, cheap enough
# to run for every pre-registered comparison in a round.
DEFAULT_RESAMPLES = 200_000

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


def _monte_carlo(pooled: list, n_a: int, statistic, observed: float,
                 resamples: int, seed: int) -> float:
    """Share of random label reassignments at least as extreme as the
    observed one, by the (r+1)/(m+1) estimator."""
    rng = random.Random(seed)
    at_least = 0
    shuffled = list(pooled)
    for _ in range(resamples):
        rng.shuffle(shuffled)
        if statistic(shuffled[:n_a], shuffled[n_a:]) >= observed - 1e-12:
            at_least += 1
    return (at_least + 1) / (resamples + 1)


def _test(a: list, b: list, statistic, exact_fn,
          resamples: int, seed: int) -> dict:
    if not a or not b:
        raise ValueError("both samples must be non-empty")
    n_comb = math.comb(len(a) + len(b), len(a))
    if n_comb <= _MAX_ENUM:
        return {"p": exact_fn(a, b), "method": "exact_enumeration",
                "combinations": n_comb, "resamples": None, "seed": None}
    observed = statistic(list(a), list(b))
    p = _monte_carlo(list(a) + list(b), len(a), statistic, observed,
                     resamples, seed)
    return {"p": p, "method": "random_permutation",
            "combinations": n_comb, "resamples": resamples, "seed": seed}


def _u_statistic(xs: list[float], ys: list[float]) -> float:
    u = 0.0
    for x in xs:
        for y in ys:
            if x < y:
                u += 1.0
            elif x == y:
                u += 0.5
    return u


def _pass_gap(xs: list, ys: list) -> float:
    return sum(bool(v) for v in xs) / len(xs) - \
        sum(bool(v) for v in ys) / len(ys)


def rank_sum_test(a: list[float], b: list[float],
                  resamples: int = DEFAULT_RESAMPLES,
                  seed: int = 0) -> dict:
    """One-sided rank-sum for H1: a tends LOWER than b.

    Exact when the enumeration fits, a seeded random-permutation test
    otherwise; the returned dict always says which, so nothing silently
    becomes an approximation.
    """
    return _test(a, b, _u_statistic, mann_whitney_exact, resamples, seed)


def pass_rate_test(a: list[bool], b: list[bool],
                   resamples: int = DEFAULT_RESAMPLES,
                   seed: int = 0) -> dict:
    """One-sided test for H1: a passes MORE often than b."""
    return _test([bool(v) for v in a], [bool(v) for v in b], _pass_gap,
                 permutation_exact, resamples, seed)


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
