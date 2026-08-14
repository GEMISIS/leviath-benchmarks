"""The shared evidence-conduct block, stated once per stage prompt.

The hallucination suite's fairness control: whatever discipline the
structured arm's *structure* enforces, the flat arms' *prompts* demand
in the same words. Every stage prompt in every arm - structured bases,
generated variants, and both flat baselines - carries this exact text,
so every LLM request in every arm sees the same conduct rules exactly
once. What the benchmark then measures is whether structure enforces
what instructions merely request.

add_conduct.py injects the block into the hand-authored bases (variants
inherit through regeneration); make_flat.py appends it to the flat work
prompt; check_pairs.py asserts the block is present verbatim in every
stage prompt of every blueprint.
"""

CONDUCT_MARK = "Evidence conduct"

CONDUCT = """\
Evidence conduct, applying to everything you produce:
- Cite the source of every factual claim (file and line, log entry,
  or document section) so a reader can check it without you.
- Keep a running record of key findings together with their sources as
  you work, and reuse that record instead of trusting memory.
- If the available material does not establish something you need, ask
  for it when you have a way to ask; otherwise state the gap explicitly.
  Never fill a gap with what similar systems usually do - an unsupported
  guess presented as fact is worse than a missing value."""
