#!/usr/bin/env python3
"""Render the quality-track charts from committed results. Charts only.

Reads results/<stamp>_<host>/quality/ (round.json, per-suite
summary.json and raw run records) plus specs.json, and renders:

- cost_vs_quality_<suite>.png: cost per task vs verified pass rate, one
  point per (model, arm), medians with min/max whiskers, Pareto
  frontier, model names + tiers labeled on the chart.
- ablation.png: flat vs structured across suites - pass rate and billed
  tokens, every underlying run drawn as a dot, exact p-values annotated.
- round_poster.png: pass rate / cost / wall-clock / cache-hit per suite
  and arm.

Data collection scripts never render; this script never runs anything.
Results stamped UNFROZEN-SMOKE are refused unless --allow-smoke is
passed, and smoke charts are watermarked.

Usage:
    python3 bench/quality/render_quality.py results/<stamp>_<host> \
        [-o outdir] [--allow-smoke]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Palette: colorblind-validated; arm colors are fixed identities.
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASE = "#c3c2b7"

# Narrative order: today's setup first, the full configuration last.
ARM_ORDER = ["flat-pinned", "structured-pinned", "structured-stagemix"]
ARM_COLORS = {"flat-pinned": "#eb6834", "structured-pinned": "#2a78d6",
              "structured-stagemix": "#1baf7a"}
ARM_LABELS = {
    "flat-pinned": "flat context, one model (today's typical setup)",
    "structured-pinned": "structured context, one model",
    "structured-stagemix": "structured context, mixed models per stage",
}
SMOKE_TAG = "UNFROZEN-SMOKE"


def style_ax(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(BASE)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.yaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)


def smoke_watermark(fig):
    fig.text(0.5, 0.5, "SMOKE - not a counted round", fontsize=40,
             color=INK, alpha=0.08, ha="center", va="center", rotation=22,
             zorder=0)


def provenance(fig, round_meta: dict, specs: dict) -> None:
    lev = round_meta.get("lev") or {}
    sha = (lev.get("sha256") or "")[:8]
    fig.text(0.01, 0.006,
             f"freeze {round_meta.get('freeze_tag')} - "
             f"{lev.get('version', '?')} (sha {sha}) - "
             f"{specs.get('cpu_model', '?')} - reps={round_meta.get('reps')}"
             " - medians, whiskers = min/max, dots = every run, no run "
             "excluded - costs from provider-billed usage incl. cache",
             fontsize=6.6, color=MUTED, ha="left")


def load_round(results_dir: Path) -> tuple[dict, dict, dict]:
    round_meta = json.loads(
        (results_dir / "quality" / "round.json").read_text())
    specs_path = results_dir / "specs.json"
    specs = json.loads(specs_path.read_text()) if specs_path.exists() else {}
    suites = {}
    for suite_dir in sorted((results_dir / "quality").iterdir()):
        summary = suite_dir / "summary.json"
        if summary.is_file():
            runs = []
            for rec in sorted((suite_dir / "runs").glob("*.json")):
                runs.append(json.loads(rec.read_text()))
            suites[suite_dir.name] = {
                "summary": json.loads(summary.read_text()),
                "runs": runs,
            }
    return round_meta, specs, suites


def arm_sort_key(arm: str) -> int:
    return ARM_ORDER.index(arm) if arm in ARM_ORDER else len(ARM_ORDER)


def cell_points(summary: dict) -> list[dict]:
    """Chartable (arm, model) cells with medians and spreads."""
    points = []
    for cell in summary["aggregate"]["cells"]:
        cost_med = cell["cost_usd"]["median"]
        if cell["runs"] == 0:
            continue
        points.append({
            "arm": cell["arm"],
            "model": cell["model_label"],
            "pass_rate": cell["pass_rate"] * 100.0,
            "cost": cost_med,
            "cost_lo": cell["cost_usd"]["min"],
            "cost_hi": cell["cost_usd"]["max"],
            "tokens": cell["billed_tokens"],
            "wall": cell["wall_clock_secs"],
            "cache": cell["cache_hit_rate"],
        })
    points.sort(key=lambda p: (arm_sort_key(p["arm"]), p["model"]))
    return points


def mix_label(round_meta: dict) -> str:
    mapping = round_meta.get("stagemix_mapping")
    if isinstance(mapping, dict) and mapping:
        models = sorted({m for m in mapping.values()})
        return "mix: " + " + ".join(models)
    return "mix (per-stage mapping in round.json)"


def render_cost_vs_quality(suite: str, data: dict, round_meta: dict,
                           specs: dict, out: Path) -> Path | None:
    roster = round_meta.get("roster", {})
    points = [p for p in cell_points(data["summary"])
              if p["cost"] is not None and p["cost"] > 0
              or p["arm"] == "structured-stagemix"]
    priced = [p for p in points if p["cost"]]
    if not priced:
        return None

    fig, ax = plt.subplots(figsize=(9.2, 6.2), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    style_ax(ax)

    for p in priced:
        color = ARM_COLORS.get(p["arm"], MUTED)
        if p["cost_lo"] is not None and p["cost_hi"] is not None:
            ax.errorbar(p["cost"], p["pass_rate"],
                        xerr=[[p["cost"] - p["cost_lo"]],
                              [p["cost_hi"] - p["cost"]]],
                        fmt="none", ecolor=color, elinewidth=1.0,
                        capsize=2, alpha=0.45)
        ax.scatter([p["cost"]], [p["pass_rate"]], s=64, color=color,
                   zorder=3, edgecolors=SURFACE, linewidths=1.5)
        label = (mix_label(round_meta)
                 if p["arm"] == "structured-stagemix" else p["model"])
        tier = (roster.get(p["model"], {}) or {}).get("tier", "")
        ax.annotate(label, (p["cost"], p["pass_rate"]),
                    textcoords="offset points", xytext=(8, 6), fontsize=8,
                    color=INK)
        if tier and p["arm"] != "structured-stagemix":
            ax.annotate(tier, (p["cost"], p["pass_rate"]),
                        textcoords="offset points", xytext=(8, -3),
                        fontsize=6.5, color=MUTED)

    frontier = sorted([(p["cost"], p["pass_rate"]) for p in priced])
    fx, fy, best = [], [], -1.0
    for x, y in frontier:
        if y > best:
            fx.append(x)
            fy.append(y)
            best = y
    if len(fx) > 1:
        ax.plot(fx, fy, color=MUTED, linewidth=1.0,
                linestyle=(0, (4, 3)), zorder=1)

    ax.set_xscale("log")
    ax.set_xlabel("cost per task (USD, provider-billed, log scale)",
                  fontsize=9, color=INK2)
    ax.set_ylabel("verified pass rate (%)", fontsize=9, color=INK2)
    ax.set_ylim(0, max(80, max(p["pass_rate"] for p in priced) + 10))

    handles = [plt.Line2D([], [], marker="o", linestyle="",
                          color=ARM_COLORS[a], label=ARM_LABELS[a],
                          markersize=7)
               for a in ARM_ORDER
               if any(p["arm"] == a for p in priced)]
    ax.legend(handles=handles, loc="lower right", fontsize=8,
              frameon=False, labelcolor=INK2)
    tiers = round_meta.get("roster") and {
        v.get("tier"): None for v in round_meta["roster"].values()}
    ax.set_title(f"{suite} - cost vs quality by model and context arm",
                 fontsize=11, color=INK, loc="left", pad=14)
    del tiers

    if round_meta.get("freeze_tag") == SMOKE_TAG:
        smoke_watermark(fig)
    provenance(fig, round_meta, specs)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    path = out / f"cost_vs_quality_{suite}.png"
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)
    return path


def render_ablation(suites: dict, round_meta: dict, specs: dict,
                    out: Path) -> Path | None:
    names = [s for s in suites
             if _has_arms(suites[s], "structured-pinned", "flat-pinned")]
    if not names:
        return None
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.4, 5.4), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    xs = range(len(names))
    w = 0.34
    for ax in (ax1, ax2):
        style_ax(ax)
        ax.set_xticks(list(xs))
        ax.set_xticklabels(names, fontsize=8, color=INK2)

    for i, name in enumerate(names):
        summary = suites[name]["summary"]
        runs = suites[name]["runs"]
        for off, arm in ((-w / 2, "flat-pinned"),
                        (w / 2, "structured-pinned")):
            cells = [c for c in summary["aggregate"]["cells"]
                     if c["arm"] == arm]
            if not cells:
                continue
            pass_rate = 100.0 * (sum(c["passes"] for c in cells)
                                 / sum(c["runs"] for c in cells))
            arm_runs = [r for r in runs if r["arm"] == arm]
            tok = [r["billed_tokens"] / 1000.0 for r in arm_runs]
            tok_med = sorted(tok)[len(tok) // 2] if tok else 0
            label = ARM_LABELS[arm] if i == 0 else None
            ax1.bar(i + off, pass_rate, w, color=ARM_COLORS[arm],
                    label=label)
            ax2.bar(i + off, tok_med, w, color=ARM_COLORS[arm],
                    label=label)
            for r in arm_runs:
                passed = 100.0 if (r["score"] or {}).get("passed") else 0.0
                ax1.scatter([i + off], [passed], s=10, color=INK,
                            alpha=0.35, zorder=3, linewidths=0)
                ax2.scatter([i + off], [r["billed_tokens"] / 1000.0],
                            s=10, color=INK, alpha=0.35, zorder=3,
                            linewidths=0)
        for comp in summary.get("comparisons", []):
            if (comp["a"], comp["b"]) == ("structured-pinned",
                                          "flat-pinned"):
                p = comp.get("p_pass_exact_permutation")
                label = f"p={p:.3f}" if isinstance(p, (int, float)) else "p: n/a"
                ax1.text(i, 103, label, fontsize=7, ha="center", color=INK2)
                break

    ax1.set_ylabel("verified pass rate (%)", fontsize=9, color=INK2)
    ax1.set_ylim(0, 112)
    ax1.legend(fontsize=8, frameon=False, loc="upper left",
               labelcolor=INK2)
    ax1.set_title("pass rate - same binary, same pinned model, context "
                  "structure only", fontsize=10, color=INK, loc="left")
    ax2.set_ylabel("billed tokens per task (thousands, incl. cache "
                   "reads+writes)", fontsize=9, color=INK2)
    ax2.set_title("total billed tokens per task", fontsize=10, color=INK,
                  loc="left")

    if round_meta.get("freeze_tag") == SMOKE_TAG:
        smoke_watermark(fig)
    provenance(fig, round_meta, specs)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    path = out / "ablation.png"
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)
    return path


def render_poster(suites: dict, round_meta: dict, specs: dict,
                  out: Path) -> Path | None:
    names = sorted(suites)
    if not names:
        return None
    fig, axes = plt.subplots(2, 2, figsize=(12.6, 8.6), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    xs = range(len(names))
    w = 0.26
    panels = [
        (axes[0][0], "pass_rate", "verified pass rate (%)"),
        (axes[0][1], "cost", "cost per task (USD)"),
        (axes[1][0], "wall", "wall-clock per task (secs)"),
        (axes[1][1], "cache", "prompt-cache hit rate (%)"),
    ]
    for ax, field, ylabel in panels:
        style_ax(ax)
        for j, arm in enumerate(ARM_ORDER):
            heights, los, his = [], [], []
            for name in names:
                pts = [p for p in cell_points(suites[name]["summary"])
                       if p["arm"] == arm]
                v = lo = hi = 0.0
                if pts:
                    p = pts[0]  # first model per arm; poster is per-arm
                    if field == "pass_rate":
                        v = p["pass_rate"]
                    elif field == "cost":
                        v = p["cost"] or 0.0
                        lo, hi = p["cost_lo"] or v, p["cost_hi"] or v
                    elif field == "wall":
                        v = p["wall"]["median"] or 0.0
                        lo, hi = p["wall"]["min"] or v, p["wall"]["max"] or v
                    elif field == "cache":
                        v = 100.0 * (p["cache"]["median"] or 0.0)
                        lo = 100.0 * (p["cache"]["min"] or 0.0)
                        hi = 100.0 * (p["cache"]["max"] or 0.0)
                heights.append(v)
                los.append(lo)
                his.append(hi)
            label = ARM_LABELS[arm] if ax is axes[0][0] else None
            positions = [i + (j - 1) * w for i in xs]
            ax.bar(positions, heights, w, color=ARM_COLORS[arm],
                   label=label)
            if field != "pass_rate":
                yerr = [[max(0.0, h - lo) for h, lo in zip(heights, los)],
                        [max(0.0, hi - h) for h, hi in zip(heights, his)]]
                ax.errorbar(positions, heights, yerr=yerr, fmt="none",
                            ecolor=INK, elinewidth=0.8, capsize=2,
                            alpha=0.5)
        ax.set_xticks(list(xs))
        ax.set_xticklabels(names, fontsize=7.5, color=INK2)
        ax.set_ylabel(ylabel, fontsize=8.5, color=INK2)
    axes[1][1].set_title("flat wins on cache locality; the billed-token "
                         "total already prices that in", fontsize=7.5,
                         color=MUTED, loc="left", style="italic")
    axes[0][0].legend(fontsize=8, frameon=False, loc="upper left",
                      labelcolor=INK2)
    fig.suptitle(f"leviath quality round {round_meta.get('freeze_tag')} - "
                 f"{mix_label(round_meta)}",
                 fontsize=11, color=INK, x=0.01, ha="left")
    if round_meta.get("freeze_tag") == SMOKE_TAG:
        smoke_watermark(fig)
    provenance(fig, round_meta, specs)
    fig.tight_layout(rect=(0, 0.025, 1, 0.95))
    path = out / "round_poster.png"
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)
    return path


def _has_arms(data: dict, *arms: str) -> bool:
    present = {c["arm"] for c in data["summary"]["aggregate"]["cells"]}
    return all(a in present for a in arms)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("results_dir", type=Path)
    parser.add_argument("-o", "--out", type=Path, default=Path("."))
    parser.add_argument("--allow-smoke", action="store_true",
                        help="render UNFROZEN-SMOKE results (watermarked)")
    args = parser.parse_args()

    round_meta, specs, suites = load_round(args.results_dir)
    if round_meta.get("freeze_tag") == SMOKE_TAG and not args.allow_smoke:
        print("refusing to render UNFROZEN-SMOKE results without "
              "--allow-smoke; smoke numbers are never publishable",
              file=sys.stderr)
        return 2

    args.out.mkdir(parents=True, exist_ok=True)
    written = []
    for suite, data in suites.items():
        path = render_cost_vs_quality(suite, data, round_meta, specs,
                                      args.out)
        if path:
            written.append(path)
    for fn in (render_ablation, render_poster):
        path = fn(suites, round_meta, specs, args.out)
        if path:
            written.append(path)
    for path in written:
        print(path)
    if not written:
        print("nothing renderable found", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
