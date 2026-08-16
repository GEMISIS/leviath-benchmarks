#!/usr/bin/env python3
"""Generate the policy-conflicts-xl corpus.

The past-the-biggest-window variant of policy-conflicts: the same
policy-library world scaled until the working set exceeds a million
tokens, so even at a native 1M window no arm can hold everything and
context management is forced on all of them. Twelve semantic conflicts
(same disjoint-vocabulary discipline), twelve decoy pairs, the same
prior trap - all machinery imported from the base generator, which
guarantees the two tasks can never drift apart; this file only sets
the scale and counts.

Usage:
    python3 generate.py [--seed N] [--out DIR] [--check]
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
import tempfile
from pathlib import Path

_BASE_DIR = Path(__file__).resolve().parent.parent / "policy-conflicts"
_spec = importlib.util.spec_from_file_location(
    "policy_conflicts_base", _BASE_DIR / "generate.py")
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

DEFAULT_SEED = 7717
SCALE = 4
N_CONFLICTS = 12
N_DECOYS = 12
N_POOL = len(base.CONFLICTS)  # the full 14-template pool


def build(seed: int):
    return base.build(seed, scale=SCALE, n_conflicts=N_CONFLICTS,
                      n_decoys=N_DECOYS, n_pool=N_POOL)


def run_check(task_dir: Path, seed: int) -> int:
    corpus, registry = build(seed)
    base.self_test(corpus, registry)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        base.write_out(tmp_dir, corpus, registry, seed)
        fresh = base._tree(tmp_dir)
    committed = {k: v for k, v in base._tree(task_dir).items()
                 if k == "answers.json" or k.startswith("seed-files/")}
    problems = []
    for rel in sorted(set(fresh) | set(committed)):
        if rel not in committed:
            problems.append(f"missing from committed corpus: {rel}")
        elif rel not in fresh:
            problems.append(f"stale committed file: {rel}")
        elif fresh[rel] != committed[rel]:
            problems.append(f"byte mismatch: {rel}")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        print(f"check FAILED for seed {seed}", file=sys.stderr)
        return 1
    print(f"check OK: {len(fresh)} files byte-identical for "
          f"seed {seed}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out",
                        default=str(Path(__file__).resolve().parent))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    task_dir = Path(args.out)
    if args.check:
        return run_check(task_dir, args.seed)
    corpus, registry = build(args.seed)
    base.self_test(corpus, registry)
    base.write_out(task_dir, corpus, registry, args.seed)
    total = sum(len(t.encode()) for t in corpus.values())
    biggest = max(len(t.encode()) for t in corpus.values())
    print(f"seed {args.seed}: {len(corpus)} files, "
          f"{total / 1024 / 1024:.2f} MiB total, "
          f"~{total / 4.6 / 1e6:.2f}M tokens, biggest {biggest} bytes")
    for line in registry["answers"]:
        print(f"  {line}")
    print("self-test OK (via the base generator's derivations)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
