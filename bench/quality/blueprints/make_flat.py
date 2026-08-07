#!/usr/bin/env python3
"""Generate the flat-context counterpart of each frozen blueprint.

The flat arm is the ablation baseline: same binary, same tools, same
permissions - only the structure removed. Concretely:

- one working stage plus one output stage, instead of the structured
  stage graph;
- a single large sliding-window conversation region (the classic
  truncating window today's setups use; typed conversation entries
  require a sliding window region, so this is also the only valid flat
  layout), instead of per-purpose regions;
- the union of the structured stages' tools, minus the context_* region
  tools (there are no regions to route into);
- an iteration budget equal to the SUM of the structured stages' caps,
  so neither arm gets more turns than the other;
- the same [tool_permissions] table and the same [compaction] model.

The single system prompt describes the same workflow as the structured
stages without referencing region mechanics. Outputs are committed and
frozen; check_pairs.py asserts the invariants above hold for every
pair.

Usage:
    python3 make_flat.py
"""
from __future__ import annotations

import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent

PAIRS = {
    "coder-bench": "flat-coder",
    "analyst-bench": "flat-analyst",
    "researcher-bench": "flat-researcher",
    "loganalyzer-bench": "flat-loganalyzer",
}

# One working prompt per role: the structured agent's workflow in plain
# terms, no region mechanics. Kept deliberately competent - the flat arm
# is a baseline, not a strawman.
WORK_PROMPTS = {
    "flat-coder": """
Complete the coding task described in `task`.

Work the way a careful engineer works: first read the relevant code and
understand the existing structure, then plan briefly, then implement in
small verified steps. Run the code or its tests after each meaningful
change and fix what breaks. Before finishing, review your changes as a
whole - correctness, edge cases, consistency with the surrounding code -
and make sure everything you changed actually runs.
""",
    "flat-analyst": """
Complete the data-analysis task described in `task`.

Inspect the available data files first (formats, columns, sizes), then
compute the answer with scripts rather than eyeballing - write small
commands or programs, check their output, and build up to the result.
Quantify everything and double-check any number you are about to report
by recomputing it a second way when feasible. State the final answer
exactly in the format the task asks for.
""",
    "flat-researcher": """
Complete the research task described in `task`.

Gather information from the sources available to you, cross-check
claims across more than one source when possible, and keep track of
what is established versus uncertain. Then analyze what you gathered
and produce the answer the task asks for, exactly in the requested
format, distinguishing evidence from inference.
""",
    "flat-loganalyzer": """
Analyze the log file(s) named in `task` and answer the question asked.

Identify the log format first, then compute your answer with scripts
(grep/awk/python via bash) rather than eyeballing - write small
commands, check their output, and build up to the result. Quantify
everything: counts, timestamps, rates. Double-check the final number by
recomputing it a second way when feasible, then report exactly what the
task asks for.
""",
}

ANSWER_PROMPT = """
Deliver the final answer to the task, exactly as requested. If the task
asked for a specific format, follow it precisely. Report only what you
actually established.
"""


def _fmt_models(models: list[dict]) -> str:
    inner = ", ".join(
        "{ provider = \"%s\", model = \"%s\" }" % (m["provider"], m["model"])
        for m in models)
    return "{ models = [%s] }" % inner


def _pick_model_list(doc: dict) -> list[dict]:
    """The structured agent's frontier list (the one carrying opus)."""
    for stage in doc["stages"].values():
        models = (stage.get("model") or {}).get("models") or []
        if any("opus" in m.get("model", "") for m in models):
            return models
    first = next(iter(doc["stages"].values()))
    return (first.get("model") or {}).get("models") or []


def make_flat(structured_name: str, flat_name: str) -> str:
    doc = tomllib.loads(
        (HERE / structured_name / "agent.leviath").read_text())
    stages = doc["stages"]

    # context_* tools route into regions the flat layout does not have;
    # blocking/interactive tools are withdrawn under --yolo on both arms
    # (and would trip the autonomous-stage lint here).
    tools = sorted({t for s in stages.values()
                    for t in s.get("available_tools", [])
                    if not _excluded_tool(t)})
    tools_toml = "[" + ", ".join(f'"{t}"' for t in tools) + "]"
    total_iters = sum(int(s.get("max_iterations", 10))
                      for s in stages.values())
    models = _fmt_models(_pick_model_list(doc))
    perms = "\n".join(f"{k} = \"{v}\""
                      for k, v in doc.get("tool_permissions", {}).items())

    regions = doc.get("context", {}).get("regions", {})
    task_region = regions.get("task", {})
    required_message = task_region.get("required_message")
    req_msg = (f", required_message = {_toml_str(required_message)}"
               if required_message else "")

    compaction = doc.get("compaction", {})
    compaction_block = ""
    if compaction:
        compaction_block = (
            "[compaction]\n"
            f"provider = \"{compaction.get('provider')}\"\n"
            f"model = \"{compaction.get('model')}\"\n\n")

    work_prompt = WORK_PROMPTS[flat_name].strip()
    upstream = doc["agent"]["name"]

    return f"""# Flat-context ablation counterpart of {structured_name}
# (bundled agent: {upstream}). GENERATED by make_flat.py - do not edit
# by hand; regenerate and review instead. Same tools, same permissions,
# same total iteration budget; one stage, one compacting conversation
# window. check_pairs.py asserts those invariants.

[agent]
name = "{flat_name}"
version = "{doc['agent']['version']}"
description = "Flat-context baseline for {upstream}: identical tools and permissions, no stages, no context regions beyond a single conversation window"
entry_stage = "work"

[tool_permissions]
{perms}

[stages.work]
mode = "autonomous"
model = {models}
description = "Do the whole task in one loop"
available_tools = {tools_toml}
max_iterations = {total_iters}
system_prompt = \"\"\"
{work_prompt}
\"\"\"

[stages.work.tool_routing]
default_region = "conversation"

[stages.work.transitions.answer]
hint = "The task is complete - deliver the final answer"

[stages.answer]
mode = "output"
model = {models}
description = "Deliver the final answer"
max_iterations = 8
system_prompt = \"\"\"
{ANSWER_PROMPT.strip()}
\"\"\"

[stages.answer.transitions]

{compaction_block}[context.regions]
task = {{ kind = "pinned", budget = "2%", max_tokens = 3000, required = true, seed = "task"{req_msg} }}
conversation = {{ kind = "sliding_window", max_items = 200, budget = "75%", max_tokens = 120000, strategy = "bulk", overflow = 20 }}
error_report = {{ kind = "pinned", budget = "1%", max_tokens = 2000 }}
"""


def _excluded_tool(tool: str) -> bool:
    return (tool.startswith("context_") or tool.startswith("ask_user")
            or tool in ("present_for_review", "edit_document"))


def _toml_str(value: str) -> str:
    return '"' + value.replace('"', '\\"') + '"'


def main() -> int:
    for structured_name, flat_name in PAIRS.items():
        out = HERE / flat_name
        out.mkdir(parents=True, exist_ok=True)
        text = make_flat(structured_name, flat_name)
        tomllib.loads(text)  # must parse before it lands on disk
        (out / "agent.leviath").write_text(text)
        print(f"{flat_name}: generated from {structured_name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
