#!/bin/zsh
# Round 1 of the 128k iteration (flagship arm ONLY, per spend controls):
# v2.2 blueprints = verify triage + stage-owned evidence + format-true
# drafts. Target: chronicle/noisy 128k at or above the 64k bar
# (0.88-1.0 / 1.0), policy recovered to v1 levels or better.
set -u
WT="$(cd "$(dirname "$0")/../../.." && pwd)"

# This round ran on leviath main @0a157925; build
# that commit (cargo build --release --bin lev) and point LEV
# at the binary to reproduce byte-for-byte.
LEV="${LEV:?set LEV to a lev binary (lev-main-0a157925)}"
cd "$WT" || exit 1

echo "=== R1 cliff-128k $(date -u +%H:%M:%SZ)"
python3 bench/quality/run_quality.py --suite hallucination \
  --arms structured-mix-flagship --models "Claude Sonnet 5" --reps 5 \
  --subset bench/quality/subsets/hallucination_cliff.json \
  --window-tokens 128000 \
  --unsafe-smoke --budget-usd 90 --task-timeout 3600 --concurrency 3 \
  --lev "$LEV" --out results/v22_cliff_w128k
echo "R1A-EXIT=$?"

echo "=== R1 policy-128k $(date -u +%H:%M:%SZ)"
python3 bench/quality/run_quality.py --suite hallucination \
  --arms structured-mix-flagship --models "Claude Sonnet 5" --reps 5 \
  --subset bench/quality/subsets/hallucination_policy.json \
  --window-tokens 128000 \
  --unsafe-smoke --budget-usd 40 --task-timeout 7200 --concurrency 3 \
  --lev "$LEV" --out results/v22_policy_w128k
echo "R1B-EXIT=$?"

echo "=== R1 policy-xl $(date -u +%H:%M:%SZ)"
python3 bench/quality/run_quality.py --suite hallucination \
  --arms structured-mix-flagship --models "Claude Sonnet 5" --reps 1 \
  --subset bench/quality/subsets/hallucination_policy_xl.json \
  --unsafe-smoke --budget-usd 30 --task-timeout 10800 --concurrency 1 \
  --lev "$LEV" --out results/v22_policy_xl
echo "R1C-EXIT=$?"
echo "R1-DONE $(date -u +%H:%M:%SZ)"
