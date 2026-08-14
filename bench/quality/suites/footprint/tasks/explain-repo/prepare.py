"""Seeding for explain-repo: materialize the pinned checkout.

`repo.json` names a local repository and a pinned commit. seed() runs
    git -C <path> archive <commit> | tar -x -C <workdir>/repo
so the agent works against exactly the pinned tree: tracked files only,
no .git directory, no untracked build output, no network. If the pinned
commit is not present in the local repository the seed fails loudly -
a silently different tree would invalidate every grounded citation the
verifier later checks.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


def seed(task_dir: Path, workdir: Path) -> None:
    task_dir, workdir = Path(task_dir), Path(workdir)
    cfg = json.loads((task_dir / "repo.json").read_text())
    src, commit = cfg["path"], cfg["commit"]

    if not (Path(src) / ".git").exists():
        raise RuntimeError(f"explain-repo: source repository not found "
                           f"at {src} (repo.json 'path')")

    probe = subprocess.run(
        ["git", "-C", src, "cat-file", "-e", f"{commit}^{{commit}}"],
        capture_output=True, text=True)
    if probe.returncode != 0:
        raise RuntimeError(
            f"explain-repo: pinned commit {commit} is unknown in {src} "
            f"(fetch it there first; seeding never touches the network): "
            f"{probe.stderr.strip()}")

    dest = workdir / "repo"
    dest.mkdir(parents=True, exist_ok=True)
    if any(dest.iterdir()):
        raise RuntimeError(f"explain-repo: {dest} is not empty")

    archive = subprocess.Popen(
        ["git", "-C", src, "archive", commit],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    extract = subprocess.run(
        ["tar", "-x", "-C", str(dest)],
        stdin=archive.stdout, capture_output=True, text=True)
    archive.stdout.close()
    _, archive_err = archive.communicate()
    if archive.returncode != 0:
        raise RuntimeError(f"explain-repo: git archive failed: "
                           f"{archive_err.decode(errors='replace').strip()}")
    if extract.returncode != 0:
        raise RuntimeError(f"explain-repo: tar extract failed: "
                           f"{extract.stderr.strip()}")
    if not (dest / "Cargo.toml").is_file():
        raise RuntimeError(f"explain-repo: {dest} materialized without a "
                           f"root Cargo.toml - wrong tree?")
