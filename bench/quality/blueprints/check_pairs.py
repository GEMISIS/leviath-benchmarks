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

from make_flat import PAIRS, _excluded_tool  # noqa: E402


def load(name: str) -> dict:
    return tomllib.loads((HERE / name / "agent.leviath").read_text())


def check_policy(name: str) -> list[str]:
    """The benchmark policy, asserted: single-model stages, no HITL."""
    doc = load(name)
    problems = []
    for sname, stage in doc.get("stages", {}).items():
        models = (stage.get("model") or {}).get("models") or []
        if len(models) != 1:
            problems.append(f"{name}/{sname}: {len(models)} models in "
                            "list (policy: exactly 1, no fallbacks)")
        blocking = [t for t in stage.get("available_tools", [])
                    if _excluded_tool(t) and not t.startswith("context_")]
        if blocking:
            problems.append(f"{name}/{sname}: blocking tools {blocking}")
        if stage.get("allow_blocking_tools"):
            problems.append(f"{name}/{sname}: allow_blocking_tools set")
    raw = (HERE / name / "agent.leviath").read_text()
    if "ask_user_confirm" in raw:
        problems.append(f"{name}: prompt text still references "
                        "ask_user_confirm")
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
    if f_regions != {"task", "conversation", "error_report"}:
        problems.append(f"flat regions {sorted(f_regions)} != "
                        "[task, conversation, error_report]")

    s_comp = s.get("compaction")
    f_comp = f.get("compaction")
    if s_comp != f_comp:
        problems.append(f"compaction differs: {s_comp} vs {f_comp}")

    return problems


def main() -> int:
    failed = False
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
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
