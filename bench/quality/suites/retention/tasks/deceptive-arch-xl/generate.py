#!/usr/bin/env python3
"""Generate the deceptive-arch-XL corpus: the past-every-window tier.

Same lying-codebase design as deceptive-arch, scaled so the working
set exceeds a million tokens - at native 1M windows no arm can hold
the corpus, so context management is forced on everyone, not just the
pinned tiers. Twelve deceptive chains (eight load-bearing for the
capability) against twelve honest ones.

This is a thin shim over the base generator's `--scale` knob: one
source of truth for emission, self-testing and determinism; this file
pins the XL seed, scale and size bounds. Usage matches every suite
generator:

    python3 generate.py [--seed N] [--out DIR] [--check]
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
_BASE = HERE.parent / "deceptive-arch" / "generate.py"
_spec = importlib.util.spec_from_file_location("deceptive_arch_base",
                                               _BASE)
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

DEFAULT_SEED = 8117
SCALE = 4
EXPECTED_LBD = 8
MIN_TOTAL_BYTES = 6_400_000
MAX_TOTAL_BYTES = 8_400_000


def build_xl(seed: int):
    corpus, meta = base.build(seed, scale=SCALE)
    meta["scale"] = SCALE
    return corpus, meta


def self_test_xl(corpus, meta) -> None:
    base.self_test(corpus, meta, expected_lbd=EXPECTED_LBD,
                   min_bytes=MIN_TOTAL_BYTES,
                   max_bytes=MAX_TOTAL_BYTES)


def run_check(task_dir: Path, seed: int) -> int:
    corpus, meta = build_xl(seed)
    self_test_xl(corpus, meta)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        base.write_out(tmp_dir, corpus, meta)
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
    print(f"check OK: {len(fresh)} files byte-identical for seed "
          f"{seed}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", default=str(HERE))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    task_dir = Path(args.out)
    if args.check:
        return run_check(task_dir, args.seed)
    corpus, meta = build_xl(args.seed)
    self_test_xl(corpus, meta)
    base.write_out(task_dir, corpus, meta)
    total = sum(len(t.encode()) for t in corpus.values())
    print(f"seed {args.seed} scale {SCALE}: {len(corpus)} files, "
          f"{total / 1024:.0f} KiB (~{total // 4 // 1000}k tokens)")
    for c in meta["chains"]:
        if c["deceptive"]:
            print(f"  DECEPTIVE {c['id']:16} {c['defect']:18} "
                  f"fix={c['fix_locus']}")
    print(f"  load-bearing deceptive: "
          f"{', '.join(meta['load_bearing_deceptive'])}")
    print("self-test OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
