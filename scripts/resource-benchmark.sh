#!/bin/bash
# Absolute resource-footprint benchmark: one `lev serve` daemon hosting N
# concurrent agents doing REAL inference.
#
# This intentionally measures Leviath ONLY — no competitor tools. The July
# 2026 cross-tool comparison was withdrawn (see results/archive-2026-07/):
# its Leviath side used dry_run (no inference) and its published JSON was
# hand-curated. This script instead:
#   - runs a real blueprint on a real task for every agent (costs real API
#     money — keep BLUEPRINT/TASK cheap),
#   - emits the EXACT file that gets published, byte-for-byte, including the
#     method parameters actually used,
#   - marks a concurrency level "valid": false unless every agent spawned and
#     none was in a failed state at measurement end.
#
# Usage:
#   LEVIATH_API_TOKEN=... ./scripts/resource-benchmark.sh
# Env overrides:
#   AGENT_COUNTS="1 10 25 50"  BLUEPRINT=simple-coder  WARMUP_SECONDS=8
#   MEASURE_SECONDS=15  TASK="..."  OUTPUT=results/rounds/<tag>/resource.json

set -euo pipefail

AGENT_COUNTS=(${AGENT_COUNTS:-1 10 25 50})
WARMUP_SECONDS=${WARMUP_SECONDS:-8}
MEASURE_SECONDS=${MEASURE_SECONDS:-15}
SAMPLE_INTERVAL=1
BLUEPRINT=${BLUEPRINT:-simple-coder}
TASK=${TASK:-"Write a Python function that returns the nth Fibonacci number iteratively, plus a short test."}
LEV_BIN="${LEV_BIN:-$(command -v lev 2>/dev/null || echo "$HOME/.cargo/bin/lev")}"
LEV_PORT=${LEV_PORT:-3998}
OUTPUT="${OUTPUT:-$(dirname "$0")/../results/resource-footprint.json}"
: "${LEVIATH_API_TOKEN:?set LEVIATH_API_TOKEN (lev serve refuses to start without one)}"

log() { echo "$(date '+%H:%M:%S') $*"; }

get_rss_kb() {
    local pid=$1 total=0 rss child
    rss=$(ps -o rss= -p "$pid" 2>/dev/null | tr -d ' ') || true
    [[ -n "${rss:-}" && "$rss" -gt 0 ]] && total=$((total + rss))
    for child in $(pgrep -P "$pid" 2>/dev/null); do
        total=$((total + $(get_rss_kb "$child")))
    done
    echo "$total"
}

api() {
    curl -sf -H "Authorization: Bearer $LEVIATH_API_TOKEN" "$@"
}

[[ -x "$LEV_BIN" ]] || { log "ERROR: lev not found at $LEV_BIN"; exit 1; }

WORKROOT=$(mktemp -d)
SERIES_TMP=$(mktemp)
LEV_VERSION=$("$LEV_BIN" --version 2>/dev/null | tail -1)

log "Starting lev serve on port $LEV_PORT ($LEV_VERSION)"
"$LEV_BIN" serve --port "$LEV_PORT" >/dev/null 2>&1 &
LEV_PID=$!
trap 'kill "$LEV_PID" 2>/dev/null || true; rm -rf "$WORKROOT" "$SERIES_TMP"' EXIT
sleep 3
kill -0 "$LEV_PID" 2>/dev/null || { log "ERROR: lev serve failed to start"; exit 1; }

first=1
for n in "${AGENT_COUNTS[@]}"; do
    log "$n concurrent agents (blueprint=$BLUEPRINT, real inference)..."
    ids=()
    for ((i=1; i<=n; i++)); do
        wd="$WORKROOT/n$n-agent$i"; mkdir -p "$wd"
        id=$(api -X POST "http://127.0.0.1:$LEV_PORT/api/agents" \
            -H "Content-Type: application/json" \
            -d "{\"blueprint\": \"$BLUEPRINT\", \"task\": \"$TASK\", \"workdir\": \"$wd\"}" \
            | python3 -c 'import json,sys; print(json.load(sys.stdin).get("id",""))') || id=""
        [[ -n "$id" ]] && ids+=("$id") || log "  WARN: spawn $i failed"
    done

    sleep "$WARMUP_SECONDS"
    peak=0
    for ((s=0; s<MEASURE_SECONDS; s+=SAMPLE_INTERVAL)); do
        rss=$(get_rss_kb "$LEV_PID")
        (( rss > peak )) && peak=$rss
        sleep "$SAMPLE_INTERVAL"
    done

    # A level only counts if every agent spawned AND none is in a failed state.
    failed=$(api "http://127.0.0.1:$LEV_PORT/api/agents" \
        | python3 -c 'import json,sys; a=json.load(sys.stdin); l=a if isinstance(a,list) else a.get("agents",[]); print(sum(1 for x in l if str(x.get("status","")).lower() in ("failed","error")))' \
        2>/dev/null || echo "-1")
    valid=true
    [[ ${#ids[@]} -ne $n || "$failed" != "0" ]] && valid=false
    log "  peak RSS $((peak / 1024)) MB, spawned ${#ids[@]}/$n, failed=$failed, valid=$valid"

    [[ $first -eq 0 ]] && echo "," >> "$SERIES_TMP"; first=0
    printf '    {"agents": %d, "spawned": %d, "failed_agents": %s, "peak_rss_kb": %d, "peak_rss_mb": %d, "valid": %s}' \
        "$n" "${#ids[@]}" "$failed" "$peak" "$((peak / 1024))" "$valid" >> "$SERIES_TMP"

    # Cancel whatever is still running before the next level.
    for id in "${ids[@]}"; do
        api -X DELETE "http://127.0.0.1:$LEV_PORT/api/agents/$id" >/dev/null 2>&1 || true
    done
    sleep 2
done

mkdir -p "$(dirname "$OUTPUT")"
{
  echo "{"
  echo "  \"benchmark\": \"resource-footprint\","
  echo "  \"date\": \"$(date -u '+%Y-%m-%dT%H:%M:%SZ')\","
  echo "  \"tool\": {\"name\": \"leviath\", \"version\": \"$LEV_VERSION\", \"binary\": \"$LEV_BIN\"},"
  echo "  \"system\": {\"os\": \"$(sw_vers -productName 2>/dev/null || uname -s) $(sw_vers -productVersion 2>/dev/null || uname -r)\", \"arch\": \"$(uname -m)\", \"cpu\": \"$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo unknown)\", \"ram_gb\": $((($(sysctl -n hw.memsize 2>/dev/null || echo 0)) / 1073741824))},"
  echo "  \"method\": {\"real_inference\": true, \"blueprint\": \"$BLUEPRINT\", \"task\": \"$TASK\", \"warmup_seconds\": $WARMUP_SECONDS, \"measure_seconds\": $MEASURE_SECONDS, \"sample_interval_seconds\": $SAMPLE_INTERVAL, \"rss\": \"sum of lev serve process tree (ps -o rss + descendants), peak of per-second samples\"},"
  echo "  \"series\": ["
  cat "$SERIES_TMP"; echo
  echo "  ]"
  echo "}"
} > "$OUTPUT"
python3 -c "import json; json.load(open('$OUTPUT'))" || { log "ERROR: emitted invalid JSON"; exit 1; }
log "wrote $OUTPUT — publish this file verbatim; never hand-edit it."
