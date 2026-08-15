"""Hallucination Suite plugin for the quality runner.

The published does-structure-reduce-invention benchmark
(HALLUCINATION-METHODOLOGY.md). Three tasks, each aimed at one cause
of hallucination, all run with the context window pinned small
(--window-tokens 32000) so the limits are genuinely hit:

- incident-chronicle (log-analyzer): three sequential incidents plus a
  divergent-defaults document; details established early must be
  reproduced exactly at the end. Measures compaction loss and
  training-prior fill-in (prior_matches: a wrong answer that equals the
  famous real-world value instead of the corpus's documented one).
- noisy-incident (log-analyzer): one quiet true cause, three loud
  exonerated decoys. Measures attention misdirection (decoy_captures) -
  every decoy carries citable exoneration evidence, checked by the
  generator's self-test, so exclusion is investigation, not luck.
- redacted-ledger (analyst): a required fact is absent from the corpus
  and held by a scripted user; the agent must ask rather than invent.
  Measures ask-vs-fabricate (asked). Runs on ask-enabled arm variants
  with the harness answering interactions deterministically.

Two measurement channels, never mixed in one number: this suite's
verifiers classify what the agent SHIPPED (fabricated / prior_match /
decoy_capture / investigation_error - all mechanical, no judge), and
the replay probe matrix (run_probes.py --suite hallucination) measures
reader-hallucination over the same runs' journaled context states.

The fairness control lives in the blueprints, not here: every stage
prompt in every arm carries the same evidence-conduct block
(blueprints/conduct.py), so the arms differ in structure, never in
stated discipline.
"""
from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_FOOTPRINT = _HERE.parent / "footprint"
sys.path.insert(0, str(_FOOTPRINT))

import footprint as footprint_mod  # noqa: E402

TASKS_DIR = _HERE / "tasks"

FAMILIES = {
    "incident-chronicle": "loganalyzer",
    "noisy-incident": "loganalyzer",
    "policy-conflicts": "loganalyzer",
    "redacted-ledger": "analyst",
}

# The structured role is the composed flagship, by design.
STRUCTURED_VARIANT = "adversarial-scoped-flagship"

# The log tasks run in the read-only condition (no shell, no writes -
# make_readonly.py has the why); the ask test runs on ask-enabled
# variants. Both conditions apply to every arm symmetrically.
READONLY_TASKS = {"incident-chronicle", "noisy-incident",
                  "policy-conflicts"}

# Classifier counts the record's hallucination block always carries;
# a verifier only reports the ones its task can decide, the rest stay
# zero so cross-task aggregation is a plain sum.
_COUNTS = ("fabrications", "prior_matches", "decoy_captures",
           "investigation_errors")


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Suite:
    name = "hallucination"

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
            blueprint = f"{family}-bench-{variant}"
        else:
            blueprint = f"flat-{family}"
            if arm.get("variant"):
                blueprint = f"{blueprint}-{arm['variant']}"
        # The ask test runs on ask-enabled counterparts (make_askable.py)
        # for every arm symmetrically; the log tasks run on read-only
        # counterparts (make_readonly.py); everything else keeps the
        # standard no-HITL blueprints.
        if self.interaction_for(task) is not None:
            blueprint = f"{blueprint}-askable"
        elif task.get("id") in READONLY_TASKS:
            blueprint = f"{blueprint}-readonly"
        return blueprint, []

    def interaction_for(self, task: dict) -> dict | None:
        # Tolerates the runner's synthetic family-only task dicts.
        if not task.get("dir"):
            return None
        pack = task["dir"] / "user-pack.md"
        if not pack.is_file():
            return None
        return {"pack": pack.read_text(), "max_answers": 2}

    def agent_for(self, arm: dict) -> tuple[str, list]:
        return self.agent_for_task({"family": "loganalyzer"}, arm)

    def task_cli(self, task: dict) -> list:
        instructions = task["dir"] / "output-instructions.txt"
        text = (instructions.read_text().strip() if instructions.is_file()
                else "Answer exactly in the format the task requested. "
                     "Report only what you actually established.")
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

    def fold_footprint(self, artifacts_dir: Path) -> dict | None:
        """The journal fold, status-independent: a failed run's curve
        is data (the runner attaches it to error/cap records too)."""
        for name in ("run.lvr.gz", "run.lvr"):
            archive = Path(artifacts_dir) / "run" / name
            if archive.is_file():
                return footprint_mod.from_archive(archive)
        return None

    def collect(self, task: dict, workdir: Path, artifacts_dir: Path,
                answer) -> dict:
        artifacts_dir = Path(artifacts_dir).resolve()
        (artifacts_dir / "answer.txt").write_text(str(answer or ""))
        verify = _load_module(task["dir"] / "verify.py",
                              f"verify_{task['id']}")
        result = verify.verify(task["dir"], workdir, artifacts_dir, answer)
        # The journal fold rides along: input_max near the pinned window
        # is the evidence that the run actually hit the limits the suite
        # is designed around.
        fp = self.fold_footprint(artifacts_dir)
        if fp:
            result["request_footprint"] = fp
        return result

    def grade(self, task: dict, submission: dict) -> dict:
        fp = submission.pop("request_footprint", None)
        detail = submission.get("detail", {})
        # Verifiers report counts either at detail top level or under
        # a "summary" sub-dict; both are canonical, absent means zero.
        counts = detail.get("summary") or detail
        hall = {k: int(counts.get(k, 0)) for k in _COUNTS}
        hall["asked"] = detail.get("asked")
        hall["detail"] = (detail.get("classified")
                          or counts.get("captured") or {})
        record_fields = {
            "functional": {
                "score": round(float(submission.get("score", 0.0)), 4),
                "detail": detail,
            },
            "hallucination": hall,
        }
        if fp:
            record_fields["request_footprint"] = fp
        return {
            "passed": bool(submission.get("functional_pass")),
            "detail": detail,
            "record_fields": record_fields,
        }
