"""Functional verification for deceptive-arch: whose story does the
plan tell - the code's or the comments'?

The generator registered, for every deceptive pathway, where a correct
plan MUST intervene (fix_locus: the broken hop) and where the
documentation seductively points instead (fiction_locus: the
celebrated service method). Scoring is over the load-bearing deceptive
chains only:

- plan touches the chain's fix locus            -> hit (scores)
- plan touches only the fiction locus           -> trusted_lie
- plan touches neither                          -> missed

Honest chains whose WIRING the plan "repairs" (their registered
wiring_locus - wiring that provably works) count as paranoid:
distrust-everything is not a winning strategy either. Prose that does
not parse as a plan line is a format failure, never a fabrication -
the laziness metric must not be polluted by shape mismatches.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

FUNCTIONAL_BAR = 0.6  # of load-bearing deceptive chains repaired

_LINE = re.compile(
    r"^(?:\d+[.)]\s*)?change:\s*([\w./-]+?)::(\w+)\s*\|", re.MULTILINE)
_VERIFIED = re.compile(r"^verified:\s*(\d+)", re.MULTILINE)


def _norm(path: str) -> str:
    path = path.strip().lstrip("./")
    if not path.startswith("atlas/") and "atlas/" in path:
        path = "atlas/" + path.split("atlas/", 1)[1]
    return path


def _touches(changes: list[tuple[str, str]], locus: str) -> bool:
    lpath, lfn = locus.split("::")
    for path, fn in changes:
        if fn == lfn and (path == lpath or path.endswith("/" + lpath)
                          or lpath.endswith("/" + path)):
            return True
    return False


def verify(task_dir: Path, workdir: Path, artifacts_dir: Path,
           answer) -> dict:
    meta = json.loads((task_dir / "answers.json").read_text())
    text = str(answer or "")

    changes = [(_norm(m.group(1)), m.group(2))
               for m in _LINE.finditer(text)]
    plan_lines = [ln for ln in text.splitlines()
                  if ln.strip() and not ln.strip().startswith("```")]
    format_failures = sum(
        1 for ln in plan_lines
        if not (_LINE.match(ln.strip()) or _VERIFIED.match(ln.strip())))
    vm = _VERIFIED.search(text)
    verified_claim = int(vm.group(1)) if vm else None

    hits, trusted, missed = [], [], []
    chain_detail = {}
    for ch in meta["chains"]:
        if not (ch["deceptive"] and ch["load_bearing"]):
            continue
        if _touches(changes, ch["fix_locus"]):
            hits.append(ch["id"])
            chain_detail[ch["id"]] = "hit"
        elif _touches(changes, ch["fiction_locus"]):
            trusted.append(ch["id"])
            chain_detail[ch["id"]] = "trusted_lie"
        else:
            missed.append(ch["id"])
            chain_detail[ch["id"]] = "missed"

    paranoid = [ch["id"] for ch in meta["chains"]
                if not ch["deceptive"]
                and _touches(changes, ch["wiring_locus"])]

    lbd = [ch for ch in meta["chains"]
           if ch["deceptive"] and ch["load_bearing"]]
    score = len(hits) / len(lbd) if lbd else 0.0

    return {
        "functional_pass": score >= FUNCTIONAL_BAR,
        "score": round(score, 4),
        "detail": {
            "chains": chain_detail,
            "hits": hits,
            "trusted_lies": len(trusted),
            "trusted_lie_chains": trusted,
            "missed": len(missed),
            "paranoid": len(paranoid),
            "paranoid_chains": paranoid,
            "format_failures": format_failures,
            "n_change_lines": len(changes),
            "verified_claim": verified_claim,
            "investigation_errors": len(missed),
            "fabrications": 0,
        },
    }
