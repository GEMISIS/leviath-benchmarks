#!/bin/bash
# Run ALL 5 benchmark tasks sequentially and validate each one.
# Usage: run_multi_track.sh <approach> <blueprint_path> <run_id>
#
# Example:
#   ./scripts/run_multi_track.sh leviath blueprints/structured-coder/agent.leviath run1
#   ./scripts/run_multi_track.sh flat blueprints/simple-coder.leviath run1
set -euo pipefail

APPROACH="${1:?Usage: $0 <approach> <blueprint_path> <run_id>}"
BLUEPRINT="${2:?Usage: $0 <approach> <blueprint_path> <run_id>}"
RUN_ID="${3:?Usage: $0 <approach> <blueprint_path> <run_id>}"

BENCH_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS_DIR="$BENCH_ROOT/results/multi-track/${APPROACH}-${RUN_ID}"
mkdir -p "$RESULTS_DIR"

TASKS=("stress-test" "cli-tool" "rest-api" "refactor" "full-stack")
SUMMARY_FILE="$RESULTS_DIR/summary.json"

# Colour helpers (disabled if not a TTY)
if [ -t 1 ]; then
    GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; BOLD='\033[1m'; NC='\033[0m'
else
    GREEN=''; RED=''; YELLOW=''; BOLD=''; NC=''
fi

echo -e "${BOLD}=== Multi-Track Benchmark ===${NC}"
echo "Approach : $APPROACH"
echo "Blueprint: $BLUEPRINT"
echo "Run ID   : $RUN_ID"
echo "Results  : $RESULTS_DIR"
echo ""

TOTAL_PASSED=0
TOTAL_FAILED=0
TOTAL_TESTS=0
declare -a TASK_RESULTS=()

for TASK in "${TASKS[@]}"; do
    TASK_DIR="$BENCH_ROOT/tasks/$TASK"
    WORKDIR=$(mktemp -d "/tmp/bench-${TASK}-XXXXXX")

    echo -e "${BOLD}--- Task: $TASK ---${NC}"
    echo "  Workdir: $WORKDIR"

    # ── 1. Copy seed files (preserve seed-files/ dir for validation imports) ──
    if [ -d "$TASK_DIR/seed-files" ]; then
        cp -r "$TASK_DIR/seed-files" "$WORKDIR/seed-files"
        # Also copy contents to workdir root (agent sees them at top level)
        cp -r "$TASK_DIR/seed-files/"* "$WORKDIR/" 2>/dev/null || true
    fi

    # ── 2. Run the agent (skip if no harness binary yet) ────────────────
    AGENT_META="$WORKDIR/.agent-meta.json"
    START_TS=$(date +%s)

    LEV_BIN="${LEV_BIN:-$(command -v lev 2>/dev/null || echo "$HOME/dev/leviath/target/release/lev")}"
    FLAT_BIN="${FLAT_BIN:-$BENCH_ROOT/target/release/flat-baseline}"
    API_KEY="${ANTHROPIC_API_KEY:-$(grep 'anthropic_api_key' ~/.leviath/config.toml 2>/dev/null | sed 's/.*= *"//' | sed 's/"//')}"
    ABS_TASK="$(realpath "$TASK_DIR/task.md")"

    # Resolve blueprint to absolute path
    ABS_BLUEPRINT="$(cd "$BENCH_ROOT" && realpath "$BLUEPRINT")"

    # Snapshot existing runs before this task (for meta capture)
    RUNS_BEFORE=$(ls -d "$HOME/.leviath/runs/"*/ 2>/dev/null | wc -l | tr -d ' ')

    if [ "$APPROACH" = "leviath" ] && [ -x "$LEV_BIN" ]; then
        echo "  Running leviath agent..."
        echo "  Blueprint: $ABS_BLUEPRINT"
        echo "  Task: $ABS_TASK"
        (cd "$WORKDIR" && "$LEV_BIN" run "$ABS_BLUEPRINT" \
            --task "$ABS_TASK" \
            --foreground \
            --yolo) > "$WORKDIR/.agent.log" 2>&1 || true
        # Find the NEW run directory (created after RUNS_BEFORE)
        NEW_RUN=$(ls -td "$HOME/.leviath/runs/"*/ 2>/dev/null | head -1)
        RUNS_AFTER=$(ls -d "$HOME/.leviath/runs/"*/ 2>/dev/null | wc -l | tr -d ' ')
        if [ "$RUNS_AFTER" -gt "$RUNS_BEFORE" ] && [ -n "$NEW_RUN" ]; then
            cp "$NEW_RUN/meta.json" "$AGENT_META" 2>/dev/null || true
            echo "  Meta captured from: $NEW_RUN"
        else
            echo "  ⚠ No new run directory found for meta capture"
        fi
    elif [ "$APPROACH" = "flat" ] && [ -x "$FLAT_BIN" ]; then
        echo "  Running flat baseline agent..."
        "$FLAT_BIN" \
            --task "$(cat "$ABS_TASK")" \
            --model "claude-sonnet-5" \
            --workdir "$WORKDIR" \
            --max-iterations 200 \
            --api-key "$API_KEY" \
            --output "$AGENT_META" > "$WORKDIR/.agent.log" 2>&1 || true
    else
        echo -e "  ${YELLOW}⚠  No agent runner found for approach '$APPROACH'.${NC}"
        echo -e "  ${YELLOW}   LEV_BIN=$LEV_BIN  FLAT_BIN=$FLAT_BIN${NC}"
    fi

    END_TS=$(date +%s)
    DURATION=$((END_TS - START_TS))

    # ── 3. Validate ─────────────────────────────────────────────────────
    VALIDATION_DIR="$TASK_DIR/validation"
    TASK_RESULT_FILE="$RESULTS_DIR/${TASK}.json"

    if [ ! -d "$VALIDATION_DIR" ]; then
        echo -e "  ${YELLOW}⚠  No validation directory — skipping.${NC}"
        TASK_RESULTS+=("{\"task\":\"$TASK\",\"passed\":0,\"failed\":0,\"total\":0,\"pass_rate\":0,\"skipped\":true}")
        continue
    fi

    # Copy validation suite into workdir
    cp -r "$VALIDATION_DIR" "$WORKDIR/validation"

    # Set up venv and install deps
    (
        cd "$WORKDIR"
        python3 -m venv .venv 2>/dev/null || true
        # shellcheck disable=SC1091
        source .venv/bin/activate

        if [ -f validation/requirements.txt ]; then
            pip install -r validation/requirements.txt -q 2>&1 | tail -1
        fi
        if [ -f requirements.txt ]; then
            pip install -r requirements.txt -q 2>&1 | tail -1
        fi

        # Run pytest with JSON report
        PYTEST_REPORT="$WORKDIR/.pytest-report.json"
        python3 -m pytest validation/ -v --tb=line \
            --json-report --json-report-file="$PYTEST_REPORT" 2>&1 | tail -10 || true

        # Parse results
        python3 << PYEOF
import json, os

report_path = "$PYTEST_REPORT"
result_path = "$TASK_RESULT_FILE"

if not os.path.exists(report_path):
    result = {"task": "$TASK", "passed": 0, "failed": 0, "total": 0, "pass_rate": 0.0, "error": "pytest report not generated"}
else:
    with open(report_path) as f:
        report = json.load(f)

    passed = report['summary'].get('passed', 0)
    failed = report['summary'].get('failed', 0)
    errors = report['summary'].get('error', 0)
    total = passed + failed + errors

    failures = [t['nodeid'].split('::')[-1] for t in report.get('tests', []) if t['outcome'] in ('failed', 'error')]

    # Read agent meta if available
    meta = {}
    meta_path = "$AGENT_META"
    if os.path.exists(meta_path):
        try:
            with open(meta_path) as f:
                meta = json.load(f)
        except Exception:
            pass

    result = {
        "task": "$TASK",
        "approach": "$APPROACH",
        "run_id": "$RUN_ID",
        "duration_seconds": $DURATION if $DURATION > 0 else meta.get("duration_seconds", 0),
        "tool_calls": meta.get("tool_calls", 0),
        "prompt_tokens": meta.get("prompt_tokens", 0),
        "completion_tokens": meta.get("completion_tokens", 0),
        "estimated_cost_usd": round(
            meta.get("prompt_tokens", meta.get("total_prompt_tokens", 0)) * 3 / 1_000_000 +
            meta.get("completion_tokens", meta.get("total_completion_tokens", 0)) * 15 / 1_000_000, 2),
        "passed": passed,
        "failed": failed,
        "total": total,
        "pass_rate": round(passed / total * 100, 2) if total > 0 else 0.0,
        "failures": failures,
    }

with open(result_path, 'w') as f:
    json.dump(result, f, indent=2)

# Print compact result line
pr = result.get('pass_rate', 0)
print(f"  {result['task']}: {result.get('passed',0)}/{result.get('total',0)} ({pr}%)")
PYEOF
    ) || true

    # Accumulate totals
    if [ -f "$TASK_RESULT_FILE" ]; then
        T_PASSED=$(python3 -c "import json; print(json.load(open('$TASK_RESULT_FILE')).get('passed',0))")
        T_FAILED=$(python3 -c "import json; print(json.load(open('$TASK_RESULT_FILE')).get('failed',0))")
        T_TOTAL=$(python3 -c "import json; print(json.load(open('$TASK_RESULT_FILE')).get('total',0))")
        TOTAL_PASSED=$((TOTAL_PASSED + T_PASSED))
        TOTAL_FAILED=$((TOTAL_FAILED + T_FAILED))
        TOTAL_TESTS=$((TOTAL_TESTS + T_TOTAL))
    fi

    echo ""
done

# ── Summary ─────────────────────────────────────────────────────────────

echo -e "${BOLD}=== Summary: ${APPROACH} / ${RUN_ID} ===${NC}"
echo ""
printf "%-15s %8s %8s %8s %10s\n" "TASK" "PASSED" "FAILED" "TOTAL" "RATE"
printf "%-15s %8s %8s %8s %10s\n" "───────────────" "────────" "────────" "────────" "──────────"

for TASK in "${TASKS[@]}"; do
    TASK_RESULT_FILE="$RESULTS_DIR/${TASK}.json"
    if [ -f "$TASK_RESULT_FILE" ]; then
        python3 -c "
import json
r = json.load(open('$TASK_RESULT_FILE'))
print(f\"  {r['task']:<13s} {r.get('passed',0):>8d} {r.get('failed',0):>8d} {r.get('total',0):>8d} {r.get('pass_rate',0):>9.1f}%\")
"
    else
        printf "  %-13s %8s %8s %8s %10s\n" "$TASK" "-" "-" "-" "skipped"
    fi
done

echo ""
if [ "$TOTAL_TESTS" -gt 0 ]; then
    OVERALL_RATE=$(python3 -c "print(round($TOTAL_PASSED / $TOTAL_TESTS * 100, 2))")
    echo -e "${BOLD}Overall: ${TOTAL_PASSED}/${TOTAL_TESTS} (${OVERALL_RATE}%)${NC}"
else
    OVERALL_RATE=0
    echo -e "${YELLOW}No tests were executed.${NC}"
fi

# Write combined summary JSON
python3 << PYEOF
import json, glob, os

results_dir = "$RESULTS_DIR"
tasks = []
for f in sorted(glob.glob(os.path.join(results_dir, "*.json"))):
    if os.path.basename(f) == "summary.json":
        continue
    with open(f) as fh:
        tasks.append(json.load(fh))

summary = {
    "approach": "$APPROACH",
    "run_id": "$RUN_ID",
    "tasks": tasks,
    "totals": {
        "passed": $TOTAL_PASSED,
        "failed": $TOTAL_FAILED,
        "total": $TOTAL_TESTS,
        "pass_rate": $OVERALL_RATE,
    }
}

with open(os.path.join(results_dir, "summary.json"), "w") as f:
    json.dump(summary, f, indent=2)
PYEOF

echo ""
echo "Results saved to: $RESULTS_DIR"
