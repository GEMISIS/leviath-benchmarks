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

import shutil
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from conduct import CONDUCT  # noqa: E402

PAIRS = {
    "coder-bench": "flat-coder",
    "analyst-bench": "flat-analyst",
    "researcher-bench": "flat-researcher",
    "loganalyzer-bench": "flat-loganalyzer",
}

# The strong flat baseline: identical to the flat arm except the one
# window compacts on overflow (summarize-oldest) instead of evicting,
# which is what production harnesses actually do when the context
# fills. Generated from the same structured source in the same pass so
# it can never drift from its flat sibling; check_pairs.py asserts the
# only difference is the conversation region's overflow strategy.
COMPACT_VARIANTS = {flat: f"{flat}-compacting" for flat in PAIRS.values()}

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

Inspect the available data files first - formats, row counts, columns and
what they mean - and read any documentation shipped with them properly
rather than noting that it exists. Its definitions govern: if a manual
or data dictionary defines a metric, compute that definition even when
an everyday reading of the question suggests another one, and when two
readings are genuinely defensible, follow the documented one and say
why. Then work out what exactly to compute, including the traps:
rows to exclude, joins that duplicate rows, nulls, mixed units, dates
that need parsing, categories defined by the documentation rather than
intuition.

Compute with scripts rather than eyeballing - small steps, checking each
one's output before building on it, watching whether row counts move the
way you expected. A filter that silently matched nothing produces a
confident, wrong zero. Then recompute the figure a second, independent
way and reconcile the two before reporting it.

Match the deliverable to the request: if the task asked a specific
question, answer exactly that, in exactly the format it asked for, with
no preamble and no report nobody asked for.
""",
    "flat-researcher": """
Complete the research task described in `task`.

Gather information from the sources available to you, cross-check
claims across more than one source when possible, and keep track of
what is established versus uncertain. Then analyze what you gathered
and produce the answer the task asks for, exactly in the requested
format, distinguishing evidence from inference.

Match the deliverable to the request: if the task asked a specific
question, answer exactly that, with no preamble and no written report
nobody asked for.
""",
    "flat-loganalyzer": """
Analyze the log file(s) named in `task` and answer the question asked.

Identify the log format first, then compute your answer with scripts
(grep/awk/python via bash) rather than eyeballing - write small
commands, check their output, and build up to the result. Compute over
the file on disk; pulling the whole log into context buys nothing and
costs a lot. Quantify everything: counts, timestamps, rates.
Double-check the final number by recomputing it a second way when
feasible.

Match the deliverable to the request: if the task asked a specific
question, answer exactly that, in exactly the format it asked for, with
no preamble and no report nobody asked for.
""",
}

# The hardened variants' extra discipline: the wind-down every
# production harness carries, plus tighter tool-result hygiene. This is
# baseline STRENGTHENING - if hardened flat stops collapsing, the
# honest claim narrows to "discipline can be prompted, but structure is
# the sum of the disciplines, guaranteed".
WIND_DOWN = """
Budget your investigation. If tool results start coming back empty or
truncated, if a call fails twice in a row, or if you notice yourself
re-reading files you have already read, STOP investigating immediately
and call submit_output with your best current answer - a partial
report delivered beats a perfect one that never ships. Never respond
with an empty message: when in doubt, submit what you have."""

ANSWER_PROMPT = """
Deliver the final answer to the task. Report only what you actually
established.

If the task states an exact output format - a required final line, a
particular shape, "reply with only X" - reproduce it literally, and put
nothing else around it. An answer that is right but not in the
requested form is unusable by whoever asked, so it is not an answer.
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


def make_flat(structured_name: str, flat_name: str,
              compacting: bool = False, hardened: bool = False) -> str:
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

    base_flat = (flat_name.removesuffix("-hardened")
                 .removesuffix("-compacting"))
    work_prompt = WORK_PROMPTS[base_flat].strip()
    upstream = doc["agent"]["name"]

    if compacting:
        conversation = ('conversation = { kind = "sliding_window", '
                        'max_items = 400, budget = "91%", '
                        'strategy = "compact", compact_count = 20 }')
        overflow_note = (
            "# The window compacts on overflow - the oldest entries are\n"
            "# summarized rather than evicted, which is what production\n"
            "# harnesses do when the context fills. The ONLY difference\n"
            f"# from {base_flat} is that overflow strategy.")
        desc = (f"Strong flat baseline for {upstream}: identical to "
                f"{base_flat} except the window compacts on overflow "
                "instead of evicting")
    else:
        conversation = ('conversation = { kind = "sliding_window", '
                        'max_items = 400, budget = "91%", '
                        'strategy = "bulk", overflow = 20 }')
        overflow_note = (
            "# The window evicts oldest-first on overflow - the classic\n"
            "# truncating loop.")
        desc = (f"Flat-context baseline for {upstream}: identical tools "
                "and permissions, one loop, one conversation window")

    return f"""# Flat-context ablation counterpart of {structured_name}
# (agent name: {upstream}). GENERATED by make_flat.py - do not edit
# by hand; regenerate and review instead.
#
# One stage that works and answers, which is how today's agents are
# built: a single loop with every tool, a large conversation window, and
# compaction when it fills. `mode = "output"` grants submit_output and
# requires the call, so the run ends with an answer rather than through
# a separate reporting stage.
#
# Same tools, same permissions, same total iteration budget as the
# structured agent, and its window is a percentage of the model's
# context exactly like the structured regions - the baseline is
# unstructured, not handicapped. check_pairs.py asserts that.
{overflow_note}

[agent]
name = "{flat_name}"
version = "{doc['agent']['version']}"
description = "{desc}"
entry_stage = "work"

[tool_permissions]
{perms}

[stages.work]
mode = "output"
model = {models}
description = "Do the whole task and answer, in one loop"
available_tools = {tools_toml}
max_iterations = {total_iters}
system_prompt = \"\"\"
{work_prompt}

{CONDUCT}
{(chr(10) + WIND_DOWN.strip() + chr(10)) if hardened else ""}
{ANSWER_PROMPT.strip()}
\"\"\"

[stages.work.tool_routing]
{'max_result_tokens = 6000' + chr(10) if hardened else ""}default_region = "conversation"

[stages.work.transitions]

{compaction_block}[context.regions]
# min_tokens floors survive a small pinned window (the CRS window
# sweep): a percentage budget that starves the task text kills the run
# at spawn, which measures the harness rather than the arm.
task = {{ kind = "pinned", budget = "2%", min_tokens = 4000, required = true, seed = "task"{req_msg} }}
{conversation}
error_report = {{ kind = "pinned", budget = "2%" }}
# Declared so the per-stage prompt gets its own region instead of being
# injected into `task` (the first pinned region), where it both churns
# the cache prefix and competes with the task text for budget.
stage_instructions = {{ kind = "pinned", budget = "3%", min_tokens = 2000, max_tokens = 4000 }}
"""


def _excluded_tool(tool: str) -> bool:
    return (tool.startswith("context_") or tool.startswith("ask_user")
            or tool in ("present_for_review", "edit_document"))


def _toml_str(value: str) -> str:
    return '"' + value.replace('"', '\\"') + '"'


def _mirror_tools(structured_name: str, flat_name: str) -> int:
    """Copy the agent's own tools/*.rhai to the flat counterpart.

    The flat arm grants the same tools by construction, and a granted
    tool the agent does not carry makes the blueprint invalid - so the
    scripts travel with it, byte-identical.
    """
    src, dst = HERE / structured_name / "tools", HERE / flat_name / "tools"
    if dst.is_dir():
        for stale in dst.iterdir():
            stale.unlink()
    if not src.is_dir():
        return 0
    dst.mkdir(exist_ok=True)
    for p in sorted(src.iterdir()):
        if p.is_file():
            shutil.copyfile(p, dst / p.name)
    return len(list(dst.iterdir()))


def main() -> int:
    for structured_name, flat_name in PAIRS.items():
        variants = [(flat_name, False, False),
                    (COMPACT_VARIANTS[flat_name], True, False),
                    (f"{flat_name}-hardened", False, True),
                    (f"{COMPACT_VARIANTS[flat_name]}-hardened", True,
                     True)]
        for name, compacting, hardened in variants:
            out = HERE / name
            out.mkdir(parents=True, exist_ok=True)
            text = make_flat(structured_name, name,
                             compacting=compacting, hardened=hardened)
            tomllib.loads(text)  # must parse before it lands on disk
            (out / "agent.leviath").write_text(text)
            n = _mirror_tools(structured_name, name)
            extra = f", {n} tool script(s) mirrored" if n else ""
            print(f"{name}: generated from {structured_name}{extra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
