# Hallucination Suite — methodology

*Second of the three focused quality benchmarks (with the Context
Footprint Suite, and the retention/window suite to come). This one
answers: does context structure change how often the system invents
things?*

---

## Pre-registered hypotheses

Both were observed as directions in the 2026-08-14 calibration runs and
are registered here BEFORE the counted round; the round publishes
whatever it finds:

- **H1 — structure reduces hallucination.** Under an identical fixed
  reader, contexts built by the structured flagship produce fewer
  hallucinated probe answers than contexts built by flat arms.
  (Observed 20.0% vs 24.2%, one-sided Fisher p = 0.33 at n=1 run/arm —
  a direction, not evidence.)
- **H2 — the context-builder model moves the rate more than the
  structure does.** Contexts built by Opus-driven runs hallucinated at
  30–48% vs 20–27% for Sonnet-driven runs, consistently across window
  tiers and flat variants — the strongest pattern in the calibration
  data, and one that does not flatter the benchmark's own vendor
  positioning in any direction.

## Two measurement channels

1. **Deliverables (mechanical — no judge).** Fabrications in what the
   agent actually shipped, checked against ground truth that exists by
   construction:
   - explain-repo: every cited path, crate, and symbol either exists in
     the pinned checkout or it does not (`grounding.json` lists every
     invention);
   - log-search: a wrong root-cause service or config key is classified
     as an *investigation error* when the entity exists in the corpus
     and a *fabrication* when it exists nowhere;
   - the distinction between wrong-but-real and invented-outright is
     the channel's whole point — hallucination is the second thing.
2. **Context states (fixed reader + pinned grader).** The probe matrix
   replays each run's journaled context at every grid depth and asks
   every probe; one fixed third-vendor reader answers for every arm,
   and the cross-vendor grader's 4-point taxonomy flags confident
   inventions. The hallucination *rate* is the metric; accuracy is the
   retention suite's business, not this one's.

Probes live with the measurement, not the task
(`suites/hallucination/probes/<task>.json` over the footprint suite's
workloads): the incident probes recovered intact, plus spec-fact probes
for snake-cpp and repository-fact probes for explain-repo, each with
strict rubrics and `exact` short-circuits where an answer is
mechanically checkable.

## Round design

The workloads are the footprint suite's three tasks — same runs can
serve both suites, and sharing them is disclosed, not hidden. The
sweep that carries H2: every flat arm runs under both the workhorse and
the frontier model (Sonnet and Opus) so builder-model and structure
vary independently; the flagship arm is the composed cross-vendor
configuration as always. Counted-round requirements:

- 3–5 reps; run-level exact tests (probes within a run are clustered
  and are never treated as independent samples);
- a second-reader robustness pass (`run_probes.py --reader-model`) on
  at least one full round — the hallucination label must survive a
  reader change to be a finding;
- grader transcripts retained per probe; the hallucinated label's
  grader prompt sha frozen with the round;
- both channels reported side by side: if deliverable fabrications and
  reader hallucination disagree, that disagreement is published too.

## Honesty rules

The standing quality-track discipline applies unchanged (freeze-tags,
no run selection, seeded subsets, exact statistics, raw trees whole).
Specific to this suite: hallucination is an emotionally loaded word, so
every chart states the operational definition it uses on the chart
itself — "cited an entity that does not exist" for deliverables,
"the grader's confident-invention label on a fixed reader's answer"
for context states — and never mixes the two in one number.
