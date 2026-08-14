"""Context Footprint Suite plugin for the quality runner.

The published cost/economics benchmark. Thesis: structured context
keeps the per-request footprint small and stable, which is what makes
cheaper - or free, local - models viable; a flat window grows with the
work. Measured per arm: tokens per request over the run (stability vs
growth), cache reads vs everything else, wall clock, and dollars -
against a FUNCTIONAL success bar (compiles and plays; the injected
failures are found; the architecture document is grounded and mostly
right), not perfection.

Three tasks, one per agent family:
- snake-cpp (coder): a playable terminal Snake in C++ with a required
  --test mode; verified by compiling and running scripted scenarios.
- log-search (log-analyzer): a multi-megabyte incident corpus with a
  known injected failure chain; verified against the generator's key.
- explain-repo (researcher): explain a pinned repository's architecture
  in one document; verified by mechanical grounding of every cited
  path/symbol, an auto-derived fact checklist, and a coherence pass.

Each task directory owns its verification: `verify.py` exposing
    verify(task_dir, workdir, artifacts_dir, answer) -> {
        "functional_pass": bool, "score": float 0..1, "detail": {...}}
and optionally `prepare.py` exposing seed(task_dir, workdir) when
seeding is more than copying seed-files/ (explain-repo materializes the
pinned checkout). The suite folds each run's journal into the
request-footprint block (footprint.py) at collect time.

Retention probing is NOT part of this suite - the retention/window
suite and the hallucination suite are its successors, rebuilt
separately (see FOOTPRINT-METHODOLOGY.md).
"""
from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import footprint as footprint_mod  # noqa: E402

TASKS_DIR = _HERE / "tasks"

FAMILIES = {
    "snake-cpp": "coder",
    "log-search": "loganalyzer",
    "explain-repo": "researcher",
}

# The structured role is the composed flagship, by design.
STRUCTURED_VARIANT = "adversarial-scoped-flagship"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Suite:
    name = "footprint"

    # -- plugin protocol ---------------------------------------------
    def load_tasks(self, subset_record: dict | None) -> list[dict]:
        tasks = []
        for task_dir in sorted(TASKS_DIR.iterdir()):
            if not (task_dir / "task.md").is_file():
                continue
            task_id = task_dir.name
            if task_id not in FAMILIES:
                continue
            tasks.append({
                "id": task_id,
                "dir": task_dir,
                "family": FAMILIES[task_id],
                "prompt": (task_dir / "task.md").read_text(),
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
        return self.agent_for_task({"family": "coder"}, arm)

    def task_cli(self, task: dict) -> list:
        instructions = task["dir"] / "output-instructions.txt"
        text = (instructions.read_text().strip() if instructions.is_file()
                else "Summarize what you produced and how to use it. "
                     "Report only what you actually did.")
        return ["--output-format", "text", "--output-instructions", text]

    def prepare(self, task: dict, workdir: Path) -> str:
        prepare_py = task["dir"] / "prepare.py"
        if prepare_py.is_file():
            _load_module(prepare_py,
                         f"prepare_{task['id']}").seed(task["dir"], workdir)
        else:
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
        artifacts_dir = Path(artifacts_dir).resolve()
        (artifacts_dir / "answer.txt").write_text(str(answer or ""))
        verify = _load_module(task["dir"] / "verify.py",
                              f"verify_{task['id']}")
        result = verify.verify(task["dir"], workdir, artifacts_dir, answer)
        # The run's own journal, folded into the suite's headline data.
        for name in ("run.lvr.gz", "run.lvr"):
            archive = artifacts_dir / "run" / name
            if archive.is_file():
                fp = footprint_mod.from_archive(archive)
                if fp:
                    result["request_footprint"] = fp
                break
        return result

    def grade(self, task: dict, submission: dict) -> dict:
        fp = submission.pop("request_footprint", None)
        record_fields = {"functional": {
            "score": round(float(submission.get("score", 0.0)), 4),
            "detail": submission.get("detail", {}),
        }}
        if fp:
            record_fields["request_footprint"] = fp
        return {
            "passed": bool(submission.get("functional_pass")),
            "detail": submission.get("detail", {}),
            "record_fields": record_fields,
        }
