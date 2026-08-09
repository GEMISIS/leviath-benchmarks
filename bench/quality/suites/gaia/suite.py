"""GAIA validation suite plugin (web-dependent research questions).

Each run gets the question (and its attached file, when the task has
one, copied into the working directory) and must produce GAIA's mandated
FINAL ANSWER format. Grading is the vendored upstream quasi-exact-match
scorer.

Honesty caveats, carried into any published round: GAIA validation
answers are public (contamination is possible in principle), and the
questions are web-dependent, so absolute numbers drift over time. Arms
are interleaved by the runner within a round, which keeps the ablation
comparison fair even as the web moves.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import datasets  # noqa: E402
import scorer  # noqa: E402

_PROMPT = """{question}
{file_note}
Finish your reply with a line in exactly this format:
FINAL ANSWER: [YOUR FINAL ANSWER]

YOUR FINAL ANSWER should be a number OR as few words as possible OR a
comma separated list of numbers and/or strings. If you are asked for a
number, don't use commas or units ($, %) unless specified otherwise. If
you are asked for a string, don't use articles or abbreviations (e.g.
for cities), and write digits in plain text unless specified otherwise.
If you are asked for a comma separated list, apply the above rules to
each element."""

_FINAL = re.compile(r"FINAL ANSWER:\s*(.+)", re.IGNORECASE)

_ANSWER_SCHEMA = {
    "type": "object",
    "properties": {
        "final_answer": {
            "type": "string",
            "description": "The answer alone - a number, a few words, or "
                           "a comma separated list. No explanation.",
        },
    },
    "required": ["final_answer"],
    # Deliberately permissive: a refused submission is handed back to
    # the agent, and an output stage that spends its whole budget being
    # refused ends the run with no answer at all. Only final_answer is
    # ever read, so an agent that adds a field it wanted to explain
    # itself with still gets graded on the answer.
    "additionalProperties": True,
}


def _extract(submission: str) -> str:
    """The answer, however the agent chose to hand it back."""
    text = str(submission).strip()
    try:
        obj = json.loads(text)
        if isinstance(obj, dict) and isinstance(obj.get("final_answer"), str):
            return obj["final_answer"].strip()
    except (json.JSONDecodeError, TypeError):
        pass
    matches = _FINAL.findall(text)
    return matches[-1].strip() if matches else text


class Suite:
    name = "gaia_validation"
    stagemix_mapping = None
    # GAIA's terms forbid storing the dataset in any public repository.
    # The runner honors this flag by never writing context replays for
    # this suite (they would embed question text and attachment
    # contents), and grade detail below carries no ground-truth answers.
    contains_gated_data = True
    # The researcher's web_search tool uses Brave when BRAVE_API_KEY is
    # set and otherwise falls back, silently, to a Wikipedia-only
    # search. That fallback would quietly turn a web-research benchmark
    # into a Wikipedia benchmark, so the runner refuses the suite
    # without the key rather than publishing a degraded number.
    requires_env = {
        "BRAVE_API_KEY": "without it the agents' web_search falls back "
                         "to Wikipedia-only results, which understates a "
                         "web-dependent suite",
    }

    def load_tasks(self, subset_record: dict | None) -> list[dict]:
        tasks = datasets.tasks()
        if subset_record:
            wanted = set(subset_record["task_ids"])
            tasks = [t for t in tasks if t["id"] in wanted]
        return tasks

    def agent_for(self, arm: dict) -> tuple[str, list]:
        blueprint = ("researcher-bench" if arm["role"] == "structured"
                     else "flat-researcher")
        if arm.get("variant"):
            blueprint = f"{blueprint}-{arm['variant']}"
        return blueprint, []

    def task_cli(self, task: dict) -> list:
        # GAIA grades one short string by exact match, and a research
        # answer wrapped in prose fails on form rather than substance -
        # measuring formatting instead of research. The schema makes the
        # shape a contract the runtime enforces (a submission that does
        # not satisfy it is handed back to the agent), identically for
        # every arm, so what is graded is the answer itself.
        return ["--output-format", "json",
                "--output-schema", json.dumps(_ANSWER_SCHEMA),
                "--output-instructions",
                "Put ONLY the final answer in final_answer: a number OR "
                "as few words as possible OR a comma separated list, "
                "with no commas/units in numbers and no "
                "articles/abbreviations in strings unless specified. "
                "Nothing else: no explanation, no confidence note, no "
                "restating of the question."]

    def prepare(self, task: dict, workdir: Path) -> str:
        file_note = "\n"
        name = task.get("file_name")
        if name:
            shutil.copy(datasets.DATASETS_DIR / name, workdir / name)
            file_note = (f"\nThe file {name} mentioned in the question is "
                         "in your working directory.\n")
        return _PROMPT.format(question=task["Question"],
                              file_note=file_note)

    def collect(self, task: dict, workdir: Path, artifacts_dir: Path,
                answer: str | None):
        answer = answer or ""
        (artifacts_dir / "answer.txt").write_text(answer)
        return answer

    def grade(self, task: dict, submission: str) -> dict:
        candidate = _extract(submission)
        passed = scorer.question_scorer(candidate, task["Final answer"])
        # The model's own answer is our output and may be recorded; the
        # dataset's gold answer is gated content and never is.
        return {"passed": bool(passed), "detail": {"got": candidate}}
