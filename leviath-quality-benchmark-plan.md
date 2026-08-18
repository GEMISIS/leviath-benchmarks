# Leviath Quality Benchmark Plan — SUPERSEDED

*This planning note (August 13, 2026) is superseded by the implemented
methodology at [`bench/quality/CRS-METHODOLOGY.md`](bench/quality/CRS-METHODOLOGY.md).*

The Context Retention Suite it proposed is now built into the Python
quality harness (`bench/quality/suites/crs/`), with these deliberate
departures from the original note, decided during review:

- **The Leviath arm is always the composed cross-vendor flagship** —
  never a same-model-per-stage structured arm. The benchmark is a
  system comparison (Leviath as recommended vs a single-model flat
  loop), stated as such; the retention headline stays model-controlled
  because every probe is answered by one fixed reader model.
- **Probes are replayed, not injected.** Runs execute undisturbed;
  probes are asked post-hoc against the journaled context state at each
  depth (`run_probes.py`). No contamination, no skipped probes, and
  failed runs are probed up to where they died.
- **Flat baselines are the same runtime** (generated flat blueprints,
  pair-checked), plus a `flat-compacting` strong baseline. The old
  external Rust baseline stays retired — the July withdrawal
  post-mortem (`bench/quality/suites/crs/recovered/`) explains why.
- **The suite is rebalanced toward non-coding tasks** (incident
  forensics, records reconciliation, docs audit) across four agent
  families — Leviath is a runtime, not a coding agent, and no
  harness/coding-agent comparison is made or implied.
- **Publication posture**: smoke rounds are exploratory; freezing a
  counted round is the commitment to publish its result. The caching
  tradeoff is documented transparently (leviath#418), separately from
  the retention headline.
- Several of the note's premises did not survive contact with the
  recovered code (the `runner.rs:495` probe TODO, the "corrupted"
  stress-test probes, the 15-multiple probe grids); the corrections are
  recorded in `bench/quality/suites/crs/README.md`.
