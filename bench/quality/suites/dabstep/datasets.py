"""Pinned DABstep task and context files.

DABstep (Adyen, CC-BY-4.0) is a data-analysis benchmark over real
payment-processing files with constrained-format answers. Only the
10-task dev split ships public answers, so that is what grades locally;
the 440-task main split is scored by the upstream leaderboard and is out
of scope here (a submission file can still be produced from the raw
records later).

Files are downloaded once by `python3 datasets.py fetch` and verified
against the sha256 pins on every use.
"""
from __future__ import annotations

import hashlib
import json
import sys
import urllib.request
from pathlib import Path

__all__ = ["DATASETS_DIR", "CONTEXT_FILES", "ensure", "verify",
           "dev_tasks", "context_path"]

DATASETS_DIR = Path(__file__).resolve().parent / "datasets"
_BASE = "https://huggingface.co/datasets/adyen/DABstep/resolve/main/data"

TASKS_FILE = ("tasks/dev.jsonl",
              "c1da755a6fe9cb538fc84719f51e1db0bff0190a1d6905767ac18c755e66a07b")
CONTEXT_FILES = {
    "acquirer_countries.csv":
        "6744cf1962e4b5086342821e627f4557c32f06c3c58e8b0ff3b449dcc634f37f",
    "fees.json":
        "9a833666ae9be5a8e756dd1fe076c72e7c502d64161315ffa8fee9e5bf2599dc",
    "manual.md":
        "bb7f4ca6fdc759af1f480702b3a3b12e17e9293b0d38a1dbfbbc8ffc1e572d2c",
    "merchant_category_codes.csv":
        "83247d79f5ddcdd180e02f184b644f4912731942a2fc58d91f2a06b911d04b41",
    "merchant_data.json":
        "f158e834de27ee8407e99d9c32da690357981d2770958fd302a9bb79ced83581",
    "payments-readme.md":
        "8754b92d0b3127856ff72266ea482995d2a1f6a34d0a12732f7c26f527f2c4a5",
    "payments.csv":
        "5fbb26210a45427d7a6560cfab3a362a08e4067f27cd03695f211a51c47ffc25",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _pins() -> list[tuple[str, str, str]]:
    rel, sha = TASKS_FILE
    pins = [(rel, Path(rel).name, sha)]
    pins += [(f"context/{name}", name, sha)
             for name, sha in CONTEXT_FILES.items()]
    return pins


def verify(datasets_dir: Path = DATASETS_DIR) -> None:
    for rel, local, sha in _pins():
        path = datasets_dir / local
        if not path.is_file():
            raise FileNotFoundError(
                f"{path} missing - run `python3 "
                "bench/quality/suites/dabstep/datasets.py fetch` first")
        actual = _sha256(path)
        if actual != sha:
            raise ValueError(f"{path} sha256 {actual} != pinned {sha}")


def ensure(datasets_dir: Path = DATASETS_DIR) -> None:
    datasets_dir.mkdir(parents=True, exist_ok=True)
    for rel, local, sha in _pins():
        path = datasets_dir / local
        if path.is_file() and _sha256(path) == sha:
            continue
        url = f"{_BASE}/{rel}"
        print(f"fetching {url}")
        path.write_bytes(urllib.request.urlopen(url, timeout=300).read())
    verify(datasets_dir)


def dev_tasks(datasets_dir: Path = DATASETS_DIR) -> list[dict]:
    verify(datasets_dir)
    tasks = []
    for line in (datasets_dir / "dev.jsonl").read_text().splitlines():
        row = json.loads(line)
        row["id"] = f"dev_{row['task_id']}"
        tasks.append(row)
    return tasks


def context_path(name: str, datasets_dir: Path = DATASETS_DIR) -> Path:
    return datasets_dir / name


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "fetch":
        ensure()
        print("datasets present and verified")
    else:
        print("usage: python3 datasets.py fetch", file=sys.stderr)
        sys.exit(2)
