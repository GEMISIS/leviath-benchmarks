#!/usr/bin/env python3
"""Assert the property that was broken: no edge summarises a deliverable.

A bare `transform = "compact"` hands EVERY stage-specific region to the
summariser - the runtime preserves only pinned, compact-history, hashmap
and persistent-custom regions. That silently includes `results`, which
holds the run's actual figures and, for a tool-less output stage, is the
only channel it can read. An analysis whose numbers were paraphrased on
the way to the answer stage is not an analysis.

So: every edge states carry/compact/clear explicitly, protected regions
are never summarised, and they are cleared only on an edge whose
destination can rebuild them.

Run after any blueprint edit, alongside check_pairs.py.
"""
import glob
import sys
import tomllib
from pathlib import Path

BP = Path(__file__).resolve().parent

# Regions whose content is the run's evidence or deliverable. These may
# never be summarised or cleared on an edge.
PROTECTED = {"results", "test_results", "findings", "answer", "evidence",
             "implementation", "plan", "data_map"}

bad = []
for path in sorted(glob.glob(str(BP / "*" / "agent.leviath"))):
    doc = tomllib.load(open(path, "rb"))
    agent = Path(path).parent.name
    for stage, st in doc["stages"].items():
        for target, edge in (st.get("transitions") or {}).items():
            tf = edge.get("transform", "direct")
            if tf == "compact":
                bad.append(f"{agent}: {stage} -> {target} uses a bare compact")
                continue
            if tf != "custom":
                continue
            cfg = edge.get("transform_config") or {}
            carry = set(cfg.get("carry") or [])
            # Summarising a deliverable is always wrong: the figures stop
            # being the figures.
            hit = PROTECTED.intersection(cfg.get("compact") or []) - carry
            if hit:
                bad.append(f"{agent}: {stage} -> {target} would "
                           f"compact {sorted(hit)}")
            # Clearing one is wrong only if the destination cannot rebuild
            # it. Dropping stale test output on the way back into the stage
            # that reruns the tests is correct; dropping it on the way out
            # to a stage that only reads it destroys the evidence.
            dest = doc["stages"].get(target) or {}
            routing = dest.get("tool_routing") or {}
            # An override is a region string or a {region,
            # max_result_tokens} table; a cap-only table names no region.
            writes = {v if isinstance(v, str) else v.get("region")
                      for v in routing.get("overrides", {}).values()}
            writes.discard(None)
            if routing.get("default_region"):
                writes.add(routing["default_region"])
            hit = PROTECTED.intersection(cfg.get("clear") or []) - carry - writes
            if hit:
                bad.append(f"{agent}: {stage} -> {target} clears "
                           f"{sorted(hit)}, which {target} cannot rebuild")

for line in bad:
    print("FAIL:", line)
print(f"{len(bad)} violations" if bad else
      "no edge summarises or clears a deliverable region")
sys.exit(1 if bad else 0)
