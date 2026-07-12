#!/usr/bin/env python3
"""
Generate SVG benchmark charts from results/benchmark-results.json.

Usage:
    cd charts && python3 generate.py

Outputs SVG charts to charts/output/.
"""

import json
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
import numpy as np


# ---------------------------------------------------------------------------
# Style constants
# ---------------------------------------------------------------------------

BG_COLOR = "#1a1a2e"
SURFACE_COLOR = "#16213e"
GRID_COLOR = "#2a2a4a"
TEXT_COLOR = "#e0e0e0"
TITLE_COLOR = "#ffffff"
LEVIATH_COLOR = "#00d4aa"
BASELINE_COLOR = "#ff6b6b"
ACCENT_GRAY = "#8888aa"

FONT_FAMILY = "sans-serif"

plt.rcParams.update({
    "font.family": FONT_FAMILY,
    "font.size": 11,
    "text.color": TEXT_COLOR,
    "axes.labelcolor": TEXT_COLOR,
    "axes.edgecolor": GRID_COLOR,
    "xtick.color": TEXT_COLOR,
    "ytick.color": TEXT_COLOR,
    "figure.facecolor": BG_COLOR,
    "axes.facecolor": SURFACE_COLOR,
    "savefig.facecolor": BG_COLOR,
    "savefig.edgecolor": BG_COLOR,
    "grid.color": GRID_COLOR,
    "grid.alpha": 0.3,
})


def load_results():
    """Load benchmark results JSON."""
    script_dir = Path(__file__).parent
    results_path = script_dir.parent / "results" / "benchmark-results.json"
    if not results_path.exists():
        print(f"Error: {results_path} not found")
        sys.exit(1)
    with open(results_path) as f:
        return json.load(f)


def output_dir():
    """Ensure output directory exists and return its path."""
    d = Path(__file__).parent / "output"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _add_bar_labels(ax, bars, fmt="{:.0f}%", color=TEXT_COLOR, fontsize=9):
    """Add labels on top of bars."""
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.5,
                fmt.format(height),
                ha="center", va="bottom",
                color=color, fontsize=fontsize, fontweight="bold",
            )


# ---------------------------------------------------------------------------
# Chart 1: Pass Rate by Category
# ---------------------------------------------------------------------------

def generate_pass_rate(data):
    """Grouped bar chart: pass rate % per category for each approach."""
    leviath = data["approaches"]["leviath"]["test_results"]["by_category"]
    baseline = data["approaches"]["flat_baseline"]["test_results"]["by_category"]

    categories = sorted(set(list(leviath.keys()) + list(baseline.keys())))
    if not categories:
        categories = [
            "happy_path", "schema_validation", "idempotency", "rate_limiting",
            "dlq", "backoff", "router", "transformer", "metrics",
            "api_auth", "audit", "circuit_breaker",
        ]

    labels = [c.replace("_", " ").title() for c in categories]

    def pass_rate(cat_data, cat):
        entry = cat_data.get(cat, {"total": 0, "passed": 0})
        total = entry.get("total", 0)
        if total == 0:
            return 0
        return (entry.get("passed", 0) / total) * 100

    leviath_rates = [pass_rate(leviath, c) for c in categories]
    baseline_rates = [pass_rate(baseline, c) for c in categories]

    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots(figsize=(16, 7))
    bars1 = ax.bar(x - width / 2, leviath_rates, width, label="Leviath",
                   color=LEVIATH_COLOR, edgecolor=LEVIATH_COLOR, alpha=0.9, zorder=3)
    bars2 = ax.bar(x + width / 2, baseline_rates, width, label="Flat Baseline",
                   color=BASELINE_COLOR, edgecolor=BASELINE_COLOR, alpha=0.9, zorder=3)

    ax.set_ylabel("Pass Rate (%)", fontsize=12, fontweight="bold")
    ax.set_title("Test Pass Rate by Category", fontsize=16, fontweight="bold",
                 color=TITLE_COLOR, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=40, ha="right", fontsize=9)
    ax.set_ylim(0, 110)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.legend(loc="upper right", framealpha=0.8, facecolor=SURFACE_COLOR,
              edgecolor=GRID_COLOR, fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.3, zorder=0)

    _add_bar_labels(ax, bars1)
    _add_bar_labels(ax, bars2)

    fig.tight_layout()
    fig.savefig(output_dir() / "pass-rate.svg", format="svg", dpi=150)
    plt.close(fig)
    print("  ✓ pass-rate.svg")


# ---------------------------------------------------------------------------
# Chart 2: Cost Comparison
# ---------------------------------------------------------------------------

def generate_cost_comparison(data):
    """Bar chart: total cost per approach."""
    approaches = data["approaches"]
    names = ["Leviath", "Flat Baseline"]
    costs = [
        approaches["leviath"].get("estimated_cost_usd", 0),
        approaches["flat_baseline"].get("estimated_cost_usd", 0),
    ]
    colors = [LEVIATH_COLOR, BASELINE_COLOR]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(names, costs, color=colors, edgecolor=colors, alpha=0.9,
                  width=0.5, zorder=3)
    ax.set_ylabel("Cost (USD)", fontsize=12, fontweight="bold")
    ax.set_title("Total Cost Comparison", fontsize=16, fontweight="bold",
                 color=TITLE_COLOR, pad=15)
    ax.grid(axis="y", linestyle="--", alpha=0.3, zorder=0)

    _add_bar_labels(ax, bars, fmt="${:.2f}", fontsize=11)

    fig.tight_layout()
    fig.savefig(output_dir() / "cost-comparison.svg", format="svg", dpi=150)
    plt.close(fig)
    print("  ✓ cost-comparison.svg")


# ---------------------------------------------------------------------------
# Chart 3: Time Comparison
# ---------------------------------------------------------------------------

def generate_time_comparison(data):
    """Bar chart: total time per approach."""
    approaches = data["approaches"]
    names = ["Leviath", "Flat Baseline"]
    durations = [
        approaches["leviath"].get("duration_seconds", 0),
        approaches["flat_baseline"].get("duration_seconds", 0),
    ]
    colors = [LEVIATH_COLOR, BASELINE_COLOR]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(names, durations, color=colors, edgecolor=colors, alpha=0.9,
                  width=0.5, zorder=3)
    ax.set_ylabel("Duration (seconds)", fontsize=12, fontweight="bold")
    ax.set_title("Total Time Comparison", fontsize=16, fontweight="bold",
                 color=TITLE_COLOR, pad=15)
    ax.grid(axis="y", linestyle="--", alpha=0.3, zorder=0)

    _add_bar_labels(ax, bars, fmt="{:.0f}s", fontsize=11)

    fig.tight_layout()
    fig.savefig(output_dir() / "time-comparison.svg", format="svg", dpi=150)
    plt.close(fig)
    print("  ✓ time-comparison.svg")


# ---------------------------------------------------------------------------
# Chart 4: Efficiency (Tool Calls)
# ---------------------------------------------------------------------------

def generate_efficiency(data):
    """Bar chart: tool calls per approach."""
    approaches = data["approaches"]
    names = ["Leviath", "Flat Baseline"]
    tool_calls = [
        approaches["leviath"].get("tool_calls", 0),
        approaches["flat_baseline"].get("tool_calls", 0),
    ]
    colors = [LEVIATH_COLOR, BASELINE_COLOR]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(names, tool_calls, color=colors, edgecolor=colors, alpha=0.9,
                  width=0.5, zorder=3)
    ax.set_ylabel("Tool Calls", fontsize=12, fontweight="bold")
    ax.set_title("Efficiency: Tool Calls per Approach", fontsize=16,
                 fontweight="bold", color=TITLE_COLOR, pad=15)
    ax.grid(axis="y", linestyle="--", alpha=0.3, zorder=0)

    _add_bar_labels(ax, bars, fmt="{:.0f}", fontsize=11)

    fig.tight_layout()
    fig.savefig(output_dir() / "efficiency.svg", format="svg", dpi=150)
    plt.close(fig)
    print("  ✓ efficiency.svg")


# ---------------------------------------------------------------------------
# Chart 5: Summary Table
# ---------------------------------------------------------------------------

def generate_summary_table(data):
    """Visual table with all metrics side by side."""
    leviath = data["approaches"]["leviath"]
    baseline = data["approaches"]["flat_baseline"]

    l_tests = leviath.get("test_results", {})
    b_tests = baseline.get("test_results", {})

    l_total = l_tests.get("total", 0)
    b_total = b_tests.get("total", 0)
    l_pass_rate = (l_tests.get("passed", 0) / l_total * 100) if l_total else 0
    b_pass_rate = (b_tests.get("passed", 0) / b_total * 100) if b_total else 0

    rows = [
        ["Model", leviath.get("model", "—"), baseline.get("model", "—")],
        ["Blueprint", leviath.get("blueprint", "—"), "—"],
        ["Duration", f"{leviath.get('duration_seconds', 0)}s",
         f"{baseline.get('duration_seconds', 0)}s"],
        ["Tool Calls", str(leviath.get("tool_calls", 0)),
         str(baseline.get("tool_calls", 0))],
        ["API Requests", str(leviath.get("api_requests", 0)),
         str(baseline.get("api_requests", 0))],
        ["Prompt Tokens", f"{leviath.get('prompt_tokens', 0):,}",
         f"{baseline.get('prompt_tokens', 0):,}"],
        ["Completion Tokens", f"{leviath.get('completion_tokens', 0):,}",
         f"{baseline.get('completion_tokens', 0):,}"],
        ["Cost (USD)", f"${leviath.get('estimated_cost_usd', 0):.2f}",
         f"${baseline.get('estimated_cost_usd', 0):.2f}"],
        ["Tests Passed", f"{l_tests.get('passed', 0)}/{l_total}",
         f"{b_tests.get('passed', 0)}/{b_total}"],
        ["Pass Rate", f"{l_pass_rate:.1f}%", f"{b_pass_rate:.1f}%"],
        ["Errors", str(l_tests.get("errors", 0)), str(b_tests.get("errors", 0))],
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_axis_off()

    col_labels = ["Metric", "Leviath", "Flat Baseline"]

    table = ax.table(
        cellText=rows,
        colLabels=col_labels,
        cellLoc="center",
        loc="center",
    )

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.6)

    # Style the table
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor(GRID_COLOR)
        if row == 0:
            # Header row
            cell.set_facecolor("#0f3460")
            cell.set_text_props(color=TITLE_COLOR, fontweight="bold", fontsize=12)
        else:
            cell.set_facecolor(SURFACE_COLOR if row % 2 == 0 else BG_COLOR)
            cell.set_text_props(color=TEXT_COLOR)
            if col == 1:
                cell.set_text_props(color=LEVIATH_COLOR, fontweight="bold")
            elif col == 2:
                cell.set_text_props(color=BASELINE_COLOR, fontweight="bold")

    ax.set_title("Benchmark Summary", fontsize=16, fontweight="bold",
                 color=TITLE_COLOR, pad=20, y=0.98)

    fig.tight_layout()
    fig.savefig(output_dir() / "summary-table.svg", format="svg", dpi=150)
    plt.close(fig)
    print("  ✓ summary-table.svg")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Loading results from benchmark-results.json...")
    data = load_results()

    print(f"Generating charts for benchmark: {data.get('benchmark', 'unknown')}")
    print(f"Task: {data.get('task', 'unknown')}")
    print()

    generate_pass_rate(data)
    generate_cost_comparison(data)
    generate_time_comparison(data)
    generate_efficiency(data)
    generate_summary_table(data)

    print()
    out = output_dir()
    print(f"All charts saved to {out}/")
    print(f"  Files: {', '.join(f.name for f in sorted(out.glob('*.svg')))}")


if __name__ == "__main__":
    main()
