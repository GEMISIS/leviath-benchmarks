# Site brief: the Quality tab for leviath.dev/benchmarks

For the agent building the benchmarks section. The Performance tab
keeps the existing runtime benchmarks; this brief covers the new
Quality tab. Source of truth for every number:
`bench/quality/FLAGSHIP-VS-FLAT.md` (and the tables regenerate from
`results/` by script). Do not restate numbers from memory; copy them
from that file, and keep them attributed to the round
(`round 2026-08-18, pre-freeze`). When the counted round freezes, the
tab gets the freeze tag and the raw-tree link.

## Tab naming and the one-line split

- **Performance** — how fast the runtime is.
- **Quality** — what the agents it runs actually deliver.

One sentence at the top of Quality: *"Same runtime, same tools, same
budgets — the only variable is context structure."* That sentence is
the whole methodology in miniature and disarms the vendor-strawman
read before it forms.

## Page order (this order matters)

1. **Hero: survival.** P(deliverable) under window pressure.
   `0/60 flat · 30/30 flagship` on the pressure task, with the
   window-tier bars (32/64/128k). Lead with the forfeit, not with
   score averages — a forfeit is unarguable. Include the sentence that
   the flat baselines carry every flagship discipline as prose
   (hardened variants) and still fail: that is the strongest single
   fact on the page.
2. **Truthfulness.** "0 fabrications in 10/10 precision reports at
   128k." Frame: the verify stage is an architectural guarantee, not a
   prompt suggestion — the unverified version of the same pipeline
   shipped 8 invented figures, and the page should SAY that, because
   the delta is the proof the mechanism works.
3. **The honest map — when structure pays and when it doesn't.**
   Three-column layout: *wins* (scarce windows, precision
   deliverables, past-1M prose: 0.92 vs 0.88), *ties* (comfortable
   tasks, sessions — note flat is far cheaper here), *flat wins*
   (mid-window prose synthesis, small local models). This section is
   load-bearing for credibility; do not shrink it. The copy tone is
   guidance, not confession: "here is where a single loop is the right
   tool" reads as engineering judgment.
4. **Economics.** The footprint table (score · cost per arm per task)
   and the cache story: flagship caching now inside the flat band on
   its best task. Always pair cost with score — never show a cost
   column alone in either direction.
5. **The design loop.** Short section: "we run this benchmark against
   our own recommended agent, and it finds our bugs before users do" —
   with two arcs as proof (0.49→0.99 chronicle; 0.17→1.0 session).
   This converts the iteration history from churn into the product's
   development discipline. Keep it to those two numbers; the full
   anatomy belongs in the methodology doc, not the marketing page.
6. **Methodology + reproducibility footer.** Same-binary ablation,
   pair-checked blueprints, 5 reps, seeded tasks with held-out keys,
   all runbooks and blueprints public, raw trees at freeze. Link the
   full comparison doc and (when it lands) the whitepaper.

## Rules for the builder

- **Never omit a flat win.** The policy-128k crossover and the
  deceptive-arch result appear on the page. They are what make the
  survival claim credible.
- **P(deliverable) before scores; scores before costs; never a mean
  across different tasks.** Pooled averages are where benchmark pages
  go to die on Hacker News.
- **Label everything that is thin.** Single-rep cells (XL, retention)
  say n=1 inline. The two open items (coder-family tasks, live-service
  v2.2) get an explicit "not yet counted" marker rather than silence.
- **No invented visuals.** Charts render from the repo's chart set or
  from the tables in FLAGSHIP-VS-FLAT.md. If a number isn't in that
  file, it doesn't go on the site.
- **Name the failure mode, not the competitor.** The baselines are
  "a single-model loop with a large window" — never a named harness
  or vendor. The 94%-empty-response stat describes model behavior
  under window pressure, not any product.
- **Version the page.** Numbers carry the round tag; the page states
  that a frozen counted round supersedes it. Committing to publish
  the frozen round regardless of outcome is part of the pitch — say
  so ("results publish at freeze, whatever they show").
- **Keep the two tabs consistent in voice**: Performance says how fast;
  Quality says how true. Neither editorializes about the other.

## Claims cleared for headline use (verbatim-safe)

- "Same binary, same tools, same budgets — only the context structure
  differs. The baselines carry every discipline our agents use, as
  prompt text."
- "Under window pressure, single-loop agents didn't degrade — they
  stopped delivering. 0 of 60 runs produced the report. The structured
  agent delivered 30 of 30."
- "With a verification stage in the pipeline: zero fabricated figures
  across every rep at the hardest tier."
- "Structure costs 3–8× where you don't need it. We tell you where you
  don't need it."

## Claims NOT cleared

- Any pooled "X% better than flat" number. (Task-shaped results;
  pooling misrepresents both directions.)
- Hallucination-rate comparisons against flat on pressure tasks (flat
  produced no deliverables to hallucinate in; the honest phrasing is
  the collapse-not-confabulation one).
- Latency/throughput claims on the Quality tab (wall clock is a cost
  there: flagship is 3–10× slower; if latency comes up, it points to
  the Performance tab's own numbers).
