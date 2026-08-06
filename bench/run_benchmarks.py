#!/usr/bin/env python3
"""Run the leviath performance benchmarks and write raw results.

Two tracks, both against a deterministic mock provider (no network, no
token cost, byte-identical work every run):

- **memory**: 10 / 100 / 1,000 / 10,000 spawned agents at a fixed
  inference pool (512) and per-call latency (1.5s). Measures what N
  concurrent agents cost: live-memory peak and settle, CPU, exact
  concurrency.
- **pools**: a fixed 1,000-agent workload at pool widths 128 / 256 /
  512 / 1024. Measures what throughput costs: drain time, effective
  calls/s, CPU. (Pool 1024 requires leviath >= the 2048-blocking-thread
  fix; on older daemons it silently behaves like ~512.)

Outputs are RAW ONLY - per-tier monitor CSVs, reconstructed run
intervals, and a summary.json per track, plus specs.json pinning the
machine and binary. No charts are generated here; render them however
you like from the CSVs.

Usage:
    python3 bench/run_benchmarks.py --lev /path/to/lev [--track all]

The whole suite is ~45 minutes on a 16-core machine. Everything runs in
an isolated home (/tmp/levbench); your real ~/.leviath is never touched.
A safety guard aborts a tier if system available memory drops under 4 GB.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import psutil

import machine_specs

BENCH_DIR = Path(__file__).resolve().parent
# Short path on purpose: the control socket lives under it and Unix socket
# paths have a hard length cap (SUN_LEN).
HOME = Path("/tmp/levbench")
RUNS_DIR = HOME / ".leviath" / "runs"
WORKDIR = HOME / "work"
TERMINAL = {"complete", "error", "cancelled", "complete_interactive"}
LATENCY_MS = 1500
SETTLE_SECS = 45
MEMORY_TIERS = [10, 100, 1000, 10000]
MEMORY_POOL = 512
POOL_TIERS = [128, 256, 512, 1024]
POOL_SPAWNS = 1000
DIFF = ("--- a/x.py\n+++ b/x.py\n@@\n-except Exception: pass\n"
        "+except ValueError as e: log(e)")

CONFIG_TEMPLATE = """# leviath-benchmarks isolated home (generated).

[model_providers.mockx]
script = "mockx"

[limits]
max_concurrent_inferences = {pool}
max_concurrent_tools = 32
"""


def install_home() -> None:
    """Providers + agents from the repo into the isolated home, fresh."""
    shutil.rmtree(HOME, ignore_errors=True)
    (HOME / ".leviath" / "providers").mkdir(parents=True)
    WORKDIR.mkdir(parents=True)
    shutil.copy(BENCH_DIR / "providers" / "mockx.rhai",
                HOME / ".leviath" / "providers" / "mockx.rhai")
    shutil.copytree(BENCH_DIR / "agents", HOME / ".leviath" / "agents")


def env_for(latency_ms: int) -> dict:
    env = dict(os.environ, LEVIATH_HOME=str(HOME), LEVIATH_SKIP_DOTENV="1",
               LEVMOCK_LATENCY_MS=str(latency_ms))
    env.pop("LEVIATH_RUNS_DIR", None)
    return env


def spawn_batches(lev: str, spawns: int, label: str, env: dict) -> tuple[int, float]:
    """The 30/30/20/20 agent mix via one `lev run --count` batch per type."""
    batches = [
        ("wide-researcher", int(spawns * 0.3), []),
        ("deep-researcher", int(spawns * 0.3), []),
        ("reviewer", int(spawns * 0.2), ["--diff", DIFF]),
        ("data-analyst",
         spawns - int(spawns * 0.3) * 2 - int(spawns * 0.2), []),
    ]
    batches = [b for b in batches if b[1] > 0]

    def one(spec):
        agent, count, extra = spec
        out = subprocess.run(
            [lev, "run", agent, "--task", f"bench {label} {agent}", "--yolo",
             "--json", "--count", str(count), "--workdir", str(WORKDIR)]
            + extra,
            env=env, capture_output=True, text=True, timeout=1800)
        if out.returncode != 0:
            print(f"  batch {agent} FAILED: {out.stderr.strip()[:200]}",
                  file=sys.stderr)
            return 0
        return len(json.loads(out.stdout))

    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(batches)) as pool:
        total = sum(pool.map(one, batches))
    return total, time.time() - t0


def run_statuses() -> dict:
    counts: dict = {}
    for d in RUNS_DIR.iterdir() if RUNS_DIR.exists() else []:
        try:
            s = json.loads((d / "meta.json").read_text()).get("status")
        except Exception:
            continue
        counts[s] = counts.get(s, 0) + 1
    return counts


def summarize_tier(csv_path: Path) -> dict:
    """Fold one tier's monitor CSV + runs CSV into the summary record."""
    rows = list(csv.DictReader(open(csv_path)))
    live = [float(r["live_mb"]) for r in rows if r["live_mb"]]
    rss = [float(r["rss_mb"]) for r in rows if r["rss_mb"]]
    cpu = [float(r["cpu_percent"]) for r in rows if r["cpu_percent"]]
    tail = live[-20:] if len(live) >= 20 else live
    record = {
        "samples": len(rows),
        "live_mb_peak": max(live) if live else None,
        "live_mb_settled": round(sum(tail) / len(tail), 1) if tail else None,
        "rss_mb_peak": max(rss) if rss else None,
        "cpu_machine_pct_peak": max(cpu) if cpu else None,
        "cpu_machine_pct_avg": round(sum(cpu) / len(cpu), 2) if cpu else None,
    }
    runs_csv = csv_path.with_name(csv_path.stem + "_runs.csv")
    if runs_csv.exists():
        ivals = [(float(r["start_seconds"]), float(r["end_seconds"]))
                 for r in csv.DictReader(open(runs_csv))]
        events = sorted([(s, 1) for s, _ in ivals] + [(e, -1) for _, e in ivals],
                        key=lambda t: (t[0], t[1]))
        peak = c = 0
        for _, delta in events:
            c += delta
            peak = max(peak, c)
        record["total_runs"] = len(ivals)
        record["exact_peak_concurrency"] = peak
        if ivals:
            t_start = min(s for s, _ in ivals)
            t_end = max(e for _, e in ivals)
            record["active_span_secs"] = round(t_end - t_start, 1)
            # CPU restricted to the span when runs were actually alive: the
            # whole-window average dilutes over the idle settle tail and
            # understates what the workload cost.
            active_cpu = [float(r["cpu_percent"]) for r in rows
                          if r["cpu_percent"]
                          and t_start <= float(r["elapsed_seconds"]) <= t_end]
            if active_cpu:
                record["cpu_active_avg_pct"] = round(
                    sum(active_cpu) / len(active_cpu), 2)
                record["cpu_active_peak_pct"] = round(max(active_cpu), 2)
    return record


def run_tier(lev: str, spawns: int, pool: int, label: str, out_dir: Path,
             interval: float, window_cap: int) -> dict:
    """One tier: fresh daemon + monitor, batch spawn, drain, settle, stop."""
    (HOME / ".leviath" / "config.toml").write_text(
        CONFIG_TEMPLATE.format(pool=pool))
    shutil.rmtree(RUNS_DIR, ignore_errors=True)
    RUNS_DIR.mkdir(parents=True)
    env = env_for(LATENCY_MS)

    daemon = subprocess.Popen([lev, "daemon"], env=env,
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.STDOUT,
                              start_new_session=True)
    # Cold start: exec until the control socket answers a real request
    # (includes one CLI round trip, ~50-100ms of which is client startup).
    cold_t0 = time.time()
    cold_start = None
    while time.time() - cold_t0 < 30:
        if daemon.poll() is not None:
            raise RuntimeError(f"{label}: daemon died at start")
        probe = subprocess.run([lev, "ps", "--json"], env=env,
                               capture_output=True, timeout=10)
        if probe.returncode == 0:
            cold_start = round(time.time() - cold_t0, 3)
            break
        time.sleep(0.05)
    if cold_start is None:
        raise RuntimeError(f"{label}: daemon never became reachable")
    mon = subprocess.Popen(
        [sys.executable, str(BENCH_DIR / "monitor.py"), "--pid",
         str(daemon.pid), "-o", str(out_dir), "-i", str(interval),
         "--max-samples", str(int(window_cap / interval))],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
        start_new_session=True)
    time.sleep(2)

    t0 = time.time()
    spawned, spawn_secs = spawn_batches(lev, spawns, label, env)
    print(f"  spawned {spawned} in {spawn_secs:.1f}s", flush=True)

    drained_at = None
    aborted = False
    while time.time() - t0 < window_cap * 3:
        st = run_statuses()
        total = sum(st.values())
        done = sum(v for k, v in st.items() if k in TERMINAL)
        if psutil.virtual_memory().available < 4 * 1024 ** 3:
            print(f"  ABORT {label}: system memory guard", file=sys.stderr)
            aborted = True
            break
        if total >= spawned and done >= total and total > 0:
            drained_at = round(time.time() - t0, 1)
            break
        time.sleep(min(10, max(2, spawns / 200)))

    if not aborted:
        # Bigger bursts release memory over a longer tail; a fixed 45s window
        # snapshots mid-release at 10k+ and misreports the settle.
        time.sleep(max(SETTLE_SECS, spawns // 80))
    # SIGINT makes the monitor write its CSV/PNG/runs outputs.
    os.killpg(os.getpgid(mon.pid), signal.SIGINT)
    try:
        mon.wait(timeout=120)
    except subprocess.TimeoutExpired:
        mon.kill()
    os.killpg(os.getpgid(daemon.pid),
              signal.SIGKILL if aborted else signal.SIGTERM)
    try:
        daemon.wait(timeout=20)
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(daemon.pid), signal.SIGKILL)

    # The monitor writes timestamped outputs; give them the tier's name.
    newest = max(p for p in out_dir.glob("leviath_monitor_*.csv")
                 if not p.stem.endswith("_runs"))
    stem = newest.stem
    newest.rename(out_dir / f"{label}.csv")
    runs_artifact = out_dir / f"{stem}_runs.csv"
    if runs_artifact.exists():
        runs_artifact.rename(out_dir / f"{label}_runs.csv")
    png_artifact = out_dir / f"{stem}.png"
    if png_artifact.exists():
        # Raw-output policy: the monitor renders a PNG as a side effect;
        # results directories carry data only.
        png_artifact.unlink()
    record = {
        "label": label,
        "spawns_requested": spawns,
        "spawns_ok": spawned,
        "pool": pool,
        "latency_ms": LATENCY_MS,
        "cold_start_secs": cold_start,
        "spawn_secs": round(spawn_secs, 2),
        "drained_at_secs": drained_at,
        "aborted": aborted,
        "statuses": run_statuses(),
        **summarize_tier(out_dir / f"{label}.csv"),
    }
    print(f"  {label}: drained={drained_at}s "
          f"live_peak={record['live_mb_peak']}MB "
          f"concurrency={record.get('exact_peak_concurrency')}", flush=True)
    return record


def parse_version(text: str | None) -> tuple | None:
    """`lev 0.2.0` / `v0.2.0` -> (0, 2, 0), or None if unparseable."""
    if not text:
        return None
    token = text.strip().split()[-1].lstrip("v")
    parts = token.split(".")
    try:
        return tuple(int(p) for p in parts[:3])
    except ValueError:
        return None


def latest_released_version() -> tuple | None:
    """The newest leviath release tag on GitHub, or None if unreachable."""
    import urllib.request

    try:
        req = urllib.request.Request(
            "https://api.github.com/repos/GEMISIS/leviath/releases/latest",
            headers={"Accept": "application/vnd.github+json",
                     "User-Agent": "leviath-benchmarks"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return parse_version(json.load(resp).get("tag_name"))
    except Exception:
        return None


def resolve_lev(path_arg: str | None, allow_outdated: bool) -> str:
    """Find the lev binary and gate on it being the latest release."""
    candidate = path_arg or shutil.which("lev")
    if candidate is None or not Path(candidate).exists():
        sys.exit(
            "error: no leviath install found.\n"
            "  Install leviath first (https://github.com/GEMISIS/leviath#installation),\n"
            "  or point at a binary explicitly: --lev /path/to/lev\n"
            "  This tool never installs anything for you."
        )
    lev = str(Path(candidate).resolve())
    local = parse_version(machine_specs._lev_version(lev))
    latest = latest_released_version()
    if latest is None:
        print("warning: could not reach GitHub to check the latest leviath "
              "release; skipping the version gate", file=sys.stderr)
        return lev
    if local is None:
        sys.exit(f"error: could not read a version from '{lev} --version'; "
                 "is this a leviath binary?")
    if local < latest and not allow_outdated:
        sys.exit(
            f"error: this lev is {'.'.join(map(str, local))} but the latest "
            f"release is {'.'.join(map(str, latest))}.\n"
            "  Benchmarks published from old builds mislead everyone who "
            "reads them.\n"
            "  Upgrade leviath, or pass --allow-outdated to measure an old "
            "build on purpose\n"
            "  (the version lands in specs.json either way)."
        )
    return lev


AGGREGATE_FIELDS = (
    "cold_start_secs", "spawn_secs", "drained_at_secs", "live_mb_peak",
    "live_mb_settled", "rss_mb_peak", "cpu_machine_pct_peak",
    "cpu_machine_pct_avg", "cpu_active_avg_pct", "cpu_active_peak_pct",
    "exact_peak_concurrency", "total_runs", "active_span_secs",
)


def aggregate(label: str, runs: list[dict]) -> dict:
    """Median / min / max across a tier's repetitions.

    Median rather than mean because one repetition disturbed by unrelated
    system activity should not drag the reported number; min/max carry the
    spread so readers see the variance instead of trusting a point value.
    With one repetition all three are that run's value.
    """
    import statistics

    def fold(fn):
        out = {}
        for field in AGGREGATE_FIELDS:
            values = [r[field] for r in runs
                      if isinstance(r.get(field), (int, float))]
            if values:
                out[field] = round(fn(values), 3)
        return out

    return {
        "label": label,
        "repetitions": len(runs),
        "median": fold(statistics.median),
        "min": fold(min),
        "max": fold(max),
        "runs": runs,
    }


def run_tier_repeated(lev: str, spawns: int, pool: int, label: str,
                      out_dir: Path, interval: float, window_cap: int,
                      repeat: int) -> dict:
    runs = []
    for rep in range(1, repeat + 1):
        rep_label = label if repeat == 1 else f"{label}_rep{rep}"
        runs.append(run_tier(lev, spawns, pool, rep_label, out_dir,
                             interval, window_cap))
    return aggregate(label, runs)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the leviath performance benchmarks.")
    parser.add_argument("--lev", default=None,
                        help="path to the lev binary (default: `lev` on PATH)")
    parser.add_argument("--track", choices=["memory", "pools", "all"],
                        default="all",
                        help="which benchmark track to run (default: all)")
    parser.add_argument("--repeat", type=int, default=1,
                        help="repetitions per tier; summaries report "
                             "median and min/max (use 3+ for published "
                             "numbers, default: 1)")
    parser.add_argument("--allow-outdated", action="store_true",
                        help="permit benchmarking a lev older than the "
                             "latest release")
    parser.add_argument("--out", default=str(BENCH_DIR.parent / "results"))
    args = parser.parse_args()
    if args.repeat < 1:
        parser.error("--repeat must be at least 1")
    lev = resolve_lev(args.lev, args.allow_outdated)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    result_dir = Path(args.out) / f"{stamp}_{socket.gethostname()}"
    result_dir.mkdir(parents=True)
    (result_dir / "specs.json").write_text(
        json.dumps(machine_specs.gather(lev), indent=2) + "\n")
    install_home()

    if args.track in ("memory", "all"):
        print(f"== memory track (pool {MEMORY_POOL}, {LATENCY_MS}ms/call) ==",
              flush=True)
        mem_dir = result_dir / "memory"
        mem_dir.mkdir()
        tiers = []
        for n in MEMORY_TIERS:
            interval = 1.0 if n >= 10000 else 0.5
            window = {10: 240, 100: 240, 1000: 480}.get(n, 1800)
            tiers.append(run_tier_repeated(lev, n, MEMORY_POOL, f"mem_{n}",
                                           mem_dir, interval, window,
                                           args.repeat))
        (mem_dir / "summary.json").write_text(
            json.dumps({"track": "memory", "repetitions": args.repeat,
                        "tiers": tiers}, indent=2) + "\n")

    if args.track in ("pools", "all"):
        print(f"== pool track ({POOL_SPAWNS} spawns, {LATENCY_MS}ms/call) ==",
              flush=True)
        pool_dir = result_dir / "pools"
        pool_dir.mkdir()
        tiers = []
        for p in POOL_TIERS:
            tiers.append(run_tier_repeated(lev, POOL_SPAWNS, p, f"pool_{p}",
                                           pool_dir, 0.5, 900, args.repeat))
        (pool_dir / "summary.json").write_text(
            json.dumps({"track": "pools", "repetitions": args.repeat,
                        "tiers": tiers}, indent=2) + "\n")

    shutil.rmtree(HOME, ignore_errors=True)
    print(f"results: {result_dir}")
    return 0


if __name__ == "__main__":
    lat = subprocess.Popen(
        [sys.executable, str(BENCH_DIR / "latency_server.py")],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True)
    time.sleep(1)
    try:
        sys.exit(main())
    finally:
        lat.terminate()
