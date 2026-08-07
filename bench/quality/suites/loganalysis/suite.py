"""Log-analysis suite plugin for the quality runner.

Tasks are generated (see generate_tasks.py) from pinned public datasets;
each run gets a sliced log file in its working directory and must answer
one question with a single integer. Grading is exact match after
minimal normalization; held-out answers grade against their committed
salted hash.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import datasets  # noqa: E402
import verifier  # noqa: E402

TASKS_DIR = _HERE / "tasks"

_PROMPT = """The file log.txt in your working directory contains a server log.

{question}

Line numbers are 1-indexed from the top of log.txt. Work only from
log.txt. Reply with ONLY the final answer: {answer_format}."""


class Suite:
    name = "loganalysis"
    stagemix_mapping = None  # filled from the frozen blueprint at freeze

    def __init__(self):
        self._salt = None

    # -- plugin protocol ---------------------------------------------
    def load_tasks(self, subset_record: dict | None) -> list[dict]:
        tasks = []
        for split in ("public", "heldout"):
            split_dir = TASKS_DIR / split
            if not split_dir.is_dir():
                continue
            for path in sorted(split_dir.glob("*.json")):
                tasks.append(json.loads(path.read_text()))
        index_path = TASKS_DIR / "heldout_answers.sha256"
        if index_path.is_file():
            seed = json.loads(index_path.read_text())["seed"]
            self._salt = hashlib.sha256(
                f"loganalysis-heldout-{seed}".encode()).hexdigest()
        if subset_record:
            wanted = set(subset_record["task_ids"])
            tasks = [t for t in tasks if t["id"] in wanted]
        return tasks

    def agent_for(self, arm: dict) -> tuple[str, list]:
        blueprint = ("loganalyzer-bench" if arm["role"] == "structured"
                     else "flat-loganalyzer")
        return blueprint, []

    def prepare(self, task: dict, workdir: Path) -> str:
        lines = datasets.raw_lines(task["dataset"])
        lo = task["slice"]["start_line"] - 1
        hi = task["slice"]["end_line"]
        (workdir / "log.txt").write_text("\n".join(lines[lo:hi]) + "\n")
        return _PROMPT.format(question=task["question"],
                              answer_format=task["answer_format"])

    def collect(self, task: dict, workdir: Path, artifacts_dir: Path,
                answer: str | None):
        answer = answer or ""
        (artifacts_dir / "answer.txt").write_text(answer)
        return answer

    def grade(self, task: dict, submission: str) -> dict:
        return verifier.check(task, submission, salt=self._salt)
