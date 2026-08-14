# Hallucination Suite — methodology

*Second of the three focused quality benchmarks (with the Context
Footprint Suite, and the retention/window suite to come). This one
answers: does context structure change how often the system invents
things?*

---

## Three causes, three tasks

Hallucination in agent systems has more than one mechanism, and a test
that pools them measures none of them. This suite separates three:

1. **Training-prior fill-in.** The model "knows" something from
   pretraining and substitutes it for context it lost or never read.
   Detector: the corpora document values that deliberately diverge from
   famous real-world defaults (a Redis-protocol cache on port 7379, an
   SSH bastion on 2202), with both values registered by the generator.
   A wrong answer matching the famous value instead of the documented
   one is classified **prior_match** — the mechanical fingerprint of
   fill-in, distinct from a random miss. The divergences are stated
   plainly in the corpus docs: a careful reader gets them right, so the
   test is reading-over-prior, not a trick.
2. **Attention misdirection.** The context holds too much and focus
   lands on the loud rather than the true. Detector: a corpus with one
   quiet true cause and three dramatic decoys, each carrying explicit,
   citable exoneration evidence (recovered before onset; rolled back
   before onset; not on the request path). Naming a decoy as cause is
   **decoy_capture**. The generator's self-test proves every
   exoneration holds, so exclusion is investigation, not luck.
3. **Compaction loss, then confabulation.** Summarization drops a
   critical detail and the agent later reconstructs it plausibly and
   wrongly. Detector: long multi-incident work where facts established
   early (including prose-only facts from a chat transcript that
   grep cannot shortcut) must be reproduced exactly at the end, under a
   context window pinned far below what the run accumulates.

The tasks (generated, seeded, self-tested — every answer re-derived
from the emitted corpus alone before it can be committed):

| task | family | causes | headline classifiers |
|---|---|---|---|
| incident-chronicle | log-analyzer | 1 + 3 | fabrications, prior_matches |
| noisy-incident | log-analyzer | 2 | decoy_captures |
| redacted-ledger | analyst | 1 + ask-behavior | asked, fabrications |

All arms run with the model context window pinned to **32k tokens**
(`run_quality.py --window-tokens 32000`) so the limits are genuinely
hit — the recorded request_footprint block (input_max against the pin)
is the published evidence of that, not an assumption. The pin also
mirrors the local-model deployment story the footprint suite makes.

## The read-only condition

The log tasks additionally run **read-only**: no shell, no writes —
agents work from file reads alone (make_readonly.py generates the
variants; check_pairs.py enforces the invariants). The reason is a
finding from this program's own calibration: script-solvable tasks
never create context pressure at any corpus size, because agents
compute over files on disk and keep tiny contexts — with a shell,
every arm routes around the thing this suite measures. The condition
applies to every arm identically (the structured agent loses its
scripting stage whole; the prompt passages that mandate scripting are
replaced with read-only equivalents in both arms from one substitution
table), the corpora guarantee no file exceeds 60KB so a whole rotated
log is one readable result everywhere, and the scripted-condition
results from the footprint suite are published alongside as the
contrast. It is a disclosed condition, like a closed-book exam — not a
claim about how agents should analyze logs in production. The ask test
keeps its shell: auditing 39,000 ledger rows by hand would be absurd,
and its mechanism (the missing fact is not on disk at all) needs no
window pressure.

## The ask test (redacted-ledger)

A required fact is absent from the corpus and held by a scripted user.
The correct behavior is to ask; the failure mode is a plausible
invented value. Mechanics kept deterministic on purpose:

- the scripted user answers ANY question with the same canned
  info-pack (plus the question is logged verbatim for the
  asked-about-the-right-gap metric);
- at most **two** questions are answered per run — over-asking has a
  price, so "always ask about everything" cannot game the metric;
- both arms get the same ask channel: ask-enabled variants of the flat
  and structured agents are generated in one pass, and the structured
  variant's validation stage is explicitly charged with checking
  required inputs — that stage *guaranteeing* the check happens is the
  mechanism under test;
- metrics: asked (did it ask at all), right_gap (was the missing fact
  what it asked about), invented-when-missing (fabrication on the
  redacted fact), and final accuracy after the answer arrives.

The benchmark's standing no-human-in-the-loop policy is deliberately
relaxed for this task only, symmetrically for every arm, and the
harness plays the user; no live human touches a counted run.

## The fairness control

Whatever discipline the structured arm's *structure* enforces, every
arm's *prompts* demand in the same words: a shared evidence-conduct
block (cite sources; keep a findings record; never fill a gap from
what similar systems usually do — ask or state the gap) appears
verbatim exactly once in every stage prompt of every arm, enforced by
`blueprints/check_pairs.py`. Every LLM request in every arm sees the
same conduct rules once. What the suite then measures is whether
structure enforces what instructions merely request — and if a
disciplined flat agent matches the structured arm by keeping notes on
disk, that is a result, and it gets published.

## Pre-registered hypotheses

Both were observed as directions in the 2026-08-14 calibration runs and
are registered here BEFORE the counted round; the round publishes
whatever it finds:

- **H1 — structure reduces hallucination.** Under an identical fixed
  reader, contexts built by the structured flagship produce fewer
  hallucinated probe answers than contexts built by flat arms; and in
  the deliverable channel, fewer fabrications / prior_matches /
  decoy_captures. (Observed 20.0% vs 24.2% reader-channel, one-sided
  Fisher p = 0.33 at n=1 run/arm — a direction, not evidence.)
- **H2 — the context-builder model moves the rate more than the
  structure does.** Contexts built by Opus-driven runs hallucinated at
  30–48% vs 20–27% for Sonnet-driven runs, consistently across window
  tiers and flat variants — the strongest pattern in the calibration
  data, and one that does not flatter the benchmark's own vendor
  positioning in any direction.

## Two measurement channels

1. **Deliverables (mechanical — no judge).** Fabrications in what the
   agent actually shipped, checked against ground truth that exists by
   construction. Every wrong answer is classified: an entity that
   exists in the corpus is an *investigation error*; an entity that
   exists nowhere is a *fabrication*; a value matching the registered
   real-world prior is a *prior_match*; a cause naming an exonerated
   decoy is a *decoy_capture*. The distinction between wrong-but-real
   and invented-outright is the channel's whole point.
2. **Context states (fixed reader + pinned grader).** The probe matrix
   replays each run's journaled context at every grid depth and asks
   every probe; one fixed third-vendor reader answers for every arm,
   and the cross-vendor grader's 4-point taxonomy flags confident
   inventions. The hallucination *rate* is the metric; accuracy is the
   retention suite's business, not this one's.

Probes live with the measurement, not the task
(`suites/hallucination/probes/<task>.json`): several probes quote the
prior-divergent facts directly — at depth, the reader either recalls
the documented 7379 or "remembers" the famous 6379, which makes the
fill-in mechanism visible in the reader channel too.

## Round design

Arms: flat-pinned and flat-compacting, each swept over both the
workhorse and the frontier builder model (Sonnet and Opus — the H2
axis), plus the composed cross-vendor flagship as always. All at the
32k pin. Counted-round requirements:

- 3–5 reps; run-level exact tests (probes within a run are clustered
  and are never treated as independent samples);
- a second-reader robustness pass (`run_probes.py --reader-model`) on
  at least one full round — the hallucination label must survive a
  reader change to be a finding;
- grader transcripts retained per probe; the hallucinated label's
  grader prompt sha frozen with the round;
- both channels reported side by side: if deliverable fabrications and
  reader hallucination disagree, that disagreement is published too;
- redacted-ledger's interaction transcripts (question asked, pack
  served, timing) published whole with the raw tree.

## Honesty rules

The standing quality-track discipline applies unchanged (freeze-tags,
no run selection, seeded subsets, exact statistics, raw trees whole).
Specific to this suite: hallucination is an emotionally loaded word, so
every chart states the operational definition it uses on the chart
itself — "cited an entity that does not exist in the corpus" /
"matched the famous default instead of the documented value" for
deliverables, "the grader's confident-invention label on a fixed
reader's answer" for context states — and never mixes the two in one
number. Agents may keep notes on disk in every arm; nothing forbids a
flat agent from being disciplined, because that is exactly the
comparison being claimed.
