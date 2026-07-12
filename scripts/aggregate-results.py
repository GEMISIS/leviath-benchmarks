#!/usr/bin/env python3
"""
Aggregate multiple benchmark runs into a summary with statistics.
Reads results/runs/*.json, outputs results/benchmark-results.json
"""
import json
import math
import os
from pathlib import Path
from collections import defaultdict

def mean(values):
    return sum(values) / len(values) if values else 0

def stddev(values):
    if len(values) < 2:
        return 0
    m = mean(values)
    return math.sqrt(sum((x - m) ** 2 for x in values) / (len(values) - 1))

def ci95(values):
    """95% confidence interval half-width (t-distribution for small n)."""
    n = len(values)
    if n < 2:
        return 0
    # t-values for 95% CI: n=2→12.71, n=3→4.30, n=4→3.18, n=5→2.78
    t_values = {2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571, 7: 2.447}
    t = t_values.get(n, 2.0)
    return t * stddev(values) / math.sqrt(n)

def aggregate():
    script_dir = Path(__file__).parent
    runs_dir = script_dir.parent / 'results' / 'runs'
    output_path = script_dir.parent / 'results' / 'benchmark-results.json'

    # Collect runs by approach
    approaches = defaultdict(list)
    for f in sorted(runs_dir.glob('*.json')):
        with open(f) as fh:
            run = json.load(fh)
        approaches[run['approach']].append(run)

    result = {
        "benchmark": "stress-test-v3",
        "date": "2026-07-11",
        "task": "Multi-Tenant Event Processing Platform",
        "validation_tests": 69,
        "methodology": {
            "model": "claude-sonnet-5",
            "validation": "69 hidden tests across 13 categories, unseen by agent",
            "baseline": "Independent Rust binary, same API + tools, single flat context window",
            "seed_files": "11 spec files, 4 config files, identical for both approaches"
        },
        "approaches": {}
    }

    for approach, runs in approaches.items():
        n = len(runs)
        pass_rates = [r['pass_rate'] for r in runs]
        costs = [r['estimated_cost_usd'] for r in runs]
        durations = [r['duration_seconds'] for r in runs]
        tool_calls_list = [r['tool_calls'] for r in runs]
        passed_list = [r['passed'] for r in runs]

        # Category-level aggregation
        # Count how many times each test failed across runs
        all_failures = defaultdict(int)
        for r in runs:
            for f in r.get('failures', []):
                all_failures[f] += 1

        approach_data = {
            "version": "v3",
            "model": "claude-sonnet-5",
            "runs": n,
            "pass_rate": {
                "mean": round(mean(pass_rates), 1),
                "stddev": round(stddev(pass_rates), 1),
                "ci95": round(ci95(pass_rates), 1),
                "min": round(min(pass_rates), 1),
                "max": round(max(pass_rates), 1),
                "values": [round(v, 1) for v in pass_rates]
            },
            "cost_usd": {
                "mean": round(mean(costs), 2),
                "stddev": round(stddev(costs), 2),
                "ci95": round(ci95(costs), 2),
                "values": [round(v, 2) for v in costs]
            },
            "duration_seconds": {
                "mean": round(mean(durations)),
                "stddev": round(stddev(durations)),
                "values": durations
            },
            "tool_calls": {
                "mean": round(mean(tool_calls_list)),
                "stddev": round(stddev(tool_calls_list)),
                "values": tool_calls_list
            },
            "tests_passed": {
                "mean": round(mean(passed_list), 1),
                "values": passed_list
            },
            "common_failures": {name: count for name, count in 
                               sorted(all_failures.items(), key=lambda x: -x[1])
                               if count >= n // 2 + 1}  # failures in majority of runs
        }

        if approach == "leviath":
            approach_data["blueprint"] = "simple-coder"

        result["approaches"][approach] = approach_data

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)

    # Print summary
    for name, data in result['approaches'].items():
        n = data['runs']
        pr = data['pass_rate']
        cost = data['cost_usd']
        print(f"\n{'='*50}")
        print(f"{name.upper()} ({n} runs)")
        print(f"  Pass rate: {pr['mean']}% ± {pr['ci95']}% (95% CI)")
        print(f"  Cost: ${cost['mean']} ± ${cost['ci95']}")
        print(f"  Duration: {data['duration_seconds']['mean']}s")
        print(f"  Tool calls: {data['tool_calls']['mean']}")
        if data['common_failures']:
            print(f"  Common failures ({len(data['common_failures'])}):")
            for f, c in data['common_failures'].items():
                print(f"    - {f} ({c}/{n} runs)")

    print(f"\nSaved to {output_path}")

if __name__ == '__main__':
    aggregate()
