#!/usr/bin/env python3
"""Generate the benchmark charts for one round, from committed data only.

Usage:
    charts/generate.py results/rounds/<freeze-tag>/

Reads:
    <round>/benchmark-results.json       (from scripts/aggregate-results.py)
    <round>/runs/*.json                  (for the ladder completion matrix)
    <round>/resource-footprint.json      (optional, from resource-benchmark.sh)
    <round>/rates.json                   (for the pricing footnote)

Writes to charts/output/: for each chart, a light and a -dark SVG+PNG, all
with transparent backgrounds for README embedding.

Honesty rules (METHODOLOGY.md):
    - every individual run is plotted; no bars that hide spread
    - every chart carries a footer: freeze tag, model, n, run dates, pricing
      pin date, and the exact p-value where a comparison is claimed
    - this script reads committed files only — if a number isn't in the round
      directory, it doesn't go on a chart
    - cache hit rate is annotated even where the structured arm is worse

Palette validated for CVD + contrast in light and dark modes (dataviz
validator, 2026-07-29):
    arms:        structured #0066FF · flat #B45309
    token types: input #0066FF · cache read #0D9488 · cache write #7C3AED ·
                 output #BE185D
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ARM_COLORS = {"structured": "#0066FF", "flat": "#B45309"}
TOKEN_COLORS = {
    "input_tokens": "#0066FF",
    "cache_read_input_tokens": "#0D9488",
    "cache_creation_input_tokens": "#7C3AED",
    "output_tokens": "#BE185D",
}
TOKEN_LABELS = {
    "input_tokens": "uncached input",
    "cache_read_input_tokens": "cache reads",
    "cache_creation_input_tokens": "cache writes",
    "output_tokens": "output",
}
COMPLETION_THRESHOLD = 80.0  # pass-rate % that counts as "completed" (pre-registered)

MODES = {
    "light": {"ink": "#1F2328", "muted": "#57606A", "grid": "#D0D7DE"},
    "dark": {"ink": "#E6EDF3", "muted": "#8B949E", "grid": "#30363D"},
}

OUT = Path(__file__).parent / "output"


def style(ax, mode):
    m = MODES[mode]
    ax.set_facecolor("none")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(m["grid"])
    ax.tick_params(colors=m["muted"], labelsize=9)
    ax.xaxis.label.set_color(m["muted"])
    ax.yaxis.label.set_color(m["muted"])
    ax.title.set_color(m["ink"])
    ax.grid(True, color=m["grid"], linewidth=0.5, alpha=0.6)
    ax.set_axisbelow(True)


def footer(fig, text, mode, reserve=0.18):
    fig.subplots_adjust(bottom=reserve)
    fig.text(0.01, 0.01, text, fontsize=6.5, color=MODES[mode]["muted"],
             va="bottom", ha="left", wrap=True)


def save(fig, name, mode):
    OUT.mkdir(exist_ok=True)
    suffix = "" if mode == "light" else "-dark"
    for ext in ("svg", "png"):
        fig.savefig(OUT / f"{name}{suffix}.{ext}", transparent=True, dpi=200)
    plt.close(fig)
    print(f"wrote charts/output/{name}{suffix}.svg/.png")


def base_footer(results, rates):
    arms = results["arms"]
    n = ", ".join(f"{a} n={d['runs']}" for a, d in sorted(arms.items()))
    models = sorted({str(d["model"]) for d in arms.values()})
    comp = results.get("comparison", {})
    p = (f"  ·  exact rank-sum p: pass {comp['pass_rate_p']}, "
         f"tokens {comp['total_billed_tokens_p']}") if comp else ""
    return (f"freeze {results['freeze_tag']}  ·  {n}  ·  model {'; '.join(models)}"
            f"  ·  costs from provider-billed usage at rates pinned "
            f"{rates['pinned_at']}{p}  ·  all runs shown")


def quality_cost(results, runs, rates, mode):
    fig, ax = plt.subplots(figsize=(6.5, 4.4))
    for arm, color in ARM_COLORS.items():
        if arm not in results["arms"]:
            continue
        d = results["arms"][arm]
        xs, ys = d["cost_usd"]["values"], d["pass_rate"]["values"]
        ax.scatter(xs, ys, s=70, color=color, label=arm, zorder=3,
                   edgecolors="none", alpha=0.9)
        ax.scatter([d["cost_usd"]["median"]], [d["pass_rate"]["median"]],
                   marker="+", s=160, color=color, linewidths=2, zorder=4)
    ax.set_xlabel("cost per run (USD, billed usage)")
    ax.set_ylabel("held-out suite pass rate (%)")
    ax.set_title("Quality vs cost — every run shown, + marks the median",
                 fontsize=11, loc="left")
    leg = ax.legend(frameon=False, fontsize=9)
    for t in leg.get_texts():
        t.set_color(MODES[mode]["ink"])
    style(ax, mode)
    footer(fig, base_footer(results, rates), mode)
    save(fig, "quality-cost", mode)


def token_composition(results, runs, rates, mode):
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    order = [r for a in ("structured", "flat") for r in runs if r["approach"] == a]
    xs = range(len(order))
    bottoms = [0] * len(order)
    for key, color in TOKEN_COLORS.items():
        vals = [r["usage"][key] / 1e6 for r in order]
        ax.bar(xs, vals, bottom=bottoms, color=color, width=0.7,
               label=TOKEN_LABELS[key], edgecolor="none")
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    for i, r in enumerate(order):
        u = r["usage"]
        total = sum(u[k] for k in TOKEN_COLORS)
        hit = u["cache_read_input_tokens"] / max(1, total - u["output_tokens"]) * 100
        ax.text(i, bottoms[i] * 1.01, f"{hit:.0f}%\ncached",
                ha="center", va="bottom", fontsize=7, color=MODES[mode]["muted"])
    ax.set_xticks(list(xs))
    labels, seen = [], {}
    for r in order:
        seen[r["approach"]] = seen.get(r["approach"], 0) + 1
        labels.append(f"{r['approach']}\n#{seen[r['approach']]}")
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0, max(bottoms) * 1.22)
    ax.set_ylabel("billed tokens per run (millions)")
    ax.set_title("Token composition per run, cache hit rate annotated",
                 fontsize=11, loc="left")
    leg = ax.legend(frameon=False, fontsize=8, ncol=4, loc="upper center",
                    bbox_to_anchor=(0.5, -0.22))
    for t in leg.get_texts():
        t.set_color(MODES[mode]["ink"])
    style(ax, mode)
    footer(fig, base_footer(results, rates), mode, reserve=0.30)
    save(fig, "token-composition", mode)


def ladder_matrix(all_runs, results, rates, mode):
    tasks = sorted({r["task"] for r in all_runs})
    if len(tasks) < 2:
        print("ladder-matrix skipped: runs cover a single task")
        return
    arms = sorted({r["approach"] for r in all_runs})
    fig, ax = plt.subplots(figsize=(1.8 + 1.6 * len(tasks), 1.2 + 0.9 * len(arms)))
    for yi, arm in enumerate(arms):
        for xi, task in enumerate(tasks):
            cell = [r for r in all_runs if r["approach"] == arm and r["task"] == task]
            if not cell:
                ax.text(xi, yi, "—", ha="center", va="center",
                        color=MODES[mode]["muted"])
                continue
            k = sum(1 for r in cell if r["pass_rate"] >= COMPLETION_THRESHOLD)
            frac = k / len(cell)
            color = ARM_COLORS.get(arm, "#888888")
            ax.add_patch(plt.Rectangle((xi - 0.45, yi - 0.35), 0.9, 0.7,
                                       color=color, alpha=0.15 + 0.55 * frac,
                                       linewidth=0))
            rates_txt = ", ".join(f"{r['pass_rate']:.0f}" for r in cell)
            ax.text(xi, yi + 0.08, f"{k}/{len(cell)}", ha="center", va="center",
                    fontsize=12, color=MODES[mode]["ink"], fontweight="bold")
            ax.text(xi, yi - 0.2, rates_txt, ha="center", va="center",
                    fontsize=6.5, color=MODES[mode]["muted"])
    ax.set_xlim(-0.6, len(tasks) - 0.4)
    ax.set_ylim(len(arms) - 0.4, -0.6)
    ax.set_xticks(range(len(tasks)))
    ax.set_xticklabels(tasks, fontsize=9)
    ax.set_yticks(range(len(arms)))
    ax.set_yticklabels(arms, fontsize=9)
    ax.set_title(f"Runs completed per task (pass ≥ {COMPLETION_THRESHOLD:.0f}% "
                 "within budget) — individual pass rates below each count",
                 fontsize=10, loc="left")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=MODES[mode]["muted"], length=0)
    footer(fig, base_footer(results, rates), mode)
    save(fig, "ladder-completion", mode)


def rss_curve(resource, mode):
    series = [s for s in resource["series"] if s.get("valid")]
    invalid = [s for s in resource["series"] if not s.get("valid")]
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    xs = [s["agents"] for s in series]
    ys = [s["peak_rss_mb"] for s in series]
    ax.plot(xs, ys, color=ARM_COLORS["structured"], linewidth=2, marker="o",
            markersize=6)
    for x, y in zip(xs, ys):
        ax.annotate(f"{y} MB", (x, y), textcoords="offset points",
                    xytext=(0, 9), ha="center", fontsize=8,
                    color=MODES[mode]["ink"])
    ax.set_xlabel("concurrent agents (real inference)")
    ax.set_ylabel("peak RSS of lev serve tree (MB)")
    ax.set_title("Absolute memory of one daemon — no comparison bars",
                 fontsize=11, loc="left")
    ax.set_ylim(bottom=0)
    style(ax, mode)
    m = resource["method"]
    note = (f"{resource['tool']['version']}  ·  {resource['system']['os']} "
            f"{resource['system']['arch']}, {resource['system']['ram_gb']} GB"
            f"  ·  warmup {m['warmup_seconds']}s, sampled {m['measure_seconds']}s @ "
            f"{m['sample_interval_seconds']}s  ·  blueprint {m['blueprint']}"
            f"  ·  real_inference={str(m['real_inference']).lower()}")
    if invalid:
        note += ("  ·  EXCLUDED (agents failed/missing): "
                 + ", ".join(str(s["agents"]) for s in invalid))
    footer(fig, note, mode)
    save(fig, "resource-footprint", mode)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    round_dir = Path(sys.argv[1]).resolve()
    results = json.loads((round_dir / "benchmark-results.json").read_text())
    rates = json.loads((round_dir / "rates.json").read_text())
    runs = [json.loads(f.read_text())
            for f in sorted((round_dir / "runs").glob("*.json"))]
    flagship = [r for r in runs if r["task"] == "stress-test"] or runs

    for mode in MODES:
        quality_cost(results, flagship, rates, mode)
        token_composition(results, flagship, rates, mode)
        ladder_matrix(runs, results, rates, mode)
        resource_file = round_dir / "resource-footprint.json"
        if resource_file.exists():
            rss_curve(json.loads(resource_file.read_text()), mode)
        else:
            print("resource-footprint.json absent — RSS chart skipped")


if __name__ == "__main__":
    main()
