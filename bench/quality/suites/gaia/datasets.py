"""GAIA validation-split fetcher (gated - requires HF_TOKEN).

GAIA's data is gated on Hugging Face: accept the terms for
gaia-benchmark/GAIA with your account, then export HF_TOKEN before
running `python3 datasets.py fetch`. The 165 validation questions (and
their attached files) download into datasets/, which is never committed
- the dataset's own terms ask that its content not be redistributed,
and validation answers are public, so committing them would also be a
contamination vector.

Every downloaded file's sha256 is recorded into datasets/manifest.json
on first fetch; later verifies compare against that manifest, so a
silent upstream change is caught even though we cannot pin hashes in
code before the gated download.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

__all__ = ["DATASETS_DIR", "ensure", "tasks"]

DATASETS_DIR = Path(__file__).resolve().parent / "datasets"
_BASE = "https://huggingface.co/datasets/gaia-benchmark/GAIA/resolve/main"
_SPLIT = "2023/validation"


def _request(url: str) -> bytes:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError(
            "GAIA is a gated dataset: accept its terms on Hugging Face "
            "and export HF_TOKEN before fetching")
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {token}"})
    return urllib.request.urlopen(req, timeout=300).read()


def ensure(datasets_dir: Path = DATASETS_DIR) -> None:
    datasets_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = datasets_dir / "manifest.json"
    manifest = (json.loads(manifest_path.read_text())
                if manifest_path.is_file() else {})

    meta_path = datasets_dir / "metadata.jsonl"
    if not meta_path.is_file():
        meta_path.write_bytes(
            _request(f"{_BASE}/{_SPLIT}/metadata.jsonl"))
    _record(manifest, meta_path)

    for row in _rows(meta_path):
        name = row.get("file_name")
        if not name:
            continue
        local = datasets_dir / name
        if not local.is_file():
            print(f"fetching attachment {name}")
            local.write_bytes(_request(f"{_BASE}/{_SPLIT}/{name}"))
        _record(manifest, local)

    manifest_path.write_text(json.dumps(manifest, indent=2,
                                        sort_keys=True) + "\n")
    verify(datasets_dir)


def verify(datasets_dir: Path = DATASETS_DIR) -> None:
    manifest_path = datasets_dir / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(
            f"{manifest_path} missing - run `python3 "
            "bench/quality/suites/gaia/datasets.py fetch` first")
    manifest = json.loads(manifest_path.read_text())
    for name, sha in manifest.items():
        path = datasets_dir / name
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != sha:
            raise ValueError(
                f"{path} sha256 {actual} != recorded {sha} - the "
                "upstream data changed since first fetch")


def tasks(datasets_dir: Path = DATASETS_DIR) -> list[dict]:
    verify(datasets_dir)
    out = []
    for row in _rows(datasets_dir / "metadata.jsonl"):
        row["id"] = f"gaia_{row['task_id']}"
        out.append(row)
    return out


def _rows(meta_path: Path) -> list[dict]:
    return [json.loads(line)
            for line in meta_path.read_text().splitlines() if line.strip()]


def _record(manifest: dict, path: Path) -> None:
    manifest[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "fetch":
        ensure()
        print("datasets present and verified")
    else:
        print("usage: HF_TOKEN=... python3 datasets.py fetch",
              file=sys.stderr)
        sys.exit(2)
