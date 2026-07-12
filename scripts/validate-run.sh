#!/bin/bash
# Validate a benchmark run against the hidden test suite
# Usage: validate-run.sh <workdir> <approach> <run_number> [<meta_json>]
set -e

WORKDIR="$1"
APPROACH="$2"
RUN_NUM="$3"
META_JSON="$4"

if [ -z "$WORKDIR" ] || [ -z "$APPROACH" ] || [ -z "$RUN_NUM" ]; then
    echo "Usage: $0 <workdir> <approach> <run_number> [<meta_json>]"
    exit 1
fi

BENCH_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS_DIR="$BENCH_ROOT/results/runs"
mkdir -p "$RESULTS_DIR"

echo "=== Validating $APPROACH run $RUN_NUM ==="
echo "Workdir: $WORKDIR"

# Copy validation tests
cp -r "$BENCH_ROOT/tasks/stress-test/validation" "$WORKDIR/"

# Set up venv
cd "$WORKDIR"
python3 -m venv .venv 2>/dev/null || true
source .venv/bin/activate
pip install -r validation/requirements.txt -q 2>&1 | tail -1
pip install -r requirements.txt -q 2>&1 | tail -1

# Run validation with JSON output
python3 -m pytest validation/ -v --tb=line --json-report --json-report-file=/tmp/pytest-report.json 2>&1 | tail -5

# Parse results
python3 << PYEOF
import json

with open('/tmp/pytest-report.json') as f:
    report = json.load(f)

passed = report['summary'].get('passed', 0)
failed = report['summary'].get('failed', 0)
errors = report['summary'].get('error', 0)
total = passed + failed + errors

failures = [t['nodeid'].split('::')[-1] for t in report.get('tests', []) if t['outcome'] == 'failed']

# Get meta info
meta = {}
meta_path = "$META_JSON"
if meta_path:
    try:
        with open(meta_path) as f:
            meta = json.load(f)
    except:
        pass

result = {
    "run": $RUN_NUM,
    "approach": "$APPROACH",
    "duration_seconds": meta.get("duration_seconds", 0) or int(meta.get("updated_at", 0) - meta.get("started_at", 0)),
    "tool_calls": meta.get("tool_calls", 0),
    "prompt_tokens": meta.get("prompt_tokens", 0),
    "completion_tokens": meta.get("completion_tokens", 0),
    "estimated_cost_usd": round(meta.get("prompt_tokens", 0) * 3 / 1_000_000 + meta.get("completion_tokens", 0) * 15 / 1_000_000, 2),
    "passed": passed,
    "failed": failed,
    "total": total,
    "pass_rate": round(passed / total * 100, 2) if total > 0 else 0,
    "failures": failures
}

outpath = "$RESULTS_DIR/${APPROACH}-run${RUN_NUM}.json"
with open(outpath, 'w') as f:
    json.dump(result, f, indent=2)

print(f"\n=== {result['approach']} run {result['run']} ===")
print(f"Pass rate: {result['passed']}/{result['total']} ({result['pass_rate']}%)")
print(f"Cost: \${result['estimated_cost_usd']}")
print(f"Saved to: {outpath}")
PYEOF
