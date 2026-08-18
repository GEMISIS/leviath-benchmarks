# Flagship versus Flat

**The complete comparison, 2026-08-18.** One runtime (leviath main
@3f464a5d/@0a157925, all cache and window fixes landed), one blueprint
discipline (pair-checked: same tools, same permissions, same total
iteration budget), five task families, windows from 32k to past-1M
tokens. The flagship is the shipped recommendation — six stages, four
models, three vendors, an adversarial critic mid-pipeline and a
fact-checking verifier at the deliverable. The flat arms are the
single-model loop the industry defaults to, in four flavors (pinned /
compacting eviction, each optionally hardened with wind-down + result
hygiene). Flat results are 5 reps on the uniform binary; flagship
numbers are the v2.2 architecture where stated, with the v1→v2.2 arc
reported openly because half of what this round measured was our own
agent's design flaws.

## The verdict in one table

| dimension | winner | the number that decides it |
|---|---|---|
| survival under window pressure | **flagship, by forfeit** | chronicle: flat 0/60 deliverables across 32/64/128k (hardened included); flagship 30/30 completions |
| quality at the hardest tier (128k) | **flagship** | chronicle 0.99 vs no flat deliverable; noisy 1.0 vs 0.93–1.0 |
| truthfulness | **flagship (after v2.2)** | 0 fabrications in 10/10 reps at 128k; v1 had 8 — the verify stage closed the channel |
| past-1M prose | **flagship on quality, flat on value** | 0.92 vs 0.83–0.88 — at 7× the cost |
| past-1M / plain code investigation | **flat** | deceptive-arch(-xl): flat 0.5–0.63 vs flagship 0.25–0.6 at 10–15× the cost |
| multi-request sessions | **tie at 1.0** — flat at 1/30th the cost | standing-desk: both 1.0; $0.47 vs $14.98 |
| easy / native-window tasks | **flat** | snake-cpp, log-search: everyone 1.0; flat is 3–8× cheaper |
| local models (27B, hard 32k) | **flat, decisively** | flat: 1.0 / 0.92 live cells; structured: timeouts and 0.08 |
| cost, overall | **flat everywhere it survives** | 2.8–8× cheaper wherever both arms deliver |

The one-sentence version: **structure is survival gear — it wins
exactly where the window is scarce or the deliverable is precision-
critical, ties where tasks are comfortable, and loses on cost
everywhere it isn't needed.**

## 1. Survival: the cliff is real, and hardening does not fix it

The incident-chronicle task (write 17 exact figures from a rotating log
corpus, read-only) at pinned windows:

| window | flat-pinned | flat-compacting | both hardened | flagship |
|---|---|---|---|---|
| 32k | 0/5 | 0/5 | 0/10 | 5/5 · 0.85 |
| 64k | 0/5 | 0/5 | 0/10 | 5/5 · 0.94 (v2.2) |
| 128k | 0/5 | 0/5 | 0/10 | 5/5 · **0.99** (v2.2) |

Sixty flat attempts, zero deliverables, and the dominant failure mode
is not confusion — it is the model devolving to empty responses near a
full window (94% of classified flat failures). Hardened prompts carry
every discipline the flagship's stages carry, as prose; the discipline
does not survive contact with a full window. On the noisy-incident
task the same cliff has a task-dependent edge: flats recover at 128k
(0.93–1.0) and hardening moves the boundary (2/5 hardened deliveries
at 64k where plain flats had none). Recovery windows are task-shaped;
the cliff itself is universal.

Cost note for fairness: a flat run that dies costs $2–10 and delivers
nothing. P(deliverable) is the metric that matters under pressure, and
it is 0 for flat on this task at every tested window.

## 2. Quality where both arms deliver

Where flats survive, the gap narrows — and twice it inverts:

- **noisy 128k**: flagship 1.0 (×5), flat-pinned-hardened 1.0 (×5),
  other flats 0.93. Effectively a tie; flagship costs 3–5×.
- **policy 128k** (44-doc conflict-finding, prose): flats 0.73–0.82,
  flagship 0.71 (v2.2; one rep died to a harness workspace race).
  The prose crossover from earlier rounds replicates: **do not buy
  structure for mid-window prose synthesis.**
- **policy-xl (~1.57M tokens)**: flagship **0.92** (11/12 conflicts,
  reviewing 53 of 435 docs — targeted, not exhaustive) vs flat 0.83 /
  0.88. Structure re-earns its keep past the window horizon — at
  $12.82 vs $1.71–1.87, which is the honest price of that margin.
- **deceptive-arch(-xl)** (lying codebase, coder family — untouched by
  the v2 surgery): flat 0.5–0.63, flagship 0.25–0.6 at 10–15× cost.
  The flagship's coder pipeline under-investigates (17 of 294 files in
  the XL rep) and misses chains it did read. This is the flagship's
  weakest family and the next anatomy candidate.

## 3. Truthfulness: collapse, not confabulation — and then zero

Across ~1,500 replay probes and every counted run, the story held:
flat agents under pressure collapse rather than confabulate (they
deliver nothing, so they fabricate nothing), and flagship errors were
dominated by honest abstention. The exception was v1's 128k chronicle:
three of five reps shipped complete, well-formatted reports whose
facts were misattributed or filled from training priors — 8
fabrications, round-hour timestamps, canonical config spellings the
corpus deliberately avoids. The verify stage was built against exactly
that: v2.2 shows **0 fabrications and 1 investigation error across all
10 reps at 128k**, with prior-trap hits at zero. The channel that
produced plausible-but-wrong deliverables is closed, and it cost about
$1–2 per run in verification reads.

## 4. Sessions and interaction

The 12-request standing-desk session is the starkest arc in the round:

| variant | score | what happened |
|---|---|---|
| flagship on the ask-test blueprint | 0.17 | pipeline submits after phase 2 — a single-deliverable shape cannot host a session |
| + session loop (revisit budgets) | 0.58 | mechanism works; the agent quits at phase 7 because the exit felt earned |
| + "only the user ends the session" | **1.0** | 12/12 phases, dependent-phase retention 1.0 |

Both flat arms scored 1.0 from the start at ~$0.47: a single loop is
natively session-shaped. The flagship now matches it at $14.98 —
structure adds nothing here but no longer subtracts. live-service (the
137-call server diagnosis) sits at parity (0.83 all arms on Sonnet);
the v2 flagship's quick single rep (0.67 at $0.29) is flagged as an
open item, not a counted result.

## 5. Economics on the fixed runtime

With the cache fixes landed (anchored markers; declared volatility;
within-stage chunking), measured on the footprint suite:

| task | flat-pinned | flat-compacting | structured-pinned | flagship |
|---|---|---|---|---|
| explain-repo | 0.87 · $1.93 | 0.94 · $4.29 | 0.92 · $7.51 | **0.98 · $5.46** |
| log-search | 1.0 · $0.66 | 1.0 · $0.65 | 1.0 · $1.03 | 1.0 · $2.10 |
| snake-cpp | 1.0 · $0.26 | 1.0 · $0.49 | 1.0 · $4.75 | 1.0 · $1.80 |

The published claim that "flagship caching is structurally worse
everywhere" is retired: on its best task the flagship caches at 62%,
inside the flat band (66–72%). What remains structural: cross-vendor
stages get no cache credit from 2 of 4 providers, short stages never
accumulate reusable history, and stage transitions still re-pay the
system prefix. Wall clock stays flagship's real tax: 3–10× slower
end-to-end. Cost columns in this doc are priced at the corrected
1-hour-TTL write premium (2.0× input, not the 5-minute 1.25× an
earlier rates file assumed — that error under-reported roughly $200
across two days of verification spend, and is why account billing ran
ahead of the priced ledger).

The multi-model split is also now measured: by token share the
flagship runs ~77% OpenAI (corpus-reading stages), ~19% Anthropic
(reasoning stages), ~5% OpenRouter (critic). By dollars Anthropic
dominates, because Opus prices the reasoning and output tokens.

## 6. The local arm (Qwen 3.8 27B, hard 32k window)

Flat on local is genuinely viable for interactive work: live-service
1.0, standing-desk 0.92, at $0. Structure on a 27B is wall-clock
prohibitive (timeouts at 75 min where flat finishes in 9–16 min) and
was session-broken before the fix (0.08). Code-corpus investigation
dies for both arms on the hard window (an un-evictable parallel-read
tail — leviath #485, eviction half still open). The local story:
**single-loop for local interactive agents; structured local needs
either smaller pipelines or bigger iron.**

## 7. What the benchmark did to its own agent

Half of this round's value is that it caught the flagship's design
flaws with measurements, and every fix was verified by re-measurement:

1. **The unverified deliverable.** The critic attacked the analysis,
   nobody attacked the report; complete-looking reports shipped wrong
   facts at 128k. → verify stage, draft gated in a required region.
   0.49 → 0.99.
2. **Evidence died young.** Every cross-stage edge carried nothing but
   a summary; the corpus region cleared at stage exit; a findings
   budget squeeze silently deleted oldest entries. → carry the draft,
   floor the budgets, fold the dormant script stage away.
3. **The wrong stage owned the reading.** After the binge edge was
   compacted, ingest swept 247 documents whose detail died at the
   transition while analyze rubber-stamped in 4 tool-less calls
   (policy fell to 0.08). → ingest stops at structure; every finding
   must cite a file opened in the stage that claims it. Policy-xl
   0.79 → 0.92.
4. **The pipeline couldn't host a session.** → session variant;
   0.17 → 1.0.
5. **The verifier over-corrected.** Its first draft deleted every
   claim it lacked budget to re-check (policy 0.79 → 0.0). → triage;
   only contradiction removes a claim. Recovered and then some.

The meta-lesson for the whitepaper: **structured context is not a
setting, it is a design discipline — and the failure modes of a bad
structure are as measurable as the failure modes of no structure.**
The same harness that shows flat agents collapsing shows exactly where
a pipeline leaks, and the fix loop (measure → anatomy → surgery →
re-measure) converged in two rounds.

## 8. When to buy structure

- **Buy it** when the window is scarce relative to the corpus
  (pressure tasks: it is the difference between an answer and
  nothing), when the deliverable is precision-critical (the verify
  stage is the only mechanism that produced 0 fabrications at 128k),
  and past the window horizon on prose synthesis (0.92 vs 0.88).
- **Don't buy it** for tasks that fit comfortably in the window
  (2.8–8× cost for equal scores), for mid-window prose synthesis
  (flats win outright), for linear sessions (tie at 30× the price),
  or on small local models (wall clock kills it).
- **Not yet decided:** code-corpus investigation (flagship's coder
  pipeline is the weakest and hasn't had its anatomy pass), and
  live-service under the v2.2 blueprints (single cheap rep, open).

## Caveats, all of them

Flat tiers: 5 reps, uniform binary, byte-identical blueprints across
the whole campaign. Flagship 128k + policy + XL + session: v2.2, 5
reps except XL cells (1 rep each). Flagship 32k/64k: v2.0 blueprints
(the surgery targeted 128k failure modes; 64k v2.0 already scored
0.94/1.0 — v2.2 can only be re-measured, expected ≥). Three v2.0 32k
reps died to since-fixed runtime 400s (#495) and are excluded rather
than imputed. deceptive-arch cells are single-rep with known variance.
Cost columns: priced at corrected 1h-TTL rates; pre-fix cache-era
costs are historical and marked. Grader/probe spend is measurement,
not agent cost, and runs on non-Anthropic models. Raw run trees are
local per repo policy, published at counted-round freeze; every table
here regenerates from `results/` by script.
