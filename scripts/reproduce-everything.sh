#!/bin/bash
# Reproduce a published round's numbers and charts from committed data.
# Usage: scripts/reproduce-everything.sh <freeze-tag>
#
# This does NOT re-run agents (that reproduces the protocol, not the numbers —
# see METHODOLOGY.md). It verifies the committed raw runs deterministically
# regenerate the aggregate and the charts.

set -euo pipefail
TAG="${1:?usage: scripts/reproduce-everything.sh <freeze-tag>}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ROUND="$ROOT/results/rounds/$TAG"

[[ -d "$ROUND/runs" ]] || { echo "no committed runs at $ROUND/runs"; exit 1; }
git -C "$ROOT" rev-parse -q --verify "refs/tags/$TAG" >/dev/null \
  || { echo "freeze tag '$TAG' not found"; exit 1; }

python3 "$ROOT/scripts/aggregate-results.py" "$ROUND"
python3 "$ROOT/charts/generate.py" "$ROUND"

echo
echo "Aggregate + charts regenerated from committed runs for '$TAG'."
echo "Diff against the published artifacts to verify byte-comparable output:"
echo "  git -C '$ROOT' diff -- results/rounds/$TAG charts/output"
