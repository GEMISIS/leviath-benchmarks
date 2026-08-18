#!/bin/zsh
# The white-paper round, uniform binary: leviath main (post-#455/#456
# fixes), all three tiers, 5 reps. The 0.3.10-stable 32k tier stays
# archived as a cross-version comparison point.
set -u
WT="$(cd "$(dirname "$0")/../../.." && pwd)"
# This round ran on leviath main @94b5a5e4; build that commit
# (cargo build --release --bin lev) and point LEV at the binary to
# reproduce byte-for-byte.
LEV="${LEV:?set LEV to a lev binary (lev-main-94b5a5e4)}"
cd "$WT" || exit 1

for WIN in 64000 128000; do
  echo "=== paper2 tier ${WIN} $(date -u +%H:%M:%SZ)"
  python3 bench/quality/run_quality.py --suite hallucination \
    --arms flat-pinned,flat-compacting,flat-pinned-hardened,flat-compacting-hardened,structured-mix-flagship \
    --models "Claude Sonnet 5" --reps 5 \
    --subset bench/quality/subsets/hallucination_cliff.json \
    --window-tokens "$WIN" \
    --unsafe-smoke --budget-usd 200 --task-timeout 3600 \
    --concurrency 3 --lev "$LEV" \
    --out "results/paper2_w$((WIN / 1000))k"
  echo "PAPER2-TIER-${WIN}-EXIT=$?"
done
echo "PAPER2-DONE $(date -u +%H:%M:%SZ)"
