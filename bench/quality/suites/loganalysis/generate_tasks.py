#!/usr/bin/env python3
"""Generate the log-analysis tasks from the pinned datasets.

A pure function of (seed, pinned dataset bytes): re-running with the
same seed must produce byte-identical task files - that property is
itself a test. Each task slices a contiguous window out of one dataset
and asks one question whose ground truth is machine-computed, either
from the raw lines alone (substring counts, first occurrence, level
counts - independently checkable with grep) or from the loghub 2k
line-by-line annotations (template questions - the annotation is the
declared arbiter, stated in the task prompt).

Split: half public (answer committed in plaintext), half held-out
(answer committed only as sha256(salt || normalized answer)). Both the
generator and the datasets are public, so the held-out split guards our
own development process against teaching-to-the-test - it is not a
defense against a determined adversary, and the docs say so. The reveal
file (salt + plaintext answers) is deterministic and re-emitted with
--reveal at publish time.

Usage:
    python3 generate_tasks.py --seed 42 --n 40 [--out tasks/] [--reveal]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import datasets  # noqa: E402

SLICE_MIN, SLICE_MAX = 300, 800
_TYPES = ("level_count", "substring_count", "first_occurrence",
          "template_distinct", "template_top_count")


def _salt(seed: int) -> str:
    return hashlib.sha256(f"loganalysis-heldout-{seed}".encode()).hexdigest()


def normalized(answer) -> str:
    return str(answer).strip().casefold()


def answer_hash(salt: str, answer) -> str:
    return hashlib.sha256((salt + normalized(answer)).encode()).hexdigest()


def _constant_fragment(template: str) -> str | None:
    """Longest constant run of a template, usable as a grep needle."""
    parts = [p.strip() for p in template.split("<*>")]
    parts = [p for p in parts if len(p) >= 12]
    return max(parts, key=len) if parts else None


def _make_task(rng: random.Random, dataset: str, raw: list[str],
               rows: list[dict], kind: str, index: int) -> dict | None:
    lo = rng.randrange(0, len(raw) - SLICE_MIN)
    hi = min(len(raw), lo + rng.randrange(SLICE_MIN, SLICE_MAX + 1))
    slice_raw = raw[lo:hi]
    slice_rows = rows[lo:hi]

    if kind == "level_count":
        levels = sorted({r["Level"] for r in slice_rows})
        level = rng.choice(levels)
        answer = sum(1 for r in slice_rows if r["Level"] == level)
        question = (f"How many log lines have severity level "
                    f"'{level}' (case-insensitive)?")
    elif kind == "substring_count":
        needles = sorted({f for r in slice_rows
                          if (f := _constant_fragment(r["EventTemplate"]))})
        if not needles:
            return None
        needle = rng.choice(needles)
        answer = sum(1 for line in slice_raw if needle in line)
        if answer == 0:
            return None
        question = (f"How many log lines contain the exact text "
                    f"\"{needle}\"?")
    elif kind == "first_occurrence":
        needles = sorted({f for r in slice_rows
                          if (f := _constant_fragment(r["EventTemplate"]))})
        if not needles:
            return None
        needle = rng.choice(needles)
        answer = next((i + 1 for i, line in enumerate(slice_raw)
                       if needle in line), None)
        if answer is None:
            return None
        question = (f"On which line number (1-indexed from the top of "
                    f"the file) does the text \"{needle}\" first appear?")
    elif kind == "template_distinct":
        answer = len({r["EventId"] for r in slice_rows})
        question = (
            "How many distinct message templates appear? A template "
            "treats variable fields (ids, numbers, paths, addresses) as "
            "wildcards; two lines share a template when they differ only "
            "in such fields. Ground truth follows the loghub 2k "
            "annotations for this dataset.")
    elif kind == "template_top_count":
        counts: dict[str, int] = {}
        for r in slice_rows:
            counts[r["EventId"]] = counts.get(r["EventId"], 0) + 1
        answer = max(counts.values())
        question = (
            "How many times does the most frequent message template "
            "occur? A template treats variable fields (ids, numbers, "
            "paths, addresses) as wildcards. Ground truth follows the "
            "loghub 2k annotations for this dataset.")
    else:
        raise ValueError(kind)

    return {
        "id": f"log_{index:03d}",
        "type": kind,
        "dataset": dataset,
        "slice": {"start_line": lo + 1, "end_line": hi},
        "question": question,
        "answer_format": "a single integer",
        "answer": answer,
    }


def generate(seed: int, n: int) -> list[dict]:
    datasets.verify()
    data = {name: (datasets.raw_lines(name), datasets.structured_rows(name))
            for name in sorted(datasets.REGISTRY)}
    rng = random.Random(seed)
    tasks: list[dict] = []
    attempts = 0
    while len(tasks) < n and attempts < n * 50:
        attempts += 1
        dataset = rng.choice(sorted(data))
        kind = _TYPES[len(tasks) % len(_TYPES)]
        raw, rows = data[dataset]
        task = _make_task(rng, dataset, raw, rows, kind, len(tasks) + 1)
        if task is not None:
            tasks.append(task)
    if len(tasks) < n:
        raise RuntimeError(f"only generated {len(tasks)}/{n} tasks")
    return tasks


def write_tasks(tasks: list[dict], seed: int, out_dir: Path) -> None:
    salt = _salt(seed)
    half = len(tasks) // 2
    order = list(range(len(tasks)))
    random.Random(seed + 1).shuffle(order)
    public_idx = set(order[:len(tasks) - half])
    index = {"seed": seed, "salt_scheme":
             "sha256('loganalysis-heldout-' + seed); "
             "hash = sha256(salt + normalized answer)", "heldout": {}}
    for split in ("public", "heldout"):
        (out_dir / split).mkdir(parents=True, exist_ok=True)
    for i, task in enumerate(tasks):
        task = dict(task)
        if i in public_idx:
            path = out_dir / "public" / f"{task['id']}.json"
        else:
            digest = answer_hash(salt, task.pop("answer"))
            task["answer_sha256"] = digest
            index["heldout"][task["id"]] = digest
            path = out_dir / "heldout" / f"{task['id']}.json"
        path.write_text(json.dumps(task, indent=2, sort_keys=True) + "\n")
    (out_dir / "heldout_answers.sha256").write_text(
        json.dumps(index, indent=2, sort_keys=True) + "\n")


def reveal(seed: int, n: int) -> dict:
    tasks = generate(seed, n)
    salt = _salt(seed)
    half = len(tasks) // 2
    order = list(range(len(tasks)))
    random.Random(seed + 1).shuffle(order)
    heldout_idx = set(order[len(tasks) - half:])
    return {"seed": seed, "salt": salt,
            "answers": {tasks[i]["id"]: tasks[i]["answer"]
                        for i in sorted(heldout_idx)}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--n", type=int, default=40)
    parser.add_argument("--out",
                        default=str(Path(__file__).parent / "tasks"))
    parser.add_argument("--reveal", action="store_true",
                        help="print the held-out reveal JSON instead of "
                             "writing task files")
    args = parser.parse_args()
    if args.reveal:
        print(json.dumps(reveal(args.seed, args.n), indent=2,
                         sort_keys=True))
        return 0
    write_tasks(generate(args.seed, args.n), args.seed, Path(args.out))
    print(f"wrote {args.n} tasks under {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
