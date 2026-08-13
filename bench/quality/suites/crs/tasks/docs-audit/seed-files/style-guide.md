# Documentation Style Guide (rev 8)

## Corpus layout

The corpus has exactly three content sections: `product-specs/` holds
feature specifications, `api/` holds endpoint references, and `sops/`
holds operational procedures. The governance documents (POLICY.md,
this guide, and INDEX.md) live at the corpus root and are the only
documents allowed there. INDEX.md is the entry point and lists every
content document.

## Identifiers and titles

Document ids are assigned from a central register and never reused.
The H1 is the only level-1 heading in a document and repeats the id,
as required by the policy.

## Versioning

Versions are digits-only MAJOR.MINOR.PATCH. Pre-release tags are
never published to this corpus; bump MINOR for additive changes and
MAJOR for breaking ones. This matches the policy's versioning rule
exactly.

## Links

Links between documents are always written root-relative
(`api/rate-limits.md`, never `../api/rate-limits.md` or an absolute
URL) and belong in a `## See also` section.

## Examples

Configuration examples use INI blocks. Credential values in examples
are always the placeholder `<REDACTED>`, per the policy's credential
rule.
