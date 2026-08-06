#!/usr/bin/env python3
"""Render one overview figure from a benchmark results directory.

Presentation lives here, data lives in results/: run this by hand when you
want a picture; nothing in the benchmark itself generates charts.

Usage:
    python3 bench/render_chart.py results/<stamp>_<host> [-o chart.png]
        [--coldstart results/<other-stamp>_<host>]

The results directory must hold memory/ and pools/ summaries; the
coldstart/ track is read from the same directory unless --coldstart names
a different results directory (tracks can be run separately).
"""
import argparse
import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("results", help="results/<stamp>_<host> directory")
parser.add_argument("-o", "--out", default="benchmark_overview.png")
parser.add_argument("--coldstart", default=None,
                    help="results dir holding coldstart/ (default: same)")
args = parser.parse_args()

R = Path(args.results)
COLD_DIR = Path(args.coldstart) if args.coldstart else R
OUT = Path(args.out)
for need, where in (("memory", R), ("pools", R), ("coldstart", COLD_DIR)):
    if not (where / need / "summary.json").exists():
        sys.exit(f"error: {where / need}/summary.json not found")

spec = json.load(open(R / "specs.json"))
mem = json.load(open(R / "memory" / "summary.json"))["tiers"]
pools = json.load(open(R / "pools" / "summary.json"))["tiers"]
cold = json.load(open(COLD_DIR / "coldstart" / "summary.json"))
m = lambda t: t["median"]

MEM_SERIES = [("mem_10", "10", "tab:green"), ("mem_100", "100", "tab:blue"),
              ("mem_1000", "1k", "tab:purple"), ("mem_10000", "10k", "tab:red")]
POOL_SERIES = [("pool_128", "128", "tab:green"), ("pool_256", "256", "tab:blue"),
               ("pool_512", "512", "tab:purple"), ("pool_1024", "1024", "tab:red")]
mem_labels = ["10", "100", "1k", "10k"]
pool_labels = ["128", "256", "512", "1024"]
x4 = range(4)


def label_bars(ax, bars, fmt):
    for bar in bars:
        ax.annotate(fmt.format(bar.get_height()),
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    textcoords="offset points", xytext=(0, 3),
                    ha="center", fontsize=9)


def bar_spread(ax, xs, tiers, field, color, fmt, width=0.8):
    """Median bars with min/max whiskers across the tier's repetitions.
    With one repetition the whiskers have zero length and vanish."""
    med = [t["median"][field] for t in tiers]
    lo = [t["median"][field] - t["min"][field] for t in tiers]
    hi = [t["max"][field] - t["median"][field] for t in tiers]
    bars = ax.bar(xs, med, width, color=color)
    ax.errorbar(xs, med, yerr=[lo, hi], fmt="none", ecolor="black",
                capsize=3, linewidth=1)
    label_bars(ax, bars, fmt)
    return bars


def each_rep_series(track, stem, col):
    """One (xs, ys) per repetition CSV of this tier (mem_10.csv or
    mem_10_rep1.csv ... - both layouts)."""
    out = []
    for path in sorted((R / track).glob(f"{stem}*.csv")):
        if path.stem.endswith("_runs"):
            continue
        xs, ys = [], []
        for r in csv.DictReader(open(path)):
            if r[col]:
                xs.append(float(r["elapsed_seconds"]))
                ys.append(float(r[col]))
        out.append((xs, ys))
    return out


fig, axes = plt.subplots(3, 3, figsize=(16, 13))

# ── Row 1: memory ladder ──
ax = axes[0][0]
bar_spread(ax, x4, mem, "live_mb_peak", "tab:purple", "{:.0f}")
ax.set_xticks(x4, mem_labels)
ax.set_xlabel("Agents spawned")
ax.set_ylabel("MB")
ax.set_title("Peak live memory")

ax = axes[0][1]
for stem, label, color in MEM_SERIES:
    for i, (xs, ys) in enumerate(each_rep_series("memory", stem, "live_mb")):
        ax.plot(xs, ys, color=color, linewidth=1.3, alpha=0.7,
                label=label if i == 0 else None)
ax.set_xlim(0, 900)
ax.set_xlabel("Seconds since tier start")
ax.set_ylabel("Live memory (MB)")
ax.set_title("Memory over time: rises with work, returns after drain")
ax.legend(fontsize=9, title="agents")

ax = axes[0][2]
width = 0.4
ax.bar([i - width / 2 for i in x4], [m(t)["total_runs"] for t in mem],
       width, color="lightgray", label="total runs")
bar_spread(ax, [i + width / 2 for i in x4], mem, "exact_peak_concurrency",
           "tab:orange", "{:.0f}", width=width)
ax.bar(0, 0, color="tab:orange", label="peak simultaneous")
ax.set_xticks(x4, mem_labels)
ax.set_xlabel("Agents spawned")
ax.set_ylabel("Runs")
ax.set_title("Concurrency: simultaneous vs total runs")
ax.legend(fontsize=9)

# ── Row 2: pool sweep ──
ax = axes[1][0]
bar_spread(ax, x4, pools, "drained_at_secs", "tab:red", "{:.0f}s")
ax.set_xticks(x4, pool_labels)
ax.set_xlabel("Inference pool width")
ax.set_ylabel("Seconds")
ax.set_title("Time to finish 1,000 agents")

ax = axes[1][1]
for stem, label, color in POOL_SERIES:
    for i, (xs, ys) in enumerate(each_rep_series("pools", stem, "live_mb")):
        ax.plot(xs, ys, color=color, linewidth=1.3, alpha=0.7,
                label=label if i == 0 else None)
ax.set_xlim(0, 330)
ax.set_xlabel("Seconds since tier start")
ax.set_ylabel("Live memory (MB)")
ax.set_title("Pool sweep over time: tall-and-short vs low-and-long")
ax.legend(fontsize=9, title="pool")

ax = axes[1][2]
bar_spread(ax, x4, pools, "cpu_active_avg_pct", "tab:red", "{:.1f}%")
ax.set_xticks(x4, pool_labels)
ax.set_xlabel("Inference pool width")
ax.set_ylabel("% of whole machine (16 cores)")
ax.set_ylim(0, 100)
ax.set_title("CPU while runs were active\n(avg of whole-machine share; 100% = all cores)")

# ── Row 3: cold start + CPU over time ──
ax = axes[2][0]
boot = cold["daemon_boot"]
ready_ms = (boot["ready_secs"]["median"]
            - boot["probe_baseline_secs"]["median"]) * 1000
accept_ms = boot["socket_accept_secs"]["median"] * 1000
newrun = cold["new_run_cold"]
paused = cold["paused_resumption"]

def spread(s):
    return ((s["median"] - s["min"]) * 1000,
            min((s["max"] - s["median"]) * 1000, 60))

# The boot segment of every bar is measured INSIDE that scenario (a 1ms
# socket-accept watcher runs during the command), never assumed from
# another bar.
scen = [
    ("daemon boot", ready_ms, 0.0, *spread(boot["ready_secs"])),
    ("new run,\nnothing running",
     newrun["boot_accept_secs"]["median"] * 1000,
     (newrun["total_secs"]["median"]
      - newrun["boot_accept_secs"]["median"]) * 1000,
     *spread(newrun["total_secs"])),
    ("paused run\nresumed",
     paused["boot_accept_secs"]["median"] * 1000,
     (paused["total_secs"]["median"]
      - paused["boot_accept_secs"]["median"]) * 1000,
     *spread(paused["total_secs"])),
]
xs = range(len(scen))
b1 = ax.bar(xs, [s[1] for s in scen], color="tab:blue",
            label="daemon boot portion")
b2 = ax.bar(xs, [s[2] for s in scen], bottom=[s[1] for s in scen],
            color="lightsteelblue", label="everything after boot")
totals = [s[1] + s[2] for s in scen]
ax.errorbar(xs, totals,
            yerr=[[s[3] for s in scen], [s[4] for s in scen]],
            fmt="none", ecolor="black", capsize=4)
for i, total in enumerate(totals):
    ax.annotate(f"{total:.0f}ms", (i, total), textcoords="offset points",
                xytext=(0, 5), ha="center", fontsize=9)
ax.set_xticks(xs, [s[0] for s in scen])
ax.set_ylabel("Milliseconds")
ax.legend(fontsize=8, loc="upper left")
ax.set_title("Fully-cold scenarios (25/15/10 reps)\n"
             "(boot measured within each scenario; whiskers = min/max)")

ax = axes[2][1]
for stem, label, color in MEM_SERIES:
    for i, (xs, ys) in enumerate(each_rep_series("memory", stem, "cpu_percent")):
        ax.plot(xs, ys, color=color, linewidth=0.9, alpha=0.6,
                label=label if i == 0 else None)
ax.set_xlim(0, 900)
ax.set_ylim(0, 100)
ax.set_xlabel("Seconds since tier start")
ax.set_ylabel("CPU, % of whole machine")
ax.set_title("CPU over time - memory ladder")
ax.legend(fontsize=9, title="agents")

ax = axes[2][2]
for stem, label, color in POOL_SERIES:
    for i, (xs, ys) in enumerate(each_rep_series("pools", stem, "cpu_percent")):
        ax.plot(xs, ys, color=color, linewidth=0.9, alpha=0.6,
                label=label if i == 0 else None)
ax.set_xlim(0, 330)
ax.set_ylim(0, 100)
ax.set_xlabel("Seconds since tier start")
ax.set_ylabel("CPU, % of whole machine")
ax.set_title("CPU over time - pool sweep")
ax.legend(fontsize=9, title="pool")

for row in axes:
    for ax in row:
        ax.grid(True, alpha=0.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

ram_gb = round(spec["ram_total_bytes"] / 2**30)
size_bytes = spec.get("lev_binary_size_bytes")
if size_bytes is None:
    # Results recorded before the field existed: read the binary if it is
    # still where specs.json says it was.
    try:
        size_bytes = Path(spec["lev_path"]).stat().st_size
    except OSError:
        size_bytes = None
size_note = f", {size_bytes / 2**20:.1f} MB single binary" if size_bytes else ""
reps = json.load(open(R / "memory" / "summary.json")).get("repetitions", 1)
rep_note = f" - median of {reps} reps, whiskers = min/max" if reps > 1 else ""
fig.suptitle(
    f"leviath benchmarks - {spec['cpu_model']} ({spec['cpu_logical_cores']} cores, "
    f"{ram_gb} GB RAM), {spec['lev_version']}{size_note}{rep_note}\n"
    "row 1: memory ladder at pool 512  |  row 2: pool sweep at 1,000 agents  |  "
    "row 3: fully-cold scenarios and CPU over time\n"
    "mixed multi-stage agent fleet, mock inference 1.5s/call",
    fontsize=12)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(OUT, dpi=115)
print(f"wrote {OUT}")
