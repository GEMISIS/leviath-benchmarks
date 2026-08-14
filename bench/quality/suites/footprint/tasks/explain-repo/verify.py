"""Functional verification for explain-repo: grounded, right, coherent.

Three checks over the architecture document (read from the workdir's
ARCHITECTURE-EXPLAINED.md, falling back to the answer text):

1. Grounding (mechanical, the hallucination detector): every path-like
   or backtick-quoted code reference in the document is checked against
   the seeded checkout under workdir/repo - paths by existence, bare
   symbols by a bounded grep over *.rs/*.toml contents. Fewer than five
   references total means an ungrounded essay: grounding_rate = 0.
2. Fact checklist (auto-derived at verify time, never hardcoded): the
   workspace member crate names parsed from the checkout's root
   Cargo.toml; checklist_rate is the fraction mentioned. Binary names
   from the CLI crate's [[bin]] are derived and reported in detail.
3. Coherence (LLM pass, generous): the round's grader model judges
   whether the document reads as an accurate, coherent architecture
   explanation. Missing key or grading error => coherence None, which
   is EXCLUDED from the score (the other two renormalize).

score = 0.5*grounding + 0.3*checklist + 0.2*coherence.
functional_pass = grounding >= 0.85 AND checklist >= 0.6 AND
(coherence is None or coherence >= 0.5). Generous by design: soft spots
are tolerated, fabricated citations are not.
"""
from __future__ import annotations

import json
import os
import re
import sys
import tomllib
from pathlib import Path

_QUALITY_DIR = Path(__file__).resolve().parents[4]
if str(_QUALITY_DIR) not in sys.path:
    sys.path.insert(0, str(_QUALITY_DIR))

from core import evaluator, providers  # noqa: E402,F401

DOC_NAME = "ARCHITECTURE-EXPLAINED.md"
MIN_REFS = 5
GROUNDING_BAR = 0.85
CHECKLIST_BAR = 0.6
COHERENCE_BAR = 0.5
WEIGHTS = {"grounding": 0.5, "checklist": 0.3, "coherence": 0.2}

_KEY_FOR_PROVIDER = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
}

# ── reference extraction ─────────────────────────────────────────────
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
# Bare (outside backticks) path-like references.
BARE_PATH_RE = re.compile(
    r"\b(?:repo/)?(?:crates|src|docs|xtask|perf-tools|coverage)"
    r"/[A-Za-z0-9_\-./]*[A-Za-z0-9_]")
BARE_FILE_RE = re.compile(r"\b[A-Za-z0-9_\-./]+\.(?:rs|toml|lock)\b")
# Backticked-token shapes that count as code references.
FILE_EXT_RE = re.compile(r"\.(?:rs|toml|md|lock|yml|yaml|json|sh)$")
CRATE_RE = re.compile(r"^[a-z][a-z0-9_]*(?:-[a-z0-9_]+)+$")
CAMEL_RE = re.compile(r"^[A-Z][A-Za-z0-9]*(?:::[A-Za-z0-9_]+)*$")
FUNC_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:::[A-Za-z0-9_]+)*\(\)$")
MODPATH_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:::[A-Za-z0-9_]+)+$")
SNAKE_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")

# Never treated as repo references (the deliverable names itself).
EXCLUDED = {DOC_NAME, DOC_NAME.lower()}


def _clean(tok: str) -> str:
    return tok.strip().strip(",.;:!?()[]{}\"'").rstrip("/")


def _classify_backtick(tok: str) -> tuple[str, str] | None:
    """Return (kind, needle) for a backticked token, or None to skip."""
    tok = _clean(tok)
    if not tok or tok in EXCLUDED or " " in tok or "\t" in tok:
        return None  # commands and prose phrases are not citations
    if "/" in tok or FILE_EXT_RE.search(tok):
        return ("path", tok)
    if FUNC_RE.match(tok):
        return ("symbol", tok[:-2].split("::")[-1])
    if MODPATH_RE.match(tok):
        return ("symbol", tok.split("::")[-1])
    if CRATE_RE.match(tok) or CAMEL_RE.match(tok) or SNAKE_RE.match(tok):
        return ("symbol", tok)
    return None  # bare lowercase words etc.: too ambiguous to count


def extract_refs(doc: str) -> list[tuple[str, str, str]]:
    """All unique code references as (display, kind, needle)."""
    refs: dict[str, tuple[str, str]] = {}
    spans = []
    for m in BACKTICK_RE.finditer(doc):
        spans.append(m.span())
        got = _classify_backtick(m.group(1))
        if got:
            refs.setdefault(_clean(m.group(1)), got)
    # Blank out backticked spans, then sweep for bare paths.
    chars = list(doc)
    for a, b in spans:
        for i in range(a, b):
            chars[i] = " "
    bare = "".join(chars)
    for rx in (BARE_PATH_RE, BARE_FILE_RE):
        for m in rx.finditer(bare):
            tok = _clean(m.group(0))
            if tok and tok not in EXCLUDED:
                refs.setdefault(tok, ("path", tok))
    return [(disp, kind, needle)
            for disp, (kind, needle) in sorted(refs.items())]


# ── grounding ────────────────────────────────────────────────────────
def _build_index(repo: Path) -> list[str]:
    """Lowercased contents of every *.rs / *.toml in the checkout."""
    index = []
    for pattern in ("*.rs", "*.toml"):
        for f in sorted(repo.rglob(pattern)):
            try:
                index.append(f.read_text(errors="replace").lower())
            except OSError:
                continue
    return index


def _path_grounded(repo: Path, ref: str) -> bool:
    p = ref.lstrip("./")
    if p.startswith("repo/"):
        p = p[len("repo/"):]
    p = p.split("#")[0].split(":")[0].rstrip("/")
    if not p:
        return False
    if "*" in p:  # glob citation like `crates/*/src/lib.rs` or `*.rs`
        try:
            if next(repo.glob(p), None) is not None:
                return True
            return next(repo.glob(f"**/{p}"), None) is not None
        except ValueError:
            return False
    if (repo / p).exists():
        return True
    # Generosity: a crate-relative path missing the crates/ prefix.
    return (repo / "crates" / p).exists()


def _symbol_grounded(index: list[str], needle: str) -> bool:
    n = needle.lower()
    return any(n in content for content in index)


def check_grounding(repo: Path, doc: str) -> dict:
    refs = extract_refs(doc)
    index = _build_index(repo)
    grounded, ungrounded = [], []
    for disp, kind, needle in refs:
        ok = (_path_grounded(repo, needle) if kind == "path"
              else _symbol_grounded(index, needle))
        (grounded if ok else ungrounded).append(
            {"ref": disp, "kind": kind})
    total = len(refs)
    rate = 0.0 if total < MIN_REFS else len(grounded) / total
    return {"rate": round(rate, 4), "total_refs": total,
            "grounded": len(grounded), "ungrounded": ungrounded,
            "min_refs": MIN_REFS,
            "indexed_files": len(index)}


# ── fact checklist ───────────────────────────────────────────────────
def derive_ground_truth(repo: Path) -> dict:
    root = tomllib.loads((repo / "Cargo.toml").read_text())
    members = root.get("workspace", {}).get("members", [])
    crates, bins = [], []
    for member in members:
        manifest = repo / member / "Cargo.toml"
        if not manifest.is_file():
            continue
        data = tomllib.loads(manifest.read_text())
        name = data.get("package", {}).get("name")
        if name:
            crates.append(name)
        for bin_tbl in data.get("bin", []):
            if bin_tbl.get("name"):
                bins.append(bin_tbl["name"])
    return {"crates": crates, "bins": bins}


def _crate_mentioned(doc: str, doc_lower: str, name: str) -> bool:
    if name.lower() in doc_lower:
        return True
    # Short form ("core" for "leviath-core") counts ONLY backticked or
    # near the word "crate".
    short = name.split("-")[-1]
    if len(short) < 3:
        return False
    if re.search(rf"`{re.escape(short)}`", doc, re.IGNORECASE):
        return True
    for m in re.finditer(rf"\b{re.escape(short)}\b", doc_lower):
        window = doc_lower[max(0, m.start() - 40):m.end() + 40]
        if "crate" in window:
            return True
    return False


def check_checklist(repo: Path, doc: str) -> dict:
    truth = derive_ground_truth(repo)
    doc_lower = doc.lower()
    mentioned = [c for c in truth["crates"]
                 if _crate_mentioned(doc, doc_lower, c)]
    missing = [c for c in truth["crates"] if c not in mentioned]
    rate = len(mentioned) / len(truth["crates"]) if truth["crates"] else 0.0
    bins_mentioned = [
        b for b in truth["bins"]
        if re.search(rf"`{re.escape(b)}`", doc)
        or re.search(rf"\b{re.escape(b)}\b\s+(?:binary|command|cli)",
                     doc, re.IGNORECASE)]
    return {"rate": round(rate, 4), "crates": truth["crates"],
            "mentioned": mentioned, "missing": missing,
            "bins": truth["bins"], "bins_mentioned": bins_mentioned}


# ── coherence ────────────────────────────────────────────────────────
def check_coherence(doc: str, crates: list[str]) -> tuple[float | None, dict]:
    try:
        arms = json.loads((_QUALITY_DIR / "arms.json").read_text())
        label = arms["probes"]["grader_model"]
        grader_id = arms["models"][label]["id"]
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        return None, {"skipped": f"grader lookup failed: {exc}"}

    provider = grader_id.partition("/")[0]
    key_name = _KEY_FOR_PROVIDER.get(provider)
    keys = {k: os.environ.get(k, "") for k in _KEY_FOR_PROVIDER.values()}
    if not key_name or not keys.get(key_name):
        return None, {"skipped": f"no {key_name or provider} key in the "
                                 "environment; coherence excluded"}

    crate_list = ", ".join(crates)
    probe = {
        "question": ("Is this an accurate, coherent architecture "
                     "explanation of a Rust workspace whose crates are "
                     f"{crate_list}? Grade correct/partial/wrong."),
        "expected": "a coherent, accurate architecture explanation",
        "rubric": (
            "Grade the document as an onboarding architecture "
            "explanation, generously. correct: coherent, reads as an "
            "accurate description of how a workspace with these crates "
            "fits together (crate responsibilities, end-to-end flow, "
            "key abstractions, how pieces communicate); minor "
            "imprecision is fine. partial: broadly plausible and "
            "on-topic but shallow, or with a few claims that look "
            "wrong or confused. wrong: incoherent, off-topic, mostly "
            "generic boilerplate, or fundamentally misrepresents the "
            "workspace structure. Do NOT penalize omissions of minor "
            "crates or brevity within the stated scope."),
    }
    try:
        verdict = evaluator.grade_answer(
            probe, doc, grader_model_id=grader_id, keys=keys)
    except Exception as exc:  # offline, provider error: exclude
        return None, {"skipped": f"grader call failed: {exc}",
                      "grader_model": grader_id}
    if verdict.get("method") == "grading_error":
        return None, {"skipped": "grading_error from the grader; "
                                 "coherence excluded",
                      "grader_model": grader_id,
                      "reasoning": verdict.get("reasoning")}
    return float(verdict["score"]), {
        "grader_model": grader_id, "grade": verdict.get("grade"),
        "reasoning": verdict.get("reasoning")}


# ── entry point ──────────────────────────────────────────────────────
def verify(task_dir: Path, workdir: Path, artifacts_dir: Path,
           answer) -> dict:
    workdir = Path(workdir)
    artifacts_dir = Path(artifacts_dir)
    repo = workdir / "repo"

    doc_file = workdir / DOC_NAME
    if doc_file.is_file() and doc_file.read_text().strip():
        doc, doc_source = doc_file.read_text(), DOC_NAME
    else:
        doc, doc_source = str(answer or ""), "answer text (file missing)"

    grounding = check_grounding(repo, doc)
    checklist = check_checklist(repo, doc)
    coherence, coherence_detail = check_coherence(doc, checklist["crates"])

    artifacts_dir.mkdir(parents=True, exist_ok=True)
    (artifacts_dir / "grounding.json").write_text(json.dumps(
        {"doc_source": doc_source, **grounding}, indent=2) + "\n")

    g, c = grounding["rate"], checklist["rate"]
    if coherence is None:
        denom = WEIGHTS["grounding"] + WEIGHTS["checklist"]
        score = (WEIGHTS["grounding"] * g + WEIGHTS["checklist"] * c) / denom
    else:
        score = (WEIGHTS["grounding"] * g + WEIGHTS["checklist"] * c
                 + WEIGHTS["coherence"] * coherence)

    functional_pass = (g >= GROUNDING_BAR and c >= CHECKLIST_BAR
                       and (coherence is None or coherence >= COHERENCE_BAR))

    return {
        "functional_pass": bool(functional_pass),
        "score": round(score, 4),
        "detail": {
            "doc_source": doc_source,
            "word_count": len(doc.split()),
            "grounding": {k: grounding[k] for k in
                          ("rate", "total_refs", "grounded")}
            | {"ungrounded": [u["ref"] for u in grounding["ungrounded"]]},
            "checklist": {k: checklist[k] for k in
                          ("rate", "mentioned", "missing",
                           "bins", "bins_mentioned")},
            "coherence": {"score": coherence, **coherence_detail},
            "bars": {"grounding": GROUNDING_BAR,
                     "checklist": CHECKLIST_BAR,
                     "coherence": COHERENCE_BAR},
            "weights": WEIGHTS,
            "renormalized_without_coherence": coherence is None,
        },
    }
