"""probes.json loading and validation for the Context Retention Suite.

Schema, per task:

    {"probes": [{"after_tool_calls": int, "type": str, "question": str,
                 "expected": str, "rubric": str}, ...]}

`type` is a reporting key (factual_recall, cross_file, architecture,
...). Depths must be positive and strictly increasing - the retention
curve's x-axis comes straight from them.
"""
from __future__ import annotations

import json
from pathlib import Path

REQUIRED = ("after_tool_calls", "type", "question", "expected", "rubric")


def load_probes(path: Path) -> list[dict]:
    doc = json.loads(Path(path).read_text())
    probes = doc.get("probes")
    if not isinstance(probes, list) or not probes:
        raise ValueError(f"{path}: no probes array")
    last = 0
    for i, probe in enumerate(probes):
        missing = [k for k in REQUIRED if k not in probe]
        if missing:
            raise ValueError(f"{path}: probe {i} missing {missing}")
        depth = probe["after_tool_calls"]
        if not isinstance(depth, int) or depth <= last:
            raise ValueError(
                f"{path}: probe {i} depth {depth!r} not strictly "
                f"increasing (previous {last})")
        last = depth
    return probes
