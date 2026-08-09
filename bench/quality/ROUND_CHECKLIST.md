# Running a counted round

Every step here exists because skipping it invalidates the round. The
methodology behind them is in [`../../METHODOLOGY.md`](../../METHODOLOGY.md).

## Before the freeze

1. **Roster.** Confirm every model in `arms.json` still satisfies the
   recency rule (released within roughly two months) and that its
   `released` date is right. Drop what has aged out; leave a tier empty
   rather than backfilling it with an older model.
2. **Rates.** Re-capture `rates.json` from each provider's published
   pricing, update `captured_utc`, and pin the OpenRouter route for any
   entry marked `pricing_varies_by_provider` so the pinned price is the
   billed price.
3. **Agents.** Run `apply_bench_policy.py`, `make_flat.py`, and
   `check_pairs.py`; bump `[agent] version` on anything that changed.
4. **Subsets.** Draw each suite's subset with `core/subset.py` and
   commit it, with any exclusions declared and reasoned *before* the
   draw.
5. **Keys.** Fill `.env` (never commit it) and fund each provider
   account - see the table below.
6. **Capability.** Run one smoke cell per suite with `--unsafe-smoke`
   against the mock provider, and one cheap real cell per provider, to
   prove keys, adapters, and containers work before spending.
7. **Tag.** `git tag qbench-YYYY-MM-rN` on a clean tree. The runner
   refuses to start otherwise.

## Funding

Fund each account before the round; a key that runs dry mid-round
produces `error` records that count as non-completion and cannot be
retried away.

| account | fund | what it covers |
|---|---|---|
| Anthropic | $600 | the frontier and workhorse sweeps, and the heavy stages of the mixed-models arm - the largest single line |
| OpenRouter | $150 | the open-weight and economy entries that route through it |
| OpenAI | $120 | the frontier/workhorse/economy entries on the native provider |
| Brave Search | free tier, or a paid plan for a large research round | the agents' `web_search` tool; without the key it degrades to Wikipedia-only results, and the runner refuses the GAIA suite rather than publish that. Estimate queries as runs x roughly 5-15 searches and check the tier's monthly cap before the round |
| Hugging Face | - | dataset access only (a gated download token, no billing) |

These are round-scale figures, not per-suite: the container coding
suites dominate them, because a single long agentic task there bills
one to two orders of magnitude more tokens than a log-analysis or
DABstep task. Set `--budget-usd` per invocation regardless; cells past
the cap are recorded as `cap` (non-completion), never dropped.

Suites that ship a large context file need headroom on both guards. A
flat-context arm can pull the whole file into its one window and then
re-send it every iteration; the ceiling counts cache reads, because
they are billed, so such a run reaches a million tokens in under twenty
seconds. That is a real result about flat context and it should be
recorded as one - but only if the ceiling was set high enough that the
run was allowed to be a result rather than a guard artifact.

Size `--per-run-max-tokens` from the smoke cells, not from taste. It is
a runaway guard, not a budget: set below what a healthy run of that
suite costs, it silently converts working cells into non-completions
and the arm looks broken rather than expensive. Take the most expensive
healthy smoke run for the suite and leave real headroom above it.

## After the round

Grade, reveal held-out answers, aggregate, render, and publish the
results tree whole. Results are never committed to this repo - the
round's raw tree is published as a CI artifact, and any hand-assembled
subset of it is not a round.
