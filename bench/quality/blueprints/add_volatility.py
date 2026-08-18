#!/usr/bin/env python3
"""Annotate region declarations with volatility (leviath #474/#480).

The runtime orders the prompt by each region's declared volatility
(stable first, then grows, then rewritten) and places cache markers in
front of the churn. Undeclared regions default to `rewritten` - sorted
last, never cached ahead of anything - so an unannotated blueprint gets
no benefit from the ordering work. This script applies one honest,
name+kind-based policy to the four hand-maintained bases; every
generated variant (adversarial/scoped/mix/flat/askable/readonly)
inherits the annotations through the regeneration chain.

The policy, matching the runtime docs and the #474 guidance:
- `stable`  - seeded at spawn, never agent-written: the task text and
  static reference material. Sorts first; a write here would invalidate
  the whole prompt, so only genuinely static regions qualify.
- `grows`   - appended to as the run goes (agent-written pinned regions,
  sliding windows, compact histories). Chunked so the settled part
  caches while only the newest entries are re-sent.
- (default) - compacting/temporary/clearable regions are rebuilt or
  evicted wholesale; the `rewritten` default is already the honest
  declaration, so those lines are left untouched.

Exception to the default (leviath #490): a lifecycle region may now
declare `grows` and get within-stage chunk caching - the kind only
names when contents are thrown away, not whether they hold still in
between. The temporary regions that are append-mostly corpus dumps
(`logs`, `data_preview`, `raw_findings`) declare it; working regions
that genuinely rewrite (`scratch`, `test_results`, `contradictions`)
keep the default.

Idempotent: lines already carrying `volatility` are skipped.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

BASES = ("analyst-bench", "coder-bench", "loganalyzer-bench",
         "researcher-bench")

# Seeded-once, never a context_write target in any of our stages.
STABLE_NAMES = {"task", "stage_instructions", "query", "conventions",
                "format", "scope", "architecture", "repo_files"}

GROWS_KINDS = {"pinned", "sliding_window", "compact_history"}

# Append-mostly lifecycle regions (leviath #490): chunk-cacheable
# within a stage once declared, evicted wholesale at stage exit as
# before. Only these names; other temporary/clearable regions rewrite.
TEMP_GROWS_NAMES = {"logs", "data_preview", "raw_findings"}

LINE_RE = re.compile(
    r'^(\s*)([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{\s*kind\s*=\s*"([a-z_]+)"')


def annotate(text: str) -> tuple[str, int]:
    out, changed = [], 0
    for line in text.splitlines(keepends=True):
        m = LINE_RE.match(line)
        if m and "volatility" not in line:
            name, kind = m.group(2), m.group(3)
            vol = None
            if name in STABLE_NAMES and kind == "pinned":
                vol = "stable"
            elif kind in GROWS_KINDS:
                vol = "grows"
            elif (name in TEMP_GROWS_NAMES
                  and kind in ("temporary", "clearable")):
                vol = "grows"
            if vol:
                needle = f'kind = "{kind}"'
                line = line.replace(needle,
                                    f'{needle}, volatility = "{vol}"', 1)
                changed += 1
        out.append(line)
    return "".join(out), changed


def main() -> int:
    total = 0
    for base in BASES:
        path = HERE / base / "agent.leviath"
        text = path.read_text()
        new, changed = annotate(text)
        if changed:
            path.write_text(new)
        print(f"{base}: {changed} region lines annotated")
        total += changed
    return 0 if total or "--check" not in sys.argv else 1


if __name__ == "__main__":
    sys.exit(main())
