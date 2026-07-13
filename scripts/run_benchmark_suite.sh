#!/bin/bash
# Run the multi-track benchmark suite for BOTH approaches and compare results.
#
# Usage: run_benchmark_suite.sh [run_id]
#
# Example:
#   ./scripts/run_benchmark_suite.sh run1
#   ./scripts/run_benchmark_suite.sh           # auto-generates run id
set -euo pipefail

BENCH_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RUN_ID="${1:-run-$(date +%Y%m%d-%H%M%S)}"

LEVIATH_BLUEPRINT="${LEVIATH_BLUEPRINT:-$BENCH_ROOT/blueprints/structured-coder/agent.leviath}"
FLAT_BLUEPRINT="${FLAT_BLUEPRINT:-$BENCH_ROOT/blueprints/simple-coder.leviath}"

REPORT_DIR="$BENCH_ROOT/results/multi-track"
COMBINED_REPORT="$REPORT_DIR/comparison-${RUN_ID}.json"
mkdir -p "$REPORT_DIR"

# Colour helpers
if [ -t 1 ]; then
    GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; BOLD='\033[1m'; NC='\033[0m'
else
    GREEN=''; RED=''; YELLOW=''; BOLD=''; NC=''
fi

echo -e "${BOLD}╔══════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   Multi-Track Benchmark Comparison       ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════╝${NC}"
echo ""
echo "Run ID : $RUN_ID"
echo ""

# ── Run Leviath approach ────────────────────────────────────────────────

echo -e "${BOLD}▶ Running LEVIATH approach...${NC}"
echo ""
bash "$BENCH_ROOT/scripts/run_multi_track.sh" leviath "$LEVIATH_BLUEPRINT" "$RUN_ID" || true
echo ""

# ── Run Flat approach ───────────────────────────────────────────────────

echo -e "${BOLD}▶ Running FLAT approach...${NC}"
echo ""
bash "$BENCH_ROOT/scripts/run_multi_track.sh" flat "$FLAT_BLUEPRINT" "$RUN_ID" || true
echo ""

# ── Compare Results ─────────────────────────────────────────────────────

echo -e "${BOLD}╔══════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   Comparative Results                    ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════╝${NC}"
echo ""

python3 << PYEOF
import json, os

report_dir = "$REPORT_DIR"
run_id = "$RUN_ID"

leviath_summary_path = os.path.join(report_dir, f"leviath-{run_id}", "summary.json")
flat_summary_path = os.path.join(report_dir, f"flat-{run_id}", "summary.json")

def load_summary(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

leviath = load_summary(leviath_summary_path)
flat = load_summary(flat_summary_path)

if not leviath and not flat:
    print("  No results found for either approach.")
    exit(0)

# Build task-by-task comparison
tasks = set()
leviath_tasks = {}
flat_tasks = {}

if leviath:
    for t in leviath.get("tasks", []):
        name = t.get("task", "unknown")
        tasks.add(name)
        leviath_tasks[name] = t

if flat:
    for t in flat.get("tasks", []):
        name = t.get("task", "unknown")
        tasks.add(name)
        flat_tasks[name] = t

# Print comparison table
header = f"{'TASK':<15s} {'LEVIATH':>12s} {'FLAT':>12s} {'DELTA':>10s}"
sep    = f"{'─'*15:<15s} {'─'*12:>12s} {'─'*12:>12s} {'─'*10:>10s}"
print(header)
print(sep)

for task in sorted(tasks):
    lt = leviath_tasks.get(task, {})
    ft = flat_tasks.get(task, {})

    l_rate = lt.get("pass_rate", 0)
    f_rate = ft.get("pass_rate", 0)
    l_str = f"{lt.get('passed', 0)}/{lt.get('total', 0)} ({l_rate}%)" if lt else "—"
    f_str = f"{ft.get('passed', 0)}/{ft.get('total', 0)} ({f_rate}%)" if ft else "—"

    delta = l_rate - f_rate
    if delta > 0:
        d_str = f"+{delta:.1f}%"
    elif delta < 0:
        d_str = f"{delta:.1f}%"
    else:
        d_str = "0.0%"

    print(f"  {task:<13s} {l_str:>12s} {f_str:>12s} {d_str:>10s}")

print()

# Totals
l_totals = leviath.get("totals", {}) if leviath else {}
f_totals = flat.get("totals", {}) if flat else {}
l_overall = l_totals.get("pass_rate", 0)
f_overall = f_totals.get("pass_rate", 0)
overall_delta = l_overall - f_overall

print(f"{'OVERALL':<15s} {l_overall:>11.1f}% {f_overall:>11.1f}% {overall_delta:>+9.1f}%")
print()

# Cost comparison (if available)
l_cost = sum(t.get("estimated_cost_usd", 0) for t in leviath.get("tasks", [])) if leviath else 0
f_cost = sum(t.get("estimated_cost_usd", 0) for t in flat.get("tasks", [])) if flat else 0
if l_cost > 0 or f_cost > 0:
    print(f"Est. Cost:      Leviath ${l_cost:.2f}  |  Flat ${f_cost:.2f}")

l_dur = sum(t.get("duration_seconds", 0) for t in leviath.get("tasks", [])) if leviath else 0
f_dur = sum(t.get("duration_seconds", 0) for t in flat.get("tasks", [])) if flat else 0
if l_dur > 0 or f_dur > 0:
    print(f"Duration:       Leviath {l_dur}s  |  Flat {f_dur}s")

print()

# Write combined report
combined = {
    "run_id": run_id,
    "leviath": leviath,
    "flat": flat,
    "comparison": {
        "leviath_overall_pass_rate": l_overall,
        "flat_overall_pass_rate": f_overall,
        "delta": overall_delta,
        "leviath_cost_usd": l_cost,
        "flat_cost_usd": f_cost,
        "leviath_duration_seconds": l_dur,
        "flat_duration_seconds": f_dur,
    }
}

report_path = "$COMBINED_REPORT"
with open(report_path, "w") as f:
    json.dump(combined, f, indent=2)

print(f"Combined report saved to: {report_path}")
PYEOF
