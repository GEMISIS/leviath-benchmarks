"""Freeze-tag enforcement for counted quality rounds.

A counted run requires:
- HEAD carrying an exact ``qbench-*`` tag,
- a clean working tree,
- the frozen inputs (arms.json, rates.json, subset files, blueprints)
  hashing to what they hash to right now - recorded into round.json so
  any later drift is visible.

``--unsafe-smoke`` bypasses all of it but stamps every record with the
freeze tag ``UNFROZEN-SMOKE``, which the aggregator and renderer refuse
for anything publishable.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

__all__ = ["SMOKE_TAG", "current_tag", "require_frozen", "manifest_sha256s"]

SMOKE_TAG = "UNFROZEN-SMOKE"


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True)


def current_tag(repo: Path) -> str | None:
    out = _git(repo, "describe", "--tags", "--exact-match")
    if out.returncode != 0:
        return None
    tag = out.stdout.strip()
    return tag if tag.startswith("qbench-") else None


def require_frozen(repo: Path) -> str:
    """Return the freeze tag or raise with the exact reason."""
    tag = current_tag(repo)
    if tag is None:
        raise RuntimeError(
            "counted runs require HEAD to carry an exact qbench-* tag "
            "(use --unsafe-smoke for development runs)")
    dirty = _git(repo, "status", "--porcelain").stdout.strip()
    if dirty:
        raise RuntimeError(
            "counted runs require a clean working tree; uncommitted:\n"
            + dirty)
    return tag


def manifest_sha256s(paths: list[Path]) -> dict[str, str]:
    """sha256 of every frozen input, keyed by repo-relative-ish path."""
    out = {}
    for path in sorted(paths):
        path = Path(path)
        if path.is_dir():
            digest = hashlib.sha256()
            for sub in sorted(path.rglob("*")):
                if sub.is_file():
                    digest.update(sub.relative_to(path).as_posix().encode())
                    digest.update(sub.read_bytes())
            out[str(path)] = digest.hexdigest()
        elif path.is_file():
            out[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            raise FileNotFoundError(f"frozen input missing: {path}")
    return out
