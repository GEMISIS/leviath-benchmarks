#!/usr/bin/env bash
# run-benchmark.sh — Run a stress-test benchmark for a given approach.
#
# Usage:
#   ./run-benchmark.sh <approach>
#
# Where <approach> is one of: leviath, flat
#
set -euo pipefail

APPROACH="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TASK_DIR="$SCRIPT_DIR/tasks/stress-test"
VALIDATION_DIR="$TASK_DIR/validation"
RESULTS_DIR="$SCRIPT_DIR/results"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

if [[ -z "$APPROACH" ]]; then
  echo "Usage: $0 <approach>"
  echo "  approach: leviath | flat"
  exit 1
fi

if [[ "$APPROACH" != "leviath" && "$APPROACH" != "flat" ]]; then
  echo "Error: approach must be 'leviath' or 'flat'"
  exit 1
fi

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

WORKDIR="$(mktemp -d)"
echo "=== Stress Test Benchmark ==="
echo "Approach:  $APPROACH"
echo "Workdir:   $WORKDIR"
echo "Timestamp: $TIMESTAMP"
echo ""

# Copy seed files into workdir
cp -r "$TASK_DIR/seed-files/"* "$WORKDIR/"
echo "Copied seed files to workdir."

# ---------------------------------------------------------------------------
# Run the approach
# ---------------------------------------------------------------------------

START_TIME=$(date +%s)

echo ""
echo "--- Running $APPROACH approach ---"
echo ""

if [[ "$APPROACH" == "leviath" ]]; then
  echo "Running Leviath agent..."
  # Invoke Leviath with the task file pointed at the workdir
  # Adjust the command below to match your Leviath CLI invocation
  if command -v leviath &>/dev/null; then
    cd "$WORKDIR"
    leviath run \
      --blueprint "$SCRIPT_DIR/blueprints/simple-coder.leviath" \
      --task "$TASK_DIR/task.md" \
      --workdir "$WORKDIR" \
      2>&1 | tee "$WORKDIR/agent.log" || true
  else
    echo "WARNING: 'leviath' command not found. Skipping agent run."
    echo "         Place your implementation in: $WORKDIR/src/"
  fi
elif [[ "$APPROACH" == "flat" ]]; then
  echo "Running flat baseline..."
  if [[ -f "$SCRIPT_DIR/target/release/flat-baseline" ]]; then
    cd "$WORKDIR"
    "$SCRIPT_DIR/target/release/flat-baseline" \
      --task "$TASK_DIR/task.md" \
      --workdir "$WORKDIR" \
      2>&1 | tee "$WORKDIR/agent.log" || true
  else
    echo "WARNING: flat-baseline binary not found. Skipping agent run."
    echo "         Place your implementation in: $WORKDIR/src/"
  fi
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo "Agent completed in ${DURATION}s."

# ---------------------------------------------------------------------------
# Run validation tests
# ---------------------------------------------------------------------------

echo ""
echo "--- Running validation tests ---"
echo ""

# Copy validation tests into the workdir
cp -r "$VALIDATION_DIR" "$WORKDIR/validation"

# Install validation requirements
cd "$WORKDIR"
pip3 install -q -r validation/requirements.txt 2>/dev/null || \
  pip3 install --user -q -r validation/requirements.txt 2>/dev/null || \
  pip3 install --break-system-packages -q -r validation/requirements.txt 2>/dev/null || true

# Install the implementation's requirements if present
if [[ -f "$WORKDIR/requirements.txt" ]]; then
  pip3 install -q -r "$WORKDIR/requirements.txt" 2>/dev/null || \
    pip3 install --user -q -r "$WORKDIR/requirements.txt" 2>/dev/null || \
    pip3 install --break-system-packages -q -r "$WORKDIR/requirements.txt" 2>/dev/null || true
fi

# Run pytest with JSON report
REPORT_FILE="$WORKDIR/test-report.json"
cd "$WORKDIR"
python3 -m pytest validation/ \
  -v \
  --json-report \
  --json-report-file="$REPORT_FILE" \
  --tb=short \
  -x || true

# ---------------------------------------------------------------------------
# Parse results
# ---------------------------------------------------------------------------

echo ""
echo "--- Results ---"
echo ""

if [[ -f "$REPORT_FILE" ]]; then
  python3 -c "
import json, sys

with open('$REPORT_FILE') as f:
    report = json.load(f)

summary = report.get('summary', {})
total = summary.get('total', 0)
passed = summary.get('passed', 0)
failed = summary.get('failed', 0)
errors = summary.get('error', 0)

print(f'Total:   {total}')
print(f'Passed:  {passed}')
print(f'Failed:  {failed}')
print(f'Errors:  {errors}')
print(f'Pass %%:  {passed/total*100:.1f}%%' if total else 'Pass %: N/A')

# Count by category (test class name → category)
categories = {}
for test in report.get('tests', []):
    nodeid = test.get('nodeid', '')
    outcome = test.get('outcome', '')
    # Extract class name: validation/test_pipeline.py::TestHappyPath::test_...
    parts = nodeid.split('::')
    cls = parts[1] if len(parts) > 1 else 'unknown'
    # Convert TestHappyPath → happy_path
    cat = cls.replace('Test', '').strip()
    # CamelCase to snake_case
    import re
    cat = re.sub(r'(?<!^)(?=[A-Z])', '_', cat).lower()
    if cat not in categories:
        categories[cat] = {'total': 0, 'passed': 0}
    categories[cat]['total'] += 1
    if outcome == 'passed':
        categories[cat]['passed'] += 1

print()
print('By category:')
for cat, data in sorted(categories.items()):
    pct = data['passed']/data['total']*100 if data['total'] else 0
    print(f'  {cat:25s} {data[\"passed\"]}/{data[\"total\"]} ({pct:.0f}%)')
"
else
  echo "No test report generated."
fi

echo ""
echo "Duration:  ${DURATION}s"
echo "Workdir:   $WORKDIR"
echo "Report:    $REPORT_FILE"
echo ""
echo "Done."
