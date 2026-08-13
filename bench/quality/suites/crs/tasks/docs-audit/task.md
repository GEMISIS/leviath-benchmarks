# Task: Documentation Compliance Sweep — Meridian Commerce

You are auditing the Meridian Commerce documentation corpus ahead of
its annual governance review. Some documents violate the governance
policy; find every violation and report the totals.

## Read the governance documents first, in full

- `POLICY.md` — the six numbered rules. Every judgment in this audit
  is defined by this document, including what counts as one violation
  for each rule.
- `style-guide.md` — the corpus layout, link conventions, and
  formatting conventions the policy assumes.

Read both completely before opening any content document; you will
need their exact wording throughout.

## The corpus

- `INDEX.md` — the entry point, listing every content document.
- `product-specs/`, `api/`, `sops/` — the one hundred twenty content
  documents in scope. The governance documents at the corpus root are
  exempt, as the policy states.

Audit every content document against all six rules. Apply each rule's
own counting unit: Rules 1, 3, and 5 count non-conforming documents;
Rules 2 and 4 count individual occurrences (each broken link, each
offending line); Rule 6 counts conflicting document pairs. A document
can violate several rules at once.

## Required report format

Your final report must be exactly seven lines, in this order, with no
headings, labels, or commentary around them:

1. Total violations of Rule 1 (Identifiers). A bare integer.
2. Total violations of Rule 2 (Cross-references). A bare integer.
3. Total violations of Rule 3 (Deprecation). A bare integer.
4. Total violations of Rule 4 (Credential hygiene). A bare integer.
5. Total violations of Rule 5 (Versioning). A bare integer.
6. Total violations of Rule 6 (Cross-document numeric consistency).
   A bare integer.
7. The five documents with the most violations in total (summing all
   rules with their counting units; a Rule 6 violation counts against
   the pair's non-authoritative document, as the policy defines; ties
   broken by taking the alphabetically earlier path), written as
   root-relative paths sorted alphabetically, comma-separated, no
   spaces (e.g. `api/webhooks.md,sops/key-rotation.md,...`).

Any deviation from this seven-line format makes the report unusable.
