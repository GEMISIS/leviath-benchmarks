#!/bin/bash
# Preflight for a benchmark round — run this BEFORE burning API money.
# Usage: scripts/preflight.sh <freeze-tag>
# Verifies: binaries, credentials, python scoring deps, blueprint validity,
# and that the round is properly frozen (tag exists, rates.json pinned).

set -uo pipefail
TAG="${1:?usage: scripts/preflight.sh <freeze-tag>}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FAIL=0
say() { printf '%-60s %s\n' "$1" "$2"; }
check() { if eval "$2" >/dev/null 2>&1; then say "$1" "ok"; else say "$1" "FAIL"; FAIL=1; fi; }

LEV_BIN="${LEV_BIN:-$(command -v lev 2>/dev/null || echo "$HOME/.cargo/bin/lev")}"
check "lev binary ($LEV_BIN)" "[[ -x '$LEV_BIN' ]]"
check "python3" "command -v python3"
check "Anthropic credentials (env or ~/.leviath/config.toml)" \
  "[[ -n \"\${ANTHROPIC_API_KEY:-}\" ]] || grep -q anthropic ~/.leviath/config.toml"

check "freeze tag '$TAG' exists in this repo" "git -C '$ROOT' rev-parse -q --verify 'refs/tags/$TAG'"
check "working tree clean at freeze tag" \
  "[[ -z \"\$(git -C '$ROOT' status --porcelain -- tasks blueprints scripts)\" ]]"
check "round dir + pinned rates (results/rounds/$TAG/rates.json)" \
  "python3 '$ROOT/scripts/cost.py' 2>/dev/null; [[ -f '$ROOT/results/rounds/$TAG/rates.json' ]]"

check "blueprint: structured arm validates (engineer-v3)" "'$LEV_BIN' validate '$ROOT/blueprints/engineer-v3'"
check "blueprint: flat-mode validates" "'$LEV_BIN' validate '$ROOT/blueprints/flat-mode'"

# Scoring deps install into a throwaway venv — this is what caught fire last
# time (a typo'd package name meant pytest-json-report silently never
# installed and every score came back "pytest report not generated").
VENVDIR=$(mktemp -d)
if python3 -m venv "$VENVDIR/venv" >/dev/null 2>&1 \
   && "$VENVDIR/venv/bin/pip" install -q -r "$ROOT/tasks/stress-test/validation/requirements.txt" >/dev/null 2>&1 \
   && "$VENVDIR/venv/bin/python" -c "import pytest_jsonreport" >/dev/null 2>&1; then
  say "scoring deps install cleanly (incl. pytest-json-report)" "ok"
else
  say "scoring deps install cleanly (incl. pytest-json-report)" "FAIL"; FAIL=1
fi
rm -rf "$VENVDIR"

if [[ $FAIL -ne 0 ]]; then echo; echo "PREFLIGHT FAILED — fix before running."; exit 1; fi
echo; echo "Preflight clean for round '$TAG'."
