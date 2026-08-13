#!/usr/bin/env python3
"""Generate the docs-audit corpus.

Forty interlinked markdown documents (product specs, API references,
SOPs) plus the governance documents that judge them: POLICY.md (five
numbered rules) and style-guide.md. The generator injects an exact set
of rule violations - identifier mismatches, broken cross-references,
deprecations without a successor, plaintext credential examples,
malformed versions - and computes the answer key from what it
injected; a self-test then re-audits the emitted files from scratch
with an independent implementation of the five rules, so the corpus
provably supports the key.

Hard constraints:

- Determinism: pure function of --seed; byte-identical re-runs
  (--check verifies against the committed copy).
- Stable reference docs: POLICY.md and style-guide.md are constants,
  independent of the seed; probes.json quotes facts from them.
- The "worst offenders" answer must be unambiguous under the stated
  tie-break: five designated offender documents carry at least three
  violations each while every other document carries at most one, and
  an assert enforces that separation.
- Violation counts must be exact: prose and link vocabularies are
  constructed so no accidental match of a rule pattern can occur, and
  the self-test would fail loudly if one did.

Usage:
    python3 generate.py [--seed N] [--out DIR] [--check]
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import tempfile
from pathlib import Path

DEFAULT_SEED = 3319

RULES = ["R1", "R2", "R3", "R4", "R5"]
SINGLETON_RULES = {"R1", "R3", "R5"}  # at most one per document

EXEMPT = {"POLICY.md", "style-guide.md", "INDEX.md"}

TOPICS = {
    "product-specs": [
        "checkout flow", "loyalty points", "gift cards",
        "inventory sync", "order tracking", "price rules",
        "tax engine", "shipping quotes", "returns portal",
        "wishlist sharing", "promotions engine",
        "subscription billing", "storefront themes"],
    "api": [
        "auth tokens", "rate limits", "webhooks", "orders endpoint",
        "customers endpoint", "payments endpoint", "refunds endpoint",
        "catalog endpoint", "search endpoint", "inventory endpoint",
        "shipping endpoint", "reporting endpoint", "errors reference",
        "pagination rules"],
    "sops": [
        "deploy procedure", "rollback procedure", "incident response",
        "on-call handbook", "database backup", "key rotation",
        "access review", "release checklist", "capacity planning",
        "monitoring setup", "data archival", "certificate renewal",
        "vendor onboarding"],
}

POLICY_MD = """\
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
"""

STYLE_GUIDE_MD = """\
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
"""

SENTENCES = [
    "This document describes the {topic} area of the Meridian "
    "Commerce platform.",
    "The {topic} behavior is owned by the {owner} team and reviewed "
    "each quarter.",
    "Changes to {topic} go through the standard review workflow "
    "before release.",
    "Configuration for {topic} is loaded at service start and "
    "refreshed every {n} minutes.",
    "Requests beyond the configured limit receive a structured error "
    "response with a stable error code.",
    "Identifiers used here follow the corpus-wide conventions in the "
    "style guide.",
    "Operational alerts for this area route to the owning team's "
    "rotation.",
    "The defaults listed below apply unless overridden per "
    "environment.",
    "Consumers should treat undocumented fields as unstable and "
    "subject to change without notice.",
    "Rollout is gated on the weekly release train unless an exemption "
    "is filed.",
    "Numbers in this section are targets, not guarantees, and are "
    "revisited during capacity planning.",
    "Earlier drafts of this behavior were consolidated here from the "
    "team wiki.",
]

BULLETS = [
    "default page size: {n}",
    "maximum batch size: {n}",
    "request timeout: {n} ms",
    "retry budget: {n} attempts",
    "cache lifetime: {n} seconds",
    "soft quota per client: {n} per hour",
]

OWNERS = ["platform-core", "storefront", "payments-platform",
          "discovery", "identity", "traffic-eng", "comms"]

BAD_VERSIONS = ["2.1", "v1.4.0", "1.0.0-beta", "latest", "3"]

CRED_WORDS = ["copper", "violet", "meadow", "harbor", "lantern"]


def slug_of(topic: str) -> str:
    return topic.replace(" ", "-")


# ---------------------------------------------------------------------
# Violation allocation. Five offender docs get >= 3 violations each;
# every other doc gets at most one, so the "worst five" are separated
# from the field by construction (asserted at the end of build()).
# ---------------------------------------------------------------------


def _allocate(rng: random.Random, paths: list[str],
              budgets: dict[str, int]) -> tuple[dict[str, list[str]],
                                                list[str]]:
    offenders = rng.sample(paths, 5)
    targets = {o: 3 for o in offenders}
    extra = sum(budgets.values()) - 15
    for i in range(10):
        if extra <= 0:
            break
        off = offenders[i % 5]
        if targets[off] < 5:
            targets[off] += 1
            extra -= 1
    assign: dict[str, list[str]] = {p: [] for p in paths}
    non_offenders = [p for p in paths if p not in offenders]
    # Singleton rules are placed first, while every offender still has
    # room; the repeatable rules then top the offenders up to target.
    for rule in ["R1", "R3", "R5", "R2", "R4"]:
        for _ in range(budgets[rule]):
            cands = [o for o in offenders
                     if len(assign[o]) < targets[o]
                     and (rule not in SINGLETON_RULES
                          or rule not in assign[o])]
            if cands:
                doc = max(cands, key=lambda o: (
                    targets[o] - len(assign[o]), -offenders.index(o)))
            else:
                doc = rng.choice([p for p in non_offenders
                                  if not assign[p]])
            assign[doc].append(rule)
    for off in offenders:
        assert len(assign[off]) >= 3, "offender under-filled"
    for p in non_offenders:
        assert len(assign[p]) <= 1, "non-offender over-filled"
    return assign, offenders


# ---------------------------------------------------------------------
# Corpus construction
# ---------------------------------------------------------------------


def build(seed: int) -> tuple[dict[str, str], list[str]]:
    rng = random.Random(seed)

    # --- doc skeletons ----------------------------------------------
    docs: list[dict] = []
    ids = rng.sample(range(1000, 10000), 40)
    i = 0
    for section in ("product-specs", "api", "sops"):
        for topic in TOPICS[section]:
            docs.append({
                "path": f"{section}/{slug_of(topic)}.md",
                "topic": topic, "title": topic.title(),
                "id": f"DOC-{ids[i]}",
                "version": (f"{rng.randrange(1, 4)}."
                            f"{rng.randrange(0, 10)}."
                            f"{rng.randrange(0, 10)}"),
                "owner": rng.choice(OWNERS),
                "status": "active", "superseded_by": None,
            })
            i += 1
    by_path = {d["path"]: d for d in docs}
    paths = [d["path"] for d in docs]

    # Two legitimately deprecated docs exercise Rule 3's happy path.
    dep_ok = rng.sample(docs, 2)
    for d in dep_ok:
        d["status"] = "deprecated"
        d["superseded_by"] = rng.choice(
            [p for p in paths if p != d["path"]])

    # --- violations --------------------------------------------------
    budgets = {"R1": rng.randrange(3, 7), "R2": rng.randrange(5, 10),
               "R3": rng.randrange(2, 5), "R4": rng.randrange(3, 6),
               "R5": rng.randrange(3, 7)}
    assign, offenders = _allocate(
        rng, [p for p in paths if by_path[p] not in dep_ok], budgets)
    for p in paths:
        d = by_path[p]
        rules = assign.get(p, [])
        d["viol"] = rules
        if "R3" in rules:
            d["status"] = "deprecated"
            d["superseded_by"] = (
                p.replace(".md", "-next.md") if rng.random() < 0.5
                else None)
            if d["superseded_by"] is not None:
                assert d["superseded_by"] not in by_path
        if "R5" in rules:
            d["version"] = rng.choice(BAD_VERSIONS)

    # --- render ------------------------------------------------------
    corpus: dict[str, str] = {
        "POLICY.md": POLICY_MD,
        "style-guide.md": STYLE_GUIDE_MD,
    }
    for d in docs:
        corpus[d["path"]] = _render_doc(rng, d, by_path, paths)

    index_lines = ["# Documentation Index", "",
                   "Every content document, by section. Governance "
                   "documents: [POLICY.md](POLICY.md), "
                   "[style-guide.md](style-guide.md).", ""]
    for section in ("product-specs", "api", "sops"):
        index_lines.append(f"## {section}")
        index_lines.append("")
        for d in docs:
            if d["path"].startswith(section + "/"):
                index_lines.append(
                    f"- [{d['id']}: {d['title']}]({d['path']})")
        index_lines.append("")
    corpus["INDEX.md"] = "\n".join(index_lines).rstrip("\n") + "\n"

    # --- answers from the injected ground truth ---------------------
    totals = {p: len(assign.get(p, [])) for p in paths}
    worst = sorted(paths, key=lambda p: (-totals[p], p))[:5]
    assert set(worst) == set(offenders), "offender separation broken"
    answers = [str(budgets[r]) for r in RULES] + \
        [",".join(sorted(offenders))]
    return corpus, answers


def _render_doc(rng: random.Random, d: dict, by_path: dict,
                paths: list[str]) -> str:
    rules = d["viol"]
    h1_id = d["id"]
    if "R1" in rules:
        # The H1 disagrees with the front matter by one digit.
        h1_id = d["id"][:-1] + str((int(d["id"][-1]) + 1) % 10)
        assert h1_id != d["id"]

    front = ["---", f"id: {d['id']}", f"title: {d['title']}",
             f"version: {d['version']}", f"status: {d['status']}"]
    if d["superseded_by"] is not None:
        front.append(f"superseded_by: {d['superseded_by']}")
    front += [f"owner: {d['owner']}", "---", ""]

    body = [f"# {h1_id}: {d['title']}", ""]
    intro = rng.sample(SENTENCES, 3)
    body.append(" ".join(
        s.format(topic=d["topic"], owner=d["owner"],
                 n=rng.randrange(5, 90)) for s in intro))
    body.append("")
    body.append("## Overview")
    body.append("")
    body.append(" ".join(
        s.format(topic=d["topic"], owner=d["owner"],
                 n=rng.randrange(5, 90))
        for s in rng.sample(SENTENCES, 4)))
    body.append("")
    body.append("## Behavior")
    body.append("")
    body.append(" ".join(
        s.format(topic=d["topic"], owner=d["owner"],
                 n=rng.randrange(5, 90))
        for s in rng.sample(SENTENCES, 5)))
    body.append("")
    body.append("## Defaults")
    body.append("")
    for b in rng.sample(BULLETS, rng.randrange(3, 5)):
        body.append("- " + b.format(n=rng.randrange(10, 4000)))
    body.append("")

    # Configuration example. Docs assigned Rule 4 violations show
    # plaintext credentials here; everyone else uses the placeholder.
    n_cred = rules.count("R4")
    if n_cred or rng.random() < 0.5:
        slug = d["path"].split("/")[1][:-3]
        body.append("## Configuration")
        body.append("")
        body.append("```ini")
        body.append(f"[{slug}]")
        body.append("endpoint = "
                    f"https://internal.meridian.example/v2/{slug}")
        body.append(f"timeout_ms = {rng.randrange(200, 9000)}")
        cred_lines = ['api_key = "<REDACTED>"']
        bad = [
            f'api_key = "sk_live_{rng.randrange(16 ** 12):012x}"',
            f"password: {rng.choice(CRED_WORDS)}{rng.randrange(10, 99)}",
            f'token = "tok_{rng.randrange(16 ** 10):010x}"',
        ]
        for k in range(n_cred):
            cred_lines.append(bad[k % 3])
        body.extend(cred_lines if n_cred else cred_lines[:1])
        body.append("```")
        body.append("")

    body.append("## See also")
    body.append("")
    links = rng.sample([p for p in paths if p != d["path"]],
                       rng.randrange(1, 4))
    for target in links:
        t = by_path[target]
        body.append(f"- [{t['id']}: {t['title']}]({target})")
    for _ in range(rules.count("R2")):
        broken = rng.choice(
            [p for p in paths if p != d["path"]]
        ).replace(".md", "-v2.md")
        assert broken not in by_path
        body.append(f"- [Background notes]({broken})")
    body.append("")
    return "\n".join(front + body).rstrip("\n") + "\n"


# ---------------------------------------------------------------------
# Self-test: independent audit of the emitted corpus.
# ---------------------------------------------------------------------

_ID_RE = re.compile(r"^DOC-\d{4}$")
_VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
_LINK_RE = re.compile(r"\]\(([^)]+)\)")
_CRED_RE = re.compile(r"^\s*(api_key|token|password)\s*[:=]\s*(.+)$")


def _front_matter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return {}
    fm = {}
    for line in lines[1:]:
        if line == "---":
            break
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip()
    return fm


def derive_answers(corpus: dict[str, str]) -> list[str]:
    counts = {r: 0 for r in RULES}
    totals: dict[str, int] = {}
    for path in sorted(corpus):
        if path in EXEMPT:
            continue
        text = corpus[path]
        fm = _front_matter(text)
        n = 0

        h1 = next((line for line in text.splitlines()
                   if line.startswith("# ")), "")
        doc_id = fm.get("id", "")
        if not _ID_RE.match(doc_id) or \
                not h1.startswith(f"# {doc_id}: "):
            counts["R1"] += 1
            n += 1

        for m in _LINK_RE.finditer(text):
            target = m.group(1)
            if target.endswith(".md") and "://" not in target \
                    and target not in corpus:
                counts["R2"] += 1
                n += 1

        if fm.get("status") == "deprecated":
            successor = fm.get("superseded_by")
            if not successor or successor not in corpus:
                counts["R3"] += 1
                n += 1

        for line in text.splitlines():
            m = _CRED_RE.match(line)
            if m and m.group(2).strip().strip('"') != "<REDACTED>":
                counts["R4"] += 1
                n += 1

        if not _VERSION_RE.match(fm.get("version", "")):
            counts["R5"] += 1
            n += 1

        totals[path] = n

    worst = sorted(totals, key=lambda p: (-totals[p], p))[:5]
    return [str(counts[r]) for r in RULES] + [",".join(sorted(worst))]


def self_test(corpus: dict[str, str], answers: list[str]) -> None:
    derived = derive_answers(corpus)
    if derived != answers:
        for i, (d, a) in enumerate(zip(derived, answers)):
            if d != a:
                print(f"  answer {i + 1}: derived {d!r} != key {a!r}",
                      file=sys.stderr)
        raise SystemExit("self-test FAILED: corpus does not support "
                         "the answer key")


# ---------------------------------------------------------------------
# Output + --check
# ---------------------------------------------------------------------


def write_out(out_dir: Path, corpus: dict[str, str],
              answers: list[str], seed: int) -> None:
    for rel, text in sorted(corpus.items()):
        path = out_dir / "seed-files" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
    (out_dir / "answers.json").write_bytes(json.dumps(
        {"seed": seed, "answers": answers},
        indent=2).encode("utf-8") + b"\n")


def _tree(root: Path) -> dict[str, bytes]:
    return {str(p.relative_to(root)): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def run_check(task_dir: Path, seed: int) -> int:
    corpus, answers = build(seed)
    self_test(corpus, answers)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        write_out(tmp_dir, corpus, answers, seed)
        fresh = _tree(tmp_dir)
    committed = {k: v for k, v in _tree(task_dir).items()
                 if k == "answers.json" or k.startswith("seed-files/")}
    problems = []
    for rel in sorted(set(fresh) | set(committed)):
        if rel not in committed:
            problems.append(f"missing from committed corpus: {rel}")
        elif rel not in fresh:
            problems.append(f"stale committed file: {rel}")
        elif fresh[rel] != committed[rel]:
            problems.append(f"byte mismatch: {rel}")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        print(f"check FAILED for seed {seed}", file=sys.stderr)
        return 1
    print(f"check OK: {len(fresh)} files byte-identical for seed {seed}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out",
                        default=str(Path(__file__).resolve().parent))
    parser.add_argument("--check", action="store_true",
                        help="regenerate into a temp dir and diff "
                             "against the committed corpus")
    args = parser.parse_args()
    task_dir = Path(args.out)
    if args.check:
        return run_check(task_dir, args.seed)
    corpus, answers = build(args.seed)
    self_test(corpus, answers)
    write_out(task_dir, corpus, answers, args.seed)
    total = sum(len(t.encode()) for t in corpus.values())
    print(f"seed {args.seed}: {len(corpus)} files, "
          f"{total / 1024:.0f} KiB")
    print(f"  rule counts R1..R5: {', '.join(answers[:5])}")
    print(f"  worst offenders: {answers[5]}")
    print("self-test OK: all answers re-derived from the emitted corpus")
    return 0


if __name__ == "__main__":
    sys.exit(main())
