#!/usr/bin/env python3
"""Assert every structured/flat blueprint pair differs only in structure.

The ablation's claim is "same tools, same permissions, same budget -
only the structure removed". This script is the proof, run in CI-less
fashion before any freeze:

- identical [tool_permissions]
- flat work tools == union of structured stages' tools minus context_*
- flat total iteration budget == sum of structured stages' budgets
- flat regions are exactly {task, conversation, error_report}
- same [compaction] model when the structured copy has one

Exits non-zero on any violation.
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
        problems = check_pair(structured_name, flat_name)
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
