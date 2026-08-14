#!/usr/bin/env python3
"""Render the quality-track charts from recorded results. Charts only.

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
ARM_ORDER = ["flat-pinned", "flat-compacting", "structured-pinned",
             "structured-stagemix", "structured-mix-flagship"]
ARM_COLORS = {"flat-pinned": "#eb6834", "flat-compacting": "#b45309",
              "structured-pinned": "#2a78d6",
              "structured-stagemix": "#1baf7a",
              "structured-mix-flagship": "#1baf7a"}
ARM_LABELS = {
    "flat-pinned": "flat context, one model (today's typical setup)",
    "flat-compacting": "flat context + compaction "
                       "(production-style baseline)",
    "structured-pinned": "structured context, one model",
    "structured-stagemix": "structured context, mixed models per stage",
    "structured-mix-flagship": "Leviath flagship (structured regions, "
                               "cross-vendor stage mix)",
}
SMOKE_TAG = "UNFROZEN-SMOKE"
# Extra mixed arms (structured-mix-<name>) get their own shades of the
# mix identity, so several compositions can share a chart.
MIX_SHADES = ["#1baf7a", "#0d7f7f", "#6aa84f", "#2f8f5b"]


def arm_color(arm: str) -> str:
    if arm in ARM_COLORS:
        return ARM_COLORS[arm]
    extras = sorted(a for a in _seen_arms if a not in ARM_COLORS)
    idx = extras.index(arm) if arm in extras else 0
    return MIX_SHADES[idx % len(MIX_SHADES)]


def arm_label(arm: str) -> str:
    if arm in ARM_LABELS:
        return ARM_LABELS[arm]
    tail = arm.replace("structured-mix-", "").replace("structured-", "")
    return f"structured context, {tail} model mix"


_seen_arms: set[str] = set()


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
             "excluded - costs from provider-billed usage incl. cache"
             " - p* = seeded random-permutation test, otherwise exact",
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
            _seen_arms.update(r["arm"] for r in runs)
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
            "runs": cell["runs"],
            "unfinished": cell["runs"] - (cell.get("statuses", {})
                                          .get("complete", 0)),
        })
    points.sort(key=lambda p: (arm_sort_key(p["arm"]), p["model"]))
    return points


def mix_label(round_meta: dict, arm: str | None = None) -> str:
    """The composition of a mixed arm, short enough to sit beside a point."""
    mapping = round_meta.get("stagemix_mapping") or {}
    if mapping and all(isinstance(v, dict) for v in mapping.values()):
        mapping = mapping.get(arm) or (next(iter(mapping.values()))
                                       if len(mapping) == 1 else {})
    if isinstance(mapping, dict) and mapping:
        # Model ids without the provider prefix; round.json carries the
        # full stage-to-model mapping.
        models = sorted({str(m).split("/")[-1] for m in mapping.values()})
        return "mix: " + " + ".join(models)
    return "mix (per-stage mapping in round.json)"


def render_cost_vs_quality(suite: str, data: dict, round_meta: dict,
                           specs: dict, out: Path) -> Path | None:
    roster = round_meta.get("roster", {})
    points = [p for p in cell_points(data["summary"])
              if (p["cost"] is not None and p["cost"] > 0)
              or p["model"] is None]
    priced = [p for p in points if p["cost"]]
    if not priced:
        return None

    fig, ax = plt.subplots(figsize=(9.2, 6.2), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    style_ax(ax)

    for p in priced:
        color = arm_color(p["arm"])
        if p["cost_lo"] is not None and p["cost_hi"] is not None:
            ax.errorbar(p["cost"], p["pass_rate"],
                        xerr=[[p["cost"] - p["cost_lo"]],
                              [p["cost_hi"] - p["cost"]]],
                        fmt="none", ecolor=color, elinewidth=1.0,
                        capsize=2, alpha=0.45)
        # A point whose runs mostly never finished is a different claim
        # from a point that failed the tasks, so it does not get to look
        # like one: hollow marker, and the count said out loud.
        mostly_unfinished = p["unfinished"] > p["runs"] / 2
        ax.scatter([p["cost"]], [p["pass_rate"]], s=64,
                   color=SURFACE if mostly_unfinished else color,
                   zorder=3, edgecolors=color,
                   linewidths=2.0 if mostly_unfinished else 1.5)
        mix = p["model"] is None
        label = mix_label(round_meta, p["arm"]) if mix else p["model"]
        tier = (roster.get(p["model"], {}) or {}).get("tier", "")
        # The mix label is long and sits at whatever pass rate it earned,
        # often beside a pinned point; drop it below the marker so the
        # two never overprint.
        ax.annotate(label, (p["cost"], p["pass_rate"]),
                    textcoords="offset points",
                    xytext=(8, -14) if mix else (8, 6),
                    fontsize=7.5 if mix else 8, color=INK)
        sub = tier if (tier and not mix) else ""
        if p["unfinished"]:
            note = f"{p['unfinished']}/{p['runs']} unfinished"
            sub = f"{sub} - {note}" if sub else note
        if sub:
            ax.annotate(sub, (p["cost"], p["pass_rate"]),
                        textcoords="offset points",
                        xytext=(8, -25) if mix else (8, -3),
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
                          color=arm_color(a), label=arm_label(a),
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
    """Flat vs structured, one group per (suite, pinned model).

    Pooling the swept models into one bar would average a model that
    finished with one that capped out on every run - a pass rate
    neither model had. The comparison is per pinned model by
    construction, so the chart is too.
    """
    groups = []
    for name in suites:
        if not _has_arms(suites[name], "structured-pinned", "flat-pinned"):
            continue
        models = sorted({r["model_label"] for r in suites[name]["runs"]
                         if r["arm"] in ("flat-pinned", "structured-pinned")
                         and r["model_label"]})
        for model in models:
            groups.append((name, model))
    if not groups:
        return None

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.8), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    xs = range(len(groups))
    w = 0.34
    labels = [f"{s}\n{m}" for s, m in groups]
    for ax in (ax1, ax2):
        style_ax(ax)
        ax.set_xticks(list(xs))
        ax.set_xticklabels(labels, fontsize=7.5, color=INK2)

    for i, (name, model) in enumerate(groups):
        summary = suites[name]["summary"]
        runs = [r for r in suites[name]["runs"] if r["model_label"] == model]
        for off, arm in ((-w / 2, "flat-pinned"),
                         (w / 2, "structured-pinned")):
            arm_runs = [r for r in runs if r["arm"] == arm]
            if not arm_runs:
                continue
            passes = sum(1 for r in arm_runs
                         if (r["score"] or {}).get("passed"))
            pass_rate = 100.0 * passes / len(arm_runs)
            # Cap-outs and errors have no measurement to rank; they are
            # still failures above, but they are not a token total.
            tok = sorted(r["billed_tokens"] / 1000.0 for r in arm_runs
                         if r["status"] == "complete")
            tok_med = tok[len(tok) // 2] if tok else 0.0
            label = arm_label(arm) if i == 0 else None
            ax1.bar(i + off, pass_rate, w, color=arm_color(arm),
                    label=label)
            ax2.bar(i + off, tok_med, w, color=arm_color(arm), label=label)
            for r in arm_runs:
                passed = 100.0 if (r["score"] or {}).get("passed") else 0.0
                ax1.scatter([i + off], [passed], s=10, color=INK,
                            alpha=0.35, zorder=3, linewidths=0)
                if r["status"] == "complete":
                    ax2.scatter([i + off], [r["billed_tokens"] / 1000.0],
                                s=10, color=INK, alpha=0.35, zorder=3,
                                linewidths=0)
            incomplete = [r for r in arm_runs if r["status"] != "complete"]
            if incomplete:
                # Said out loud on the chart: a bar this low can mean the
                # runs failed the task or never finished it, and those
                # are different claims.
                ax1.text(i + off, pass_rate + 2.5,
                         f"{len(incomplete)}/{len(arm_runs)} unfinished",
                         fontsize=5.8, ha="center", va="bottom",
                         color=INK2, rotation=90, zorder=4)
        for comp in summary.get("comparisons", []):
            if (comp["a"], comp["b"]) != ("structured-pinned",
                                          "flat-pinned"):
                continue
            if comp.get("model_label") != model:
                continue
            test = comp.get("pass") or {}
            p = test.get("p", comp.get("p_pass_exact_permutation"))
            if isinstance(p, (int, float)):
                mark = "" if test.get("method") == "exact_enumeration" else "*"
                ax1.text(i, 110, f"p={p:.3f}{mark}", fontsize=7,
                         ha="center", color=INK2)
            break

    ax1.set_ylabel("verified pass rate (%)", fontsize=9, color=INK2)
    ax1.set_ylim(0, 118)
    ax1.legend(fontsize=8, frameon=False, loc="upper left",
               bbox_to_anchor=(0.0, 0.94), labelcolor=INK2)
    ax1.set_title("pass rate - same binary, same pinned model, context "
                  "structure only", fontsize=10, color=INK, loc="left")
    ax2.set_ylabel("billed tokens per task (thousands, incl. cache "
                   "reads+writes)", fontsize=9, color=INK2)
    ax2.set_title("billed tokens per task, completed runs only",
                  fontsize=10, color=INK, loc="left")

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
            label = arm_label(arm) if ax is axes[0][0] else None
            positions = [i + (j - 1) * w for i in xs]
            ax.bar(positions, heights, w, color=arm_color(arm),
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


_WINDOW_STYLES = {None: "-"}  # windows discovered per round get dashes


def _series_key(r: dict) -> tuple[str, int | None]:
    """(arm, window_tokens): the window sweep makes the window part of
    a series' identity - two tiers of one arm never merge."""
    return (r["arm"], r.get("window_tokens"))


def _series_label(arm: str, window: int | None) -> str:
    label = arm_label(arm)
    return f"{label} @{window // 1000}k" if window else label


def _window_style(window: int | None, windows: list) -> str:
    """Solid = largest window in the round; dashes shorten as the
    window shrinks. Color stays the arm's identity."""
    styles = ["-", (0, (5, 2)), (0, (2, 2)), (0, (1, 1.5))]
    ordered = sorted((w for w in windows if w), reverse=True)
    if window is None or window not in ordered:
        return "-"
    return styles[min(ordered.index(window), len(styles) - 1)]


def _retention_series(runs: list[dict]) -> dict:
    """Per (arm, window): depth -> {scores, reached, total,
    hallucinated}. Pools every task's probes at their depths."""
    series: dict[tuple, dict[int, dict]] = {}
    for r in runs:
        for e in r.get("retention") or []:
            depth = e["after_tool_calls"]
            cell = series.setdefault(_series_key(r), {}).setdefault(
                depth, {"scores": [], "reached": 0, "total": 0,
                        "hallucinated": 0})
            cell["total"] += 1
            if e.get("reached"):
                cell["reached"] += 1
                if isinstance(e.get("score"), (int, float)):
                    cell["scores"].append(float(e["score"]))
                if e.get("hallucinated"):
                    cell["hallucinated"] += 1
    return series


def render_retention(suites: dict, round_meta: dict, specs: dict,
                     out_dir: Path):
    """The CRS headline: probe accuracy vs tool-call depth, per arm.

    Solid line = mean accuracy over reached probes (0..1). Dashed line =
    hallucination rate. Point labels carry n (reached/total) so
    survivorship is visible on the chart itself, never hidden in a
    footnote. Per-task panels first, pooled panel last."""
    data = suites.get("footprint") or suites.get("crs")
    if not data:
        return None
    runs = [r for r in data["runs"] if r.get("retention")]
    if not runs:
        return None

    tasks = sorted({r["task_id"] for r in runs})
    panels = [("all tasks (pooled)", runs)] + [
        (t, [r for r in runs if r["task_id"] == t]) for t in tasks]
    ncols = min(2, len(panels))
    nrows = (len(panels) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(7.2 * ncols, 4.6 * nrows),
                             squeeze=False)
    fig.patch.set_facecolor(SURFACE)

    windows = sorted({r.get("window_tokens") for r in runs},
                     key=lambda w: (w is None, -(w or 0)))
    for i, (title, panel_runs) in enumerate(panels):
        ax = axes[i // ncols][i % ncols]
        style_ax(ax)
        series = _retention_series(panel_runs)
        for arm, window in sorted(series,
                                  key=lambda k: (arm_sort_key(k[0]),
                                                 -(k[1] or 0))):
            cells = series[(arm, window)]
            xs, ys, hs = [], [], []
            for d in sorted(cells):
                cell = cells[d]
                if not cell["scores"]:
                    continue
                xs.append(d)
                ys.append(sum(cell["scores"]) / len(cell["scores"]))
                hs.append(cell["hallucinated"] / max(cell["reached"], 1))
                if title.startswith("all"):
                    ax.annotate(f"n={cell['reached']}/{cell['total']}",
                                (d, ys[-1]), textcoords="offset points",
                                xytext=(0, -14), fontsize=5.6,
                                color=MUTED, ha="center")
            if not xs:
                continue
            style = _window_style(window, windows)
            ax.plot(xs, ys, marker="o", markersize=4, linewidth=1.8,
                    linestyle=style, color=arm_color(arm),
                    label=_series_label(arm, window))
            ax.plot(xs, hs, linestyle=":", linewidth=0.9, alpha=0.45,
                    color=arm_color(arm))
        ax.set_ylim(-0.04, 1.04)
        ax.set_title(title, fontsize=10, color=INK)
        ax.set_xlabel("tool calls", fontsize=8, color=MUTED)
        ax.set_ylabel("probe accuracy", fontsize=8, color=MUTED)
        if i == 0:
            ax.legend(fontsize=7, loc="lower left", frameon=False)
    for j in range(len(panels), nrows * ncols):
        axes[j // ncols][j % ncols].axis("off")

    windows_note = ("; dash length = window tier"
                    if len([w for w in windows if w]) > 1 else "")
    fig.suptitle("Context retention vs task depth "
                 f"(dotted = hallucination rate{windows_note})",
                 fontsize=13, color=INK)
    if round_meta.get("freeze_tag") == SMOKE_TAG:
        smoke_watermark(fig)
    provenance(fig, round_meta, specs)
    probes_cfg = round_meta.get("probes") or {}
    fig.text(0.01, 0.024,
             f"probes replayed post-hoc against journaled context; one "
             f"fixed reader ({probes_cfg.get('reader_model', '?')}), "
             f"grader {probes_cfg.get('grader_model', '?')}; probe cost "
             "excluded from cost charts; unreached probes excluded from "
             "means and shown in n",
             fontsize=6.6, color=MUTED, ha="left")
    fig.tight_layout(rect=(0, 0.045, 1, 0.96))
    path = out_dir / "retention.png"
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


def render_cost_per_success(suites: dict, round_meta: dict, specs: dict,
                            out_dir: Path):
    """Cost per passing run, per arm - cost per run rewards cheap
    failure; this is the number a buyer pays. Probe overhead excluded
    (it is measurement)."""
    data = suites.get("footprint") or suites.get("crs")
    if not data:
        return None
    runs = data["runs"]
    arms: dict[tuple, dict] = {}
    for r in runs:
        cell = arms.setdefault(_series_key(r),
                               {"cost": 0.0, "passes": 0,
                                "runs": 0, "unpriced": 0})
        cell["runs"] += 1
        if isinstance(r.get("cost_usd"), (int, float)):
            cell["cost"] += r["cost_usd"]
        else:
            cell["unpriced"] += 1
        if r.get("score", {}).get("passed"):
            cell["passes"] += 1
    if not arms or not any(c["passes"] for c in arms.values()):
        return None

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    fig.patch.set_facecolor(SURFACE)
    style_ax(ax)
    ordered = sorted(arms, key=lambda k: (arm_sort_key(k[0]),
                                          -(k[1] or 0)))
    xs = range(len(ordered))
    for x, (arm, window) in zip(xs, ordered):
        cell = arms[(arm, window)]
        cps = cell["cost"] / cell["passes"] if cell["passes"] else None
        if cps is None:
            ax.annotate("no passes", (x, 0.02), ha="center", fontsize=7,
                        color=MUTED)
            continue
        ax.bar(x, cps, width=0.62, color=arm_color(arm))
        note = f"{cell['passes']}/{cell['runs']} pass"
        if cell["unpriced"]:
            note += f", {cell['unpriced']} unpriced"
        ax.annotate(f"${cps:.2f}\n{note}", (x, cps),
                    textcoords="offset points", xytext=(0, 4),
                    ha="center", fontsize=7, color=INK)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([_series_label(a, w) for a, w in ordered],
                       fontsize=7, color=INK, wrap=True)
    ax.set_ylabel("USD per passing run", fontsize=8, color=MUTED)
    ax.set_title("Cost per successful outcome (agent spend only)",
                 fontsize=12, color=INK)
    if round_meta.get("freeze_tag") == SMOKE_TAG:
        smoke_watermark(fig)
    provenance(fig, round_meta, specs)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    path = out_dir / "cost_per_success.png"
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


def render_cost_at_depth(suites: dict, round_meta: dict, specs: dict,
                         out_dir: Path):
    """Cumulative billed tokens vs tool-call depth, per (arm, window).

    The co-headline next to retention: at large windows nothing is
    forgotten, but every call re-bills what the architecture chose to
    carry. Token-denominated (not dollars) so mixed-model arms chart on
    the same axis; the cost tables carry the dollars."""
    data = suites.get("footprint") or suites.get("crs")
    if not data:
        return None
    runs = [r for r in data["runs"] if r.get("depth_usage_curve")]
    if not runs:
        return None

    series: dict[tuple, list] = {}
    for r in runs:
        series.setdefault(_series_key(r), []).append(r)
    windows = sorted({r.get("window_tokens") for r in runs},
                     key=lambda w: (w is None, -(w or 0)))

    fig, ax = plt.subplots(figsize=(8.4, 5.0))
    fig.patch.set_facecolor(SURFACE)
    style_ax(ax)
    for (arm, window), rs in sorted(series.items(),
                                    key=lambda kv: (arm_sort_key(kv[0][0]),
                                                    -(kv[0][1] or 0))):
        # Mean cumulative billed tokens across runs, at each depth any
        # run recorded; a run that died early keeps its last value.
        depths = sorted({p["tool_calls"] for r in rs
                         for p in r["depth_usage_curve"]})
        ys = []
        for d in depths:
            vals = []
            for r in rs:
                pts = [p for p in r["depth_usage_curve"]
                       if p["tool_calls"] <= d]
                if pts:
                    p = pts[-1]
                    vals.append(p["prompt_tokens"]
                                + p["completion_tokens"]
                                + p["cached_tokens"]
                                + p["cache_write_tokens"])
            ys.append(sum(vals) / len(vals) if vals else 0)
        ax.plot(depths, [y / 1e6 for y in ys], linewidth=1.8,
                linestyle=_window_style(window, windows),
                color=arm_color(arm), label=_series_label(arm, window))
    ax.set_xlabel("tool calls", fontsize=8, color=MUTED)
    ax.set_ylabel("cumulative billed tokens (millions)", fontsize=8,
                  color=MUTED)
    ax.set_title("What depth costs each architecture",
                 fontsize=12, color=INK)
    ax.legend(fontsize=7, loc="upper left", frameon=False)
    if round_meta.get("freeze_tag") == SMOKE_TAG:
        smoke_watermark(fig)
    provenance(fig, round_meta, specs)
    fig.text(0.01, 0.024,
             "curves from each run's journaled cumulative usage (all "
             "billed components incl. cache reads/writes); runs that "
             "ended early hold their last value in the mean",
             fontsize=6.6, color=MUTED, ha="left")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    path = out_dir / "cost_at_depth.png"
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


LOCAL_WINDOWS = [(8_000, "8k local"), (32_000, "32k local"),
                 (128_000, "128k")]


def _stage_bands(ax, requests: list[dict], color: str) -> None:
    """Shade a multi-stage run's stage spans and name each one, so a
    curve's sudden drops read as what they are: a new stage opening a
    fresh scoped context."""
    stages = [q.get("stage") for q in requests]
    if len({s for s in stages if s}) < 2:
        return
    spans = []
    start = 0
    for i in range(1, len(stages) + 1):
        if i == len(stages) or stages[i] != stages[start]:
            if stages[start]:
                spans.append((start + 1, i, stages[start]))
            start = i
    total = len(stages)
    for j, (x0, x1, name) in enumerate(spans):
        if j % 2 == 1:
            ax.axvspan(x0 - 0.5, x1 + 0.5, color=color, alpha=0.055,
                       zorder=0, linewidth=0)
        if j > 0:
            ax.axvline(x0 - 0.5, color=color, alpha=0.25,
                       linewidth=0.7, linestyle=(0, (2, 3)), zorder=1)
        # Labels sit just above the x-axis, clear of legends and the
        # window reference lines; a sliver keeps its shading but stays
        # unlabeled rather than smearing text over its neighbors.
        if (x1 - x0 + 1) / total >= 0.07:
            ax.annotate(name, ((x0 + x1) / 2, 0.015),
                        xycoords=("data", "axes fraction"),
                        fontsize=6.0, color=INK2, ha="center",
                        va="bottom", alpha=0.9,
                        rotation=90 if (x1 - x0 + 1) / total < 0.14
                        else 0)


def render_request_footprint(suites: dict, round_meta: dict, specs: dict,
                             out_dir: Path):
    """The footprint suite's headline: input tokens PER REQUEST over
    the run, per arm - stability vs growth. Horizontal reference lines
    mark common local-model windows: an arm whose curve crosses a line
    cannot run on that deployment at all, which is the local-viability
    argument drawn rather than asserted."""
    data = suites.get("footprint")
    if not data:
        return None
    runs = [r for r in data["runs"] if r.get("request_footprint")]
    if not runs:
        return None

    tasks = sorted({r["task_id"] for r in runs})
    ncols = min(len(tasks), 3)
    nrows = (len(tasks) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(6.4 * ncols, 4.8 * nrows),
                             squeeze=False)
    fig.patch.set_facecolor(SURFACE)

    for i, task in enumerate(tasks):
        ax = axes[i // ncols][i % ncols]
        style_ax(ax)
        task_runs = [r for r in runs if r["task_id"] == task]
        top = 0
        for r in sorted(task_runs,
                        key=lambda r: arm_sort_key(r["arm"])):
            fp = r["request_footprint"]
            xs = list(range(1, len(fp["requests"]) + 1))
            ys = [q["input_tokens"] for q in fp["requests"]]
            top = max(top, max(ys, default=0))
            growth = fp.get("input_growth")
            label = (f"{arm_label(r['arm'])} "
                     f"(growth {growth}x)" if growth else
                     arm_label(r["arm"]))
            ax.plot(xs, ys, linewidth=1.5, color=arm_color(r["arm"]),
                    label=label, alpha=0.9)
            # The drops in a structured curve are stage transitions -
            # each stage starts a fresh scoped context. Naming the
            # stages turns an artifact into the mechanism.
            _stage_bands(ax, fp["requests"], arm_color(r["arm"]))
        for tokens, name in LOCAL_WINDOWS:
            if tokens < top * 1.6:
                ax.axhline(tokens, color=MUTED, linewidth=0.8,
                           linestyle=(0, (4, 3)))
                ax.annotate(name, (0.99, tokens),
                            xycoords=("axes fraction", "data"),
                            textcoords="offset points", xytext=(0, 3),
                            fontsize=6.5, color=MUTED, ha="right")
        ax.set_title(task, fontsize=10, color=INK)
        ax.set_xlabel("request #", fontsize=8, color=MUTED)
        ax.set_ylabel("input tokens per request", fontsize=8,
                      color=MUTED)
        ax.legend(fontsize=6.6, loc="upper left", frameon=False)
    for j in range(len(tasks), nrows * ncols):
        axes[j // ncols][j % ncols].axis("off")

    fig.suptitle("What each request carries, over the life of the run",
                 fontsize=13, color=INK)
    if round_meta.get("freeze_tag") == SMOKE_TAG:
        smoke_watermark(fig)
    provenance(fig, round_meta, specs)
    fig.text(0.01, 0.024,
             "per-request input = delta of the journal's cumulative "
             "provider-billed counters (prompt + cache reads + cache "
             "writes); dashed lines mark deployments whose window the "
             "curve must stay under to run there",
             fontsize=6.6, color=MUTED, ha="left")
    fig.tight_layout(rect=(0, 0.05, 1, 0.95))
    path = out_dir / "request_footprint.png"
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


def _win_suffix(r: dict) -> str:
    w = r.get("window_tokens")
    return f" @{w // 1000}k" if w else ""


def _bar_groups(runs: list[dict]) -> tuple[list, list]:
    """(task, window) groups x arm series, both in stable order."""
    groups = sorted({(r["task_id"], r.get("window_tokens"))
                     for r in runs},
                    key=lambda g: (g[0], g[1] or 0))
    arms = sorted({r["arm"] for r in runs}, key=arm_sort_key)
    return groups, arms


def _group_label(task: str, window) -> str:
    return f"{task}\n@{window // 1000}k" if window else task


def render_outcomes(suites: dict, round_meta: dict, specs: dict,
                    out_dir: Path):
    """Priority one, drawn first: what each arm actually delivered.
    Functional score per (task, window) x arm; a run that produced no
    deliverable is an explicit DNF marker, never a hidden zero."""
    written = None
    for suite, data in suites.items():
        runs = [r for r in data["runs"] if r.get("functional")
                or r.get("status") not in (None, "complete")]
        if not runs or suite not in ("footprint", "hallucination"):
            continue
        groups, arms = _bar_groups(runs)
        width = 0.8 / max(len(arms), 1)
        fig, ax = plt.subplots(
            figsize=(max(6.4, 1.9 * len(groups)), 4.6))
        fig.patch.set_facecolor(SURFACE)
        style_ax(ax)
        for ai, arm in enumerate(arms):
            xs, ys = [], []
            for gi, (task, window) in enumerate(groups):
                cell = [r for r in runs if r["task_id"] == task
                        and r.get("window_tokens") == window
                        and r["arm"] == arm]
                if not cell:
                    continue
                x = gi + (ai - (len(arms) - 1) / 2) * width
                scores = [(r.get("functional") or {}).get("score")
                          for r in cell]
                scores = [s for s in scores if isinstance(s, (int, float))]
                if scores:
                    xs.append(x)
                    ys.append(sum(scores) / len(scores))
                for r in cell:
                    if r.get("status") != "complete":
                        ax.annotate(r["status"].upper(), (x, 0.02),
                                    fontsize=6.2, color="#b3261e",
                                    ha="center", rotation=90,
                                    va="bottom")
            ax.bar(xs, ys, width=width * 0.92, color=arm_color(arm),
                   label=arm_label(arm), zorder=3)
        ax.set_xticks(range(len(groups)))
        ax.set_xticklabels([_group_label(t, w) for t, w in groups],
                           fontsize=7.6, color=INK2)
        ax.set_ylim(0, 1.05)
        ax.set_ylabel("functional score (bar) / no deliverable (DNF)",
                      fontsize=8, color=MUTED)
        ax.legend(fontsize=6.8, loc="lower right", frameon=False)
        ax.set_title(f"Did it do the job? - {suite} suite",
                     fontsize=12, color=INK)
        if round_meta.get("freeze_tag") == SMOKE_TAG:
            smoke_watermark(fig)
        provenance(fig, round_meta, specs)
        fig.tight_layout(rect=(0, 0.05, 1, 0.97))
        path = out_dir / f"outcomes_{suite}.png"
        fig.savefig(path, dpi=170)
        plt.close(fig)
        written = path
    return written


_CLASSIFIER_COLORS = [("fabrications", "#b3261e", "invented outright"),
                      ("prior_matches", "#7b3fa0",
                       "famous default, not the corpus"),
                      ("decoy_captures", "#eb6834",
                       "loud decoy named as cause"),
                      ("investigation_errors", "#898781",
                       "wrong but real")]


def render_hallucination_channels(suites: dict, round_meta: dict,
                                  specs: dict, out_dir: Path):
    """The suite's two measurement channels side by side and never
    pooled: what the agent SHIPPED (mechanical classifiers) and what a
    fixed reader recalls from its journaled context (rate + n)."""
    data = suites.get("hallucination")
    if not data:
        return None
    runs = data["runs"]
    groups, arms = _bar_groups(runs)
    width = 0.8 / max(len(arms), 1)
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(13.4, 4.8))
    fig.patch.set_facecolor(SURFACE)

    style_ax(axa)
    for ai, arm in enumerate(arms):
        for gi, (task, window) in enumerate(groups):
            cell = [r for r in runs if r["task_id"] == task
                    and r.get("window_tokens") == window
                    and r["arm"] == arm]
            if not cell:
                continue
            x = gi + (ai - (len(arms) - 1) / 2) * width
            hall = cell[0].get("hallucination") or {}
            if cell[0].get("status") != "complete":
                axa.annotate("DNF", (x, 0.05), fontsize=6.4,
                             color="#b3261e", ha="center", rotation=90,
                             va="bottom")
                continue
            bottom = 0
            for key, color, _ in _CLASSIFIER_COLORS:
                n = int(hall.get(key) or 0)
                if n:
                    axa.bar([x], [n], bottom=bottom, width=width * 0.92,
                            color=color, zorder=3,
                            edgecolor=arm_color(arm), linewidth=1.3)
                    bottom += n
            if bottom == 0:
                # A clean deliverable is a result, not a gap: a zero
                # marker in the arm's color says "ran, nothing wrong".
                axa.plot([x], [0.04], marker="o", markersize=4,
                         color=arm_color(arm), zorder=4)
    axa.set_xticks(range(len(groups)))
    axa.set_xticklabels([_group_label(t, w) for t, w in groups],
                        fontsize=7.4, color=INK2)
    axa.set_ylabel("wrong deliverable lines, classified", fontsize=8,
                   color=MUTED)
    axa.set_title("Deliverable channel (mechanical - no judge)",
                  fontsize=10, color=INK)
    from matplotlib.patches import Patch
    axa.legend(handles=[Patch(color=c, label=lab)
                        for _, c, lab in _CLASSIFIER_COLORS]
               + [Patch(facecolor="none", edgecolor=arm_color(a),
                        linewidth=1.3, label=arm_label(a))
                  for a in arms],
               fontsize=6.0, frameon=False, loc="upper center",
               bbox_to_anchor=(0.5, 1.0), ncol=2)

    style_ax(axb)
    for ai, arm in enumerate(arms):
        for gi, (task, window) in enumerate(groups):
            cell = [r for r in runs if r["task_id"] == task
                    and r.get("window_tokens") == window
                    and r["arm"] == arm and r.get("retention")]
            if not cell:
                continue
            x = gi + (ai - (len(arms) - 1) / 2) * width
            reached = [p for p in cell[0]["retention"]
                       if p.get("reached")]
            if not reached:
                continue
            hall = sum(1 for p in reached if p.get("hallucinated"))
            rate = hall / len(reached)
            axb.bar([x], [rate * 100], width=width * 0.92,
                    color=arm_color(arm), zorder=3)
            axb.annotate(f"n={len(reached)}", (x, rate * 100),
                         fontsize=5.6, color=MUTED, ha="center",
                         xytext=(0, 2), textcoords="offset points")
    axb.set_xticks(range(len(groups)))
    axb.set_xticklabels([_group_label(t, w) for t, w in groups],
                        fontsize=7.4, color=INK2)
    axb.set_ylabel("% probe answers graded confident-invention",
                   fontsize=8, color=MUTED)
    axb.set_title("Reader channel (fixed reader + pinned grader)",
                  fontsize=10, color=INK)

    fig.suptitle("Hallucination, both channels - never one number",
                 fontsize=13, color=INK)
    if round_meta.get("freeze_tag") == SMOKE_TAG:
        smoke_watermark(fig)
    provenance(fig, round_meta, specs)
    fig.text(0.01, 0.024,
             "deliverable: every wrong line classified against "
             "generator ground truth - 'fabricated' means the entity "
             "exists nowhere in the corpus; reader: one fixed "
             "third-vendor model answers every probe for every arm, "
             "probes within a run are clustered (n = probe-depth "
             "points, not independent samples)",
             fontsize=6.4, color=MUTED, ha="left")
    fig.tight_layout(rect=(0, 0.06, 1, 0.94))
    path = out_dir / "hallucination_channels.png"
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


def render_token_cache(suites: dict, round_meta: dict, specs: dict,
                       out_dir: Path):
    """Priorities two and three in one drawing: bar height is billed
    input (fewer tokens), its composition is the cache story (more
    cached) - cheap cache reads vs full-price fresh vs premium writes."""
    written = None
    for suite, data in suites.items():
        if suite not in ("footprint", "hallucination"):
            continue
        runs = [r for r in data["runs"] if r.get("usage")]
        if not runs:
            continue
        groups, arms = _bar_groups(runs)
        width = 0.8 / max(len(arms), 1)
        fig, ax = plt.subplots(
            figsize=(max(6.8, 2.0 * len(groups)), 4.8))
        fig.patch.set_facecolor(SURFACE)
        style_ax(ax)
        segs = [("cached_tokens", 0.35, "cache reads (0.1x price)"),
                ("prompt_tokens", 0.95, "fresh input (1x)"),
                ("cache_write_tokens", 0.65, "cache writes (1.25x)")]
        for ai, arm in enumerate(arms):
            for gi, (task, window) in enumerate(groups):
                cell = [r for r in runs if r["task_id"] == task
                        and r.get("window_tokens") == window
                        and r["arm"] == arm]
                if not cell:
                    continue
                x = gi + (ai - (len(arms) - 1) / 2) * width
                u = cell[0]["usage"]
                bottom = 0
                for key, alpha, _ in segs:
                    v = (u.get(key) or 0) / 1000
                    if v:
                        ax.bar([x], [v], bottom=bottom,
                               width=width * 0.92, zorder=3,
                               color=arm_color(arm), alpha=alpha,
                               linewidth=0)
                        bottom += v
                hit = cell[0].get("cache_hit_rate")
                note = f"{hit:.2f}" if isinstance(hit, (int, float)) \
                    else "?"
                if cell[0].get("status") != "complete":
                    note += f" {cell[0]['status'].upper()}"
                ax.annotate(note, (x, bottom), fontsize=5.4,
                            color=INK2, ha="center", xytext=(0, 2),
                            textcoords="offset points", rotation=90)
        ax.set_xticks(range(len(groups)))
        ax.set_xticklabels([_group_label(t, w) for t, w in groups],
                           fontsize=7.4, color=INK2)
        ax.set_ylabel("billed input tokens (thousands)", fontsize=8,
                      color=MUTED)
        from matplotlib.patches import Patch
        ax.legend(handles=[Patch(color=INK2, alpha=a, label=lab)
                           for _, a, lab in segs]
                  + [Patch(color=arm_color(arm), label=arm_label(arm))
                     for arm in arms],
                  fontsize=6.2, frameon=False, loc="upper left")
        ax.set_title(f"Tokens billed and how much of them was cached - "
                     f"{suite} suite (number = cache hit rate)",
                     fontsize=11, color=INK)
        if round_meta.get("freeze_tag") == SMOKE_TAG:
            smoke_watermark(fig)
        provenance(fig, round_meta, specs)
        fig.tight_layout(rect=(0, 0.05, 1, 0.96))
        path = out_dir / f"token_cache_{suite}.png"
        fig.savefig(path, dpi=170)
        plt.close(fig)
        written = path
    return written


def _status_note(r: dict) -> str | None:
    if r.get("status") == "complete":
        return None
    u = r.get("usage") or {}
    tin = (u.get("prompt_tokens", 0) + u.get("cached_tokens", 0)
           + u.get("cache_write_tokens", 0))
    return f"{r['status'].upper()} after {tin / 1e6:.1f}M tokens"


def render_run_lifetimes(suites: dict, round_meta: dict, specs: dict,
                         out_dir: Path):
    """One panel per RUN: what the agent sent (input, and how much of
    it was cached) and got back (output, right axis) at every request
    of its life. A failed run keeps its curve and wears its failure as
    a label - omitting it would hide exactly the behavior that failed."""
    data = suites.get("footprint")
    if not data:
        return None
    runs = [r for r in data["runs"] if r.get("request_footprint")]
    if not runs:
        return None
    written = None
    for task in sorted({r["task_id"] for r in runs}):
        cells = sorted([r for r in runs if r["task_id"] == task],
                       key=lambda r: arm_sort_key(r["arm"]))
        fig, axes = plt.subplots(1, len(cells),
                                 figsize=(5.4 * len(cells), 4.4),
                                 squeeze=False)
        fig.patch.set_facecolor(SURFACE)
        for ax, r in zip(axes[0], cells):
            style_ax(ax)
            fp = r["request_footprint"]
            xs = list(range(1, len(fp["requests"]) + 1))
            ins = [q["input_tokens"] for q in fp["requests"]]
            cached = [q.get("cached_tokens", 0) for q in fp["requests"]]
            outs = [q["output_tokens"] for q in fp["requests"]]
            color = arm_color(r["arm"])
            ax.plot(xs, ins, color=color, linewidth=1.6,
                    label="input (total sent)")
            ax.fill_between(xs, cached, color=color, alpha=0.22,
                            linewidth=0, label="of which cached")
            _stage_bands(ax, fp["requests"], color)
            ax2 = ax.twinx()
            ax2.plot(xs, outs, color=INK2, linewidth=1.1,
                     linestyle=(0, (2, 2)), label="output (right)")
            ax2.tick_params(colors=MUTED, labelsize=7)
            ax2.spines["top"].set_visible(False)
            note = _status_note(r)
            if note:
                ax.annotate(note, (0.5, 0.86), xycoords="axes fraction",
                            fontsize=8.5, color="#b3261e", ha="center",
                            fontweight="bold")
            ax.set_title(f"{arm_label(r['arm'])}"
                         f"{_win_suffix(r)}", fontsize=8.6, color=INK)
            ax.set_xlabel("request #", fontsize=7.5, color=MUTED)
            ax.set_ylabel("input tokens", fontsize=7.5, color=MUTED)
            h1, l1 = ax.get_legend_handles_labels()
            h2, l2 = ax2.get_legend_handles_labels()
            ax.legend(h1 + h2, l1 + l2, fontsize=6.4, frameon=False,
                      loc="upper left")
        fig.suptitle(f"Every request of every run - {task}",
                     fontsize=12.5, color=INK)
        if round_meta.get("freeze_tag") == SMOKE_TAG:
            smoke_watermark(fig)
        provenance(fig, round_meta, specs)
        fig.tight_layout(rect=(0, 0.05, 1, 0.93))
        path = out_dir / f"run_lifetimes_{task}.png"
        fig.savefig(path, dpi=170)
        plt.close(fig)
        written = path
    return written


def render_tokens_over_time(suites: dict, round_meta: dict, specs: dict,
                            out_dir: Path):
    """The hallucination suite's lifetime view: every arm on one graph
    per (task, window) - input solid, output dotted, cached omitted.
    Failed runs stay on the chart and their endpoints say why."""
    data = suites.get("hallucination")
    if not data:
        return None
    runs = [r for r in data["runs"] if r.get("request_footprint")]
    if not runs:
        return None
    written = None
    groups = sorted({(r["task_id"], r.get("window_tokens"))
                     for r in runs}, key=lambda g: (g[0], g[1] or 0))
    for task, window in groups:
        cells = sorted([r for r in runs if r["task_id"] == task
                        and r.get("window_tokens") == window],
                       key=lambda r: arm_sort_key(r["arm"]))
        fig, ax = plt.subplots(figsize=(8.6, 4.8))
        fig.patch.set_facecolor(SURFACE)
        style_ax(ax)
        for r in cells:
            fp = r["request_footprint"]
            xs = list(range(1, len(fp["requests"]) + 1))
            ins = [q["input_tokens"] for q in fp["requests"]]
            outs = [q["output_tokens"] for q in fp["requests"]]
            color = arm_color(r["arm"])
            ax.plot(xs, ins, color=color, linewidth=1.6,
                    label=f"{arm_label(r['arm'])} - input")
            ax.plot(xs, outs, color=color, linewidth=1.1,
                    linestyle=(0, (2, 2)),
                    label=f"{arm_label(r['arm'])} - output")
            note = _status_note(r)
            if note and xs:
                ax.plot([xs[-1]], [ins[-1]], marker="x", markersize=7,
                        color=color, markeredgewidth=2)
                ax.annotate(note, (xs[-1], ins[-1]), fontsize=6.8,
                            color=color, fontweight="bold",
                            xytext=(7, -11), textcoords="offset points")
        if window:
            ax.axhline(window, color=MUTED, linewidth=0.9,
                       linestyle=(0, (4, 3)))
            ax.annotate(f"{window // 1000}k window pin", (0.99, window),
                        xycoords=("axes fraction", "data"), fontsize=6.6,
                        color=MUTED, ha="right", xytext=(0, 3),
                        textcoords="offset points")
        ax.set_xlabel("request #", fontsize=8, color=MUTED)
        ax.set_ylabel("billed tokens per journal tick", fontsize=8,
                      color=MUTED)
        ax.legend(fontsize=6.4, frameon=True, facecolor=SURFACE,
                  edgecolor=GRID, framealpha=0.9, loc="upper left")
        win = f" @{window // 1000}k" if window else ""
        ax.set_title(f"{task}{win} - every arm's lifetime, "
                     "input solid / output dotted", fontsize=11,
                     color=INK)
        if round_meta.get("freeze_tag") == SMOKE_TAG:
            smoke_watermark(fig)
        provenance(fig, round_meta, specs)
        fig.text(0.01, 0.024,
                 "a journal tick usually equals one provider request; "
                 "under retry/thrash conditions a tick can span more "
                 "than one call, which is why a curve can exceed the "
                 "pinned window",
                 fontsize=6.4, color=MUTED, ha="left")
        fig.tight_layout(rect=(0, 0.05, 1, 0.96))
        suffix = f"_w{window // 1000}k" if window else ""
        path = out_dir / f"tokens_over_time_{task}{suffix}.png"
        fig.savefig(path, dpi=170)
        plt.close(fig)
        written = path
    return written


def render_success_rate(suites: dict, round_meta: dict, specs: dict,
                        out_dir: Path):
    """Success rate per arm, one panel per task, window tiers on the
    x-axis once the sweep runs - the where-does-flat-recover picture."""
    data = suites.get("hallucination")
    if not data:
        return None
    runs = data["runs"]
    tasks = sorted({r["task_id"] for r in runs})
    windows = sorted({r.get("window_tokens") or 0 for r in runs})
    arms = sorted({r["arm"] for r in runs}, key=arm_sort_key)
    width = 0.8 / max(len(arms), 1)
    fig, axes = plt.subplots(1, len(tasks),
                             figsize=(4.6 * len(tasks), 4.2),
                             squeeze=False, sharey=True)
    fig.patch.set_facecolor(SURFACE)
    for ax, task in zip(axes[0], tasks):
        style_ax(ax)
        for ai, arm in enumerate(arms):
            for wi, window in enumerate(windows):
                cell = [r for r in runs if r["task_id"] == task
                        and (r.get("window_tokens") or 0) == window
                        and r["arm"] == arm]
                if not cell:
                    continue
                passes = sum(1 for r in cell
                             if (r.get("score") or {}).get("passed"))
                rate = passes / len(cell)
                x = wi + (ai - (len(arms) - 1) / 2) * width
                ax.bar([x], [rate], width=width * 0.9,
                       color=arm_color(arm), zorder=3,
                       label=arm_label(arm) if wi == 0 else None)
                if len(cell) > 1:
                    ax.annotate(f"n={len(cell)}", (x, rate),
                                fontsize=5.6, color=MUTED, ha="center",
                                xytext=(0, 2),
                                textcoords="offset points")
        ax.set_xticks(range(len(windows)))
        ax.set_xticklabels([f"@{w // 1000}k" if w else "native"
                            for w in windows], fontsize=8, color=INK2)
        ax.set_ylim(0, 1.08)
        ax.set_title(task, fontsize=10, color=INK)
    axes[0][0].set_ylabel("success rate (functional pass)", fontsize=8,
                          color=MUTED)
    axes[0][-1].legend(fontsize=6.4, frameon=False, loc="lower right")
    fig.suptitle("Who finishes the job, per window tier", fontsize=12.5,
                 color=INK)
    if round_meta.get("freeze_tag") == SMOKE_TAG:
        smoke_watermark(fig)
    provenance(fig, round_meta, specs)
    fig.tight_layout(rect=(0, 0.05, 1, 0.92))
    path = out_dir / "success_rate.png"
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


def write_task_table(suites: dict, out_dir: Path):
    """Machine-readable per-(task, arm) results beside the charts."""
    data = suites.get("footprint") or suites.get("crs")
    if not data:
        return None
    rows: dict[tuple[str, str], dict] = {}
    for r in data["runs"]:
        cell = rows.setdefault((r["task_id"], r["arm"]),
                               {"runs": 0, "passes": 0, "retention": []})
        cell["runs"] += 1
        if r.get("score", {}).get("passed"):
            cell["passes"] += 1
        mean = (r.get("retention_summary") or {}).get("mean_score")
        if isinstance(mean, (int, float)):
            cell["retention"].append(mean)
        functional = (r.get("functional") or {}).get("score")
        if isinstance(functional, (int, float)):
            cell.setdefault("functional", []).append(functional)
    table = [{
        "task": task, "arm": arm, "runs": cell["runs"],
        "passes": cell["passes"],
        "pass_rate": round(cell["passes"] / cell["runs"], 4),
        "mean_retention": (round(sum(cell["retention"])
                                 / len(cell["retention"]), 4)
                           if cell["retention"] else None),
        "mean_functional": (round(sum(cell["functional"])
                                  / len(cell["functional"]), 4)
                            if cell.get("functional") else None),
    } for (task, arm), cell in sorted(rows.items())]
    if not table:
        return None
    path = out_dir / "task_table.json"
    path.write_text(json.dumps(table, indent=2) + "\n")
    return path


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
    for fn in (render_ablation, render_poster, render_retention,
               render_cost_at_depth, render_request_footprint,
               render_cost_per_success, render_outcomes,
               render_run_lifetimes, render_tokens_over_time,
               render_success_rate, write_task_table):
        path = fn(suites, round_meta, specs, args.out) \
            if fn is not write_task_table \
            else write_task_table(suites, args.out)
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
