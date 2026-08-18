# Result formats

Results are an interface: every number any chart shows exists in the
JSON documented here, schemas are versioned and bumped rather than
mutated, and downstream tooling should read these files rather than
scraping charts. Results never live in this repo - runs write into the
git-ignored `results/` directory, and counted rounds will be produced
and published whole by CI.

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
with tier labels, `roster_ages` (each model's release date and its age
in days at round start, for the recency rule), the stage→model mapping
for the mixed-models arm, the
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
| `usage_by_stage` / `stages_entered` | the per-stage token ledger, and the stages the run actually entered in order - the first thing any post-mortem needs, recorded for every arm |
| `run_archive` | the runtime's own files kept beside this record under `<record>.artifacts/run/`: `meta.json`, `stages.json`, `context.json` (final window), `final_output`, and the gzipped `run.lvr` event log. Suites over gated datasets keep only the first two, since the rest embed dataset text |
| `cost_usd` | priced from `rates.json`; null for unpinned rates and for the mixed-models arm (no single rate applies to its aggregate usage) |
| `rates_sha256` | the rates file this cost came from |
| `score` | `{passed: bool, detail: ...}` from the suite's grader |

Every run writes a record - failures, timeouts, and budget cap-outs
included. There is no mechanism for excluding one.

## quality-run-v2 (superset of v1)

v2 records carry everything above (with `schema: "quality-run-v2"`) plus
optional blocks written by the newer suites. v1 records stay valid;
readers accept both.

Footprint-suite blocks:

| field | meaning |
|---|---|
| `functional` | `{score: 0..1, detail}` — the generous functional bar's graded result (compiles-and-plays, facts found, document grounded), while `score.passed` carries the pass/fail |
| `request_footprint` | `{n_requests, input_p50, input_max, input_head_mean, input_tail_mean, input_growth, output_p50, secs_p50, requests: [{iteration, tool_calls, input_tokens, output_tokens, secs}]}` — per-request tokens over the run, folded from the journal's cumulative provider-billed counters. `input_growth` (tail mean ÷ head mean) is the stability verdict: ~1 holds, >1 grows |

Retention blocks (dormant since the CRS split; kept for the successor
retention/window suite):

| field | meaning |
|---|---|
| `validation` | held-out test results for the run's artifact: `{passed, failed, errors, total, failures, suite_hash}`. `suite_hash` is a sha256 manifest of the validation suite that scored it |
| `retention` | one entry per probe: `{after_tool_calls, at_tool_calls, probe_type, reached, score, grade, hallucinated, read_by, graded_by}`. Probes are replayed post-hoc against the journaled context state (never injected into the live run); a run that died before a depth carries `reached: false` there - recorded, never dropped |
| `retention_summary` | `{mean_score, n_probes, n_reached, n_hallucinated}`; mean over reached probes only, on the 0..1 accuracy scale. Hallucination is a separate rate and never enters the mean as a negative score |
| `probe_overhead` | what the measurement itself cost: `{usage, cost_usd, reader_model, grader_model, grader_prompt_sha256, probe_wrapper_sha256}`. **Excluded** from the record's `cost_usd` and from every cost comparison - it is measurement, not agent spend |

CRS artifacts live beside the record under `<record>.artifacts/`:
`probe_replays/probe_<N>.json` (reconstructed request digest, the fixed
reader model's full answer, usage) and `probe_<N>.grade.json` (the
grader transcript), plus `pytest-report.json` for the validation run.

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
