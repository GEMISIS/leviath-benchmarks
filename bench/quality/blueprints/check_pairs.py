#!/usr/bin/env python3
"""Assert the benchmark agents satisfy the rules that make scores mean
something (blueprints/AGENTS.md). Run before any freeze; exits
non-zero on any violation.

Policy, on every blueprint:

- exactly one model per stage (no fallback chains)
- no blocking/human-in-the-loop tools or opt-ins, or prompt text
  steering toward asking a person

No benchmark leakage, on every blueprint:

- no prompt text naming a suite, dataset, grader, or split. Agents may
  know their job; they may not know the test.

Pair invariants - the ablation's claim is "same tools, same
permissions, same budget - only the structure removed":

- identical [tool_permissions]
- flat work tools == union of structured stages' tools minus context_*
- flat total iteration budget == sum of structured stages' budgets
- flat regions are exactly {task, conversation, error_report}
- same [compaction] model when the structured copy has one
"""
from __future__ import annotations

import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from conduct import ASK_NOTE, CONDUCT  # noqa: E402
from make_askable import (ASKABLE, SESSION, SESSION_ANSWER_HINT,  # noqa: E402
                          SESSION_NOTE, SESSION_REVISITS)
from make_flat import COMPACT_VARIANTS, PAIRS, _excluded_tool  # noqa: E402
from make_readonly import (DROPPED_TOOLS, READONLY_FLATS,  # noqa: E402
                           READONLY_STRUCTURED)


def load(name: str) -> dict:
    return tomllib.loads((HERE / name / "agent.leviath").read_text())


def check_policy(name: str) -> list[str]:
    """The benchmark policy, asserted: single-model stages, no HITL.

    The one sanctioned exception: -askable variants (the ask test)
    carry exactly ask_user_text on exactly the stage make_askable.py
    names, for every arm symmetrically; check_askable() holds them to
    their source byte-for-byte beyond that.
    """
    doc = load(name)
    problems = []
    ask_stage = (ASKABLE.get(name.removesuffix("-askable"))
                 if name.endswith("-askable") else None)
    if name.endswith("-session"):
        # The session condition inherits the askable exemption: same
        # tool, same stage; check_session() holds it to its askable
        # source beyond the loop budget and note.
        ask_stage = SESSION.get(f'{name.removesuffix("-session")}-askable')
    for sname, stage in doc.get("stages", {}).items():
        models = (stage.get("model") or {}).get("models") or []
        if len(models) != 1:
            problems.append(f"{name}/{sname}: {len(models)} models in "
                            "list (policy: exactly 1, no fallbacks)")
        blocking = [t for t in stage.get("available_tools", [])
                    if _excluded_tool(t) and not t.startswith("context_")]
        allowed = ["ask_user_text"] if sname == ask_stage else []
        if blocking != allowed:
            problems.append(f"{name}/{sname}: blocking tools {blocking}")
        if stage.get("allow_blocking_tools") and sname != ask_stage:
            problems.append(f"{name}/{sname}: allow_blocking_tools set")
        # The fairness control: every LLM request in every arm sees the
        # same evidence-conduct block exactly once in its system prompt,
        # so the arms differ in structure, never in stated discipline.
        n_conduct = stage.get("system_prompt", "").count(CONDUCT)
        if n_conduct != 1:
            problems.append(f"{name}/{sname}: conduct block appears "
                            f"{n_conduct} times (policy: exactly once; "
                            "run add_conduct.py / regenerate)")
    raw = (HERE / name / "agent.leviath").read_text()
    if "ask_user_confirm" in raw:
        problems.append(f"{name}: prompt text still references "
                        "ask_user_confirm")
    for i, line in enumerate(raw.splitlines(), 1):
        # The policy header is the one place allowed to say the word.
        if "fallback" in line.lower() and "BENCHMARK POLICY" not in line:
            problems.append(f"{name}:{i}: text describes fallback models, "
                            "which the policy removed")
    return problems


# Names of the suites, datasets, graders, and splits this repo runs.
# An agent that mentions any of them is tuned to the test rather than
# to its job, which is exactly what rule 1 in AGENTS.md forbids.
LEAKAGE = (
    "terminal-bench", "terminalbench", "frontier-bench", "frontierbench",
    "deep-swe", "deepswe", "swe-bench", "swebench", "dabstep", "gaia",
    "loghub", "harbor", "pier", "held-out", "heldout", "public split",
    "test set", "leaderboard", "grader", "verifier",
)


def check_no_leakage(name: str) -> list[str]:
    """Agents may know their job; they may not know the test."""
    problems = []
    for i, line in enumerate(
            (HERE / name / "agent.leviath").read_text().splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue  # provenance/policy headers, not agent text
        low = line.lower()
        for term in LEAKAGE:
            if term in low:
                problems.append(f"{name}:{i}: benchmark leakage {term!r} "
                                "in agent text")
    return problems


def check_pair(structured_name: str, flat_name: str) -> list[str]:
    s, f = load(structured_name), load(flat_name)
    problems = []

    if s.get("tool_permissions") != f.get("tool_permissions"):
        problems.append("tool_permissions differ")

    s_tools = {t for st in s["stages"].values()
               for t in st.get("available_tools", [])
               if not _excluded_tool(t)}
    f_tools = set(f["stages"]["work"].get("available_tools", []))
    if s_tools != f_tools:
        problems.append(f"tool union mismatch: structured-only "
                        f"{sorted(s_tools - f_tools)}, flat-only "
                        f"{sorted(f_tools - s_tools)}")

    s_budget = sum(int(st.get("max_iterations", 10))
                   for st in s["stages"].values())
    f_budget = sum(int(st.get("max_iterations", 10))
                   for st in f["stages"].values())
    # The flat work stage carries the whole structured budget; its
    # output stage matches the structured output stage's cap.
    s_output = sum(int(st.get("max_iterations", 10))
                   for st in s["stages"].values()
                   if st.get("mode") == "output")
    if f["stages"]["work"]["max_iterations"] != s_budget:
        problems.append(
            f"iteration budget: flat work "
            f"{f['stages']['work']['max_iterations']} != structured sum "
            f"{s_budget}")
    del f_budget, s_output

    f_regions = set(f.get("context", {}).get("regions", {}))
    expected = {"task", "conversation", "error_report",
                "stage_instructions"}
    if f_regions != expected:
        problems.append(f"flat regions {sorted(f_regions)} != "
                        f"{sorted(expected)}")

    # An agent's own tools/*.rhai are part of it: a granted tool whose
    # script is missing makes the blueprint invalid, so the flat copy
    # must carry the same scripts byte-for-byte.
    def scripts(name: str) -> dict[str, bytes]:
        d = HERE / name / "tools"
        return {p.name: p.read_bytes()
                for p in sorted(d.glob("*")) if p.is_file()} \
            if d.is_dir() else {}

    s_scripts, f_scripts = scripts(structured_name), scripts(flat_name)
    if s_scripts != f_scripts:
        problems.append(
            f"tools/ differ: structured {sorted(s_scripts)}, flat "
            f"{sorted(f_scripts)} (regenerate with make_flat.py)")

    s_comp = s.get("compaction")
    f_comp = f.get("compaction")
    if s_comp != f_comp:
        problems.append(f"compaction differs: {s_comp} vs {f_comp}")

    return problems


def check_compact_variant(flat_name: str, compacting_name: str) -> list[str]:
    """The strong-baseline invariant: flat and flat-compacting differ in
    the conversation region's overflow strategy and NOTHING else."""
    f, c = load(flat_name), load(compacting_name)
    problems = []

    def masked(doc: dict) -> dict:
        doc = json_roundtrip(doc)
        doc["agent"].pop("name", None)
        doc["agent"].pop("description", None)
        conv = doc.get("context", {}).get("regions", {}).get("conversation")
        if isinstance(conv, dict):
            for key in ("strategy", "overflow", "compact_count"):
                conv.pop(key, None)
        return doc

    if masked(f) != masked(c):
        problems.append("flat and compacting variants differ beyond the "
                        "conversation overflow strategy (regenerate with "
                        "make_flat.py)")
    conv = c.get("context", {}).get("regions", {}).get("conversation", {})
    if conv.get("strategy") != "compact" or "compact_count" not in conv:
        problems.append("compacting variant's conversation is not "
                        f"strategy=compact with a compact_count: {conv}")
    return problems


def check_askable(source_name: str, stage_name: str) -> list[str]:
    """An askable variant is its source plus the ask channel on one
    stage and NOTHING else - three insertions, byte-accountable."""
    askable_name = f"{source_name}-askable"
    if not (HERE / askable_name / "agent.leviath").is_file():
        return [f"{askable_name}: missing (regenerate with "
                "make_askable.py)"]
    s, a = load(source_name), load(askable_name)
    problems = []

    stage = a.get("stages", {}).get(stage_name, {})
    s_stage = s.get("stages", {}).get(stage_name, {})
    a_tools = list(stage.get("available_tools", []))
    if a_tools != s_stage.get("available_tools", []) + ["ask_user_text"]:
        problems.append(f"{askable_name}/{stage_name}: tools are not "
                        "source + ask_user_text")
    note_counts = [st.get("system_prompt", "").count(ASK_NOTE)
                   for st in a["stages"].values()]
    if sum(note_counts) != 1 or \
            stage.get("system_prompt", "").count(ASK_NOTE) != 1:
        problems.append(f"{askable_name}: ask note must appear exactly "
                        f"once, in {stage_name} (counts {note_counts})")
    if not stage.get("system_prompt", "").startswith(
            s_stage.get("system_prompt", "").rstrip()):
        problems.append(f"{askable_name}/{stage_name}: prompt is not "
                        "the source prompt plus the note")

    # The permission table may differ in exactly one direction: "ask"
    # relaxed to "allow" (what --yolo does inline on every other cell).
    for tool, perm in a.get("tool_permissions", {}).items():
        src_perm = s.get("tool_permissions", {}).get(tool)
        if perm != src_perm and not (src_perm == "ask"
                                     and perm == "allow"):
            problems.append(f"{askable_name}: tool_permissions[{tool}] "
                            f"= {perm!r}, source {src_perm!r} (only "
                            "ask->allow is sanctioned)")

    def masked(doc: dict) -> dict:
        doc = json_roundtrip(doc)
        doc.pop("tool_permissions", None)
        st = doc["stages"].get(stage_name, {})
        st.pop("allow_blocking_tools", None)
        st.pop("available_tools", None)
        st.pop("system_prompt", None)
        return doc

    if masked(s) != masked(a):
        problems.append(f"{askable_name}: differs from {source_name} "
                        f"beyond the ask channel on {stage_name} "
                        "(regenerate with make_askable.py)")
    return problems


def check_session(askable_name: str, ask_stage: str) -> list[str]:
    """The session variant is the askable variant plus the raised
    revisit budgets and the session note - two insertions, nothing
    else. A drifted session variant would make the session cells an
    uncontrolled comparison."""
    session_name = (askable_name.removesuffix("-askable") + "-session")
    if not (HERE / session_name / "agent.leviath").is_file():
        return [f"{session_name}: missing (regenerate with "
                "make_askable.py)"]
    a, se = load(askable_name), load(session_name)
    problems = []
    stage = se.get("stages", {}).get(ask_stage, {})
    a_stage = a.get("stages", {}).get(ask_stage, {})
    if SESSION_NOTE not in stage.get("system_prompt", ""):
        problems.append(f"{session_name}/{ask_stage}: session note "
                        "missing")
    if not stage.get("system_prompt", "").startswith(
            a_stage.get("system_prompt", "").rstrip()):
        problems.append(f"{session_name}/{ask_stage}: prompt is not "
                        "the askable prompt plus the session note")

    want_hint = SESSION_ANSWER_HINT[1].split('"', 1)[1].rstrip('"')
    got_hint = (stage.get("transitions", {}).get("answer", {})
                .get("hint"))
    if got_hint != want_hint:
        problems.append(f"{session_name}/{ask_stage}: answer-edge hint "
                        f"{got_hint!r} != {want_hint!r}")

    def masked(doc: dict) -> dict:
        doc = json_roundtrip(doc)
        for name, st in doc["stages"].items():
            if name in SESSION_REVISITS:
                st.pop("max_revisits", None)
        st = doc["stages"].get(ask_stage, {})
        st.pop("system_prompt", None)
        st.get("transitions", {}).get("answer", {}).pop("hint", None)
        return doc

    for name, want in SESSION_REVISITS.items():
        got = se.get("stages", {}).get(name, {}).get("max_revisits")
        if got != want:
            problems.append(f"{session_name}/{name}: max_revisits "
                            f"{got} != {want}")
    if masked(a) != masked(se):
        problems.append(f"{session_name}: differs from {askable_name} "
                        "beyond revisits + session note (regenerate "
                        "with make_askable.py)")
    return problems


def check_readonly() -> list[str]:
    """The read-only condition's invariants: no shell/writes anywhere,
    the script stage gone, and the flat/structured symmetry (tool
    union, iteration budget) holding within the condition."""
    problems = []
    docs = {}
    for name in [READONLY_STRUCTURED] + READONLY_FLATS:
        path = HERE / f"{name}-readonly" / "agent.leviath"
        if not path.is_file():
            return [f"{name}-readonly: missing (regenerate with "
                    "make_readonly.py)"]
        docs[name] = load(f"{name}-readonly")
    s = docs[READONLY_STRUCTURED]
    if "script" in s["stages"]:
        problems.append("readonly structured still has a script stage")
    for name, doc in docs.items():
        for sname, stage in doc["stages"].items():
            bad = [t for t in stage.get("available_tools", [])
                   if t in DROPPED_TOOLS]
            if bad:
                problems.append(f"{name}-readonly/{sname}: dropped "
                                f"tools survived: {bad}")
    s_tools = {t for st in s["stages"].values()
               for t in st.get("available_tools", [])
               if not _excluded_tool(t)}
    s_budget = sum(int(st.get("max_iterations", 10))
                   for st in s["stages"].values())
    for flat in READONLY_FLATS:
        f = docs[flat]
        f_tools = set(f["stages"]["work"].get("available_tools", []))
        if f_tools != s_tools:
            problems.append(
                f"{flat}-readonly tool union mismatch: structured-only "
                f"{sorted(s_tools - f_tools)}, flat-only "
                f"{sorted(f_tools - s_tools)}")
        if f["stages"]["work"]["max_iterations"] != s_budget:
            problems.append(
                f"{flat}-readonly budget "
                f"{f['stages']['work']['max_iterations']} != readonly "
                f"structured sum {s_budget}")
    return problems


def json_roundtrip(doc: dict) -> dict:
    import copy
    return copy.deepcopy(doc)


def variants() -> list[str]:
    """Generated mixes: same shape, one model per stage, still policed."""
    known = (set(PAIRS) | set(PAIRS.values()) | set(COMPACT_VARIANTS.values()))
    return sorted(d.name for d in HERE.iterdir()
                  if d.is_dir() and (d / "agent.leviath").is_file()
                  and d.name not in known)


def main() -> int:
    failed = False
    for name in variants():
        problems = check_policy(name) + check_no_leakage(name)
        if problems:
            failed = True
            print(f"{name}:")
            for p in problems:
                print(f"  FAIL {p}")
        else:
            print(f"{name}: OK (mix)")
    for structured_name, flat_name in PAIRS.items():
        problems = (check_policy(structured_name)
                    + check_policy(flat_name)
                    + check_no_leakage(structured_name)
                    + check_no_leakage(flat_name)
                    + check_pair(structured_name, flat_name))
        if problems:
            failed = True
            print(f"{structured_name} vs {flat_name}:")
            for p in problems:
                print(f"  FAIL {p}")
        else:
            print(f"{structured_name} vs {flat_name}: OK")
    for structured_name, flat_name in PAIRS.items():
        compacting_name = COMPACT_VARIANTS[flat_name]
        if not (HERE / compacting_name / "agent.leviath").is_file():
            failed = True
            print(f"{compacting_name}: FAIL missing (regenerate with "
                  "make_flat.py)")
            continue
        problems = (check_policy(compacting_name)
                    + check_no_leakage(compacting_name)
                    + check_pair(structured_name, compacting_name)
                    + check_compact_variant(flat_name, compacting_name))
        if problems:
            failed = True
            print(f"{flat_name} vs {compacting_name}:")
            for p in problems:
                print(f"  FAIL {p}")
        else:
            print(f"{flat_name} vs {compacting_name}: OK (compacting)")
    for source_name, stage_name in ASKABLE.items():
        problems = check_askable(source_name, stage_name)
        if problems:
            failed = True
            print(f"{source_name} vs {source_name}-askable:")
            for p in problems:
                print(f"  FAIL {p}")
        else:
            print(f"{source_name} vs {source_name}-askable: OK (askable)")
    for askable_name, ask_stage in SESSION.items():
        problems = check_session(askable_name, ask_stage)
        if problems:
            failed = True
            print(f"{askable_name} vs session:")
            for p in problems:
                print(f"  FAIL {p}")
        else:
            print(f"{askable_name} vs session: OK (session)")
    problems = check_readonly()
    if problems:
        failed = True
        print("readonly condition:")
        for p in problems:
            print(f"  FAIL {p}")
    else:
        print("readonly condition: OK (no shell/writes, symmetric)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
