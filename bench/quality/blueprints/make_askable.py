#!/usr/bin/env python3
"""Generate the ask-enabled counterparts for the hallucination suite's
ask test (redacted-ledger).

The benchmark's standing policy bans human-in-the-loop tools - an agent
that can park on a person measures the person. The ask test relaxes
exactly that, symmetrically: every arm gets ask_user_text and the same
note saying the assigner is reachable (conduct.ASK_NOTE), and the
harness plays the user deterministically (core/interact.py). The flat
variants carry the tool and note in their single work stage; the
structured variant carries them in `verify`, the stage whose job is
validating inputs - the claim under test being that a stage *charged*
with the check beats an instruction merely available to a loop.

Each output is its source file with three insertions in one stage and
nothing else: ask_user_text in available_tools, allow_blocking_tools
(a lint silencer, not a behavior switch), and the note appended to the
stage prompt. check_pairs.py asserts exactly that, so an askable
variant can never drift from its source.

Run AFTER make_flat.py and make_mix.py (the sources are generated):
    python3 make_askable.py
"""
from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from conduct import ASK_NOTE  # noqa: E402

# source blueprint -> the stage that gets the ask channel
ASKABLE = {
    "flat-analyst": "work",
    "flat-analyst-compacting": "work",
    "analyst-bench-adversarial-scoped-flagship": "verify",
}

# The retention suite's standing-desk task is a 12-request SESSION, and
# the ask-test variant cannot host one: its pipeline is shaped around a
# single deliverable (revisit budgets of 2-5), so the run submits after
# the first phase or two and the remaining requests never happen - a
# measured 0.17 against the flats' 1.0. The session variant is the
# askable variant with exactly two changes: the loop budget a dozen
# phases actually need, and a session note on the ask stage telling it
# to record each verified answer in `answer_draft` and route back to
# compute for the next request. The ask channel itself stays where the
# ask test put it. Generated FROM the askable output so it can never
# drift from it.
SESSION = {
    "analyst-bench-adversarial-scoped-flagship-askable": "verify",
}
SESSION_REVISITS = {"plan": 14, "compute": 14, "verify": 14}

SESSION_NOTE = """SESSION CONDUCT: the user may have a sequence of requests, and later ones
can depend on your earlier answers. After verifying the current answer,
append it to `answer_draft` (context_append) labeled by request number,
then ask whether there is another request. For each new request, route
back to compute.

Only the user ends the session. However many requests have gone by, the
session is over when the user says there is nothing more - never because
it feels long, never because the requests seem complete, never on a
guess. If the last user reply is anything other than an explicit
"nothing more", ask again. The final deliverable is every answer in
`answer_draft`, in order; a session abandoned early delivers wrong
answers for every request that was never taken."""

# The exit edge's hint, rewritten so routing to answer reads as "the
# user ended the session" rather than "the work feels done".
SESSION_ANSWER_HINT = (
    'hint = "The figure holds up - answer"',
    'hint = "The user said there is nothing more - deliver every '
    'answer in answer_draft"')

_STAGE = re.compile(r"^\[stages\.([A-Za-z0-9_]+)\]\s*$")
_TOOLS = re.compile(r"^(available_tools = \[)(.*)(\]\s*)$")
_MODE = re.compile(r"^mode = ")


def render(source: str, stage_name: str) -> str:
    text = (HERE / source / "agent.leviath").read_text()
    # Every other cell runs --yolo, which auto-approves "ask"
    # permissions inline; the ask test runs attended so the ask TOOLS
    # survive, and without this the scripted user spends 15+ round
    # trips rubber-stamping shell approvals - measured latency and
    # journal noise, not the mechanism under test. Same table change
    # in every arm; check_pairs asserts it.
    text = re.sub(r'^(bash\s*=\s*)"ask"', r'\1"allow"', text,
                  flags=re.MULTILINE)
    text = re.sub(r'^(write_file\s*=\s*)"ask"', r'\1"allow"', text,
                  flags=re.MULTILINE)
    out: list[str] = []
    stage = None
    in_prompt = False
    granted = flagged = noted = False
    for line in text.splitlines(keepends=True):
        m = _STAGE.match(line)
        if m and not in_prompt:
            stage = m.group(1)
        elif stage == stage_name and not in_prompt:
            if _MODE.match(line) and not flagged:
                out.append(line)
                out.append("# BENCHMARK POLICY exception (ask test): the"
                           " lint silencer for the granted ask tool.\n")
                out.append("allow_blocking_tools = true\n")
                flagged = True
                continue
            t = _TOOLS.match(line)
            if t and not granted:
                line = f'{t.group(1)}{t.group(2)}, "ask_user_text"{t.group(3)}'
                granted = True
            elif line.startswith('system_prompt = """'):
                in_prompt = True
        elif in_prompt and line.rstrip() == '"""' and stage == stage_name:
            if not noted:
                out.append(f"\n{ASK_NOTE}\n")
                noted = True
            in_prompt = False
        out.append(line)
    if not (granted and flagged and noted):
        raise SystemExit(f"{source}/{stage_name}: askable render "
                         f"incomplete (tool={granted}, lint={flagged}, "
                         f"note={noted})")
    header = (f"# Ask-enabled counterpart of {source} - GENERATED by "
              "make_askable.py for the\n# hallucination suite's ask "
              "test; do not edit by hand. The ONLY differences\n# from "
              f"the source: ask_user_text granted to [stages.{stage_name}], "
              "its lint\n# silencer, and the shared ask note appended "
              "to that stage's prompt.\n")
    return header + "".join(out)


def main() -> int:
    for source, stage_name in ASKABLE.items():
        text = render(source, stage_name)
        tomllib.loads(text)  # must parse before it lands on disk
        out_dir = HERE / f"{source}-askable"
        out_dir.mkdir(exist_ok=True)
        (out_dir / "agent.leviath").write_text(text)
        # Tool scripts travel with the agent (same rule as make_flat).
        src_tools = HERE / source / "tools"
        if src_tools.is_dir():
            import shutil
            dst = out_dir / "tools"
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src_tools, dst)
        print(f"{source}-askable: ask channel on [stages.{stage_name}]")

    for source, ask_stage in SESSION.items():
        text = (HERE / source / "agent.leviath").read_text()
        # Raise the revisit budgets a 12-phase session needs. Anchored
        # per stage so a budget elsewhere is never touched.
        stage = None
        out: list[str] = []
        in_prompt = False
        raised: set[str] = set()
        noted = False
        for line in text.splitlines(keepends=True):
            m = _STAGE.match(line)
            if m and not in_prompt:
                stage = m.group(1)
            elif (stage in SESSION_REVISITS and not in_prompt
                    and line.startswith("max_revisits = ")):
                line = f"max_revisits = {SESSION_REVISITS[stage]}\n"
                raised.add(stage)
            elif line.startswith('system_prompt = """') and not in_prompt:
                in_prompt = True
            elif in_prompt and line.rstrip() == '"""':
                if stage == ask_stage and not noted:
                    out.append(f"\n{SESSION_NOTE}\n")
                    noted = True
                in_prompt = False
            out.append(line)
        if raised != set(SESSION_REVISITS) or not noted:
            raise SystemExit(f"{source}-session: incomplete "
                             f"(raised={sorted(raised)}, note={noted})")
        text = "".join(out)
        old_hint, new_hint = SESSION_ANSWER_HINT
        if text.count(old_hint) != 1:
            raise SystemExit(f"{source}-session: answer-edge hint not "
                             "found exactly once")
        text = text.replace(old_hint, new_hint, 1)
        tomllib.loads(text)
        header = (f"# Session counterpart of {source} - GENERATED by "
                  "make_askable.py for the\n# retention suite's "
                  "multi-request session task; do not edit by hand. "
                  "The ONLY\n# differences from the source: revisit "
                  f"budgets raised to {SESSION_REVISITS} and\n# the "
                  f"session note appended to [stages.{ask_stage}].\n")
        base = source.removesuffix("-askable")
        out_dir = HERE / f"{base}-session"
        out_dir.mkdir(exist_ok=True)
        (out_dir / "agent.leviath").write_text(header + text)
        src_tools = HERE / source / "tools"
        if src_tools.is_dir():
            import shutil
            dst = out_dir / "tools"
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src_tools, dst)
        print(f"{base}-session: revisits {SESSION_REVISITS}, "
              f"session note on [stages.{ask_stage}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
