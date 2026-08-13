# Documentation Governance Policy (rev 5)

Scope: every document under `product-specs/`, `api/`, and `sops/`.
The governance documents at the corpus root (POLICY.md,
style-guide.md, INDEX.md) are exempt from the rules below.

## Rule 1 — Identifiers

Front matter must declare `id:` as `DOC-` followed by exactly four
digits, and the document's H1 title must begin with that same id
followed by a colon and a space. Count one violation per
non-conforming document.

## Rule 2 — Cross-references

Every markdown link whose target ends in `.md` is root-relative and
must resolve to a file that exists in this corpus. Count one violation
per broken link occurrence.

## Rule 3 — Deprecation

A document with front-matter `status: deprecated` must declare
`superseded_by:` naming an existing corpus file. Count one violation
per non-conforming document.

## Rule 4 — Credential hygiene

No document may show a plaintext credential. Any example line
assigning `api_key`, `token`, or `password` must use the literal
placeholder `<REDACTED>` as its value. Count one violation per
offending line.

## Rule 5 — Versioning

Front matter must declare `version:` as exactly
MAJOR.MINOR.PATCH with numeric components only — no `v` prefix, no
pre-release or build suffix. Count one violation per non-conforming
document.
