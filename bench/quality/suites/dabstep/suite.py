"""DABstep suite plugin (dev split, locally graded).

Each run gets the full pinned context-file set copied into its working
directory plus one question with its mandated answer-format guidelines.
Grading is the vendored upstream scorer - exactly what the leaderboard
runs.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import datasets  # noqa: E402
import scorer  # noqa: E402

_PROMPT = """Answer the following question using the data files in your
working directory ({files}). payments-readme.md and manual.md document
the data.

Question: {question}

Answer guidelines: {guidelines}

Reply with ONLY the final answer, formatted exactly as the guidelines
require."""


class Suite:
    name = "dabstep_dev"
    stagemix_mapping = None

    def load_tasks(self, subset_record: dict | None) -> list[dict]:
        tasks = datasets.dev_tasks()
        if subset_record:
            wanted = set(subset_record["task_ids"])
            tasks = [t for t in tasks if t["id"] in wanted]
        return tasks

    def agent_for(self, arm: dict) -> tuple[str, list]:
        blueprint = ("analyst-bench" if arm["role"] == "structured"
                     else "flat-analyst")
        return blueprint, []

    def prepare(self, task: dict, workdir: Path) -> str:
        for name in datasets.CONTEXT_FILES:
            shutil.copy(datasets.context_path(name), workdir / name)
        return _PROMPT.format(files=", ".join(sorted(datasets.CONTEXT_FILES)),
                              question=task["question"],
                              guidelines=task["guidelines"])

    def collect(self, task: dict, workdir: Path, artifacts_dir: Path,
                answer: str | None):
        answer = answer or ""
        (artifacts_dir / "answer.txt").write_text(answer)
        return answer

    def grade(self, task: dict, submission: str) -> dict:
        # Grade on the final non-empty line so prose above the answer
        # does not fail an otherwise correct submission.
        lines = [ln for ln in str(submission).splitlines() if ln.strip()]
        candidate = lines[-1] if lines else ""
        passed = scorer.question_scorer(candidate, task["answer"])
        return {"passed": bool(passed),
                "detail": {"expected": task["answer"], "got": candidate}}
