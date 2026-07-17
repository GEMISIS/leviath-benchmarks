#!/bin/bash
# Run N parallel Leviath benchmark runs with a given blueprint
# Usage: ./run-benchmark.sh <blueprint-path> [num-runs] [task-path]
#
# Examples:
#   ./run-benchmark.sh blueprints/engineer-v2/agent.leviath
#   ./run-benchmark.sh blueprints/engineer-v3/agent.leviath 3
#   ./run-benchmark.sh blueprints/engineer-v2/agent.leviath 5 tasks/stress-test/task.md

set -e

BLUEPRINT="${1:?Usage: $0 <blueprint-path> [num-runs] [task-path]}"
NUM_RUNS="${2:-3}"
TASK="${3:-tasks/stress-test/task.md}"
SEED_DIR="tasks/stress-test/seed-files"
VALIDATION_DIR="tasks/stress-test/validation"

# Resolve paths relative to script location
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BLUEPRINT="$SCRIPT_DIR/$BLUEPRINT"
TASK="$SCRIPT_DIR/$TASK"
SEED_DIR="$SCRIPT_DIR/$SEED_DIR"
VALIDATION_DIR="$SCRIPT_DIR/$VALIDATION_DIR"

# Validate inputs
[ -f "$BLUEPRINT" ] || { echo "Blueprint not found: $BLUEPRINT"; exit 1; }
[ -f "$TASK" ] || { echo "Task not found: $TASK"; exit 1; }
[ -d "$SEED_DIR" ] || { echo "Seed dir not found: $SEED_DIR"; exit 1; }

echo "=== Leviath Benchmark Runner ==="
echo "Blueprint: $BLUEPRINT"
echo "Task: $TASK"
echo "Runs: $NUM_RUNS"
echo ""

# Create workdirs and launch runs
WORKDIRS=()
RUN_IDS=()

for i in $(seq 1 "$NUM_RUNS"); do
  WORKDIR=$(mktemp -d)
  cp -r "$SEED_DIR"/* "$WORKDIR/"
  WORKDIRS+=("$WORKDIR")
  
  cd "$WORKDIR"
  OUTPUT=$(lev run "$BLUEPRINT" -t "$TASK" --yolo 2>&1)
  RUN_ID=$(echo "$OUTPUT" | grep "Started run:" | awk '{print $3}')
  RUN_IDS+=("$RUN_ID")
  
  echo "Run $i: $RUN_ID → $WORKDIR"
  sleep 2
done

echo ""
echo "=== All $NUM_RUNS runs launched ==="
echo ""
echo "Monitor with: lev dash"
echo ""
echo "When complete, score with:"
echo ""

for i in $(seq 0 $((NUM_RUNS - 1))); do
  echo "  # Run $((i + 1)): ${RUN_IDS[$i]}"
  echo "  cd ${WORKDIRS[$i]}"
  echo "  cp $VALIDATION_DIR/*.py ."
  echo "  python -m pytest test_algorithms.py test_behavioral.py -v --tb=short"
  echo ""
done

# Save run info for later scoring
RESULTS_FILE="/tmp/benchmark-runs-$(date +%s).json"
echo "{" > "$RESULTS_FILE"
echo "  \"blueprint\": \"$BLUEPRINT\"," >> "$RESULTS_FILE"
echo "  \"runs\": [" >> "$RESULTS_FILE"
for i in $(seq 0 $((NUM_RUNS - 1))); do
  COMMA=""
  [ $i -lt $((NUM_RUNS - 1)) ] && COMMA=","
  echo "    {\"id\": \"${RUN_IDS[$i]}\", \"workdir\": \"${WORKDIRS[$i]}\"}$COMMA" >> "$RESULTS_FILE"
done
echo "  ]" >> "$RESULTS_FILE"
echo "}" >> "$RESULTS_FILE"

echo "Run info saved to: $RESULTS_FILE"
