#!/bin/zsh
# Hallucination suite window sweep: 64k, 128k, 256k (the 32k tier
# already ran). Same arms, same tasks (incl. reworked redacted-ledger,
# whose 32k tier gets re-run first so every tier uses the same task).
set -u
WT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$WT" || exit 1

run_tier() {
  local WIN=$1 OUT=$2 SUBSET=$3
  echo "=== tier ${WIN} -> ${OUT} $(date -u +%H:%M:%SZ)"
  python3 bench/quality/run_quality.py --suite hallucination \
    --arms flat-pinned,flat-compacting,structured-mix-flagship \
    --models "Claude Sonnet 5" --reps 1 \
    --subset "$SUBSET" \
    --window-tokens "$WIN" \
    --unsafe-smoke --budget-usd 100 --task-timeout 3600 \
    --concurrency 2 \
    --out "$OUT"
  echo "TIER-${WIN}-EXIT=$?"
}
# per-run cap left at the new 30M default: a runaway backstop, not a
# working limit - Gerald wants runs finishing on their own budgets.

run_tier 64000  results/hallucination_w64 \
  bench/quality/subsets/hallucination_r1.json
run_tier 128000 results/hallucination_w128 \
  bench/quality/subsets/hallucination_r1.json
run_tier 256000 results/hallucination_w256 \
  bench/quality/subsets/hallucination_r1.json
echo "SWEEP-DONE $(date -u +%H:%M:%SZ)"
