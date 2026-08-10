#!/usr/bin/env bash
# One-time setup for the benchmarks.
#
# Everything here is idempotent and re-runnable: it installs Python
# dependencies, fetches the suite datasets that the quality track needs,
# and - with --coding - builds the static Linux binary and harness venv
# the container-hosted coding suites need.
#
# Nothing downloads implicitly at run time. If a suite's data is missing
# the runner fails and tells you to run this; it never fetches behind
# your back mid-round, because a round that half-downloads is a round
# whose inputs nobody can reconstruct.
#
#   ./bench/setup.sh              deps + free suites (log analysis, DABstep)
#   ./bench/setup.sh --gaia       also fetch GAIA (needs HF_TOKEN, gated)
#   ./bench/setup.sh --coding     also prepare the container coding suites
#   ./bench/setup.sh --all        everything
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

WANT_GAIA=0
WANT_CODING=0
for arg in "$@"; do
  case "$arg" in
    --gaia)   WANT_GAIA=1 ;;
    --coding) WANT_CODING=1 ;;
    --all)    WANT_GAIA=1; WANT_CODING=1 ;;
    -h|--help) sed -n '2,17p' "$0"; exit 0 ;;
    *) echo "unknown option: $arg (try --help)" >&2; exit 2 ;;
  esac
done

say() { printf '\n=== %s\n' "$1"; }

say "Python dependencies"
python3 -m pip install --quiet --upgrade psutil matplotlib

say "leviath"
if command -v lev >/dev/null 2>&1; then
  echo "    $(command -v lev) - $(lev --version 2>/dev/null | head -1)"
else
  echo "    lev is not on PATH. Install it from"
  echo "    https://github.com/GEMISIS/leviath#installation, or pass"
  echo "    --lev /path/to/lev to the runners. The performance track"
  echo "    needs it; the quality track needs it too."
fi

say "API keys"
if [ -f .env ]; then
  echo "    .env present (never read by this script, never written to results)"
else
  cp .env.example .env
  echo "    wrote .env from .env.example - fill in the keys you need"
fi

say "Datasets: log analysis (generated, offline)"
python3 bench/quality/suites/loganalysis/datasets.py fetch

say "Datasets: DABstep"
python3 bench/quality/suites/dabstep/datasets.py fetch

if [ "$WANT_GAIA" = 1 ]; then
  say "Datasets: GAIA (gated - needs HF_TOKEN in the environment)"
  python3 bench/quality/suites/gaia/datasets.py fetch
else
  echo "    (skipping GAIA - it is HF-gated; re-run with --gaia)"
fi

if [ "$WANT_CODING" = 1 ]; then
  say "Container coding suites"
  if ! docker info >/dev/null 2>&1; then
    echo "    Docker is not running - start it and re-run with --coding." >&2
    exit 1
  fi

  VENV="$REPO/.harness"
  if [ ! -x "$VENV/bin/harbor" ]; then
    echo "    harness venv -> .harness"
    python3 -m venv "$VENV"
    "$VENV/bin/pip" install --quiet --upgrade pip
    "$VENV/bin/pip" install --quiet harbor
  fi
  echo "    harbor $("$VENV/bin/harbor" --version 2>/dev/null | tail -1)"

  # A statically linked binary, because the task images are not ours and
  # a glibc build dies with rc=127 the moment one ships a different libc.
  OUT="$REPO/.lev-linux"
  if [ ! -x "$OUT/release/lev" ]; then
    LEV_SRC="${LEVIATH_SRC:-$REPO/../leviath}"
    if [ ! -d "$LEV_SRC" ]; then
      echo "    leviath source not found at $LEV_SRC." >&2
      echo "    Set LEVIATH_SRC=/path/to/leviath and re-run." >&2
      exit 1
    fi
    echo "    building static lev from $LEV_SRC (a few minutes)"
    mkdir -p "$OUT"
    docker run --rm \
      -v "$LEV_SRC":/src:ro -v "$OUT":/out \
      -w /src -e CARGO_TARGET_DIR=/out rust:1-alpine \
      sh -c 'apk add --no-cache musl-dev pkgconfig perl make cmake g++ >/dev/null && \
             cargo build --release --locked -p leviath-cli'
  fi
  echo "    static lev -> $OUT/release/lev"

  TASKS="$REPO/.tasks"
  if [ ! -d "$TASKS/terminal-bench" ]; then
    echo "    downloading terminal-bench tasks"
    "$VENV/bin/harbor" download "terminal-bench@2.0" -o "$TASKS"
  fi
  echo "    tasks -> $TASKS"
fi

say "Ready"
cat <<'EOF'
    performance:  python3 bench/run_benchmarks.py
    quality:      python3 bench/quality/run_quality.py --suite dabstep \
                      --arms flat-pinned,structured-mix-flagship \
                      --models "Claude Opus 5" --reps 1 --unsafe-smoke
    tests:        python3 bench/quality/tests/test_quality.py
EOF
