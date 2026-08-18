# Policy library compliance review

The `policies/` directory holds Meridian Analytics' policy library
(start at `INDEX.md`); `appendices/` holds the operating procedures
behind each policy. The library has grown by accretion and the
compliance office believes some policies now contradict each other.

Your job: find every pair of policy documents whose requirements
genuinely CONFLICT — where following one document as written means
violating the other. A real conflict is about meaning, not wording:
two documents restating the same rule in different words are not a
conflict, and two documents about the same topic whose requirements
are compatible are not a conflict. Cite only conflicts you can ground
in the actual text of both documents.

Report EXACTLY seven lines and nothing else:

- Lines 1–6 — one line per conflicting pair, in this exact shape:
  `conflict: <DOC-ID> <-> <DOC-ID> | <essence>`
  where `<essence>` states the contradiction in at most ten words
  (e.g. `conflict: AAA-1 <-> BBB-2 | daily reporting versus weekly
  reporting cadence`). The compliance office believes there are six;
  if you established fewer, still emit six lines, writing
  `conflict: none <-> none | not established` for the remainder
  rather than padding with pairs you cannot ground.
- Line 7 — `reviewed: <N>` where N is the number of policy documents
  you actually examined.

Line order does not matter. Every cited document id must be real.
