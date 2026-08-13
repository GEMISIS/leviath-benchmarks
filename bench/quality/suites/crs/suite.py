"""Context Retention Suite plugin for the quality runner.

Long-horizon tasks (coding and non-coding) whose runs are later probed
for retention by replaying the journaled context state at fixed
tool-call depths (run_probes.py). This plugin owns only the run phase:
task loading, blueprint mapping, workdir seeding, and artifact scoring
(held-out pytest suite or answer key). Probe fields are amended onto
the records afterwards by the replay phase.

The structured role always resolves to the composed cross-vendor
flagship - the configuration the runtime actually recommends - never a
same-model-per-stage structured arm. Flat roles resolve to the
pair-checked flat blueprint (plus the `compacting` strong-baseline
variant).
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import probes as probes_mod  # noqa: E402
import validate  # noqa: E402

TASKS_DIR = _HERE / "tasks"

# Agent family per task: which pair-checked blueprint family runs it.
# Non-coding tasks exercise the other families - the suite is about the
# runtime's context layer, not about coding.
FAMILIES = {
    "cli-tool": "coder",
    "rest-api": "coder",
    "refactor": "coder",
    "full-stack": "coder",
    "data-pipeline": "coder",
    "stress-test": "coder",
    "incident-forensics": "loganalyzer",
    "records-reconciliation": "analyst",
    "docs-audit": "researcher",
}

# Tasks whose assets are complete enough to run. refactor / full-stack /
# data-pipeline were recovered with seed or validation gaps (see
# README.md) and join this set as they are repaired; the generated
# non-coding tasks join as their generators land.
RUNNABLE = {"cli-tool", "rest-api", "stress-test"}

# The structured role is the composed flagship, by design.
STRUCTURED_VARIANT = "adversarial-scoped-flagship"

_OUTPUT_INSTRUCTIONS = (
    "Summarize what you built and how to run it, then state plainly "
    "anything the task asked for that you did not finish. Report only "
    "what you actually did.")


class Suite:
    name = "crs"

    # -- plugin protocol ---------------------------------------------
    def load_tasks(self, subset_record: dict | None) -> list[dict]:
        tasks = []
        for task_dir in sorted(TASKS_DIR.iterdir()):
            if not (task_dir / "task.md").is_file():
                continue
            task_id = task_dir.name
            if task_id not in RUNNABLE:
                continue
            tasks.append({
                "id": task_id,
                "dir": task_dir,
                "family": FAMILIES[task_id],
                "prompt": (task_dir / "task.md").read_text(),
                "probes": probes_mod.load_probes(task_dir / "probes.json"),
                "verification": ("pytest"
                                 if (task_dir / "validation").is_dir()
                                 else "answer_key"),
            })
        if subset_record:
            wanted = set(subset_record["task_ids"])
            tasks = [t for t in tasks if t["id"] in wanted]
        return tasks

    def agent_for_task(self, task: dict, arm: dict) -> tuple[str, list]:
        family = task["family"]
        if arm["role"] == "structured":
            variant = arm.get("variant") or STRUCTURED_VARIANT
            return f"{family}-bench-{variant}", []
        blueprint = f"flat-{family}"
        if arm.get("variant"):
            blueprint = f"{blueprint}-{arm['variant']}"
        return blueprint, []

    def agent_for(self, arm: dict) -> tuple[str, list]:
        # Fallback for callers without task context (round metadata):
        # the coder family stands in.
        return self.agent_for_task({"family": "coder"}, arm)

    def task_cli(self, task: dict) -> list:
        return ["--output-format", "text",
                "--output-instructions", _OUTPUT_INSTRUCTIONS]

    def prepare(self, task: dict, workdir: Path) -> str:
        seed = task["dir"] / "seed-files"
        if seed.is_dir():
            for item in sorted(seed.iterdir()):
                dest = workdir / item.name
                if item.is_dir():
                    shutil.copytree(item, dest)
                else:
                    shutil.copyfile(item, dest)
        return task["prompt"]

    def collect(self, task: dict, workdir: Path, artifacts_dir: Path,
                answer) -> dict:
        (artifacts_dir / "answer.txt").write_text(str(answer or ""))
        if task["verification"] == "pytest":
            return validate.run_pytest(task["dir"], workdir, artifacts_dir)
        return validate.run_answer_key(task["dir"], answer)

    def grade(self, task: dict, submission: dict) -> dict:
        total = submission.get("total", 0)
        failed = submission.get("failed", 0) + submission.get("errors", 0)
        passed = bool(total) and failed == 0
        detail = {k: submission.get(k)
                  for k in ("passed", "failed", "errors", "total",
                            "detail")
                  if submission.get(k) is not None}
        return {
            "passed": passed,
            "detail": detail,
            # Hoisted onto the record top level by the runner: the
            # validation block is data, not a verdict.
            "record_fields": {"validation": {
                "passed": submission.get("passed", 0),
                "failed": submission.get("failed", 0),
                "errors": submission.get("errors", 0),
                "total": total,
                "failures": submission.get("failures", []),
                "suite_hash": submission.get("suite_hash"),
            }},
        }
