#!/bin/zsh
# The v2-flagship re-run: only the cells the loganalyzer surgery touches.
# v2 = script stage folded into analyze, verify (fact-check) stage added
# between report and summary with the draft gated in `report_draft`,
# findings budget floored along the main path, ingest->analyze compacted.
# Flat arms are byte-identical to the main round (readonly flats differ
# only in a never-binding iteration cap), so their tier A-E results
# stand; these runs replace the flagship column for loganalyzer tasks,
# and the v1 flagship results are kept as the design-fix "before" arm.
set -u
WT=/Users/gemisis/Documents/projects/ai/personal/leviath-benchmarks/.claude/worktrees/benchmark-improvements
SCRATCH=/private/tmp/claude-501/-Users-gemisis-Documents-projects-ai-personal-leviath-benchmarks/fb0825da-4d64-4e27-8389-bb3cb410600e/scratchpad
LEV=$SCRATCH/lev-main-3f464a5d
cd "$WT" || exit 1

for WIN in 32000 64000 128000; do
  echo "=== V2A cliff ${WIN} $(date -u +%H:%M:%SZ)"
  python3 bench/quality/run_quality.py --suite hallucination \
    --arms structured-mix-flagship \
    --models "Claude Sonnet 5" --reps 5 \
    --subset bench/quality/subsets/hallucination_cliff.json \
    --window-tokens "$WIN" \
    --unsafe-smoke --budget-usd 60 --task-timeout 3600 --concurrency 3 \
    --lev "$LEV" \
    --out "results/v2_cliff_w$((WIN / 1000))k"
  echo "V2A-${WIN}-EXIT=$?"
done

echo "=== V2B policy-128k $(date -u +%H:%M:%SZ)"
python3 bench/quality/run_quality.py --suite hallucination \
  --arms structured-mix-flagship \
  --models "Claude Sonnet 5" --reps 5 \
  --subset bench/quality/subsets/hallucination_policy.json \
  --window-tokens 128000 \
  --unsafe-smoke --budget-usd 60 --task-timeout 7200 --concurrency 3 \
  --lev "$LEV" \
  --out results/v2_policy_w128k
echo "V2B-EXIT=$?"

echo "=== V2C policy-xl $(date -u +%H:%M:%SZ)"
python3 bench/quality/run_quality.py --suite hallucination \
  --arms structured-mix-flagship \
  --models "Claude Sonnet 5" --reps 1 \
  --subset bench/quality/subsets/hallucination_policy_xl.json \
  --unsafe-smoke --budget-usd 30 --task-timeout 10800 --concurrency 1 \
  --lev "$LEV" \
  --out results/v2_policy_xl
echo "V2C-EXIT=$?"

echo "=== V2D live-service $(date -u +%H:%M:%SZ)"
python3 bench/quality/run_quality.py --suite retention \
  --arms structured-mix-flagship \
  --models "Claude Sonnet 5" --reps 1 \
  --subset bench/quality/subsets/retention_liveservice.json \
  --unsafe-smoke --budget-usd 40 --task-timeout 7200 --concurrency 1 \
  --lev "$LEV" \
  --out results/v2_live_service
echo "V2D-EXIT=$?"

echo "=== V2E footprint log-search $(date -u +%H:%M:%SZ)"
python3 bench/quality/run_quality.py --suite footprint \
  --arms structured-pinned,structured-mix-flagship \
  --models "Claude Sonnet 5" --reps 1 \
  --subset bench/quality/subsets/footprint_logsearch.json \
  --unsafe-smoke --budget-usd 20 --task-timeout 7200 --concurrency 2 \
  --lev "$LEV" \
  --out results/v2_footprint_logsearch
echo "V2E-EXIT=$?"
echo "V2-RERUN-DONE $(date -u +%H:%M:%SZ)"
