#!/usr/bin/env python3
"""Apply the benchmark policy to the structured blueprints, in place.

The blueprints in this directory are BENCHMARK-OWNED agents. They are
derived from the upstream bundled agents once (freeze_from_upstream.py
records the commit), then this script applies the benchmark policy so
the agents that run are exactly the agents this repo defines - stable
across upstream drift, and reproducible from the repo alone:

1. **Exactly one model per stage - no fallback chains.** Each stage's
   model list is collapsed to its first entry (the upstream author's
   primary choice per stage, so the native mix keeps upstream's
   cheap-stage/heavy-stage intent). A fallback firing mid-benchmark
   would silently change what was measured; now it cannot.
2. **No human in the loop.** Blocking tools (ask_user_*,
   present_for_review, edit_document) are removed from every stage's
   available_tools along with their allow_blocking_tools opt-ins, and
   the one prompt passage that steers toward asking a person is
   replaced with an explicit unattended-run instruction.

Pipeline: freeze_from_upstream.py -> apply_bench_policy.py ->
make_flat.py -> check_pairs.py (which asserts this policy held). Run
deliberately and review the diff; any change means a new freeze tag.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STRUCTURED = ["coder-bench", "analyst-bench", "researcher-bench",
              "loganalyzer-bench"]

BLOCKING = ("ask_user_confirm", "ask_user_choice", "ask_user_input",
            "present_for_review", "edit_document")

_MODEL_LINE = re.compile(
    r'^(model = \{ models = \[)(\{[^}]*\})(?:, \{[^}]*\})*(\] \})',
    re.M)

_HITL_PROMPT = (
    "If you hit a destructive or hard-to-reverse action you're unsure "
    "about, use\nask_user_confirm before proceeding. Otherwise work "
    "autonomously.")
_UNATTENDED_PROMPT = (
    "This is an unattended run: there is no human to ask. Work "
    "autonomously,\nand take only the actions the task itself requires.")

POLICY_MARK = "# BENCHMARK POLICY APPLIED (apply_bench_policy.py):"


def apply(text: str) -> str:
    # 1. Collapse every stage model list to its first entry.
    text = _MODEL_LINE.sub(r"\1\2\3", text)

    # 2a. Remove blocking tools from available_tools arrays.
    def clean_tools(match: re.Match) -> str:
        tools = re.findall(r'"([^"]+)"', match.group(1))
        kept = [t for t in tools if t not in BLOCKING]
        return ("available_tools = ["
                + ", ".join(f'"{t}"' for t in kept) + "]")
    text = re.sub(r'available_tools = \[([^\]]*)\]', clean_tools, text)

    # 2b. Drop allow_blocking_tools opt-ins and the comment block that
    # documents them (the lines immediately above the opt-in).
    lines = text.splitlines()
    out: list[str] = []
    for line in lines:
        if line.strip() == "allow_blocking_tools = true":
            while out and out[-1].lstrip().startswith("#"):
                out.pop()
            continue
        out.append(line)
    text = "\n".join(out) + ("\n" if text.endswith("\n") else "")

    # 2c. Replace the ask-a-person prompt passage.
    text = text.replace(_HITL_PROMPT, _UNATTENDED_PROMPT)

    # 3. Mark the file so the check can prove policy was applied.
    if POLICY_MARK not in text:
        header_end = text.index("\n\n")
        text = (text[:header_end]
                + f"\n{POLICY_MARK} exactly one model per stage "
                "(no fallbacks); no human-in-the-loop tools or prompts."
                + text[header_end:])
    return text


def main() -> int:
    for name in STRUCTURED:
        path = HERE / name / "agent.leviath"
        original = path.read_text()
        transformed = apply(original)
        path.write_text(transformed)
        n_models = len(re.findall(r"models = \[", transformed))
        print(f"{name}: policy applied ({n_models} stage model lists, "
              "all single-entry)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
