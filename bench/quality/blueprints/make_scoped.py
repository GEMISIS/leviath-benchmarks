#!/usr/bin/env python3
"""Generate the stage-scoped variants: every stage sees only what it needs.

Same stages, same prompts, same models as the source agent. The only
difference is that each stage declares the regions it actually reads or
writes, so the rest are parked rather than carried on every call. Parked
is not dropped: a later stage that declares a region gets it back with
its contents.

The sets come from the stage prompts and tool routing, not from taste:
a stage is given what it is told to use. Measured on the unscoped agent,
the regions a stage does not need are 68-79% of what it carries.

The routing check below is not optional. Scoping a stage and routing its
tool output are separate declarations, and the first version of this
script let them disagree - four of six stages sent tool results into a
region they had parked, so the stage got a pointer reading "read that
region for the full result" naming a region it could not read. Verify
lost the documentation it was told to check the plan against in 6 of 20
runs. Any region a stage routes into is part of that stage's scope.

Usage:
    python3 make_scoped.py                    # every configured source
    python3 make_scoped.py analyst-bench      # just one

Afterwards: check_pairs.py (the variants must satisfy the same policy).
"""
from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent

# source agent -> stage -> {region: budget percent of that stage's window}.
# Budgets are re-cut per stage: a stage carrying fewer regions should give
# the ones it kept more room, not leave the window unused.
SCOPES: dict[str, dict[str, dict[str, int]]] = {
    "analyst-bench": {
        "profile": {"task": 3, "data_map": 6, "data_preview": 55,
                    "conversation": 25, "error_report": 3},
        "plan": {"task": 5, "data_map": 12, "plan": 12, "data_preview": 38,
                 "conversation": 22, "scratch": 3, "error_report": 3},
        # data_preview earns its place here: a computation that has to
        # re-read a rule mid-flight should find it, not re-derive it.
        "compute": {"task": 3, "data_map": 6, "plan": 10, "results": 14,
                    "scripts": 22, "scripts_history": 3, "data_preview": 18,
                    "conversation": 16, "error_report": 3},
        # verify is told to check rules against the documentation itself.
        # Without data_preview that instruction is unfollowable.
        "verify": {"task": 5, "plan": 12, "results": 18, "scripts": 14,
                   "scripts_history": 3, "data_preview": 15,
                   "answer_draft": 12, "conversation": 15, "error_report": 3},
        "answer": {"task": 8, "plan": 8, "results": 22, "answer_draft": 30,
                   "conversation": 20, "error_report": 3},
        "error_recovery": {"task": 5, "plan": 10, "results": 15,
                           "scripts": 20, "data_preview": 15,
                           "conversation": 22, "scratch": 3,
                           "error_report": 5},
    },
}

# The adversarial variant is the same agent plus a critic stage. The critic
# is deliberately the narrowest scope in the graph: a technical reviewer is
# given the plan and enough context to judge it, not the whole workspace.
SCOPES["analyst-bench-adversarial"] = dict(SCOPES["analyst-bench"])
SCOPES["analyst-bench-adversarial"]["plan_review"] = {
    "task": 8, "data_map": 15, "plan": 30, "data_preview": 18,
    "conversation": 18, "scratch": 3, "error_report": 3,
}

# CACHE RULE for every table here: each stage lists its regions in the same
# relative order as the agent's global [context.regions] declaration, so the
# pinned prefix stays byte-stable across stage transitions.
SCOPES["loganalyzer-bench"] = {
    "ingest": {"task": 4, "findings": 8, "logs": 55,
               "conversation": 24, "error_report": 3},
    "analyze": {"task": 4, "severity_index": 2, "findings": 10,
                "logs": 30, "scripts": 14, "scripts_history": 3,
                "conversation": 22, "scratch": 5, "error_report": 3},
    "script": {"task": 4, "findings": 6, "logs": 28, "scripts": 32,
               "scripts_history": 3, "conversation": 18,
               "error_report": 3},
    "report": {"task": 5, "severity_index": 3, "findings": 20,
               "logs": 22, "scripts": 18, "scripts_history": 3,
               "conversation": 20, "error_report": 3},
    "error_recovery": {"task": 4, "findings": 8, "logs": 22,
                       "scripts": 22, "conversation": 24, "scratch": 4,
                       "error_report": 8},
    "summary": {"task": 8, "severity_index": 5, "findings": 35,
                "conversation": 40, "error_report": 3},
}

# The critic is deliberately narrow: the findings, the index, and enough of
# the raw log to check them against - not the script workspace.
SCOPES["loganalyzer-bench-adversarial"] = dict(SCOPES["loganalyzer-bench"])
SCOPES["loganalyzer-bench-adversarial"]["analysis_review"] = {
    "task": 6, "severity_index": 4, "findings": 20, "logs": 35,
    "conversation": 22, "scratch": 5, "error_report": 3,
}

SCOPES["researcher-bench"] = {
    "gather": {"query": 2, "scope": 2, "sources_index": 5,
               "raw_findings": 56, "conversation": 28, "error_report": 2},
    "analyze": {"query": 3, "scope": 2, "sources_index": 6, "format": 2,
                "raw_findings": 40, "claims": 14, "contradictions": 4,
                "conversation": 22, "error_report": 3},
    # summarize builds from claims, not raw bulk - that is the point of
    # the pipeline. raw_findings stays parked here.
    "summarize": {"query": 4, "sources_index": 8, "format": 3, "claims": 30,
                  "contradictions": 8, "conversation": 40, "error_report": 3},
    "error_recovery": {"query": 3, "sources_index": 5, "raw_findings": 32,
                       "conversation": 45, "error_report": 8},
    "summary": {"query": 6, "claims": 32, "conversation": 54,
                "error_report": 3},
}

# The claims critic gets the claims, the evidence to check them against, and
# the rules they were graded under - not the synthesis workspace.
SCOPES["researcher-bench-adversarial"] = dict(SCOPES["researcher-bench"])
SCOPES["researcher-bench-adversarial"]["claims_review"] = {
    "query": 3, "scope": 2, "sources_index": 8, "format": 2,
    "raw_findings": 31, "claims": 20, "contradictions": 6,
    "conversation": 22, "error_report": 3,
}

SCOPES["coder-bench"] = {
    "discover": {"task": 3, "repo_files": 5, "conventions": 4,
                 "architecture": 4, "error_report": 3, "discovery": 6,
                 "workflow": 4, "codebase": 40, "conversation": 22,
                 "scratch": 5},
    "analyze": {"task": 5, "conventions": 4, "architecture": 4, "plan": 5,
                "prototypes": 5, "error_report": 3, "discovery": 6,
                "workflow": 4, "codebase": 30, "conversation": 26},
    "prototype": {"task": 3, "plan": 6, "prototypes": 6, "stuck_report": 2,
                  "error_report": 3, "discovery": 5, "workflow": 4,
                  "codebase": 24, "implementation": 10, "test_results": 8,
                  "conversation": 22},
    "implement": {"task": 2, "conventions": 3, "plan": 5, "prototypes": 3,
                  "stuck_report": 1, "error_report": 2, "discovery": 4,
                  "workflow": 3, "baseline": 4, "codebase": 16,
                  "implementation": 26, "test_results": 8, "errors": 3,
                  "conversation": 16},
    "review": {"task": 6, "conventions": 4, "plan": 5, "error_report": 3,
               "workflow": 4, "baseline": 5, "codebase": 18,
               "implementation": 24, "test_results": 10,
               "conversation": 16},
    "reassess": {"task": 5, "conventions": 3, "architecture": 3, "plan": 8,
                 "prototypes": 4, "stuck_report": 4, "error_report": 3,
                 "discovery": 4, "workflow": 4, "codebase": 16,
                 "implementation": 16, "test_results": 10, "errors": 4,
                 "conversation": 12},
    "error_recovery": {"task": 4, "plan": 6, "error_report": 8,
                       "discovery": 4, "workflow": 3, "codebase": 20,
                       "implementation": 12, "test_results": 8,
                       "errors": 8, "conversation": 22},
    "summary": {"task": 10, "plan": 5, "error_report": 4, "workflow": 3,
                "baseline": 3, "implementation": 30, "test_results": 10,
                "errors": 5, "conversation": 25},
}

# The plan critic is the narrowest working scope in the graph: the plan, the
# contracts to hold it to, and the files needed to falsify it - not the whole
# workspace.
SCOPES["coder-bench-adversarial"] = dict(SCOPES["coder-bench"])
SCOPES["coder-bench-adversarial"]["plan_review"] = {
    "task": 6, "conventions": 3, "architecture": 4, "plan": 12,
    "prototypes": 5, "error_report": 3, "discovery": 6, "workflow": 5,
    "codebase": 25, "conversation": 22, "scratch": 3,
}

MAX_BUDGET = 97   # leave the window headroom for the stage-instruction block

# Regions a stage must have written before it may leave. Asserted per stage
# rather than globally: `required` on the global declaration would nag every
# stage that shares the global layout, including ones that run before the
# region could possibly be filled.
REQUIRED = {"analyst-bench": {"verify": {"answer_draft"}}}
REQUIRED["analyst-bench-adversarial"] = REQUIRED["analyst-bench"]
# analyze must leave with findings/claims written: they are the spine every
# downstream deliverable is built from. report/summary regions themselves
# cannot be asserted (a report is a file on disk).
REQUIRED["loganalyzer-bench"] = {"analyze": {"findings"}}
REQUIRED["loganalyzer-bench-adversarial"] = REQUIRED["loganalyzer-bench"]
REQUIRED["researcher-bench"] = {"analyze": {"claims"}}
REQUIRED["researcher-bench-adversarial"] = REQUIRED["researcher-bench"]
REQUIRED["coder-bench"] = {
    # implement's step 1 mandates capturing the baseline before the first
    # edit; without it a regression is indistinguishable from a pre-existing
    # failure. Satisfiable even at TIER 1: the prompt requires writing
    # "no baseline - nothing to run yet".
    "implement": {"baseline"},
    # A spike that records nothing wasted its detour: prototype's own prompt
    # requires appending the verdict and what was ruled out.
    "prototype": {"prototypes"},
}
REQUIRED["coder-bench-adversarial"] = REQUIRED["coder-bench"]


def routing_targets(stage: dict) -> set[str]:
    """Every region this stage's tool results can land in."""
    routing = stage.get("tool_routing") or {}
    targets = set()
    if routing.get("default_region"):
        targets.add(routing["default_region"])
    for target in (routing.get("overrides") or {}).values():
        targets.add(target if isinstance(target, str) else target.get("region"))
    return {t for t in targets if t}


def _toml_value(value) -> str:
    """Render one value as inline TOML (bools, strings, numbers, lists,
    nested tables - region specs carry seeds like { files = [...] })."""
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, list):
        return "[" + ", ".join(_toml_value(v) for v in value) + "]"
    if isinstance(value, dict):
        inner = ", ".join(f"{k} = {_toml_value(v)}" for k, v in value.items())
        return f"{{ {inner} }}"
    return str(value)


def region_line(spec: dict, name: str, pct: int, required: bool = False) -> str:
    """The global declaration, re-budgeted (and re-required) for this stage."""
    spec = dict(spec)
    spec["budget"] = f"{pct}%"
    if required:
        spec["required"] = True
    parts = [f"{key} = {_toml_value(value)}" for key, value in spec.items()]
    return f"{name} = {{ {', '.join(parts)} }}"


def generate(source: str) -> Path:
    scopes = SCOPES[source]
    src_path = HERE / source / "agent.leviath"
    text = src_path.read_text()
    doc = tomllib.loads(text)
    regions = doc["context"]["regions"]

    missing = set(scopes) - set(doc["stages"])
    if missing:
        raise SystemExit(f"{source}: scopes name absent stages: {missing}")
    unscoped = set(doc["stages"]) - set(scopes)
    if unscoped:
        raise SystemExit(f"{source}: stages with no scope: {unscoped}")

    for stage_name, scope in scopes.items():
        stage = doc["stages"][stage_name]
        for name in scope:
            if name not in regions:
                raise SystemExit(f"{source}/{stage_name}: no region {name!r}")
        # The check that the first version of this script was missing.
        blind = routing_targets(stage) - set(scope) - {"conversation"}
        if blind:
            raise SystemExit(
                f"{source}/{stage_name}: routes tool output to {sorted(blind)} "
                f"but does not declare {'it' if len(blind) == 1 else 'them'}. "
                f"The stage would get a pointer into a region it cannot read."
            )
        total = sum(scope.values())
        if total > MAX_BUDGET:
            raise SystemExit(f"{source}/{stage_name}: budgets sum to {total}%")

    for stage_name, scope in scopes.items():
        anchor = f"[stages.{stage_name}.transitions"
        idx = text.index(anchor)
        block = [
            "# Stage-scoped layout: this stage sees what its job needs and",
            "# nothing else. The rest are parked, not dropped - a later stage",
            "# that declares them gets them back with their content. Every",
            "# region this stage routes tool output into is declared here;",
            "# routing into a parked region is a dead drop (make_scoped.py",
            "# refuses to generate one).",
            f"# Budgets sum to {sum(scope.values())}% of this stage's window.",
            f"[stages.{stage_name}.context.regions]",
        ]
        req = REQUIRED.get(source, {}).get(stage_name, set())
        block += [region_line(regions[n], n, p, n in req)
                  for n, p in scope.items()]
        text = text[:idx] + "\n".join(block) + "\n\n" + text[idx:]

    version = doc["agent"]["version"]
    text = text.replace(f'version = "{version}"', f'version = "{version}-scoped"', 1)
    _, _, rest = text.partition("[agent]")
    text = (f"# Stage-scoped variant of {source}: identical stages, prompts\n"
            "# and models; each stage declares only the regions it uses.\n"
            "# GENERATED by make_scoped.py - regenerate rather than editing.\n\n"
            "[agent]" + rest)

    tomllib.loads(text)          # it must still parse
    dest = HERE / f"{source}-scoped"
    dest.mkdir(exist_ok=True)
    for extra in (HERE / source).iterdir():
        if extra.is_dir():
            import shutil
            shutil.copytree(extra, dest / extra.name, dirs_exist_ok=True)
    (dest / "agent.leviath").write_text(text)
    return dest


targets = sys.argv[1:] or sorted(SCOPES)
for source in targets:
    if source not in SCOPES:
        raise SystemExit(f"no scope defined for {source!r}")
    dest = generate(source)
    print(f"{dest.name}")
    for stage_name, scope in SCOPES[source].items():
        print(f"   {stage_name:15} {len(scope):2} regions  "
              f"{sum(scope.values()):3}%")
