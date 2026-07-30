#!/usr/bin/env python3
"""Aggregate the runs of one benchmark round into a summary.

Usage:
    scripts/aggregate-results.py results/rounds/<freeze-tag>/

Reads every  <round-dir>/runs/*.json  and writes  <round-dir>/benchmark-results.json.

Integrity rules (see METHODOLOGY.md):
  - Every run file MUST carry a "freeze_tag" matching the round directory name;
    anything else is refused. This is what prevents mixing runs scored under
    different task/suite versions (the failure mode of the July 2026 round).
  - No metadata is hardcoded here: model, task, blueprint, and suite hash are
    read from the run files and must agree across runs of the same arm.
  - All values are published: mean, median, min/max, and the raw per-run list.
    No confidence intervals on tiny samples — when exactly two arms are
    present, an exact one-sided Mann-Whitney rank-sum p-value is reported for
    pass_rate and total_billed_tokens instead.
  - Costs are recomputed here, identically for every arm, from API-reported
    usage fields via scripts/cost.py and the round's rates.json. A run file
    without usage fields is refused — no len/4 heuristics, no cache-blind
    arithmetic.
"""
import json
import statistics
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cost import compute_cost, load_rates  # noqa: E402

REQUIRED_RUN_FIELDS = (
    "approach", "freeze_tag", "model", "task", "pass_rate", "passed", "total",
    "duration_seconds", "tool_calls", "usage",
)
REQUIRED_USAGE_FIELDS = (
    "input_tokens", "output_tokens",
    "cache_creation_input_tokens", "cache_read_input_tokens",
)


def exact_rank_sum_p(a, b, larger_is_better=True):
    """Exact one-sided Mann-Whitney p-value: probability, under the null of
    exchangeability, of a rank sum for `a` at least as extreme as observed."""
    pooled = a + b
    n = len(pooled)
    # Midranks so ties are handled symmetrically.
    sorted_vals = sorted(pooled)
    midrank = {}
    for v in set(pooled):
        first = sorted_vals.index(v) + 1
        last = first + sorted_vals.count(v) - 1
        midrank[v] = (first + last) / 2
    ranks = [midrank[v] for v in pooled]
    observed = sum(ranks[:len(a)])
    count = total = 0
    for idx in combinations(range(n), len(a)):
        rs = sum(ranks[i] for i in idx)
        total += 1
        if (larger_is_better and rs >= observed) or (not larger_is_better and rs <= observed):
            count += 1
    return count / total


def summarize(values, digits=2):
    return {
        "mean": round(statistics.mean(values), digits),
        "median": round(statistics.median(values), digits),
        "min": round(min(values), digits),
        "max": round(max(values), digits),
        "values": [round(v, digits) for v in values],
        "n": len(values),
    }


def consistent(runs, field):
    vals = {json.dumps(r[field], sort_keys=True) for r in runs}
    if len(vals) != 1:
        sys.exit(f"refusing to aggregate: field '{field}' differs across runs "
                 f"of arm '{runs[0]['approach']}': {sorted(vals)}")
    return runs[0][field]


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    round_dir = Path(sys.argv[1]).resolve()
    tag = round_dir.name
    runs_dir = round_dir / "runs"
    run_files = sorted(runs_dir.glob("*.json"))
    if not run_files:
        sys.exit(f"no run files in {runs_dir}")
    rates = load_rates(round_dir / "rates.json")

    arms = defaultdict(list)
    for f in run_files:
        run = json.loads(f.read_text())
        for field in REQUIRED_RUN_FIELDS:
            if field not in run:
                sys.exit(f"refusing {f.name}: missing required field '{field}'")
        for field in REQUIRED_USAGE_FIELDS:
            if field not in run["usage"]:
                sys.exit(f"refusing {f.name}: usage missing '{field}' — costs "
                         "must come from API-reported usage, not estimates")
        if run["freeze_tag"] != tag:
            sys.exit(f"refusing {f.name}: freeze_tag '{run['freeze_tag']}' != "
                     f"round '{tag}' — do not mix rounds")
        run["_file"] = f.name
        arms[run["approach"]].append(run)

    result = {"freeze_tag": tag, "run_files": [f.name for f in run_files], "arms": {}}
    for arm, runs in sorted(arms.items()):
        usage_totals = [sum(r["usage"][k] for k in REQUIRED_USAGE_FIELDS) for r in runs]
        cache_rates = [
            r["usage"]["cache_read_input_tokens"] /
            max(1, r["usage"]["input_tokens"] + r["usage"]["cache_read_input_tokens"] +
                r["usage"]["cache_creation_input_tokens"]) * 100
            for r in runs
        ]
        result["arms"][arm] = {
            "model": consistent(runs, "model"),
            "task": consistent(runs, "task"),
            "blueprint": consistent(runs, "blueprint") if all("blueprint" in r for r in runs) else None,
            "runs": len(runs),
            "pass_rate": summarize([r["pass_rate"] for r in runs], 1),
            "cost_usd": summarize([compute_cost(r["usage"], r["model"], rates) for r in runs]),
            "total_billed_tokens": summarize(usage_totals, 0),
            "cache_hit_rate_pct": summarize(cache_rates, 1),
            "duration_seconds": summarize([r["duration_seconds"] for r in runs], 0),
            "tool_calls": summarize([r["tool_calls"] for r in runs], 0),
        }

    if len(arms) == 2:
        # The pre-registered hypothesis (METHODOLOGY.md) is that the
        # structured arm scores higher and bills fewer tokens — so that arm is
        # always A. Falls back to sorted order for other arm pairs.
        names = sorted(arms, key=lambda n: (n != "structured", n))
        (a_name, b_name) = names
        a_runs, b_runs = arms[a_name], arms[b_name]
        result["comparison"] = {
            "arms": [a_name, b_name],
            "note": "exact one-sided Mann-Whitney rank-sum p-values; "
                    f"H1: {a_name} higher pass_rate / lower tokens",
            "pass_rate_p": round(exact_rank_sum_p(
                [r["pass_rate"] for r in a_runs], [r["pass_rate"] for r in b_runs],
                larger_is_better=True), 4),
            "total_billed_tokens_p": round(exact_rank_sum_p(
                [sum(r["usage"][k] for k in REQUIRED_USAGE_FIELDS) for r in a_runs],
                [sum(r["usage"][k] for k in REQUIRED_USAGE_FIELDS) for r in b_runs],
                larger_is_better=False), 4),
        }

    out = round_dir / "benchmark-results.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    for arm, data in result["arms"].items():
        print(f"{arm}: n={data['runs']} pass median {data['pass_rate']['median']}% "
              f"[{data['pass_rate']['min']}–{data['pass_rate']['max']}], "
              f"cost median ${data['cost_usd']['median']}, "
              f"cache hit median {data['cache_hit_rate_pct']['median']}%")
    if "comparison" in result:
        c = result["comparison"]
        print(f"p(pass_rate)={c['pass_rate_p']}  p(tokens)={c['total_billed_tokens_p']}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
