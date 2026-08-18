#!/usr/bin/env python3
"""Generate the adversarial variants: each base agent plus a critic stage.

Generated rather than hand-maintained. It was hand-maintained once, and
the base agent then gained a region, a tool and two prompt changes that
never reached it - which is the same drift that left the scoped variant
without the critic and the critic without the scoping. A variant that
cannot fall behind its base is worth more than one that reads nicely.

Each critic stage lives in parts/. Everything else is the base file with
one forward edge redirected through the critic:

- analyst: plan -> compute becomes plan -> plan_review; the critic attacks
  the plan before anything is computed.
- loganalyzer: analyze -> script becomes analyze -> analysis_review; the
  critic attacks the analysis before scripts are written against it.
- researcher: analyze -> summarize becomes analyze -> claims_review; the
  critic attacks the extracted claims before a report is built from them.
- coder: analyze -> implement becomes analyze -> plan_review; the critic
  reviews exactly the plans that claimed to need no spike (the prototype
  path already checks its plan by running code, which no critic improves
  on). analyze routes by LLM choice, so the token in its transition_prompt
  is patched to match the new edge name.

Usage: python3 make_adversarial.py [agent ...]
Afterwards: make_scoped.py, make_mix.py, check_transforms.py, check_pairs.py
"""
from __future__ import annotations

import shutil
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent

# source agent -> how its critic goes in. `redirect` renames one forward
# edge header (and its transform_config header when the edge has one);
# `hint` replaces that edge's hint so the choice the model reads matches
# the new destination; `prompt_patch` fixes an LLM-choice routing token;
# `anchor` is the stage banner the critic part is inserted ahead of.
AGENTS = {
    "analyst-bench": {
        "critic": "plan_review",
        "part": "plan_review.toml",
        "redirect": ("plan", "compute"),
        "hint": ('hint = "The plan is written - compute it"',
                 'hint = "The plan is written - have it reviewed"'),
        "prompt_patch": None,
        "anchor": "# ─── Stage 3",
    },
    "loganalyzer-bench": {
        "critic": "analysis_review",
        "part": "analysis_review.toml",
        "redirect": ("analyze", "report"),
        "hint": ('hint = "The task asked for a written report or a broad review"',
                 'hint = "The analysis is drafted - have it attacked before '
                 'the report is written"'),
        "prompt_patch": (
            "- If the task asked for a written report or a broad review of "
            "these logs, respond with: report",
            "- If the task asked for a written report or a broad review of "
            "these logs, respond with: analysis_review",
        ),
        "anchor": "# ─── Stage 3",
    },
    "researcher-bench": {
        "critic": "claims_review",
        "part": "claims_review.toml",
        "redirect": ("analyze", "summarize"),
        "hint": ('hint = "The task asked for a written report or a survey of a topic"',
                 'hint = "The task asked for a written report - have the claims attacked first"'),
        "prompt_patch": None,
        "anchor": "# ─── Stage 3",
    },
    "coder-bench": {
        "critic": "plan_review",
        "part": "coder_plan_review.toml",
        "redirect": ("analyze", "implement"),
        "hint": ('hint = "The fix location and approach are clear - begin implementation"',
                 'hint = "The fix location and approach are clear - have the plan reviewed"'),
        # analyze picks its edge by name in the transition_prompt.
        "prompt_patch": (
            "- Respond with `implement` when the plan is a straightforward application of a",
            "- Respond with `plan_review` when the plan is a straightforward application of a",
        ),
        "anchor": "# ─── Stage 3",
    },
}


def generate(source: str) -> None:
    spec = AGENTS[source]
    critic, part_file = spec["critic"], spec["part"]
    src_stage, dst_stage = spec["redirect"]
    dest_name = f"{source}-adversarial"

    base = (HERE / source / "agent.leviath").read_text()
    critic_text = (HERE / "parts" / part_file).read_text()

    # The forward edge hands to the critic instead of its old target. Only
    # the header and hint change: the transform config on that edge is the
    # base's, so a change to what crosses the edge is not made twice.
    old_header = f"[stages.{src_stage}.transitions.{dst_stage}]"
    new_header = f"[stages.{src_stage}.transitions.{critic}]"
    old_hint, new_hint = spec["hint"]
    if f"{old_header}\n{old_hint}" not in base:
        raise SystemExit(f"{source}: {src_stage}->{dst_stage} edge is not "
                         "where expected")
    text = base.replace(f"{old_header}\n{old_hint}",
                        f"{new_header}\n{new_hint}", 1)
    text = text.replace(f"{old_header[:-1]}.transform_config]",
                        f"{new_header[:-1]}.transform_config]", 1)
    if spec["prompt_patch"]:
        old_tok, new_tok = spec["prompt_patch"]
        if old_tok not in text:
            raise SystemExit(f"{source}: transition_prompt token not found")
        text = text.replace(old_tok, new_tok, 1)

    # The critic stage goes in ahead of the next stage banner.
    anchor = text.index(spec["anchor"])
    text = text[:anchor] + critic_text + "\n" + text[anchor:]

    version = tomllib.loads(base)["agent"]["version"]
    text = text.replace(f'version = "{version}"',
                        f'version = "{version}-adversarial"', 1)
    _, _, rest = text.partition("[agent]")
    text = (f"# Adversarial variant of {source}: the same agent with a critic\n"
            f"# stage on the {src_stage}->{dst_stage} edge, on a different "
            "vendor's model.\n"
            "# GENERATED by make_adversarial.py - regenerate rather than "
            "editing.\n"
            f"# The critic stage itself is parts/{part_file}.\n\n"
            "[agent]" + rest)

    doc = tomllib.loads(text)
    assert critic in doc["stages"], "critic stage did not land"
    dest = HERE / dest_name
    dest.mkdir(exist_ok=True)
    for extra in (HERE / source).iterdir():
        if extra.is_dir():
            shutil.copytree(extra, dest / extra.name, dirs_exist_ok=True)
    (dest / "agent.leviath").write_text(text)
    print(f"{dest_name}: {len(doc['stages'])} stages, critic on "
          f"{doc['stages'][critic]['model']['models'][0]['model']}")


targets = sys.argv[1:] or sorted(AGENTS)
for source in targets:
    if source not in AGENTS:
        raise SystemExit(f"no adversarial spec for {source!r}")
    generate(source)
