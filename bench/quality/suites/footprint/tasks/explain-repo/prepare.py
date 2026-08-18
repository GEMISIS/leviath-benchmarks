"""Seeding for explain-repo: materialize the pinned checkout.

`repo.json` names the source repository (a public `url`, a pinned
`commit`, and the cache path a clone lands in). seed() runs
    git -C <path> archive <commit> | tar -x -C <workdir>/repo
so the agent works against exactly the pinned tree: tracked files only,
no .git directory, no untracked build output. Resolution order for the
local repository: the LEVIATH_REPO environment variable, then the
cache path (cloned from `url` on first use - the one deliberate
network touch, at setup rather than at run time). If the pinned commit
is not present after that, the seed fails loudly - a silently
different tree would invalidate every grounded citation the verifier
later checks.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


def _resolve_repo(cfg: dict, task_dir: Path) -> Path:
    env = os.environ.get("LEVIATH_REPO")
    if env and (Path(env) / ".git").exists():
        return Path(env)
    root = task_dir
    while root.parent != root and not (root / ".git").exists():
        root = root.parent
    cache = root / cfg.get("cache_path", ".tasks/leviath")
    if (cache / ".git").exists():
        return cache
    url = cfg.get("url")
    if not url:
        raise RuntimeError(
            "explain-repo: no local repository (set LEVIATH_REPO or add "
            "'url' to repo.json for a one-time clone)")
    cache.parent.mkdir(parents=True, exist_ok=True)
    clone = subprocess.run(["git", "clone", "--quiet", url, str(cache)],
                           capture_output=True, text=True)
    if clone.returncode != 0:
        raise RuntimeError(f"explain-repo: clone of {url} failed: "
                           f"{clone.stderr.strip()}")
    return cache


def seed(task_dir: Path, workdir: Path) -> None:
    task_dir, workdir = Path(task_dir), Path(workdir)
    cfg = json.loads((task_dir / "repo.json").read_text())
    commit = cfg["commit"]
    src = str(_resolve_repo(cfg, task_dir))

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
