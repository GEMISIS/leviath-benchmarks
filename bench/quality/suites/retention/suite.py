"""Retention Suite plugin - the third of the three focused benchmarks.

Footprint measures the economics; hallucination measures integrity and
survival under pressure; this suite measures the QUALITY OF MEMORY
over depth. Four memory axes, one task each:

- deceptive-arch (coder): a generated codebase whose documentation
  systematically lies about its wiring. The lazy path (trust the
  comments) is cheap and wrong; the diligent one (read the chains) is
  expensive and right. Novel channel: COVERAGE - the journal records
  which files each arm actually read, so shortcutting is measured,
  not inferred.
- live-service (log-analyzer): an interactive seeded fake service
  whose fault chain only manifests when poked - raw tool-call depth
  (150-300 calls) that no static corpus honestly produces.
- standing-desk (analyst): a 12-request assistant session driven by
  the scripted user; later requests silently depend on the agent's own
  earlier derivations. The retention curve is answer accuracy vs phase
  number, dependent vs independent phases.
- policy-conflicts stays in the hallucination suite but its probe
  matrix doubles as retention data (accuracy over depth).

Tools stay ON in this suite - depth and coverage are the pressure, not
tool removal - and probes ride the same corpora via
run_probes.py --suite retention.
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
    "deceptive-arch": "coder",
    "deceptive-arch-xl": "coder",
    "live-service": "loganalyzer",
    "standing-desk": "analyst",
}

STRUCTURED_VARIANT = "adversarial-scoped-flagship"

_COUNTS = ("fabrications", "prior_matches", "decoy_captures",
           "investigation_errors")


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Suite:
    name = "retention"

    def load_tasks(self, subset_record: dict | None) -> list[dict]:
        tasks = []
        if TASKS_DIR.is_dir():
            for task_dir in sorted(TASKS_DIR.iterdir()):
                if not (task_dir / "task.md").is_file():
                    continue
                if task_dir.name not in FAMILIES:
                    continue
                tasks.append({
                    "id": task_dir.name,
                    "dir": task_dir,
                    "family": FAMILIES[task_dir.name],
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
        # The session task needs the ask channel (the scripted user IS
        # the session); everything else runs the standard blueprints.
        # Flat loops host a session in their askable form as-is; the
        # staged pipeline needs the session variant, whose revisit
        # budgets fit a dozen phases (the askable ask-test variant
        # submits after the first phase or two - measured 0.17 vs 1.0).
        if self.interaction_for(task) is not None:
            suffix = "-session" if arm["role"] == "structured" else "-askable"
            blueprint = f"{blueprint}{suffix}"
        return blueprint, []

    def interaction_for(self, task: dict) -> dict | list | None:
        if not task.get("dir"):
            return None
        packs_dir = task["dir"] / "user-packs"
        if packs_dir.is_dir():
            packs = [p.read_text()
                     for p in sorted(packs_dir.glob("pack-*.md"))]
            if packs:
                return {"pack": packs, "max_answers": len(packs)}
        pack = task["dir"] / "user-pack.md"
        if pack.is_file():
            return {"pack": pack.read_text(), "max_answers": 2}
        return None

    def agent_for(self, arm: dict) -> tuple[str, list]:
        return self.agent_for_task({"family": "coder"}, arm)

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
        fp = self.fold_footprint(artifacts_dir)
        if fp:
            result["request_footprint"] = fp
        # The coverage channel: which of the corpus's load-bearing
        # files did this run actually read (deceptive-arch's shortcut
        # measurement, harmless absence elsewhere).
        cov_py = task["dir"] / "coverage.py"
        if cov_py.is_file():
            for name in ("run.lvr.gz", "run.lvr"):
                archive = artifacts_dir / "run" / name
                if archive.is_file():
                    try:
                        cov = _load_module(
                            cov_py, f"coverage_{task['id']}").coverage(
                            task["dir"], archive)
                        if cov:
                            result["coverage"] = cov
                    except Exception as exc:
                        result["coverage_error"] = str(exc)
                    break
        return result

    def grade(self, task: dict, submission: dict) -> dict:
        fp = submission.pop("request_footprint", None)
        cov = submission.pop("coverage", None)
        detail = submission.get("detail", {})
        counts = detail.get("summary") or detail
        hall = {k: int(counts.get(k, 0) or 0) for k in _COUNTS}
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
        if cov:
            record_fields["functional"]["detail"] = dict(
                detail, coverage=cov)
        return {
            "passed": bool(submission.get("functional_pass")),
            "detail": detail,
            "record_fields": record_fields,
        }
