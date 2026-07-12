#!/bin/bash
# Resource Footprint Benchmark: Leviath ECS vs Process-per-Agent
#
# Measures peak Device RAM (RSS) and CPU% for each tool at varying concurrency levels.
# Designed to stay under 2GB total for Leviath side, safe for 8GB+ systems.
#
# Usage: ./scripts/resource-benchmark.sh [--max-agents N] [--duration S] [--output DIR]

set -euo pipefail

# ============================================================
# Configuration
# ============================================================
MAX_AGENTS=${MAX_AGENTS:-20}
SAMPLE_INTERVAL=1          # seconds between RSS samples
WARMUP_SECONDS=3           # let process stabilize before measuring
MEASURE_SECONDS=${MEASURE_SECONDS:-15}  # how long to sample at each level
OUTPUT_DIR="${OUTPUT_DIR:-$(dirname "$0")/../results/resource}"

# Agent counts to test
AGENT_COUNTS=(1 2 5 10 20)

# Tools to benchmark (will skip if not installed)
declare -A TOOL_CMDS
TOOL_CMDS[claude]="claude --print -p 'Write a Python function that calculates fibonacci numbers recursively and iteratively, with memoization. Include comprehensive tests.' --permission-mode bypassPermissions"
TOOL_CMDS[codex]="codex exec 'Write a Python function that calculates fibonacci numbers recursively and iteratively, with memoization. Include comprehensive tests.'"
TOOL_CMDS[pi]="pi -p 'Write a Python function that calculates fibonacci numbers recursively and iteratively, with memoization. Include comprehensive tests.'"
TOOL_CMDS[opencode]="opencode --non-interactive 'Write a Python function that calculates fibonacci numbers recursively and iteratively, with memoization. Include comprehensive tests.'"

LEV_BIN="${LEV_BIN:-$HOME/dev/leviath/target/release/lev}"
LEV_PORT=3998

mkdir -p "$OUTPUT_DIR"

# ============================================================
# Helpers
# ============================================================
timestamp() { date '+%H:%M:%S'; }

log() { echo "$(timestamp) $*"; }

get_rss_kb() {
    # Get RSS in KB for a PID and all its children
    local pid=$1
    local total=0
    
    # Get the process itself
    local rss=$(ps -o rss= -p "$pid" 2>/dev/null | tr -d ' ')
    if [[ -n "$rss" && "$rss" -gt 0 ]]; then
        total=$((total + rss))
    fi
    
    # Get all descendants
    for child in $(pgrep -P "$pid" 2>/dev/null); do
        local child_rss=$(get_rss_kb "$child")
        total=$((total + child_rss))
    done
    
    echo "$total"
}

get_cpu_percent() {
    local pid=$1
    ps -o %cpu= -p "$pid" 2>/dev/null | tr -d ' ' || echo "0"
}

sample_process() {
    # Sample RSS and CPU for a PID over MEASURE_SECONDS, return peak RSS (KB) and avg CPU%
    local pid=$1
    local peak_rss=0
    local cpu_sum=0
    local samples=0
    
    for ((i=0; i<MEASURE_SECONDS; i++)); do
        if ! kill -0 "$pid" 2>/dev/null; then break; fi
        
        local rss=$(get_rss_kb "$pid")
        local cpu=$(get_cpu_percent "$pid")
        
        if [[ "$rss" -gt "$peak_rss" ]]; then
            peak_rss=$rss
        fi
        cpu_sum=$(echo "$cpu_sum + $cpu" | bc 2>/dev/null || echo "$cpu_sum")
        samples=$((samples + 1))
        
        sleep "$SAMPLE_INTERVAL"
    done
    
    local avg_cpu=0
    if [[ "$samples" -gt 0 ]]; then
        avg_cpu=$(echo "scale=1; $cpu_sum / $samples" | bc 2>/dev/null || echo "0")
    fi
    
    echo "$peak_rss $avg_cpu"
}

cleanup_pids() {
    for pid in "$@"; do
        kill "$pid" 2>/dev/null || true
        wait "$pid" 2>/dev/null || true
    done
}

# ============================================================
# System Info
# ============================================================
SYSTEM_RAM_BYTES=$(/usr/sbin/sysctl -n hw.memsize 2>/dev/null || echo 0)
SYSTEM_RAM_GB=$(echo "scale=0; $SYSTEM_RAM_BYTES / 1073741824" | bc)
CPU_MODEL=$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo "unknown")
OS_VERSION=$(sw_vers -productVersion 2>/dev/null || echo "unknown")

log "Resource Footprint Benchmark"
log "System: ${SYSTEM_RAM_GB} GB RAM, ${CPU_MODEL}"
log "OS: macOS ${OS_VERSION}"
log "Max agents: ${MAX_AGENTS}, Sample interval: ${SAMPLE_INTERVAL}s, Measure duration: ${MEASURE_SECONDS}s"
log ""

# ============================================================
# Phase 1: Leviath ECS Benchmark
# ============================================================
log "=== Phase 1: Leviath ECS Engine ==="

# Start lev serve
cd /tmp
"$LEV_BIN" serve --port "$LEV_PORT" > /tmp/lev-resource-bench.log 2>&1 &
LEV_PID=$!
sleep "$WARMUP_SECONDS"

if ! kill -0 "$LEV_PID" 2>/dev/null; then
    log "ERROR: lev serve failed to start"
    cat /tmp/lev-resource-bench.log
    exit 1
fi

LEV_RESULTS="$OUTPUT_DIR/leviath-results.json"
echo '{"tool": "leviath", "type": "ecs", "measurements": [' > "$LEV_RESULTS"

# Measure baseline (0 agents)
log "  Baseline (0 agents)..."
sleep 2
read -r base_rss base_cpu <<< $(sample_process "$LEV_PID")
log "    RSS: $((base_rss / 1024)) MB, CPU: ${base_cpu}%"
echo "  {\"agents\": 0, \"peak_rss_kb\": $base_rss, \"avg_cpu_pct\": $base_cpu}," >> "$LEV_RESULTS"

# For each concurrency level, submit tasks via API
for n in "${AGENT_COUNTS[@]}"; do
    if [[ "$n" -gt "$MAX_AGENTS" ]]; then continue; fi
    
    log "  $n concurrent agents..."
    
    # Submit n tasks via lev API (these are lightweight — they just create ECS entities)
    for ((i=1; i<=n; i++)); do
        curl -s -X POST "http://127.0.0.1:$LEV_PORT/api/v1/runs" \
            -H "Content-Type: application/json" \
            -d "{\"task\": \"Write fibonacci function $i\", \"blueprint\": \"simple-coder\", \"dry_run\": true}" \
            > /dev/null 2>&1 || true
    done
    
    sleep 2
    read -r peak_rss avg_cpu <<< $(sample_process "$LEV_PID")
    log "    RSS: $((peak_rss / 1024)) MB, CPU: ${avg_cpu}%"
    
    # Add comma handling
    if [[ "$n" -eq "${AGENT_COUNTS[-1]}" ]]; then
        echo "  {\"agents\": $n, \"peak_rss_kb\": $peak_rss, \"avg_cpu_pct\": $avg_cpu}" >> "$LEV_RESULTS"
    else
        echo "  {\"agents\": $n, \"peak_rss_kb\": $peak_rss, \"avg_cpu_pct\": $avg_cpu}," >> "$LEV_RESULTS"
    fi
done

echo "]}" >> "$LEV_RESULTS"
kill "$LEV_PID" 2>/dev/null; wait "$LEV_PID" 2>/dev/null || true
log "  Leviath done."
log ""

# ============================================================
# Phase 2: Process-per-Agent Tools
# ============================================================
log "=== Phase 2: Process-per-Agent Tools ==="

for tool_name in claude codex pi opencode; do
    tool_path=$(which "$tool_name" 2>/dev/null || echo "")
    if [[ -z "$tool_path" ]]; then
        log "  $tool_name: not installed, skipping"
        continue
    fi
    
    log "  Testing $tool_name ($tool_path)..."
    TOOL_RESULTS="$OUTPUT_DIR/${tool_name}-results.json"
    echo "{\"tool\": \"$tool_name\", \"type\": \"process_per_agent\", \"measurements\": [" > "$TOOL_RESULTS"
    
    first=true
    for n in "${AGENT_COUNTS[@]}"; do
        if [[ "$n" -gt "$MAX_AGENTS" ]]; then continue; fi
        
        log "    $n concurrent instances..."
        
        PIDS=()
        WORKDIRS=()
        
        # Spawn n instances in separate temp dirs
        for ((i=1; i<=n; i++)); do
            workdir=$(mktemp -d /tmp/resource-bench-${tool_name}-${i}-XXXX)
            WORKDIRS+=("$workdir")
            
            # Create a minimal file for the tool to work on
            echo "# TODO: implement fibonacci" > "$workdir/main.py"
            
            cd "$workdir"
            case "$tool_name" in
                claude)
                    claude --print -p "Write a Python fibonacci function with tests" \
                        --permission-mode bypassPermissions \
                        > /dev/null 2>&1 &
                    ;;
                codex)
                    # Codex needs PTY but we just want RAM — use script to fake it
                    script -q /dev/null codex exec "Write a Python fibonacci function with tests" \
                        > /dev/null 2>&1 &
                    ;;
                pi)
                    script -q /dev/null pi -p "Write a Python fibonacci function with tests" \
                        > /dev/null 2>&1 &
                    ;;
                opencode)
                    ~/go/bin/opencode --non-interactive "Write a Python fibonacci function with tests" \
                        > /dev/null 2>&1 &
                    ;;
            esac
            PIDS+=($!)
        done
        
        # Warmup — let processes initialize
        sleep "$WARMUP_SECONDS"
        
        # Measure total RSS across all instances
        total_peak_rss=0
        total_cpu=0
        alive=0
        
        for ((s=0; s<MEASURE_SECONDS; s++)); do
            sample_total_rss=0
            sample_total_cpu=0
            
            for pid in "${PIDS[@]}"; do
                if kill -0 "$pid" 2>/dev/null; then
                    rss=$(get_rss_kb "$pid")
                    cpu=$(get_cpu_percent "$pid")
                    sample_total_rss=$((sample_total_rss + rss))
                    sample_total_cpu=$(echo "$sample_total_cpu + $cpu" | bc 2>/dev/null || echo "$sample_total_cpu")
                fi
            done
            
            if [[ "$sample_total_rss" -gt "$total_peak_rss" ]]; then
                total_peak_rss=$sample_total_rss
            fi
            
            sleep "$SAMPLE_INTERVAL"
        done
        
        # Count how many are still alive
        for pid in "${PIDS[@]}"; do
            if kill -0 "$pid" 2>/dev/null; then alive=$((alive + 1)); fi
        done
        
        per_instance=$((total_peak_rss / n))
        log "      Peak total: $((total_peak_rss / 1024)) MB ($((per_instance / 1024)) MB/instance), $alive/$n alive"
        
        # Kill all
        cleanup_pids "${PIDS[@]}"
        
        # Cleanup workdirs
        for wd in "${WORKDIRS[@]}"; do rm -rf "$wd" 2>/dev/null; done
        
        if [[ "$first" != "true" ]]; then echo "," >> "$TOOL_RESULTS"; fi
        first=false
        echo -n "  {\"agents\": $n, \"peak_rss_kb\": $total_peak_rss, \"avg_cpu_pct\": $total_cpu, \"per_instance_kb\": $per_instance, \"alive\": $alive}" >> "$TOOL_RESULTS"
        
        # Safety check: if total RSS > 2GB, stop scaling this tool
        if [[ "$total_peak_rss" -gt 2097152 ]]; then
            log "      ⚠️  Exceeded 2GB, stopping further scaling for $tool_name"
            break
        fi
    done
    
    echo "" >> "$TOOL_RESULTS"
    echo "]}" >> "$TOOL_RESULTS"
    log "    $tool_name done."
    log ""
done

# ============================================================
# Phase 3: Combine results
# ============================================================
log "=== Phase 3: Combining results ==="

COMBINED="$OUTPUT_DIR/resource-benchmark.json"
python3 -c "
import json, glob, os

results = {
    'benchmark': 'resource-footprint',
    'system': {
        'ram_gb': $SYSTEM_RAM_GB,
        'cpu': '$CPU_MODEL',
        'os': 'macOS $OS_VERSION'
    },
    'config': {
        'max_agents': $MAX_AGENTS,
        'sample_interval_s': $SAMPLE_INTERVAL,
        'measure_duration_s': $MEASURE_SECONDS,
        'warmup_s': $WARMUP_SECONDS
    },
    'tools': {}
}

for f in glob.glob('$OUTPUT_DIR/*-results.json'):
    try:
        with open(f) as fh:
            data = json.load(fh)
        results['tools'][data['tool']] = data
    except Exception as e:
        print(f'Warning: failed to parse {f}: {e}')

with open('$COMBINED', 'w') as fh:
    json.dump(results, fh, indent=2)

# Print summary
print()
print('=== SUMMARY ===')
for name, data in sorted(results['tools'].items()):
    print(f'\\n{name} ({data[\"type\"]}):')
    for m in data['measurements']:
        rss_mb = m['peak_rss_kb'] / 1024
        agents = m['agents']
        print(f'  {agents:>3} agents: {rss_mb:>8.1f} MB')
"

log ""
log "Results saved to $COMBINED"
log "Done!"
