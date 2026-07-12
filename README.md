# Leviath Benchmarks

Reproducible benchmark suite measuring the performance and efficiency of the [Leviath agent framework](https://github.com/Sun-Forge-AI/leviath) against traditional flat-context baselines.

## What This Measures

This benchmark suite produces quantitative evidence for four key claims:

1. **Context Retention** - Can Leviath agents remember important details after 50+ tool calls, where flat-context agents forget?
2. **Token Efficiency** - Does Leviath's structured context management reduce token consumption vs. naive truncation?
3. **Caching Effectiveness** - How well does Leviath leverage provider-native caching for cost savings?
4. **Resource Overhead** - What is the cost of Leviath's abstractions in terms of memory, spawn time, and complexity?

## Methodology

### Fairness Guarantees

- **Same model, same tools**: Both Leviath and flat baseline use identical LLM models and tool implementations
- **Same tasks**: Both agents receive identical task descriptions and seed files
- **Independent grading**: Probe responses are graded by a *different* LLM provider than the one being benchmarked
- **Flat baseline is not a strawman**: Our baseline implements provider-native caching and represents best practices for flat-context management

### Benchmark Categories

#### 1. Context Retention Test (CRT)

**What it measures**: Ability to recall specific details from early in the conversation after many intervening tool calls.

**How it works**:
- Agent starts a coding task with detailed specifications in seed files
- At predetermined tool call counts (25, 50, 75, 100+), we inject "probe questions"
- Probe questions ask about specific details from the seed files (e.g., "What JWT algorithm was specified?" or "What's the rate limit?")
- Responses are graded on a 4-point scale: Correct (1.0), Partial (0.5), Wrong (0.0), Hallucinated (-0.5)

**Multi-file consistency**: Some probes specifically test cross-file consistency (e.g., verifying that shared types match between frontend and backend).

**Metrics**:
- Retention score: Average probe score, normalized to percentage
- Probes passed: Count of correct responses
- Decay curve: Retention score vs. tool call count

#### 2. Token Efficiency

**What it measures**: Total token consumption for completing the same task.

**How it works**:
- Run identical tasks on both Leviath and flat baseline
- Track per-inference-call token usage: prompt, completion, cached, cache_write
- Sum total tokens across entire task

**Metrics**:
- Total tokens (prompt + completion)
- Token savings percentage: (1 - leviath_total / flat_total) × 100
- Context Efficiency Score (CES): (baseline_tokens / leviath_tokens) × (1 + cache_hit_rate)

#### 3. Caching Effectiveness

**What it measures**: How well each system leverages Anthropic's prompt caching.

**How it works**:
- Enable prompt caching for both systems (system prompts, tool definitions cached)
- Track cache metrics from API responses: cached_tokens, cache_write_tokens
- Measure cache hit rate over time

**Metrics**:
- Cache hit rate: cached_tokens / total_prompt_tokens
- Cost reduction: Savings from cached tokens (at 90% discount per Anthropic pricing)
- Cache stability: How long cache remains valid

#### 4. Resource Overhead

**What it measures**: System resource costs of running Leviath vs. flat baseline.

**How it works**:
- Measure peak RSS (resident set size) memory usage
- Time agent spawn/initialization overhead
- Count tool calls to task completion

**Metrics**:
- Peak memory (MB)
- Spawn overhead (ms)
- Tool calls to completion

## Repository Structure

```
leviath-benchmarks/
├── README.md                    # This file
├── Makefile                     # Build and run commands
├── Cargo.toml                   # Rust workspace
├── tasks/                       # 5 realistic coding tasks
│   ├── rest-api/                # ~50 tool calls
│   ├── cli-tool/                # ~70 tool calls
│   ├── refactor/                # ~80 tool calls
│   ├── full-stack/              # ~100 tool calls
│   └── data-pipeline/           # ~120 tool calls
├── baselines/
│   └── flat/                    # Flat-context baseline (Rust)
├── evaluator/                   # LLM-based probe grading
├── harness/                     # Main benchmark orchestrator
├── results/                     # Raw JSON results (gitignored)
└── reports/                     # Generated markdown reports
```

## Context Window Configuration

Modern models (Claude Sonnet 5, Opus 4.8) support **1M+ input tokens**, making it nearly impossible for typical coding tasks to fill the context window. However, real-world agent workloads — large codebases, long debugging sessions, multi-file refactors — routinely exceed practical context limits.

To produce meaningful retention benchmarks, we **artificially constrain the context window** (default: 32K-80K tokens). This:

1. **Simulates real-world pressure**: A 100-file codebase easily generates 200K+ tokens of context
2. **Forces context management decisions**: Without constraints, both flat and structured approaches perform identically (no truncation = no information loss)
3. **Produces measurable differences**: The benchmark measures how well each approach handles context overflow, which is the core value proposition

The `--context-window` flag on the flat baseline and the `max_tokens` field in Leviath blueprints control this. Results should always report the configured window size alongside token metrics.

> **Note**: With unconstrained windows, both approaches achieve identical retention scores. The structured context advantage emerges specifically when the window fills up and decisions must be made about what to keep vs. evict.

## Getting Started

### Prerequisites

1. **Rust toolchain** (1.70+): `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
2. **Leviath installed**: Follow [Leviath installation guide](https://github.com/Sun-Forge-AI/leviath#installation)
3. **API keys**: Set environment variables:
   ```bash
   export ANTHROPIC_API_KEY=your_anthropic_key
   export OPENAI_API_KEY=your_openai_key  # For grading
   ```

### Build

```bash
make build
```

This compiles three binaries:
- `target/release/leviath-bench` - Main benchmark harness
- `target/release/flat-baseline` - Flat-context baseline agent
- `target/release/evaluator` - Probe grading tool

### Run Benchmarks

#### Quick Start (Free)

Test the benchmark infrastructure without API costs using the mock provider:

```bash
# Start Leviath server
lev serve

# Run resource benchmarks with mock provider (no API calls)
make bench-resources
```

#### Full Suite (Expensive)

**⚠️ Warning**: Running the full suite makes hundreds of LLM API calls and will cost $20-50 depending on models.

```bash
# Start Leviath server
lev serve

# Run all benchmarks, 3 reps each
make bench

# Or run individual categories:
make bench-retention  # Context retention tests
make bench-caching    # Caching effectiveness
make bench-tokens     # Token efficiency
```

#### Custom Runs

```bash
# Benchmark specific models
leviath-bench run --all --models claude-sonnet-4-5,claude-opus-4-8 --reps 5

# Just retention with more reps for statistical significance
leviath-bench run --retention --reps 10

# Use mock provider for development
leviath-bench run --resources --mock
```

### Generate Reports

```bash
make report
```

This creates markdown reports in `reports/`:
- `summary.md` - High-level overview
- `retention.md` - CRT results
- `caching.md` - Cache effectiveness
- `tokens.md` - Token efficiency
- `resources.md` - Memory and overhead

### Grade Probe Responses

After running retention benchmarks, grade the probe responses:

```bash
make grade RESULTS=results/retention-leviath-claude-sonnet-4-5-rest-api-0.json PROVIDER=openai MODEL=gpt-4o
```

This uses OpenAI (different provider than Anthropic) to grade responses on the 4-point scale.

## Cost Estimates

Approximate costs per full benchmark run (3 reps, 5 tasks):

| Category | Model | API Calls | Est. Cost |
|----------|-------|-----------|-----------|
| Retention | Claude Sonnet 4.5 | ~150 | $8-12 |
| Retention | Claude Opus 4.8 | ~150 | $30-50 |
| Caching | Claude Sonnet 4.5 | ~150 | $8-12 |
| Tokens | Claude Sonnet 4.5 | ~300 | $15-25 |
| Resources (mock) | N/A | 0 | $0 |

**Total for Sonnet only**: ~$40-60
**Total for both models**: ~$100-150

Grading costs: ~$2-5 for evaluator LLM calls.

## Interpreting Results

### Context Retention Score

- **>90%**: Excellent - Agent consistently recalls details
- **70-90%**: Good - Most details retained, occasional lapses
- **50-70%**: Fair - Noticeable degradation over time
- **<50%**: Poor - Significant memory loss

Flat baselines typically score 30-60% due to truncation. Leviath should score >85%.

### Context Efficiency Score (CES)

CES = (baseline_tokens / leviath_tokens) × (1 + cache_hit_rate)

- **CES > 2.0**: Excellent - Using <50% tokens of baseline
- **CES 1.5-2.0**: Good - Meaningful efficiency gains
- **CES 1.0-1.5**: Fair - Modest improvement
- **CES < 1.0**: Poor - Using more tokens than baseline (unexpected)

### Cache Hit Rate

- **>60%**: Excellent - Most prompts benefiting from cache
- **40-60%**: Good - Significant cache reuse
- **20-40%**: Fair - Some cache benefit
- **<20%**: Poor - Cache not being utilized effectively

## Contributing

### Adding New Tasks

Tasks should be realistic coding scenarios that require reading seed files, writing code, and making decisions based on specifications.

1. Create `tasks/your-task/` directory
2. Write `task.md` with clear requirements
3. Add `seed-files/` with specs, schemas, examples
4. Create `probes.json` with questions about seed file details
5. Target a specific tool call range (our tasks span 50-120)

**Good probe questions**:
- Ask about specific values from seed files (API rate limits, error codes, config values)
- Test cross-file consistency (frontend/backend type agreement)
- Verify constraint recall (dependencies allowed, SLA numbers)

**Bad probe questions**:
- Ask about agent's current code (that's in context)
- Ask opinion questions with no right answer
- Ask derivable facts (probe should test recall, not reasoning)

### Grading Rubrics

Write specific rubrics that tell the evaluator LLM:
- What the exact expected answer is
- What constitutes partial credit
- Which file/section the answer comes from

Example:
```json
{
  "question": "What is the JWT signing algorithm?",
  "expected": "RS256 (RSA with SHA-256)",
  "rubric": "Must mention RS256 specifically. Just 'JWT' or 'RSA' is partial credit. The keys/ directory contains RS256 keys."
}
```

## License

MIT License - See LICENSE file

## Acknowledgments

- Benchmark design inspired by [SWE-bench](https://www.swebench.com/)
- Probe-based retention testing adapted from machine learning eval methodologies
- Thanks to the Leviath team for the excellent agent framework

---

**Questions or issues?** Open an issue on GitHub or reach out to the maintainers.

**Want to see results?** Check `reports/` after running benchmarks, or see [published results](https://leviath.ai/benchmarks) for reference data