# July 2026 benchmark round — WITHDRAWN

The July 2026 numbers (structured-vs-flat quality/cost on stress-test, and the
cross-tool RSS comparison) were withdrawn after an internal audit on
2026-07-29 and their data files were removed from the working tree. The raw
artifacts remain in git history prior to the commit that added this file
(`results/runs/`, `results/archive/`, `results/resource/`, `charts/output/`);
the charts the leviath README embedded live in that repo's history under
`docs/benchmarks/`.

Why they were withdrawn:

- The README charts were generated from a 3-runs-per-side results file that
  was **never committed** — the numbers shown ($7.92 vs $26.06, 46 vs 41 tool
  calls, 84.5%/85.5%) are not reproducible from anything ever in this repo.
- The "69 hidden tests" suite was deleted on 2026-07-14 and replaced by a
  59-test suite; the scoring harness was also rewritten *between* runs (one
  run moved 11/69 → 63/69 on the same artifacts).
- Published costs used a cache-blind formula while the flat-baseline binary
  had a measured 1.4–2.9% cache hit rate, a buggy truncation loop, a 100k
  window, and len/4 token counting.
- The resource comparison's Leviath side used `dry_run: true` (**no real
  inference**) while competitors ran real tasks, and its published JSON was
  hand-curated (schema mismatch with the script; warmup stated 8s, hardcoded
  3s). The OpenCode 10-instance point had only 7/10 processes alive.
- The published run pair was 1 of 4+ archived runs per side; pooling all
  archived runs reverses the cost conclusion.

Do not cite any number from that round. The current contract is
[`METHODOLOGY.md`](../../METHODOLOGY.md); new rounds land under
`results/rounds/<freeze-tag>/`.
