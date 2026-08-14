# Smoke round report — footprint + hallucination suites (2026-08-14)

*UNFROZEN-SMOKE, n=1 per cell. Priorities per Gerald: better results
first, fewer tokens second, more cached third. Total round spend
~$62 arms + $21 probes.*

## What ran

- **Context Footprint Suite** (native windows, tools-on): snake-cpp,
  log-search, explain-repo × flat-pinned / flat-compacting (Sonnet) /
  cross-vendor flagship. Plus two explain-repo flagship retries (one
  killed by provider credits, one on the fixed v0.4.1 researcher).
- **Hallucination Suite** (32k window pin; log tasks read-only, ledger
  task tools-on with the scripted user): incident-chronicle,
  noisy-incident, redacted-ledger × the same three arms, plus a
  flagship rerun after a transient 529.
- **Probe matrix** over every hallucination run's journal (fixed
  reader Kimi K3, grader Terra, $21.20 excluded from arm costs).

## Scorecard against the priorities

| priority | pressure tasks (32k pin, read-only) | easy/native tasks |
|---|---|---|
| 1. results | **flagship decisively better** — the only arm that delivered at all | tie on snake/log-search (all 1.0); flagship WORSE on explain-repo (capped, no deliverable; flats shipped 0.64–0.75) |
| 2. tokens | flagship billed more in absolute terms, but tokens-per-deliverable is undefined for flat (zero deliverables) | flagship 2–5× more than flat-pinned |
| 3. cache | flagship 0.42–0.50 vs flat 0.26–0.79 | flagship 0.03–0.41 vs flat 0.52–0.88 |

Gerald's predictions held: caching is worse everywhere for the
flagship, and token use is worse wherever the task is easy enough that
hallucination pressure never materializes.

## The headline: at a genuinely-hit window, structure wins on results

incident-chronicle (4.5MB corpus, 32k pin, no shell):

| arm | outcome | fabrications | prior-matches | cost |
|---|---|---|---|---|
| flagship | **0.82 functional (14/17)** | **0** | **0** | $5.11 |
| flat-pinned | died iter 12/88, no deliverable | — | — | $0.74 |
| flat-compacting | died iter 10/88, no deliverable | — | — | $0.66 |

The flagship held every per-incident fact, every chat-only fact, and
all three prior-divergence traps (reported the corpus's 7379/2202/5,
not the famous 6379/22/3). Its three misses were cross-incident
numeric synthesis — investigation errors, nothing invented. The flat
arms' final contexts show the failure mechanism: window at 99.6% of
the pin, each 12k read evicting earlier findings, until the model
emitted a malformed `read_file {}` and the run ended without
`submit_output`. Compaction did not save the compacting variant.

noisy-incident repeated the pattern: flagship 0.86 — quiet root cause
found (cache.ttl_s at 05:41:41), **all three loud decoys correctly
ruled out with the right evidence tags, zero decoy capture** — while
flat-pinned thrashed to the 3M-token spend cap ($4.00, no deliverable)
and flat-compacting errored. Corrected footprint growth: flagship 1.17
(stable) vs flat 14–16× before dying.

Reader channel (same fixed reader for every arm): flagship 6% (T1) and
3% (T2) hallucinated vs flat's 9–22% — direction consistent with H1,
but survivorship caveats apply (dead flat runs were barely probed) and
n=1: direction, not evidence.

## Where the flagship is NOT holding up, and why

1. **Native-window economics (explain-repo).** The v0.4.0 researcher
   read the repo into `raw_findings` unboundedly: a 38% percentage
   budget resolves to 380k at Sonnet's 1M window, so eviction never
   fired — 196k-token requests, cache hit 0.07, $21.41 for 2/6 stages.
   The one-knob fix (24k absolute cap, v0.4.1) took cache to 0.41,
   made gather 3× cheaper, and stabilized growth 9.4→1.5 — but the run
   STILL capped at 3.5M: the analyze stage on Opus re-reads sources
   itself. Verdict: the researcher needs a redesign (read discipline
   in analyze, and/or a cheaper analyze model), not another retry.
   The flat arms did this task for $0.77–2.24 at 0.64–0.75 quality.
2. **Caching is structurally worse, three ways.** (a) Any append-hot
   region ahead of the message stream invalidates the conversation's
   cached prefix — the runtime then buys cache writes it can never
   read back (filed as leviath#441, with #442 for the
   percentage-budget lint). (b) The cross-vendor mix routes stages to
   providers where we get little or no cache credit (Grok/OpenRouter
   report none; OpenAI little). (c) Short runs never amortize: 15–20
   requests spread over 6 stages and 4 vendors reuse almost nothing.
3. **Counting without tools is a real weakness.** All three flagship
   T1 misses were numeric aggregation lines under the read-only
   condition. Honest gaps (it answered "0"/"none" rather than
   inventing), but a capability gap the structure does not cover.
4. **Provider weather still costs cells.** One flagship cell died to
   an Anthropic 529 at ingest; reruns are cheap but n=1 rounds are
   fragile. Credit exhaustion is now survivable (harness resumes
   paused runs after top-up).

## Test-design verdicts ("do we need a better way to test?")

- **The 32k + read-only pressure design works.** First cells in the
  program where the arms decisively separate on results. Keep it.
- **redacted-ledger needs a rework: the missing fact was derivable.**
  All three arms scored 1.0 without asking — they fit the enterprise
  rate from hundreds of correctly-priced enterprise rows (flat wrote
  a fitting script; the flagship's plan even said "recover the card
  empirically"). Legitimately impressive, zero fabrication — but it
  measures derivation, not ask-vs-invent. Fix: a tier with exactly ONE
  transaction (two rate unknowns, one equation — underivable; asking
  is the only path). The scripted-user machinery itself worked
  (16–18 interactions per run answered, questions logged).
- **The probe grader needs an elaboration-bias fix before any counted
  round.** Transcripts show correct reader answers labeled
  hallucinated for "adding unsupported specifics" that are in fact
  the run's own established findings (which the grader cannot see).
  This inflates the arm whose context is rich in findings — the
  structured arm — and poisons T3's reader numbers entirely (50%
  "hallucinated" ≈ derived-rate answers the rubric assumed
  impossible). Grader prompt change: elaboration consistent with the
  expected answer is not invention; flag only contradiction or
  fabricated entities.
- **Footprint's "per-request" is per-iteration at pinned windows** (an
  iteration can span multiple provider calls, so sums can exceed the
  window). The growth/stability story survives; the local-viability
  ceiling should come from the journaled context size instead.
  OpenAI's cached-token double-count is fixed and all records
  re-folded.
- **Still missing for counted rounds:** the Opus flat sweep (H2 - the
  strongest calibration-era pattern), 3–5 reps, second-reader
  robustness, and a completable flagship configuration for
  explain-repo.

## Changes shipped this round

Evidence-conduct block in every stage prompt of every arm (checked);
read-only condition with symmetric surgery and 60KB corpus guarantee;
ask machinery (askable variants, scripted user, no-yolo path);
raw_findings absolute cap (v0.4.1); pause-resume on credit exhaustion;
cancelled-status recording; two launch bugs caught by a $0 dry run;
verifier "none"-is-not-a-fabrication fix; OpenAI double-count fold
fix. Upstream: leviath#441 (wasted breakpoint writes), #442
(percentage-budget lint), #443 (agent-directed eviction — would become
a benchmark arm), #444 (spawn-time stage-prompt routing).
