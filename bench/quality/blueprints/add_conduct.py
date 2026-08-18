#!/usr/bin/env python3
"""Inject the shared conduct block into the hand-authored base
blueprints (conduct.py has the why). Idempotent: a prompt that already
carries the block is left alone, so re-running is always safe.

Only the four bases are edited; every generated arm inherits - the
variants through their generators reading the bases, the flat arms
through make_flat.py appending the same constant. Regenerate after
running this:

    python3 add_conduct.py && python3 make_flat.py && \
    python3 make_adversarial.py && python3 make_scoped.py && \
    python3 make_mix.py && python3 check_pairs.py
"""
from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from conduct import CONDUCT, CONDUCT_MARK  # noqa: E402
from make_flat import PAIRS  # noqa: E402

PROMPT_RE = re.compile(r'system_prompt = """\n(.*?)"""', re.DOTALL)


def inject(text: str) -> tuple[str, int, int]:
    added = skipped = 0

    def repl(m: re.Match) -> str:
        nonlocal added, skipped
        body = m.group(1)
        if CONDUCT_MARK in body:
            skipped += 1
            return m.group(0)
        added += 1
        return f'system_prompt = """\n{body.rstrip()}\n\n{CONDUCT}\n"""'

    return PROMPT_RE.sub(repl, text), added, skipped


def main() -> int:
    # The bases, plus the critic-stage fragments the adversarial
    # variants splice in - a critic's request must carry the block too.
    targets = [HERE / base / "agent.leviath" for base in PAIRS]
    targets += sorted((HERE / "parts").glob("*.toml"))
    for path in targets:
        label = (path.parent.name if path.name == "agent.leviath"
                 else f"parts/{path.name}")
        out, added, skipped = inject(path.read_text())
        doc = tomllib.loads(out)  # must still parse before landing
        for stage, sdoc in doc.get("stages", {}).items():
            if CONDUCT_MARK not in sdoc.get("system_prompt", ""):
                print(f"{label}/{stage}: no system_prompt matched the "
                      "injector - fix the regex or the blueprint")
                return 1
        path.write_text(out)
        print(f"{label}: conduct block in {added + skipped} stage "
              f"prompt(s) ({added} added, {skipped} already present)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
