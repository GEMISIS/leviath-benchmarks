"""The coverage channel: which of the registered chain files did the
agent actually READ, straight from the run's own journal.

This is the laziness measurement the task exists for - the deliverable
says whose story the plan tells; this says whether the agent looked.
Plotted together (chain coverage vs plan correctness, per arm) they
draw the shortcut hypothesis directly.

A file counts as read when any read-shaped tool touched it: read_file
/ read_files by path argument, or a shell command whose text names the
path (cat, sed, head, grep with a filename - the substring is enough;
we are measuring attention, not parsing shells).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_QUALITY = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(_QUALITY))

from core import lvr  # noqa: E402


def _read_blob(archive: Path) -> str:
    """Every read-ish tool argument in the journal, joined."""
    try:
        _, recs, _ = lvr.read_archive(archive)
    except Exception:
        return ""
    parts: list[str] = []
    for rec in recs:
        batch = rec.get("ToolBatch")
        if not batch:
            continue
        for call in batch.get("calls", []):
            name = call.get("name", "")
            args = call.get("arguments") or ""
            if name in ("read_file", "read_files", "shell", "bash",
                        "grep", "glob"):
                parts.append(str(args))
    return "\n".join(parts)


def coverage(task_dir: Path, archive_path: Path) -> dict:
    meta = json.loads((Path(task_dir) / "answers.json").read_text())
    blob = _read_blob(Path(archive_path))

    all_files = sorted({
        hop.split("::")[0]
        for ch in meta["chains"] for hop in ch["actual"]})
    read_files = {f for f in all_files if f in blob}

    chain_cov = {}
    for ch in meta["chains"]:
        files = [hop.split("::")[0] for hop in ch["actual"]]
        got = sum(1 for f in files if f in blob)
        chain_cov[ch["id"]] = round(got / len(files), 4)

    relevant = [ch for ch in meta["chains"]
                if ch["deceptive"] and ch["load_bearing"]]
    rel_files = sorted({hop.split("::")[0]
                        for ch in relevant for ch_hop in [ch["actual"]]
                        for hop in ch_hop})
    rel_read = sum(1 for f in rel_files if f in blob)

    return {
        "chain_coverage": chain_cov,
        "files_read": len(read_files),
        "relevant_read_fraction": (round(rel_read / len(rel_files), 4)
                                   if rel_files else 0.0),
    }
