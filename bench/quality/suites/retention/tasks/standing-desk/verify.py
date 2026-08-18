"""Mechanical verification for standing-desk: twelve phase files.

The agent wrote answers/phase-NN.md into its WORKDIR as the session
progressed; each phase's lines are compared against the generator's
key. The score is the mean phase score, but the chart-bearing split is
dependent vs independent phases: independent phases (no backward
reference) measure capability, dependent ones measure whether the
agent still HAS its own earlier results - the gap between the two
series is the retention metric.

Wrong lines are classified, never pooled:
- stale_dependency: the value matches a generator-registered
  alternative - the answer an agent gets by propagating a WRONG memory
  of an earlier phase (booking the other caterer, forgetting the late
  additions). Wrong, but a memory failure, not an invention.
- fabricated: an entity-shaped value (code or speaker name) that
  exists nowhere in the corpus universe. Prose or numbers are never
  counted as fabrication (shape gate, as in the hallucination suite).
- investigation_errors: everything else wrong-but-real.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

FUNCTIONAL_BAR = 0.6

# Keys whose values are unordered lists (order-normalized before
# comparison). Semicolon lists carry names; comma lists carry
# CODE=value pairs.
SEMI_LIST_KEYS = {"keynotes", "day1", "day2", "day3"}
PAIR_LIST_KEYS = {"hotels", "shuttles"}
# Keys whose value starts with an entity code / name (the fabrication
# gate applies to these).
CODE_KEYS = {"venue": "venues", "caterer": "caterers",
             "av_vendor": "av_vendors", "insurance_tier":
             "insurance_tiers", "shortlist_1": "caterers",
             "shortlist_2": "caterers"}
NAME_KEYS = SEMI_LIST_KEYS
PAIR_KEYS_UNIVERSE = {"hotels": "hotels", "shuttles": "hotels"}

_CODE = re.compile(r"^[A-Z]{2,5}-\w{1,4}$")


def _norm_money(v: str) -> str:
    return v.replace(",", "").replace(" ", "")


def _norm(key: str, value: str) -> str:
    v = " ".join(value.split())
    if key in SEMI_LIST_KEYS:
        return ";".join(sorted(p.strip() for p in v.split(";")
                               if p.strip()))
    if key in PAIR_LIST_KEYS:
        return ",".join(sorted(p.strip() for p in v.split(",")
                               if p.strip()))
    if "$" in v:
        return _norm_money(v)
    return v


def _parse_phase_file(text: str) -> dict[str, str]:
    out = {}
    for line in text.splitlines():
        line = line.strip().strip("`")
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower().lstrip("-# ").strip()
        if key and value.strip():
            out[key] = value.strip()
    return out


def verify(task_dir: Path, workdir: Path, artifacts_dir: Path,
           answer) -> dict:
    key = json.loads((task_dir / "answers.json").read_text())
    phases, registry = key["phases"], key["registry"]
    universe = registry["code_universe"]
    alts = registry.get("known_alternatives", {})

    counts = {"fabrications": 0, "stale_dependency": 0,
              "investigation_errors": 0, "phase_missing": 0}
    phase_scores: list[float] = []
    detail_phases: dict[str, dict] = {}

    def classify_wrong(nn: str, k: str, got: str) -> str:
        for altv in (alts.get(nn, {}).get(k) or []):
            if _norm(k, altv) == _norm(k, got):
                return "stale_dependency"
        tokens: list[str] = []
        if k in CODE_KEYS:
            tokens = [(got.split() or [""])[0]]
            pool = set(universe[CODE_KEYS[k]])
        elif k in NAME_KEYS:
            tokens = [p.strip() for p in got.split(";") if p.strip()
                      and p.strip().lower() != "none"]
            pool = set(universe["speakers"])
        elif k in PAIR_KEYS_UNIVERSE:
            tokens = [p.split("=")[0].strip() for p in got.split(",")
                      if p.strip()]
            pool = set(universe[PAIR_KEYS_UNIVERSE[k]])
        else:
            return "investigation_errors"
        for tok in tokens:
            shaped = bool(_CODE.match(tok)) or (
                k in NAME_KEYS and len(tok.split()) == 2
                and all(w[:1].isupper() for w in tok.split()))
            if shaped and tok not in pool:
                return "fabrications"
        return "investigation_errors"

    for nn in sorted(phases):
        expected = phases[nn]["lines"]
        path = Path(workdir) / "answers" / f"phase-{nn}.md"
        pd: dict = {"present": path.is_file()}
        if not path.is_file():
            counts["phase_missing"] += 1
            phase_scores.append(0.0)
            pd["score"] = 0.0
            detail_phases[nn] = pd
            continue
        got = _parse_phase_file(path.read_text())
        hits = 0
        wrong: dict[str, dict] = {}
        for k, want in expected.items():
            g = got.get(k.lower(), "")
            if g and _norm(k, g) == _norm(k, want):
                hits += 1
            else:
                label = (classify_wrong(nn, k, g) if g
                         else "investigation_errors")
                counts[label] += 1
                wrong[k] = {"expected": want, "got": g,
                            "classified": label}
        score = hits / len(expected)
        phase_scores.append(score)
        pd["score"] = round(score, 4)
        if wrong:
            pd["wrong"] = wrong
        detail_phases[nn] = pd

    order = sorted(phases)
    dep_idx = [i for i, nn in enumerate(order)
               if phases[nn]["dependent"]]
    ind_idx = [i for i, nn in enumerate(order)
               if not phases[nn]["dependent"]]
    dep_scores = [phase_scores[i] for i in dep_idx]
    ind_scores = [phase_scores[i] for i in ind_idx]

    total = sum(phase_scores) / len(phase_scores)
    summary_text = str(answer or "")
    summary_ok = sum(1 for nn in order
                     if f"phase-{nn}" in summary_text) >= 8

    return {
        "functional_pass": total >= FUNCTIONAL_BAR,
        "score": round(total, 4),
        "detail": {
            "phases": detail_phases,
            "phase_scores": [round(s, 4) for s in phase_scores],
            "dependent_phase_scores": [round(s, 4)
                                       for s in dep_scores],
            "independent_phase_scores": [round(s, 4)
                                         for s in ind_scores],
            "dependent_mean": round(sum(dep_scores)
                                    / len(dep_scores), 4),
            "independent_mean": round(sum(ind_scores)
                                      / len(ind_scores), 4),
            "summary_ok": summary_ok,
            "summary": counts,
        },
    }
