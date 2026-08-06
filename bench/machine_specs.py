#!/usr/bin/env python3
"""Gather the machine and binary details a benchmark result depends on.

Every result directory carries this as ``specs.json`` so a number can never
get separated from the hardware that produced it. Cross-machine comparisons
must normalize by these fields (core count for CPU, total RAM for headroom
claims).
"""
from __future__ import annotations

import hashlib
import platform
import socket
import subprocess
from datetime import datetime, timezone

import psutil


def _sysctl(name: str) -> str | None:
    try:
        out = subprocess.run(["sysctl", "-n", name], capture_output=True,
                             text=True, timeout=5)
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def _cpu_model() -> str | None:
    if platform.system() == "Darwin":
        return _sysctl("machdep.cpu.brand_string")
    if platform.system() == "Linux":
        try:
            for line in open("/proc/cpuinfo"):
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
        except OSError:
            pass
    return platform.processor() or None


def _lev_version(lev_path: str) -> str | None:
    try:
        out = subprocess.run([lev_path, "--version"], capture_output=True,
                             text=True, timeout=10)
        return out.stdout.strip().splitlines()[-1] if out.stdout else None
    except (OSError, subprocess.SubprocessError, IndexError):
        return None


def _sha256(path: str) -> str | None:
    try:
        digest = hashlib.sha256()
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1 << 20), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def gather(lev_path: str) -> dict:
    """Everything worth pinning about this run's environment."""
    vm = psutil.virtual_memory()
    return {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.release(),
        "os_version_pretty": platform.platform(),
        "arch": platform.machine(),
        "cpu_model": _cpu_model(),
        "cpu_logical_cores": psutil.cpu_count(logical=True),
        "cpu_physical_cores": psutil.cpu_count(logical=False),
        "ram_total_bytes": vm.total,
        "ram_available_at_start_bytes": vm.available,
        "python_version": platform.python_version(),
        "lev_path": lev_path,
        "lev_version": _lev_version(lev_path),
        "lev_sha256": _sha256(lev_path),
    }


if __name__ == "__main__":
    import json
    import sys

    print(json.dumps(gather(sys.argv[1] if len(sys.argv) > 1 else "lev"),
                     indent=2))
