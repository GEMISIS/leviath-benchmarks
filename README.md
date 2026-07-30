# Leviath Benchmarks

Benchmarks for the [Leviath](https://github.com/Sun-Forge-AI/leviath) agent
framework. **Read [METHODOLOGY.md](METHODOLOGY.md) first** — it is the
contract every published number must satisfy, and it exists because the July
2026 round was withdrawn after an internal audit (see
[`results/archive-2026-07/README.md`](results/archive-2026-07/README.md)).

What is measured (and what deliberately is not):

- **No head-to-head numbers against agent products** (Claude Code, Codex, Pi,
  OpenCode, …). Leviath is a framework; those sit at a different layer, and
  any purpose-built external baseline is permanently open to the "you wrote
  the loser" objection.
- **C1** — structured vs flat context as an **ablation of the same Leviath
  binary**: `blueprints/engineer-v3/` vs `blueprints/flat-mode/`.
- **C2** — cache-honest token/cost accounting from API-reported usage only
  (`scripts/cost.py` + the round's pinned `rates.json`). Cache hit rate is
  published for both arms even where the structured arm is worse.
- **C3** — a task-completion ladder (`cli-tool` → `rest-api` → `stress-test`).
- **C4** — retention probes graded by a different provider's model
  (`evaluator/`); cut from a round if not fully wired at freeze time.
- **C5** — absolute resource footprint of one daemon
  (`scripts/resource-benchmark.sh`), real inference, no comparison bars.

## Running a round

```bash
# 0. Freeze: tag this repo + the leviath repo, write results/rounds/<tag>/rates.json
# 1. Preflight (checks bins, keys, scoring deps, blueprint validity, clean tree)
scripts/preflight.sh <freeze-tag>

# 2. Run an arm on a task (repeat per run of the matrix in METHODOLOGY.md)
WORKDIR=$(mktemp -d)
cp -r tasks/stress-test/seed-files/* "$WORKDIR/"
lev run blueprints/flat-mode/agent.leviath -t tasks/stress-test/task.md --yolo

# 3. Score it (writes results/rounds/<tag>/runs/<arm>-run<N>.json)
scripts/validate-run.sh "$WORKDIR" flat 1 ~/.leviath/runs/<run-id>/meta.json <freeze-tag>

# 4. Aggregate + chart (refuses runs whose freeze_tag doesn't match)
scripts/aggregate-results.py results/rounds/<freeze-tag>/
charts/generate.py results/rounds/<freeze-tag>/
```

To verify a published round from committed data:

```bash
scripts/reproduce-everything.sh <freeze-tag>
```

## Layout

| Path | What |
|---|---|
| `tasks/<name>/` | task.md, seed files, held-out validation suite, probes.json |
| `blueprints/` | agent blueprints; `flat-mode/` is the ablation arm |
| `scripts/` | preflight, scoring, cost module, aggregator, resource benchmark |
| `charts/generate.py` | round charts (light + dark), committed data only |
| `evaluator/` | cross-provider probe grader (Rust) |
| `results/rounds/<tag>/` | one published round: runs, rates.json, aggregate, resource data |
| `results/archive-2026-07/` | withdrawn July 2026 data — do not aggregate or cite |

Historical note: `SUMMARY.md` describes the original (pre-audit) design and is
kept for context; where it conflicts with METHODOLOGY.md, METHODOLOGY.md wins.
