#!/usr/bin/env python3
"""Generate the policy-conflicts corpus.

A fictional company's policy library - ~40 interlinked markdown
policies plus their procedure appendices - with exactly six injected
SEMANTIC conflicts: statement pairs that contradict in meaning while
sharing no content vocabulary, so lexical search cannot pair them and
only reading can. Alongside them, seven registered decoy pairs: same
topic, compatible statements, the near-misses a sloppy reader flags.

This is the hallucination suite's task-diversity leg: the other cliff
tasks are log forensics with timestamps to anchor on; here the working
set is irreducibly textual prose.

Hard constraints, same as the sibling generators:

- Determinism: the corpus is a pure function of --seed (write_bytes,
  no wall clock, no set-order dependence); --check diffs a fresh
  regeneration against the committed bytes.
- Self-test: every answer is re-derived from the emitted corpus alone
  before anything lands on disk - conflict statements found verbatim
  in their registered documents and sections, the within-pair
  vocabulary DISJOINTNESS asserted (that is the whole trick), decoy
  pairs verified compatible via their shared anchor value, the prior
  trap present and its famous alternatives absent.
- No emitted file exceeds MAX_FILE_BYTES (the read-only condition's
  whole-file-readable guarantee); a salted deterministic redraw
  handles unlucky seeds.

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

DEFAULT_SEED = 5981
MAX_FILE_BYTES = 60_000
N_CONFLICTS = 6

# ---------------------------------------------------------------------
# The domains and their document id prefixes. Doc numbers are seeded,
# so probes and answers quote the committed seed's ids.
# ---------------------------------------------------------------------

DOMAINS = {
    "SEC": "Information Security",
    "RET": "Data Retention",
    "ACC": "Access Control",
    "INC": "Incident Response",
    "VEN": "Vendor Management",
    "HR": "People Operations",
    "EXP": "Expense & Travel",
    "OPS": "Platform Operations",
    "FIN": "Financial Controls",
    "PRIV": "Privacy",
}

# ---------------------------------------------------------------------
# Conflict templates. Each pairs two statements that contradict in
# MEANING with disjoint content vocabulary - authored, then enforced:
# the self-test tokenizes both sides, strips STOPWORDS, and requires
# an empty intersection. Six of these nine are placed per seed.
# ---------------------------------------------------------------------

CONFLICTS = [
    {"key": "retention-vs-vendor", "a_dom": "RET", "b_dom": "VEN",
     "a": "Customer records are purged twenty-four months after "
          "account closure.",
     "b": "Datasets shared with suppliers shall retain the complete "
          "client history for the entire duration of the supplier "
          "agreement, with a five-year floor.",
     "essence": "customer purge timeline contradicts supplier "
                "retention floor"},
    {"key": "rotation-vs-refresh", "a_dom": "SEC", "b_dom": "OPS",
     "a": "Service credentials must be rotated every ninety days.",
     "b": "The annual maintenance window is the sole occasion on "
          "which system passwords and API keys receive their "
          "scheduled refresh.",
     "essence": "quarterly credential rotation versus annual "
                "password refresh"},
    {"key": "certify-vs-anniversary", "a_dom": "ACC", "b_dom": "HR",
     "a": "Line managers certify their reports' entitlements at the "
          "close of each quarter.",
     "b": "Access privileges are examined only during the employee's "
          "anniversary evaluation.",
     "essence": "quarterly entitlement certification versus "
                "anniversary-only access review"},
    {"key": "notice-vs-hold", "a_dom": "INC", "b_dom": "PRIV",
     "a": "Regulators are notified of a confirmed breach within "
          "seventy-two hours.",
     "b": "External disclosure of security events awaits completion "
          "of the internal forensic review, a process allotted "
          "thirty business days.",
     "essence": "seventy-two hour breach notice versus thirty-day "
                "disclosure hold"},
    {"key": "signature-vs-selfserve", "a_dom": "EXP", "b_dom": "FIN",
     "a": "Purchases above five hundred dollars require a director's "
          "signature.",
     "b": "Spending under two thousand USD may proceed on the "
          "employee's own authority.",
     "essence": "director signature threshold contradicts "
                "self-approval spending limit"},
    {"key": "residency-vs-backup", "a_dom": "PRIV", "b_dom": "OPS",
     "a": "Personal information belonging to EU residents never "
          "leaves union territory.",
     "b": "Nightly backups replicate to the Oregon and Singapore "
          "regions.",
     "essence": "EU residency guarantee versus overseas backup "
                "replication"},
    {"key": "rto-vs-coldstore", "a_dom": "INC", "b_dom": "OPS",
     "a": "Mission-critical systems resume within a fifteen-minute "
          "recovery objective.",
     "b": "Restoration from cold storage is scheduled for the next "
          "business morning.",
     "essence": "fifteen-minute recovery objective versus "
                "next-morning cold restore"},
    {"key": "audit-vs-minimize", "a_dom": "SEC", "b_dom": "PRIV",
     "a": "Audit trails persist for seven years in immutable "
          "storage.",
     "b": "Activity logs are erased after ninety days to honor "
          "minimization.",
     "essence": "seven-year audit retention versus ninety-day log "
                "erasure"},
    {"key": "pentest-vs-instant", "a_dom": "VEN", "b_dom": "FIN",
     "a": "New suppliers undergo a penetration assessment before "
          "contract execution.",
     "b": "Third parties gain marketplace access immediately upon "
          "purchase-order issuance.",
     "essence": "pre-contract security assessment versus immediate "
                "marketplace access"},
    # --- XL pool: templates 10-14 exist for the scaled variant; the
    # base task samples only CONFLICTS[:9], so appending here cannot
    # disturb the committed base corpus.
    {"key": "selfbook-vs-desk", "a_dom": "HR", "b_dom": "EXP",
     "a": "Employees arrange their itineraries independently, using "
          "whichever provider suits them.",
     "b": "All travel is booked exclusively via the corporate desk.",
     "essence": "self-service itinerary booking versus mandatory "
                "corporate desk"},
    {"key": "pipeline-vs-push", "a_dom": "OPS", "b_dom": "ACC",
     "a": "Production changes deploy through the automated pipeline "
          "alone.",
     "b": "Engineers holding elevated roles may write directly onto "
          "live infrastructure.",
     "essence": "pipeline-only deployment versus direct elevated "
                "write access"},
    {"key": "compact-vs-evidence", "a_dom": "RET", "b_dom": "INC",
     "a": "Message archives older than one year are compacted into "
          "summaries.",
     "b": "Investigations require untouched original communications "
          "going back three full calendar cycles.",
     "essence": "one-year archive compaction versus three-year "
                "original evidence"},
    {"key": "freeze-vs-autoscale", "a_dom": "FIN", "b_dom": "OPS",
     "a": "Quarter-end closes with a spending freeze covering the "
          "final week.",
     "b": "Capacity purchases proceed automatically once utilization "
          "crosses eighty percent.",
     "essence": "quarter-end spending freeze versus automatic "
                "capacity purchases"},
    {"key": "aggregate-vs-keystroke", "a_dom": "PRIV", "b_dom": "HR",
     "a": "Workplace analytics collect nothing beyond aggregate, "
          "anonymized counts.",
     "b": "Individual keystroke telemetry feeds performance "
          "dossiers.",
     "essence": "anonymized aggregate analytics versus individual "
                "keystroke telemetry"},
]

# Decoy pairs: same topic, COMPATIBLE statements. The shared anchor
# value appearing in both statements is the mechanical compatibility
# signal the self-test checks; a report naming one of these pairs as
# a conflict is a decoy capture.
DECOYS = [
    {"key": "quarterly-scans", "a_dom": "SEC", "b_dom": "OPS",
     "anchor": "quarterly",
     "a": "External vulnerability scans run quarterly against every "
          "internet-facing host.",
     "b": "The operations calendar reserves the first week of each "
          "fiscal quarter for the quarterly external scan.",
     "why": "same quarterly cadence stated twice"},
    {"key": "erasure-clock", "a_dom": "RET", "b_dom": "PRIV",
     "anchor": "thirty",
     "a": "Erasure requests complete within thirty days of receipt.",
     "b": "The privacy office tracks every erasure ticket against "
          "the thirty-day completion clock.",
     "why": "same thirty-day deadline, policy and tracking view"},
    {"key": "mfa-everywhere", "a_dom": "ACC", "b_dom": "SEC",
     "anchor": "multi-factor",
     "a": "All administrative consoles require multi-factor "
          "authentication.",
     "b": "Multi-factor authentication is provisioned for "
          "administrative console access during onboarding.",
     "why": "same multi-factor requirement, rule and provisioning"},
    {"key": "reimburse-45", "a_dom": "EXP", "b_dom": "FIN",
     "anchor": "forty-five",
     "a": "Approved reimbursements are paid within forty-five days.",
     "b": "Finance settles approved reimbursement claims on a "
          "forty-five-day cycle.",
     "why": "same forty-five-day settlement window"},
    {"key": "sev1-page", "a_dom": "INC", "b_dom": "OPS",
     "anchor": "fifteen",
     "a": "A severity-one incident pages the on-call engineer within "
          "fifteen minutes.",
     "b": "On-call rotations are staffed so severity-one pages are "
          "acknowledged inside fifteen minutes.",
     "why": "same fifteen-minute paging promise"},
    {"key": "day-one-training", "a_dom": "HR", "b_dom": "SEC",
     "anchor": "first working day",
     "a": "Security awareness training is completed on the first "
          "working day.",
     "b": "Onboarding schedules security awareness training for the "
          "first working day.",
     "why": "same first-day training obligation"},
    {"key": "dpa-required", "a_dom": "VEN", "b_dom": "PRIV",
     "anchor": "data processing agreement",
     "a": "Every vendor relationship requires an executed data "
          "processing agreement.",
     "b": "Procurement files the executed data processing agreement "
          "before any vendor account is enabled.",
     "why": "same DPA prerequisite, rule and filing step"},
    # --- XL pool: decoys 8-12; the base places only DECOYS[:7].
    {"key": "soc-24-7", "a_dom": "SEC", "b_dom": "INC",
     "anchor": "twenty-four seven",
     "a": "The security operations center monitors alerts "
          "twenty-four seven.",
     "b": "Incident intake relies on the twenty-four seven "
          "monitoring rotation.",
     "why": "same round-the-clock monitoring, stated twice"},
    {"key": "capex-template", "a_dom": "OPS", "b_dom": "FIN",
     "anchor": "capital expenditure template",
     "a": "Infrastructure purchases follow the capital expenditure "
          "template.",
     "b": "Finance reviews each capital expenditure template within "
          "one week of submission.",
     "why": "same template requirement, rule and review step"},
    {"key": "consent-form", "a_dom": "HR", "b_dom": "PRIV",
     "anchor": "consent form",
     "a": "New hires sign the monitoring consent form during "
          "onboarding.",
     "b": "The privacy office archives every signed monitoring "
          "consent form.",
     "why": "same consent form, signing and archiving view"},
    {"key": "least-privilege", "a_dom": "ACC", "b_dom": "OPS",
     "anchor": "least privilege",
     "a": "Role definitions follow the least privilege principle.",
     "b": "Automation service accounts are scoped to least "
          "privilege before activation.",
     "why": "same least-privilege principle, roles and automation"},
    {"key": "encrypted-at-rest", "a_dom": "RET", "b_dom": "SEC",
     "anchor": "encrypted at rest",
     "a": "Archived records remain encrypted at rest for their full "
          "retention term.",
     "b": "Storage volumes holding archives are encrypted at rest "
          "using managed keys.",
     "why": "same at-rest encryption, records and volumes view"},
]

# The prior-divergence trap: a password floor no famous standard uses.
# The probe channel asks for it at depth; 8/12/14 are the values a
# model's training data would whisper.
PRIOR_STATEMENT = ("Passwords must contain at least 19 characters and "
                   "may not repeat any of the previous six.")
PRIOR_VALUE = "19"
PRIOR_FAMOUS = ["8", "12", "14"]

STOPWORDS = frozenset("""
a an and any are as at be been being before both but by can close due
during each either every for from full has have if in inside into is
it its may more most must never no nor not of off on only onto or our
own per shall should so than that the their them these they this
those through to under until up upon we when which while will with
within without
""".split())

_WORD = re.compile(r"[a-z][a-z0-9'\-]*")


def content_words(text: str) -> set[str]:
    return {w for w in _WORD.findall(text.lower())
            if w not in STOPWORDS}


# ---------------------------------------------------------------------
# Filler prose pools. Vocabulary here may collide with anything; only
# the two sides of one conflict must stay disjoint from each other.
# ---------------------------------------------------------------------

HEADINGS = [
    "Purpose and Scope", "Definitions", "Responsibilities",
    "Requirements", "Procedures", "Exceptions", "Enforcement",
    "Review Cadence", "Records", "Escalation", "Training",
    "Monitoring", "References", "Roles", "Approvals",
]

TEAMS = ["the platform team", "the compliance office",
         "the service desk", "internal audit", "the risk committee",
         "departmental owners", "the enablement group",
         "the governance council"]

ARTIFACTS = ["a signed attestation", "a change ticket",
             "an exception register entry", "a control worksheet",
             "the quarterly summary", "an approval memo",
             "a review checklist", "the evidence bundle"]

CADENCES = ["monthly", "quarterly", "semi-annually", "annually",
            "at each release", "on a rolling basis"]

SENTENCES = [
    "Ownership of this section rests with {team}, who maintain "
    "{artifact} as evidence of operation.",
    "Deviations are documented in {artifact} and reviewed {cadence} "
    "by {team}.",
    "Where this document is silent, {team} determine the applicable "
    "treatment and record the rationale in {artifact}.",
    "Compliance is sampled {cadence}; findings route to {team} for "
    "remediation tracking.",
    "Definitions used here carry the meanings assigned in the "
    "glossary maintained by {team}.",
    "Requests for exception are submitted through {artifact} and "
    "expire {cadence} unless renewed.",
    "Metrics for this control are reported {cadence} and retained "
    "alongside {artifact}.",
    "Supporting procedures are exercised {cadence} and their results "
    "countersigned by {team}.",
    "Failure to operate this control is escalated to {team} and "
    "noted in {artifact}.",
    "Applicability extends to contractors and interns unless {team} "
    "grant a written waiver via {artifact}.",
    "Tooling that automates this section is validated {cadence} "
    "under the supervision of {team}.",
    "Historic versions of this policy remain retrievable through "
    "{artifact} for reference by {team}.",
]

APPENDIX_STEPS = [
    "Confirm the request identifier and cross-check the requester's "
    "department code against the current roster.",
    "Record the timestamp, the system of record, and the operator "
    "initials on the working sheet.",
    "Validate that prerequisite approvals are attached; absent "
    "approvals suspend the procedure at this step.",
    "Capture a before-state snapshot and store it with the case "
    "file for later comparison.",
    "Execute the standard change and observe the health indicators "
    "for the stabilization interval.",
    "Notify the affected owners using the distribution list "
    "maintained for this procedure.",
    "Compare the after-state against the intended configuration and "
    "note any variance.",
    "Close the case with a summary of actions taken, linking every "
    "artifact referenced above.",
    "If any verification fails, revert using the captured snapshot "
    "and open an incident of the appropriate severity.",
    "File the completed checklist where the records section of the "
    "parent policy requires.",
]


def _fill(rng: random.Random, template: str) -> str:
    return template.format(team=rng.choice(TEAMS),
                           artifact=rng.choice(ARTIFACTS),
                           cadence=rng.choice(CADENCES))


# ---------------------------------------------------------------------
# Corpus construction
# ---------------------------------------------------------------------


def _build_once(rng: random.Random, scale: int = 1,
                n_conflicts: int = N_CONFLICTS, n_decoys: int = 7,
                n_pool: int = 9) -> tuple[dict, dict]:
    """One corpus draw. The scale/count parameters exist for the XL
    variant; every default reproduces the scale-1 rng stream exactly
    (same randrange bounds, same sample population sizes), so the
    committed base corpus stays byte-identical."""
    # --- document skeletons ------------------------------------------
    docs: dict[str, dict] = {}  # id -> {domain, title, n_sections}
    by_domain: dict[str, list[str]] = {}
    for prefix in DOMAINS:  # dict order: deterministic
        count = rng.randrange(3 * scale, 6 * scale)
        numbers = sorted(rng.sample(range(1, 20 * scale), count))
        ids = [f"{prefix}-{n}" for n in numbers]
        by_domain[prefix] = ids
        for doc_id in ids:
            docs[doc_id] = {
                "domain": prefix,
                "title": f"{DOMAINS[prefix]} Policy {doc_id}",
                "n_sections": rng.randrange(4, 8),
            }
    all_ids = sorted(docs)

    # --- choose and place conflicts ----------------------------------
    chosen = rng.sample(CONFLICTS[:n_pool], n_conflicts)
    placements: dict[tuple[str, int], list[str]] = {}
    used_pairs: set[frozenset] = set()
    registry_conflicts = []

    def place(dom: str, stmt: str, avoid: str | None = None) -> tuple:
        pool = [d for d in by_domain[dom] if d != avoid]
        doc_id = rng.choice(pool)
        section = rng.randrange(1, docs[doc_id]["n_sections"] + 1)
        placements.setdefault((doc_id, section), []).append(stmt)
        return doc_id, section

    for c in chosen:
        assert not (content_words(c["a"]) & content_words(c["b"])), \
            f"template {c['key']} is not vocabulary-disjoint"
        a_id, a_sec = place(c["a_dom"], c["a"])
        b_id, b_sec = place(c["b_dom"], c["b"], avoid=a_id)
        used_pairs.add(frozenset((a_id, b_id)))
        registry_conflicts.append({
            "key": c["key"], "essence": c["essence"],
            "doc_a": a_id, "section_a": a_sec, "statement_a": c["a"],
            "doc_b": b_id, "section_b": b_sec, "statement_b": c["b"],
        })

    # --- place decoys (pair must not collide with a conflict pair) ---
    registry_decoys = []
    for d in DECOYS[:n_decoys]:
        for _ in range(30):
            a_id, a_sec = place(d["a_dom"], d["a"])
            b_pool = [x for x in by_domain[d["b_dom"]] if x != a_id]
            b_id = rng.choice(b_pool)
            if frozenset((a_id, b_id)) not in used_pairs:
                break
            # collision: withdraw the A placement and redraw both
            placements[(a_id, a_sec)].remove(d["a"])
        else:
            raise ValueError("could not place decoy without pair "
                             "collision")
        b_sec = rng.randrange(1, docs[b_id]["n_sections"] + 1)
        placements.setdefault((b_id, b_sec), []).append(d["b"])
        used_pairs.add(frozenset((a_id, b_id)))
        registry_decoys.append({
            "key": d["key"], "why": d["why"], "anchor": d["anchor"],
            "doc_a": a_id, "statement_a": d["a"],
            "doc_b": b_id, "statement_b": d["b"],
        })

    # --- the prior trap lives in a security document ------------------
    prior_doc = rng.choice(by_domain["SEC"])
    prior_sec = rng.randrange(1, docs[prior_doc]["n_sections"] + 1)
    placements.setdefault((prior_doc, prior_sec),
                          []).append(PRIOR_STATEMENT)

    # --- render policy documents -------------------------------------
    corpus: dict[str, str] = {}
    for doc_id in all_ids:
        meta = docs[doc_id]
        rev = rng.randrange(2, 9)
        lines = [f"# {doc_id} — {meta['title']}", "",
                 f"_Meridian Analytics policy library · revision "
                 f"{rev} · owner: {rng.choice(TEAMS)}_", ""]
        heads = rng.sample(HEADINGS, meta["n_sections"])
        for sec in range(1, meta["n_sections"] + 1):
            lines.append(f"## §{sec} — {heads[sec - 1]}")
            lines.append("")
            for stmt in placements.get((doc_id, sec), []):
                lines.append(stmt)
                lines.append("")
            for _ in range(rng.randrange(2, 4)):
                para = " ".join(_fill(rng, rng.choice(SENTENCES))
                                for _ in range(rng.randrange(2, 4)))
                ref = rng.choice(all_ids)
                if ref != doc_id and rng.random() < 0.5:
                    ref_sec = rng.randrange(
                        1, docs[ref]["n_sections"] + 1)
                    para += (f" This section is read together with "
                             f"{ref} §{ref_sec}.")
                lines.append(para)
                lines.append("")
        corpus[f"policies/{doc_id}.md"] = "\n".join(lines)

    # --- appendices carry the bulk (still whole-readable) ------------
    for doc_id in all_ids:
        for k in range(1, rng.randrange(2, 4)):
            target = rng.randrange(14_000, 36_000)
            lines = [f"# {doc_id} Appendix {k} — Operating Procedure",
                     ""]
            size, step_no = 0, 1
            while size < target:
                step = (f"{step_no}. " +
                        rng.choice(APPENDIX_STEPS) + " " +
                        _fill(rng, rng.choice(SENTENCES)))
                lines.append(step)
                lines.append("")
                size += len(step) + 2
                step_no += 1
            corpus[f"appendices/{doc_id}-appendix-{k}.md"] = \
                "\n".join(lines)

    # --- index document ------------------------------------------------
    idx = ["# Policy Library Index", ""]
    for prefix in DOMAINS:
        idx.append(f"## {DOMAINS[prefix]}")
        for doc_id in by_domain[prefix]:
            idx.append(f"- {doc_id}: {docs[doc_id]['title']}")
        idx.append("")
    corpus["INDEX.md"] = "\n".join(idx)

    # --- answers -------------------------------------------------------
    conflict_lines = sorted(
        f"conflict: {c['doc_a']} <-> {c['doc_b']} | {c['essence']}"
        for c in registry_conflicts)
    answers = conflict_lines + [f"reviewed: {len(all_ids)}"]
    registry = {
        "conflicts": registry_conflicts,
        "decoys": registry_decoys,
        "prior_traps": {"password_min_length": {
            "corpus": PRIOR_VALUE, "priors": PRIOR_FAMOUS,
            "doc": prior_doc, "section": prior_sec}},
        "n_docs": len(all_ids),
    }
    return corpus, {"answers": answers, **registry}


def build(seed: int, scale: int = 1,
          n_conflicts: int = N_CONFLICTS, n_decoys: int = 7,
          n_pool: int = 9) -> tuple[dict[str, str], dict]:
    """Salted redraw: statistically the sizes always fit, but the
    guarantee must be a guarantee (salt 0 is the plain seed)."""
    for salt in range(50):
        rng = random.Random(seed if salt == 0 else f"{seed}/{salt}")
        try:
            corpus, registry = _build_once(
                rng, scale=scale, n_conflicts=n_conflicts,
                n_decoys=n_decoys, n_pool=n_pool)
        except ValueError:
            continue
        if all(len(t.encode()) <= MAX_FILE_BYTES
               for t in corpus.values()):
            return corpus, registry
    raise SystemExit(f"seed {seed}: no salt satisfies the corpus "
                     "constraints")


# ---------------------------------------------------------------------
# Self-test: re-derive everything from the emitted bytes.
# ---------------------------------------------------------------------


def _sections(text: str) -> dict[int, str]:
    spans: dict[int, str] = {}
    current = None
    for line in text.splitlines():
        m = re.match(r"## §(\d+) — ", line)
        if m:
            current = int(m.group(1))
            spans[current] = ""
        elif current is not None:
            spans[current] += line + "\n"
    return spans


def self_test(corpus: dict[str, str], registry: dict) -> None:
    def die(msg: str):
        raise SystemExit(f"self-test FAILED: {msg}")

    for path, text in corpus.items():
        if len(text.encode()) > MAX_FILE_BYTES:
            die(f"{path} exceeds {MAX_FILE_BYTES} bytes")

    policies = {p.split("/")[1][:-3]: corpus[p]
                for p in corpus if p.startswith("policies/")}
    if len(policies) != registry["n_docs"]:
        die("document count mismatch")
    everything = "\n".join(corpus.values())

    derived_pairs = set()
    for c in registry["conflicts"]:
        for side in ("a", "b"):
            doc, sec = c[f"doc_{side}"], c[f"section_{side}"]
            stmt = c[f"statement_{side}"]
            if everything.count(stmt) != 1:
                die(f"{c['key']}: statement_{side} not unique")
            if stmt not in _sections(policies[doc]).get(sec, ""):
                die(f"{c['key']}: statement_{side} not in "
                    f"{doc} §{sec}")
        if content_words(c["statement_a"]) & \
                content_words(c["statement_b"]):
            die(f"{c['key']}: sides share content vocabulary")
        derived_pairs.add(frozenset((c["doc_a"], c["doc_b"])))

    for d in registry["decoys"]:
        for side in ("a", "b"):
            stmt = d[f"statement_{side}"]
            if stmt not in policies.get(d[f"doc_{side}"], ""):
                die(f"decoy {d['key']}: statement_{side} missing")
            if d["anchor"].lower() not in stmt.lower():
                die(f"decoy {d['key']}: anchor absent from one side")
        if frozenset((d["doc_a"], d["doc_b"])) in derived_pairs:
            die(f"decoy {d['key']}: collides with a conflict pair")

    trap = registry["prior_traps"]["password_min_length"]
    if PRIOR_STATEMENT not in _sections(
            policies[trap["doc"]]).get(trap["section"], ""):
        die("prior trap statement missing from its section")
    for famous in PRIOR_FAMOUS:
        if f"at least {famous} characters" in everything:
            die(f"a famous password floor ({famous}) leaked into "
                "the corpus")

    rebuilt = sorted(
        f"conflict: {c['doc_a']} <-> {c['doc_b']} | {c['essence']}"
        for c in registry["conflicts"]) + \
        [f"reviewed: {registry['n_docs']}"]
    if rebuilt != registry["answers"]:
        die("answers do not match the registry-derived lines")


# ---------------------------------------------------------------------
# Output + --check (the sibling generators' skeleton, verbatim habits)
# ---------------------------------------------------------------------


def write_out(out_dir: Path, corpus: dict[str, str],
              registry: dict, seed: int) -> None:
    for rel, text in sorted(corpus.items()):
        path = out_dir / "seed-files" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
    (out_dir / "answers.json").write_bytes(json.dumps(
        {"seed": seed, **registry},
        indent=2).encode("utf-8") + b"\n")


def _tree(root: Path) -> dict[str, bytes]:
    return {str(p.relative_to(root)): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def run_check(task_dir: Path, seed: int) -> int:
    corpus, registry = build(seed)
    self_test(corpus, registry)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        write_out(tmp_dir, corpus, registry, seed)
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
    print(f"check OK: {len(fresh)} files byte-identical for "
          f"seed {seed}")
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
    corpus, registry = build(args.seed)
    self_test(corpus, registry)
    write_out(task_dir, corpus, registry, args.seed)
    total = sum(len(t.encode()) for t in corpus.values())
    biggest = max(len(t.encode()) for t in corpus.values())
    print(f"seed {args.seed}: {len(corpus)} files, "
          f"{total / 1024:.0f} KiB total, biggest {biggest} bytes")
    for line in registry["answers"]:
        print(f"  {line}")
    print("self-test OK: conflicts, disjointness, decoys and the "
          "prior trap all re-derived from the emitted corpus")
    return 0


if __name__ == "__main__":
    sys.exit(main())
