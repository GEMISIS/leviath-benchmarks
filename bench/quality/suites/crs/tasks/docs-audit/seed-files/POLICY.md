# Documentation Governance Policy (rev 6)

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

## Rule 6 — Cross-document numeric consistency

When two documents state the same operational fact — a limit, a
timeout, a retry count, an archival period, a threshold — the stated
values must agree. The document that owns the fact is authoritative:
the API reference for facts about API behavior, the SOP for facts
about operational procedure. When a pair of documents disagrees on
such a fact, the non-authoritative document of the pair is the one in
violation. Count one violation per conflicting document pair.
