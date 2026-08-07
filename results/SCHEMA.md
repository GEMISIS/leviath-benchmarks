# Result formats

Committed results are an interface: every number any chart shows exists
in the JSON documented here, schemas are versioned and bumped rather
than mutated, and downstream tooling should read these files rather
than scraping charts.

## Layout

```
results/<utc-stamp>_<hostname>/
  specs.json                 machine + binary pins (cpu, cores, RAM, OS,
                             lev version, sha256, binary size)
  memory/  pools/  coldstart/   performance tracks: summary.json + raw
                             monitor CSVs + per-run interval CSVs
  quality/
    round.json               the machine-readable entry point for the round
    <suite>/
      summary.json           per-(arm, model) aggregates + comparisons
      runs/<task>__<arm>__<model>__rep<k>.json      one record per run
      runs/<task>__<arm>__<model>__rep<k>.artifacts/  answer/patch/verifier
```

## quality/round.json

Freeze tag, seed, reps, budget, the resolved arm list, the model roster
with tier labels, the stage→model mapping for the mixed-models arm, the
subset record (seed + universe hash + task ids + declared exclusions),
rates.json sha256, per-blueprint sha256s, and the lev version + binary
sha256. Everything needed to say exactly what ran.

## quality-run-v1 (one file per run)

| field | meaning |
|---|---|
| `schema` | `"quality-run-v1"` |
| `freeze_tag` | `qbench-*` tag, or `UNFROZEN-SMOKE` for development runs (never publishable) |
| `suite` / `task_id` / `arm` / `rep` | the cell |
| `model_label` / `model_policy` | roster label and the verbatim `-m` override; `"native"` / null for the stage-mix arm |
| `blueprint` | name + sha256 of the frozen blueprint that ran |
| `lev` | version + binary sha256 |
| `status` | `complete`, `error`, `timeout`, `no_answer`, or `cap` (budget); everything except `complete` counts as a failure |
| `started_utc` / `ended_utc` / `wall_clock_secs` | timing |
| `usage` | provider-reported `prompt_tokens`, `completion_tokens`, `cached_tokens`, `cache_write_tokens` |
| `billed_tokens` | every billed token incl. cache, using the provider's declared prompt-token semantics |
| `cache_hit_rate` | cache reads / all input-side tokens (null when no input) |
| `tool_calls` / `iterations` / `final_stage` | run shape |
| `cost_usd` | priced from `rates.json`; null for unpinned rates and for the mixed-models arm (no single rate applies to its aggregate usage) |
| `rates_sha256` | the rates file this cost came from |
| `score` | `{passed: bool, detail: ...}` from the suite's grader |

Every run writes a record - failures, timeouts, and budget cap-outs
included. There is no mechanism for excluding one.

## quality summary.json

`aggregate.cells`: one entry per (arm, model) with `runs`, `passes`,
`pass_rate`, a status histogram, and `median`/`min`/`max`/`samples`
blocks for `billed_tokens`, `cost_usd`, `wall_clock_secs`,
`tool_calls`, and `cache_hit_rate`.

`comparisons`: pre-registered arm pairs per model with
`p_pass_exact_permutation` (exact permutation test on pass outcomes)
and `p_tokens_exact_mann_whitney` (exact one-sided rank-sum on billed
tokens). Exact tests only; nothing falls back to an approximation.

## Performance summaries

`memory/` and `pools/` `summary.json`: one record per tier with
`repetitions` and `median`/`min`/`max` blocks (fields documented in the
README's reading guide) plus every raw per-rep record under `runs`.
`coldstart/summary.json`: four scenario blocks, each with
`median`/`min`/`max`/`n` per metric and the full `samples` list.
Monitor CSV columns: `elapsed_seconds, timestamp, cpu_percent, rss_mb,
pss_mb, uss_mb, footprint_mb, lazy_free_mb, live_mb, active_runs`;
runs CSV: `run_id, start_seconds, end_seconds`.
