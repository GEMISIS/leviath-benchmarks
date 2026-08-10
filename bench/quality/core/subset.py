"""Pre-registered, seeded task-subset selection.

Subsets are drawn once, before the freeze, by a committed RNG seed over
a hashed task universe - never hand-picked and never sampled live at run
time. The runner only ever reads subset files.

Subset file shape:

    {
      "suite": "dabstep_dev",
      "seed": 42,
      "n": 25,
      "universe_sha256": "...",   # sha256 of the sorted task-id list
      "excluded": [],             # pre-registered exclusions, with reasons
      "task_ids": ["task_003", ...]
    }
"""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

__all__ = ["universe_sha256", "select", "write_subset", "load_subset"]


def universe_sha256(task_ids: list[str]) -> str:
    joined = "\n".join(sorted(task_ids)).encode()
    return hashlib.sha256(joined).hexdigest()


def select(seed: int, n: int, task_ids: list[str],
           excluded: dict[str, str] | None = None) -> list[str]:
    """Draw n ids from the (sorted, exclusion-filtered) universe.

    ``excluded`` maps task id -> reason; exclusions must be declared
    before the draw (e.g. a task whose environment image cannot build on
    the benchmark host) and are recorded in the subset file.
    """
    excluded = excluded or {}
    pool = sorted(t for t in task_ids if t not in excluded)
    if n > len(pool):
        raise ValueError(f"asked for {n} tasks but universe has {len(pool)}")
    return sorted(random.Random(seed).sample(pool, n))


def write_subset(path: Path, suite: str, seed: int, n: int,
                 task_ids: list[str],
                 excluded: dict[str, str] | None = None) -> dict:
    excluded = excluded or {}
    record = {
        "suite": suite,
        "seed": seed,
        "n": n,
        "universe_sha256": universe_sha256(task_ids),
        "excluded": [{"task_id": t, "reason": r}
                     for t, r in sorted(excluded.items())],
        "task_ids": select(seed, n, task_ids, excluded),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2) + "\n")
    return record


def load_subset(path: Path) -> dict:
    record = json.loads(Path(path).read_text())
    for key in ("suite", "seed", "n", "universe_sha256", "task_ids"):
        if key not in record:
            raise ValueError(f"subset file {path} missing {key!r}")
    return record
