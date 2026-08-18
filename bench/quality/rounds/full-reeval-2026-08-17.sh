#!/bin/zsh
# The full re-eval on the fixed runtime: one binary (leviath main
# @3f464a5d - post #474 anchors, #486 splice, #485 calibration,
# #490 lifecycle-grows), declared blueprints throughout (volatility
# annotations incl. the #490 temporary-region grows set).
#
# Every earlier tier mixed binaries or ran on broken caching; this
# round supersedes them all as the whitepaper's counted basis.
# Sequential tiers, each budget-capped; the credit breaker turns an
# empty account into `infra` cells rather than garbage.
set -u
WT="$(cd "$(dirname "$0")/../../.." && pwd)"

# This round ran on leviath main @3f464a5d; build
# that commit (cargo build --release --bin lev) and point LEV
# at the binary to reproduce byte-for-byte.
LEV="${LEV:?set LEV to a lev binary (lev-main-3f464a5d)}"
cd "$WT" || exit 1

FLATS=flat-pinned,flat-compacting,flat-pinned-hardened,flat-compacting-hardened

# ── A: the collapse/survival headline, three window tiers, 5 reps ──
for WIN in 32000 64000 128000; do
  echo "=== A cliff ${WIN} $(date -u +%H:%M:%SZ)"
  python3 bench/quality/run_quality.py --suite hallucination \
    --arms "$FLATS,structured-mix-flagship" \
    --models "Claude Sonnet 5" --reps 5 \
    --subset bench/quality/subsets/hallucination_cliff.json \
    --window-tokens "$WIN" \
    --unsafe-smoke --budget-usd 150 --task-timeout 3600 --concurrency 3 \
    --lev "$LEV" \
    --out "results/reeval_cliff_w$((WIN / 1000))k"
  echo "A-${WIN}-EXIT=$?"
done

# ── B: the prose crossover tier, 5 reps ──
echo "=== B policy-128k $(date -u +%H:%M:%SZ)"
python3 bench/quality/run_quality.py --suite hallucination \
  --arms "$FLATS,structured-mix-flagship" \
  --models "Claude Sonnet 5" --reps 5 \
  --subset bench/quality/subsets/hallucination_policy.json \
  --window-tokens 128000 \
  --unsafe-smoke --budget-usd 150 --task-timeout 7200 --concurrency 3 \
  --lev "$LEV" \
  --out results/reeval_policy_w128k
echo "B-EXIT=$?"

# ── C: past-1M tier, both suites, 1 rep ──
echo "=== C xl $(date -u +%H:%M:%SZ)"
python3 bench/quality/run_quality.py --suite hallucination \
  --arms flat-pinned,flat-compacting,structured-mix-flagship \
  --models "Claude Sonnet 5" --reps 1 \
  --subset bench/quality/subsets/hallucination_policy_xl.json \
  --unsafe-smoke --budget-usd 80 --task-timeout 10800 --concurrency 3 \
  --lev "$LEV" \
  --out results/reeval_policy_xl
echo "C1-EXIT=$?"
python3 bench/quality/run_quality.py --suite retention \
  --arms flat-pinned,flat-compacting,structured-mix-flagship \
  --models "Claude Sonnet 5" --reps 1 \
  --subset bench/quality/subsets/retention_xl.json \
  --unsafe-smoke --budget-usd 90 --task-timeout 10800 --concurrency 3 \
  --lev "$LEV" \
  --out results/reeval_retention_xl
echo "C2-EXIT=$?"

# ── D: retention r1 on Sonnet, then the free local pass ──
echo "=== D retention $(date -u +%H:%M:%SZ)"
python3 bench/quality/run_quality.py --suite retention \
  --arms flat-pinned,flat-compacting,structured-mix-flagship \
  --models "Claude Sonnet 5" --reps 1 \
  --subset bench/quality/subsets/retention_r1.json \
  --unsafe-smoke --budget-usd 60 --task-timeout 7200 --concurrency 3 \
  --lev "$LEV" \
  --out results/reeval_retention
echo "D1-EXIT=$?"
python3 bench/quality/run_quality.py --suite retention \
  --arms flat-pinned,structured-pinned --models "Qwen 3.8 Local" --reps 1 \
  --subset bench/quality/subsets/retention_r1.json \
  --unsafe-smoke --task-timeout 4500 --concurrency 1 \
  --home /tmp/levqual-reeval-local --lev "$LEV" \
  --out results/reeval_retention_qwen
echo "D2-EXIT=$?"

# ── E: footprint economics, uniform binary ──
echo "=== E footprint $(date -u +%H:%M:%SZ)"
python3 bench/quality/run_quality.py --suite footprint \
  --arms flat-pinned,flat-compacting,structured-pinned,structured-mix-flagship \
  --models "Claude Sonnet 5" --reps 1 \
  --unsafe-smoke --budget-usd 60 --task-timeout 7200 --concurrency 3 \
  --lev "$LEV" \
  --out results/reeval_footprint
echo "E-EXIT=$?"
echo "REEVAL-DONE $(date -u +%H:%M:%SZ)"
