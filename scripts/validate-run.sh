#!/bin/bash
# Score one benchmark run against a task's held-out suite and write the
# machine-readable run record for the round.
#
# Usage: validate-run.sh <workdir> <approach> <run_number> <meta_json> <freeze_tag> [task]
#   approach:   structured | flat (the arm label used by the aggregator)
#   meta_json:  ~/.leviath/runs/<run-id>/meta.json for the finished run
#   freeze_tag: the round's git tag; the record is refused by the aggregator
#               if it doesn't match the round directory
#   task:       task directory under tasks/ (default: stress-test)
#
# Note on token semantics: leviath's meta.json maps prompt_tokens from the
# API's input_tokens (which EXCLUDES cache reads/writes), cached_tokens from
# cache_read_input_tokens, and cache_write_tokens from
# cache_creation_input_tokens — see leviath crates/leviath-providers/src/
# anthropic.rs. Both arms are the same runtime, so usage numerators are
# comparable by construction. Costs are NOT computed here; the aggregator
# derives them via scripts/cost.py from the round's pinned rates.
set -euo pipefail

WORKDIR="${1:?usage: validate-run.sh <workdir> <approach> <run#> <meta.json> <freeze-tag> [task]}"
APPROACH="${2:?missing approach}"
RUN_NUM="${3:?missing run number}"
META_JSON="${4:?missing meta.json path (usage fields are required)}"
FREEZE_TAG="${5:?missing freeze tag}"
TASK="${6:-stress-test}"

BENCH_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS_DIR="$BENCH_ROOT/results/rounds/$FREEZE_TAG/runs"
mkdir -p "$RESULTS_DIR"

echo "=== Scoring $APPROACH run $RUN_NUM (task=$TASK, round=$FREEZE_TAG) ==="

cp -r "$BENCH_ROOT/tasks/$TASK/validation" "$WORKDIR/"
SUITE_HASH=$(git -C "$BENCH_ROOT" rev-parse "HEAD:tasks/$TASK/validation" 2>/dev/null || echo unknown)

cd "$WORKDIR"
python3 -m venv .venv 2>/dev/null || true
source .venv/bin/activate
pip install -r validation/requirements.txt -q 2>&1 | tail -1
[ -f requirements.txt ] && pip install -r requirements.txt -q 2>&1 | tail -1

python3 -m pytest validation/ -v --tb=line --json-report --json-report-file=/tmp/pytest-report.json 2>&1 | tail -5

RESULTS_DIR="$RESULTS_DIR" META_JSON="$META_JSON" APPROACH="$APPROACH" \
RUN_NUM="$RUN_NUM" FREEZE_TAG="$FREEZE_TAG" TASK="$TASK" SUITE_HASH="$SUITE_HASH" \
python3 <<'PYEOF'
import json
import os
import sys

report = json.load(open('/tmp/pytest-report.json'))
passed = report['summary'].get('passed', 0)
failed = report['summary'].get('failed', 0)
errors = report['summary'].get('error', 0)
total = passed + failed + errors
if total == 0:
    sys.exit("no tests ran — refusing to write a run record")
failures = [t['nodeid'].split('::')[-1] for t in report.get('tests', [])
            if t['outcome'] == 'failed']

meta = json.load(open(os.environ['META_JSON']))
for field in ('prompt_tokens', 'completion_tokens'):
    if field not in meta:
        sys.exit(f"meta.json missing {field} — cannot record billed usage")

result = {
    "run": int(os.environ['RUN_NUM']),
    "approach": os.environ['APPROACH'],
    "freeze_tag": os.environ['FREEZE_TAG'],
    "task": os.environ['TASK'],
    "suite_git_hash": os.environ['SUITE_HASH'],
    "model": meta.get("model"),
    "blueprint": meta.get("agent_name"),
    "duration_seconds": meta.get("duration_seconds", 0)
        or int(meta.get("updated_at", 0) - meta.get("started_at", 0)),
    "tool_calls": meta.get("tool_calls", 0),
    "usage": {
        "input_tokens": meta["prompt_tokens"],
        "output_tokens": meta["completion_tokens"],
        "cache_read_input_tokens": meta.get("cached_tokens", 0),
        "cache_creation_input_tokens": meta.get("cache_write_tokens", 0),
    },
    "passed": passed,
    "failed": failed,
    "total": total,
    "pass_rate": round(passed / total * 100, 2),
    "failures": failures,
}

outpath = os.path.join(os.environ['RESULTS_DIR'],
                       f"{os.environ['APPROACH']}-run{os.environ['RUN_NUM']}.json")
with open(outpath, 'w') as f:
    json.dump(result, f, indent=2)
print(f"\n{result['approach']} run {result['run']}: "
      f"{passed}/{total} ({result['pass_rate']}%) -> {outpath}")
PYEOF
