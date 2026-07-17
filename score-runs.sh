#!/bin/bash
# Score completed Leviath benchmark runs
# Usage: ./score-runs.sh <workdir1> [workdir2] [workdir3] ...
#
# Prerequisites: python venv with flask, pyyaml, bcrypt, pytest, pytest-timeout
#
# Example:
#   ./score-runs.sh /tmp/tmp.abc123 /tmp/tmp.def456 /tmp/tmp.ghi789

set -e

if [ $# -eq 0 ]; then
  echo "Usage: $0 <workdir1> [workdir2] ..."
  echo ""
  echo "Score one or more completed benchmark workdirs against the validation suite."
  echo ""
  echo "First time setup:"
  echo "  python3 -m venv .venv"
  echo "  source .venv/bin/activate" 
  echo "  pip install flask pyyaml bcrypt pytest pytest-timeout"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VALIDATION_DIR="$SCRIPT_DIR/tasks/stress-test/validation"

# Try to find a venv
if [ -d "$SCRIPT_DIR/.venv" ]; then
  PYTHON="$SCRIPT_DIR/.venv/bin/python"
elif [ -n "$VIRTUAL_ENV" ]; then
  PYTHON="$VIRTUAL_ENV/bin/python"
else
  PYTHON="python3"
fi

echo "=== Leviath Benchmark Scorer ==="
echo "Python: $PYTHON"
echo "Validation: $VALIDATION_DIR"
echo ""

RUN_NUM=1
for WORKDIR in "$@"; do
  if [ ! -d "$WORKDIR/src" ]; then
    echo "Run $RUN_NUM ($WORKDIR): SKIP — no src/ directory"
    RUN_NUM=$((RUN_NUM + 1))
    continue
  fi
  
  cd "$WORKDIR"
  cp "$VALIDATION_DIR"/{test_behavioral.py,test_algorithms.py,conftest.py} .
  
  # Run algo tests
  ALGO=$($PYTHON -m pytest test_algorithms.py --tb=no -q 2>&1 | tail -1)
  ALGO_PASS=$(echo "$ALGO" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+' || echo 0)
  ALGO_FAIL=$(echo "$ALGO" | grep -oE '[0-9]+ failed' | grep -oE '[0-9]+' || echo 0)
  ALGO_SKIP=$(echo "$ALGO" | grep -oE '[0-9]+ skipped' | grep -oE '[0-9]+' || echo 0)
  
  # Run behavioral tests per class with timeout
  BEH_PASS=0
  BEH_FAIL=0
  for cls in TestEventIngestion TestBatchIngestion TestDLQEndpoints TestHealthEndpoint TestMetricsEndpoint TestErrorResponseFormat TestAuthWithBcrypt TestHappyPath TestIdempotency TestRateLimiting TestAPIAuth TestSchemaValidation; do
    result=$(timeout 25 $PYTHON -m pytest "test_behavioral.py::$cls" --tb=no -q 2>&1 | grep -E "passed|failed" | tail -1)
    p=$(echo "$result" | grep -oE '[0-9]+ passed' | grep -oE '[0-9]+' || echo 0)
    f=$(echo "$result" | grep -oE '[0-9]+ failed' | grep -oE '[0-9]+' || echo 0)
    BEH_PASS=$((BEH_PASS + ${p:-0}))
    BEH_FAIL=$((BEH_FAIL + ${f:-0}))
  done
  
  TOTAL=$((ALGO_PASS + BEH_PASS))
  echo "Run $RUN_NUM ($WORKDIR):"
  echo "  Algo: ${ALGO_PASS}p/${ALGO_FAIL}f/${ALGO_SKIP}s  Behavioral: ${BEH_PASS}p/${BEH_FAIL}f"
  echo "  Score: ${TOTAL}/59"
  echo ""
  
  RUN_NUM=$((RUN_NUM + 1))
done
