"""Pinned public log datasets the log-analysis tasks are generated from.

The upstream data is the loghub 2k annotated sample set (raw log plus a
line-by-line structured CSV giving Level, EventId, and EventTemplate per
line). The files are small, public, and pinned by sha256; they are NOT
committed to this repo - `python3 datasets.py fetch` downloads them into
datasets/ and verifies every byte against the pins below. Task
generation and task preparation both refuse to run on bytes that do not
match the pins, so every derived number is reproducible.
"""
from __future__ import annotations

import csv
import hashlib
import sys
import urllib.request
from pathlib import Path

__all__ = ["REGISTRY", "DATASETS_DIR", "ensure", "verify", "raw_lines",
           "structured_rows"]

DATASETS_DIR = Path(__file__).resolve().parent / "datasets"
_BASE = "https://raw.githubusercontent.com/logpai/loghub/master"

REGISTRY = {
    "Apache": {
        "log": ("Apache/Apache_2k.log",
                "c7efa3eb686e3a96bd2f8f4457b2a7887e9cf2f3649327f1b4e87af841363ce8"),
        "structured": ("Apache/Apache_2k.log_structured.csv",
                       "54331d12eedf513f2127f4d89f0284c8b15fddfa5471103abf9db2c73d737778"),
    },
    "Zookeeper": {
        "log": ("Zookeeper/Zookeeper_2k.log",
                "e40e0af5ef9eb6e4097200f260b9d1f626b3676f861a432e87977242e75543d8"),
        "structured": ("Zookeeper/Zookeeper_2k.log_structured.csv",
                       "e4a450c67595828103cfab049d971f54eee778fdded061222ba6581bed2a210a"),
    },
    "HDFS": {
        "log": ("HDFS/HDFS_2k.log",
                "7c967000980c086ed55fa6544ba4f05fe66d44622795e890c68caf8bbb635035"),
        "structured": ("HDFS/HDFS_2k.log_structured.csv",
                       "729df59774e3dde934044028546d2a55d5e3d4370b9d12fcebbe4c087b2bf7b4"),
    },
}


def _local(name: str, kind: str) -> Path:
    rel, _ = REGISTRY[name][kind]
    return DATASETS_DIR / Path(rel).name


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(datasets_dir: Path = DATASETS_DIR) -> None:
    """Raise unless every pinned file is present and byte-identical."""
    for name, kinds in REGISTRY.items():
        for kind, (rel, sha) in kinds.items():
            path = datasets_dir / Path(rel).name
            if not path.is_file():
                raise FileNotFoundError(
                    f"{path} missing - run "
                    "`python3 bench/quality/suites/loganalysis/datasets.py "
                    "fetch` first (nothing is downloaded implicitly)")
            actual = _sha256(path)
            if actual != sha:
                raise ValueError(f"{path} sha256 {actual} != pinned {sha}")


def ensure(datasets_dir: Path = DATASETS_DIR) -> None:
    """Download any missing pinned file, then verify everything."""
    datasets_dir.mkdir(parents=True, exist_ok=True)
    for name, kinds in REGISTRY.items():
        for kind, (rel, sha) in kinds.items():
            path = datasets_dir / Path(rel).name
            if path.is_file() and _sha256(path) == sha:
                continue
            url = f"{_BASE}/{rel}"
            print(f"fetching {url}")
            data = urllib.request.urlopen(url, timeout=60).read()
            path.write_bytes(data)
    verify(datasets_dir)


def raw_lines(name: str, datasets_dir: Path = DATASETS_DIR) -> list[str]:
    return _sha_checked(name, "log", datasets_dir).read_text(
        errors="replace").splitlines()


def structured_rows(name: str,
                    datasets_dir: Path = DATASETS_DIR) -> list[dict]:
    with open(_sha_checked(name, "structured", datasets_dir),
              newline="") as fh:
        return list(csv.DictReader(fh))


def _sha_checked(name: str, kind: str, datasets_dir: Path) -> Path:
    rel, sha = REGISTRY[name][kind]
    path = datasets_dir / Path(rel).name
    if not path.is_file() or _sha256(path) != sha:
        raise ValueError(
            f"{path} missing or does not match its pin; run "
            "`python3 bench/quality/suites/loganalysis/datasets.py fetch`")
    return path


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "fetch":
        ensure()
        print("datasets present and verified")
    else:
        print("usage: python3 datasets.py fetch", file=sys.stderr)
        sys.exit(2)
