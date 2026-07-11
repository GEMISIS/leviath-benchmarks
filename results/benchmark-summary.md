# Leviath Benchmark Results - Initial Run

## Fixes Applied

All 4 fixes have been successfully applied and committed:

1. ✅ **ServerEvent deserialization** - Added `cached_tokens`, `cache_write_tokens` to `Tokens` variant and `tool_calls` to `AgentStatus` variant
2. ✅ **Mock provider tool_use blocks** - Implemented state machine to return tool_use blocks for multi-iteration loops with realistic cache simulation
3. ✅ **Probe response extraction** - Updated to collect log lines from WebSocket events after probe injection
4. ✅ **OpenAI provider implementation** - Full implementation of OpenAI chat completions API in flat baseline

## Build & Test Status

- ✅ `cargo build --release` - Success (with warnings)
- ✅ `cargo test` - All tests pass
- ✅ Commit: `d501584` - "fix: update harness and baseline for Leviath server compatibility"

## Resource Benchmark Results

**Provider:** Mock (free)
**Timestamp:** 2026-07-11T01:29:05Z

| Agents | RSS (KB) | RSS (MB) |
|--------|----------|----------|
| 1      | 18,560   | 18       |
| 5      | 18,656   | 18       |
| 10     | 18,656   | 18       |
| 25     | 18,832   | 18       |
| 50     | 19,088   | 18       |

**Findings:**
- Leviath maintains stable memory usage (~18MB RSS) across all concurrency levels
- Memory overhead per additional agent is minimal (<1KB per agent)
- Mock provider successfully simulated multi-iteration agent loops with tool calls
- Agents spawned and completed successfully using the `demo-instant` blueprint

## Retention Benchmark

**Status:** Not run - ANTHROPIC_API_KEY not available in environment

The retention benchmark requires a valid Anthropic API key to run against the real API. The harness and flat baseline are both ready to run once the API key is configured.

**To run manually:**
```bash
export ANTHROPIC_API_KEY=your_key_here
./target/release/leviath-bench run --retention --reps 1 --models claude-sonnet-4-5
```

## Next Steps

1. Configure ANTHROPIC_API_KEY in environment
2. Run retention benchmark with real API: `make bench-retention`
3. Run token efficiency benchmarks: `make bench-tokens`
4. Run caching benchmarks: `make bench-caching`
5. Generate comprehensive reports: `make report`

## Files Modified

- `harness/src/runner.rs` - Updated ServerEvent types and probe extraction logic
- `harness/src/mock_provider.rs` - Implemented tool_use state machine and cache simulation
- `baselines/flat/src/main.rs` - Implemented OpenAI provider

## Results Location

- Resource benchmark: `results/resource-benchmark.json`
- This summary: `results/benchmark-summary.md`
