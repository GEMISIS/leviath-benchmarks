"""Secret scan over a results tree before it becomes committable.

Two classes of leak are checked:

1. Known key shapes (provider API keys, tokens) by regex.
2. The literal values of every secret-looking environment variable
   present at run time (``*_KEY``, ``*_TOKEN``, ``*_SECRET``), so a key
   of any shape that actually made it into an artifact is caught.

The runner calls ``scan`` at the end of every invocation and refuses to
exit 0 on a hit. Records themselves never serialize the environment;
this is the backstop for tool output and artifacts.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

__all__ = ["scan"]

_PATTERNS = [
    re.compile(rb"sk-ant-[A-Za-z0-9_\-]{10,}"),
    re.compile(rb"sk-[A-Za-z0-9_\-]{20,}"),
    re.compile(rb"AIza[A-Za-z0-9_\-]{30,}"),
    re.compile(rb"hf_[A-Za-z0-9]{20,}"),
    re.compile(rb"github_pat_[A-Za-z0-9_]{20,}"),
]
_ENV_SUFFIXES = ("_KEY", "_TOKEN", "_SECRET")
_MAX_FILE_BYTES = 32 * 1024 * 1024


def _env_literals() -> list[bytes]:
    values = []
    for name, value in os.environ.items():
        if name.endswith(_ENV_SUFFIXES) and len(value) >= 8:
            values.append(value.encode())
    return values


def scan(root: Path) -> list[dict]:
    """Return findings ({file, kind}) for every leak under root."""
    findings = []
    literals = _env_literals()
    for path in sorted(Path(root).rglob("*")):
        if not path.is_file() or path.stat().st_size > _MAX_FILE_BYTES:
            continue
        data = path.read_bytes()
        for pattern in _PATTERNS:
            if pattern.search(data):
                findings.append({"file": str(path),
                                 "kind": f"pattern:{pattern.pattern.decode()}"})
        for literal in literals:
            if literal in data:
                findings.append({"file": str(path),
                                 "kind": "environment secret value"})
    return findings
