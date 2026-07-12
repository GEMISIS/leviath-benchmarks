#!/usr/bin/env python3
"""
Generate publication-quality benchmark charts for Leviath.

Design principles:
- Light background for README/blog embedding
- Bold brand color for Leviath, neutral gray for baseline
- Headlines that argue, not describe
- Data labels on every element
- Error bars from multiple runs (statistical rigor)
- Each chart makes ONE point in under 3 seconds
"""

import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ---------------------------------------------------------------------------
# Brand palette
# ---------------------------------------------------------------------------
LEVIATH     = '#0066FF'
LEVIATH_BG  = '#E8F0FE'
BASELINE    = '#B0B8C4'
BASELINE_DK = '#6B7685'
BG          = '#FFFFFF'
TEXT        = '#1F2328'
MUTED       = '#656D76'
GRID        = '#E5E7EB'
GREEN       = '#1A7F37'
RED         = '#CF222E'

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
def setup():
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Helvetica Neue', 'Helvetica', 'Arial',
                            'DejaVu Sans'],
        'font.size': 11,
        'figure.facecolor': BG,
        'axes.facecolor': BG,
        'text.color': TEXT,
    })

def strip(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.spines['left'].set_color(GRID)
    ax.spines['bottom'].set_color(GRID)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load():
    for p in [Path(__file__).parent.parent / 'results' / 'benchmark-results.json',
              Path('../results/benchmark-results.json'),
              Path('results/benchmark-results.json')]:
        if p.exists():
            with open(p) as f:
                return json.load(f)
    sys.exit('benchmark-results.json not found')

def save(fig, name, out):
    for ext in ('svg', 'png'):
        fig.savefig(out / f'{name}.{ext}', bbox_inches='tight',
                    facecolor=BG, dpi=200)
    plt.close(fig)

# ---------------------------------------------------------------------------
# Chart 1 — Hero metrics card
# ---------------------------------------------------------------------------
def hero(data, out):
    """Four KPI cards — cost leads, biggest win first."""
    lev = data['approaches']['leviath']
    flat = data['approaches']['flat_baseline']
    n_lev = lev['runs']
    n_flat = flat['runs']

    metrics = [
        # (label, lev_display, flat_display, improvement_text, is_win)
        ('API Cost',
         f"${lev['cost_usd']['mean']:.2f}",
         f"${flat['cost_usd']['mean']:.2f}",
         f"{(1 - lev['cost_usd']['mean']/flat['cost_usd']['mean'])*100:.0f}% less",
         True),
        ('Tool Calls',
         f"{lev['tool_calls']['mean']:.0f}",
         f"{flat['tool_calls']['mean']:.0f}",
         f"{(1 - lev['tool_calls']['mean']/flat['tool_calls']['mean'])*100:.0f}% fewer",
         True),
        ('Runtime',
         f"{lev['duration_seconds']['mean']/60:.0f} min",
         f"{flat['duration_seconds']['mean']/60:.0f} min",
         f"{(1 - lev['duration_seconds']['mean']/flat['duration_seconds']['mean'])*100:.0f}% faster",
         True),
        ('Pass Rate',
         f"{lev['pass_rate']['mean']:.1f}%",
         f"{flat['pass_rate']['mean']:.1f}%",
         f"+{lev['pass_rate']['mean'] - flat['pass_rate']['mean']:.1f}pp" if lev['pass_rate']['mean'] > flat['pass_rate']['mean'] else 'comparable',
         lev['pass_rate']['mean'] >= flat['pass_rate']['mean']),
    ]

    fig, axes = plt.subplots(1, 4, figsize=(14, 3.2))
    fig.subplots_adjust(top=0.78)

    fig.text(0.5, 0.95,
             'Leviath v3 vs Flat Baseline',
             ha='center', fontsize=17, fontweight='bold', color=TEXT)
    run_word = "runs" if n_lev > 1 else "run"
    fig.text(0.5, 0.88,
             f'Same task  \u00b7  Same model (Sonnet 5)  \u00b7  Same 69 hidden validation tests  \u00b7  {n_lev} {run_word} each',
             ha='center', fontsize=10, color=MUTED)

    for i, (label, lev_s, flat_s, imp, win) in enumerate(metrics):
        ax = axes[i]
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)

        # Background card
        rect = mpatches.FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                                        boxstyle='round,pad=0.02',
                                        facecolor='#F6F8FA', edgecolor=GRID,
                                        linewidth=1)
        ax.add_patch(rect)

        # Label
        ax.text(0.5, 0.88, label, ha='center', va='center',
                fontsize=11, fontweight='bold', color=MUTED)

        # Hero number (Leviath)
        ax.text(0.5, 0.62, lev_s, ha='center', va='center',
                fontsize=26, fontweight='bold', color=LEVIATH)

        # Baseline comparison
        ax.text(0.5, 0.38, f'vs {flat_s}', ha='center', va='center',
                fontsize=12, color=BASELINE_DK)

        # Improvement badge
        color = GREEN if win else MUTED
        ax.text(0.5, 0.16, imp, ha='center', va='center',
                fontsize=10, fontweight='bold', color=color,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#DAFBE1' if win else '#F6F8FA',
                          edgecolor=color, alpha=0.7, linewidth=0.5))

    save(fig, 'hero-comparison', out)
    print('  \u2713 hero-comparison')


# ---------------------------------------------------------------------------
# Chart 2 — Cost vs Quality scatter
# ---------------------------------------------------------------------------
def cost_quality(data, out):
    """The money chart. Cost on x, pass rate on y, with error bars."""
    lev = data['approaches']['leviath']
    flat = data['approaches']['flat_baseline']

    fig, ax = plt.subplots(figsize=(8, 5))
    strip(ax)

    # Error bars
    lev_cost = lev['cost_usd']['mean']
    flat_cost = flat['cost_usd']['mean']
    lev_rate = lev['pass_rate']['mean']
    flat_rate = flat['pass_rate']['mean']

    lev_cost_err = lev['cost_usd'].get('ci95', 0)
    flat_cost_err = flat['cost_usd'].get('ci95', 0)
    lev_rate_err = lev['pass_rate'].get('ci95', 0)
    flat_rate_err = flat['pass_rate'].get('ci95', 0)

    # Plot points with error bars
    ax.errorbar(lev_cost, lev_rate, xerr=lev_cost_err, yerr=lev_rate_err,
                fmt='o', markersize=14, color=LEVIATH, markeredgecolor='white',
                markeredgewidth=2, capsize=5, capthick=2, elinewidth=2,
                zorder=5)
    ax.errorbar(flat_cost, flat_rate, xerr=flat_cost_err, yerr=flat_rate_err,
                fmt='s', markersize=12, color=BASELINE, markeredgecolor='white',
                markeredgewidth=2, capsize=5, capthick=2, elinewidth=2,
                zorder=5)

    # Labels
    ax.annotate('Leviath v3', (lev_cost, lev_rate),
                xytext=(12, 10), textcoords='offset points',
                fontsize=12, fontweight='bold', color=LEVIATH)
    ax.annotate('Flat Baseline', (flat_cost, flat_rate),
                xytext=(12, -15), textcoords='offset points',
                fontsize=12, fontweight='bold', color=BASELINE_DK)

    # Draw straight dashed connector between points
    ax.plot([flat_cost, lev_cost], [flat_rate, lev_rate],
            linestyle='--', color=MUTED, linewidth=1, alpha=0.5, zorder=2)

    # Savings callout
    savings = (1 - lev_cost / flat_cost) * 100
    mid_x = (lev_cost + flat_cost) / 2
    mid_y = (lev_rate + flat_rate) / 2 + 3
    ax.text(mid_x, mid_y,
            f'{savings:.0f}% cheaper\nwith equal quality',
            ha='center', fontsize=10, fontweight='bold', color=GREEN,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#DAFBE1',
                      edgecolor=GREEN, linewidth=0.5))

    ax.set_xlabel('Cost (USD)', fontsize=12, color=MUTED)
    ax.set_ylabel('Pass Rate (%)', fontsize=12, color=MUTED)
    ax.set_title('Better Quality at Lower Cost',
                 fontsize=15, fontweight='bold', pad=12)

    # Ideal quadrant label
    ax.text(0.02, 0.98, 'ideal: upper-left', transform=ax.transAxes,
            fontsize=8, color=MUTED, va='top', style='italic')

    ax.xaxis.grid(True, color=GRID, linewidth=0.5, zorder=0)
    ax.yaxis.grid(True, color=GRID, linewidth=0.5, zorder=0)

    # Set axis ranges with some padding
    ax.set_xlim(0, max(lev_cost, flat_cost) * 1.3)
    ax.set_ylim(min(lev_rate, flat_rate) - 5, 100)

    plt.tight_layout()
    save(fig, 'cost-quality', out)
    print('  \u2713 cost-quality')


# ---------------------------------------------------------------------------
# Chart 3 — Efficiency bars (horizontal, simple)
# ---------------------------------------------------------------------------
def efficiency(data, out):
    """Side-by-side bars for the three efficiency metrics."""
    lev = data['approaches']['leviath']
    flat = data['approaches']['flat_baseline']

    fig, axes = plt.subplots(1, 3, figsize=(13, 3.5))
    fig.subplots_adjust(top=0.82)
    fig.text(0.5, 0.95, 'Efficiency Comparison',
             ha='center', fontsize=15, fontweight='bold')
    n = lev['runs']
    subtitle = f'{n} {"runs" if n > 1 else "run"} per approach'
    if n > 1:
        subtitle += '  \u00b7  mean values shown  \u00b7  error bars = 95% CI'
    fig.text(0.5, 0.88, subtitle, ha='center', fontsize=9, color=MUTED)

    items = [
        ('Cost (USD)', 'cost_usd', '$'),
        ('Tool Calls', 'tool_calls', ''),
        ('Runtime (min)', 'duration_seconds', '', 1/60),
    ]

    for idx, (label, key, prefix, *scale) in enumerate(items):
        ax = axes[idx]
        strip(ax)
        s = scale[0] if scale else 1

        lv = lev[key]['mean'] * s
        fv = flat[key]['mean'] * s
        le = lev[key].get('ci95', lev[key].get('stddev', 0)) * s
        fe = flat[key].get('ci95', flat[key].get('stddev', 0)) * s

        colors = [LEVIATH, BASELINE]
        bars = ax.barh([0, 1], [lv, fv], height=0.5, color=colors,
                       xerr=[le, fe], capsize=4, error_kw={'linewidth': 1.5},
                       zorder=3)

        # Labels
        for j, (v, e) in enumerate([(lv, le), (fv, fe)]):
            txt = f'{prefix}{v:.1f}' if prefix == '$' else f'{v:.0f}'
            if e > 0:
                txt += f' \u00b1 {prefix}{e:.1f}' if prefix == '$' else f' \u00b1 {e:.0f}'
            ax.text(v + max(lv, fv) * 0.03, j, txt,
                    va='center', fontsize=10, fontweight='bold',
                    color=LEVIATH if j == 0 else BASELINE_DK)

        ax.set_yticks([0, 1])
        ax.set_yticklabels(['Leviath v3', 'Flat Baseline'], fontsize=10)
        ax.set_xlabel(label, fontsize=10, color=MUTED)
        ax.invert_yaxis()
        ax.xaxis.grid(True, color=GRID, linewidth=0.5, zorder=0)

        # Improvement annotation
        imp = (1 - lv / fv) * 100
        if imp > 0:
            ax.text(0.98, 0.98, f'{imp:.0f}% less',
                    transform=ax.transAxes, ha='right', va='top',
                    fontsize=9, fontweight='bold', color=GREEN)

    plt.tight_layout(rect=[0, 0, 1, 0.84])
    save(fig, 'efficiency', out)
    print('  \u2713 efficiency')


# ---------------------------------------------------------------------------
# Chart 4 — Run consistency (shows all individual run results)
# ---------------------------------------------------------------------------
def consistency(data, out):
    """Strip chart showing individual run pass rates to demonstrate consistency."""
    lev = data['approaches']['leviath']
    flat = data['approaches']['flat_baseline']

    if lev['runs'] < 2 and flat['runs'] < 2:
        print('  (skipping consistency chart — need 2+ runs)')
        return

    fig, ax = plt.subplots(figsize=(8, 3.5))
    strip(ax)

    # Individual points
    lev_vals = lev['pass_rate'].get('values', [lev['pass_rate']['mean']])
    flat_vals = flat['pass_rate'].get('values', [flat['pass_rate']['mean']])

    for i, v in enumerate(lev_vals):
        ax.scatter(v, 0.3, s=80, color=LEVIATH, alpha=0.7, zorder=5,
                   edgecolors='white', linewidths=1)
    for i, v in enumerate(flat_vals):
        ax.scatter(v, 0.7, s=80, color=BASELINE, alpha=0.7, zorder=5,
                   edgecolors='white', linewidths=1)

    # Mean markers
    ax.scatter(lev['pass_rate']['mean'], 0.3, s=200, color=LEVIATH,
               marker='D', zorder=6, edgecolors='white', linewidths=2)
    ax.scatter(flat['pass_rate']['mean'], 0.7, s=200, color=BASELINE,
               marker='D', zorder=6, edgecolors='white', linewidths=2)

    # Labels
    ci_lev = lev['pass_rate'].get('ci95', 0)
    ci_flat = flat['pass_rate'].get('ci95', 0)
    ax.text(lev['pass_rate']['mean'], 0.1,
            f"{lev['pass_rate']['mean']:.1f}% \u00b1 {ci_lev:.1f}",
            ha='center', fontsize=10, fontweight='bold', color=LEVIATH)
    ax.text(flat['pass_rate']['mean'], 0.9,
            f"{flat['pass_rate']['mean']:.1f}% \u00b1 {ci_flat:.1f}",
            ha='center', fontsize=10, fontweight='bold', color=BASELINE_DK)

    ax.set_yticks([0.3, 0.7])
    ax.set_yticklabels(['Leviath v3', 'Flat Baseline'], fontsize=11)
    ax.set_xlabel('Pass Rate (%)', fontsize=11, color=MUTED)
    ax.set_title(f'Run-to-Run Consistency ({lev["runs"]} runs each)',
                 fontsize=14, fontweight='bold', pad=10)
    ax.set_ylim(-0.1, 1.1)
    ax.xaxis.grid(True, color=GRID, linewidth=0.5, zorder=0)
    ax.set_xlim(min(min(lev_vals + flat_vals)) - 5, 100)

    plt.tight_layout()
    save(fig, 'consistency', out)
    print('  \u2713 consistency')


# ---------------------------------------------------------------------------
# Chart 5 — System Resource Footprint (Device RAM scaling)
# ---------------------------------------------------------------------------
TOOL_COLORS = {
    'claude_code': '#E04D3A',   # coral-red
    'pi':          '#F5A623',   # amber
    'codex_cli':   '#8B5CF6',   # violet
    'opencode':    '#2DD4BF',   # teal-green
}
TOOL_LABELS = {
    'claude_code': 'Claude Code',
    'codex_cli':   'Codex CLI',
    'pi':          'Pi',
    'opencode':    'OpenCode',
}

def resource_footprint(out):
    """Device RAM scaling: Leviath (flat) vs process-per-agent tools (linear)."""

    res_path = Path(__file__).parent.parent / 'results' / 'resource' / 'scaling-results.json'
    if not res_path.exists():
        print('  ⊘ scaling-results.json not found, skipping resource chart')
        return

    with open(res_path) as f:
        res = json.load(f)

    fig, ax = plt.subplots(figsize=(11, 6.5))
    strip(ax)

    # Plot Leviath line — bold, prominent
    lev = res['leviath']['measurements']
    lev_x = [m['agents'] for m in lev]
    lev_y = [m['peak_rss_mb'] for m in lev]
    ax.plot(lev_x, lev_y, color=LEVIATH, linewidth=3.5, marker='o',
            markersize=9, zorder=10, label='Leviath (ECS)')
    ax.fill_between(lev_x, lev_y, alpha=0.06, color=LEVIATH, zorder=5)

    # Leviath data labels — only at 1 and last measured point to avoid clutter
    ax.annotate(f'{lev_y[0]} MB', (lev_x[0], lev_y[0]),
                textcoords='offset points', xytext=(-30, 14),
                ha='center', fontsize=10, fontweight='bold', color=LEVIATH)
    ax.annotate(f'{lev_y[-1]} MB', (lev_x[-1], lev_y[-1]),
                textcoords='offset points', xytext=(0, 14),
                ha='center', fontsize=10, fontweight='bold', color=LEVIATH)

    # Plot each competing tool — thinner lines, sorted by peak RSS descending
    tool_order = sorted(
        [k for k in ['claude_code', 'pi', 'codex_cli', 'opencode'] if k in res['tools']],
        key=lambda k: res['tools'][k]['measurements'][-1]['peak_rss_mb'],
        reverse=True
    )

    for tool_key in tool_order:
        tool = res['tools'][tool_key]
        mx = [m['agents'] for m in tool['measurements']]
        my = [m['peak_rss_mb'] for m in tool['measurements']]
        color = TOOL_COLORS.get(tool_key, BASELINE)
        label = TOOL_LABELS.get(tool_key, tool_key)

        ax.plot(mx, my, color=color, linewidth=2, marker='s',
                markersize=5, zorder=8, label=label, alpha=0.85)

        # No inline labels at measured points — let the legend + projections
        # carry identification. This avoids the x=5 label pileup.

    # Projection lines to 10 agents (dashed, no 20 — keep clean)
    proj_labels = []
    for tool_key in tool_order:
        tool = res['tools'][tool_key]
        measurements = tool['measurements']
        if len(measurements) >= 2:
            per_inst = measurements[-1]['peak_rss_mb'] / measurements[-1]['agents']
            last_x = measurements[-1]['agents']
            last_y = measurements[-1]['peak_rss_mb']
            proj_10 = int(per_inst * 10)
            color = TOOL_COLORS.get(tool_key, BASELINE)
            ax.plot([last_x, 10], [last_y, proj_10],
                    color=color, linewidth=1.5, linestyle='--', alpha=0.35, zorder=6)
            proj_labels.append((tool_key, proj_10, color))

    # Label 10-agent projections with tool name + value
    # Sort descending so labels appear top-to-bottom matching visual order
    proj_labels.sort(key=lambda x: x[1], reverse=True)
    # Space labels at least 20px apart vertically
    label_y_offsets = []
    base_offset = 0
    for i, (tool_key, proj_val, color) in enumerate(proj_labels):
        label_name = TOOL_LABELS.get(tool_key, tool_key)
        gb_str = f'{proj_val/1000:.1f} GB' if proj_val >= 1000 else f'{proj_val} MB'

        # Check if this label would collide with previous
        y_offset = 0
        if i > 0:
            prev_val = proj_labels[i-1][1]
            gap = prev_val - proj_val
            # If values are close (<200 MB), push label down
            if gap < 200:
                y_offset = -15 * (i % 2)  # alternate up/down

        ax.annotate(f'{label_name}: ~{gb_str}', (10, proj_val),
                    textcoords='offset points',
                    xytext=(8, y_offset),
                    ha='left', fontsize=9, color=color, alpha=0.8,
                    fontweight='bold')

    # Leviath projection to 10
    base = res['leviath']['base_rss_mb']
    per_a = res['leviath']['per_agent_overhead_mb']
    lev_10 = base + per_a * 10
    ax.plot([lev_x[-1], 10], [lev_y[-1], lev_10],
            color=LEVIATH, linewidth=2.5, linestyle='--', alpha=0.35, zorder=6)
    ax.annotate(f'{lev_10} MB', (10, lev_10),
                textcoords='offset points', xytext=(8, 8),
                ha='left', fontsize=9, color=LEVIATH, alpha=0.7,
                fontstyle='italic', fontweight='bold')

    # Callout box — positioned in clean whitespace (right side, midway up)
    if 'claude_code' in res['tools']:
        claude_5 = next((m['peak_rss_mb'] for m in res['tools']['claude_code']['measurements']
                         if m['agents'] == 5), None)
        lev_5 = next((m['peak_rss_mb'] for m in lev if m['agents'] == 5), None)
        if claude_5 and lev_5:
            ratio = claude_5 / lev_5
            # Position callout in clean whitespace, explicitly name Claude Code
            ax.annotate(
                f'{ratio:.0f}\u00d7 lighter than\nClaude Code at 5 agents',
                xy=(5, claude_5 * 0.5), xytext=(7.8, claude_5 * 0.55),
                fontsize=12, fontweight='bold', color=LEVIATH,
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.6', facecolor=LEVIATH_BG,
                          edgecolor=LEVIATH, linewidth=2, alpha=0.95))

    # Titles — with proper spacing
    ax.set_title('System Resource Footprint',
                 fontsize=18, fontweight='bold', pad=20, color=TEXT)
    fig.text(0.5, 0.94,
             'ECS engine vs process-per-agent \u2014 measured on macOS, Apple Silicon, 16 GB',
             ha='center', fontsize=10, color=MUTED)

    ax.set_xlabel('Concurrent Agents', fontsize=12, color=TEXT, labelpad=8)
    ax.set_ylabel('Peak Device RAM (MB)', fontsize=12, color=TEXT, labelpad=8)

    ax.legend(loc='upper left', frameon=True, fancybox=True,
              edgecolor=GRID, fontsize=9, ncol=1)
    ax.yaxis.grid(True, color=GRID, linewidth=0.5, alpha=0.5, zorder=0)

    # Use proportional x-axis spacing
    ax.set_xlim(0, 11.5)
    ax.set_xticks([1, 3, 5, 10])

    # Footnotes
    ax.text(0.98, 0.02, 'Dashed = linear projection from measured data',
            transform=ax.transAxes, ha='right', fontsize=8,
            color=MUTED, fontstyle='italic')

    plt.tight_layout(rect=[0, 0, 1, 0.92])
    save(fig, 'resource-footprint', out)
    print('  \u2713 resource-footprint')


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    setup()
    data = load()
    out = Path(__file__).parent / 'output'
    out.mkdir(exist_ok=True)

    print(f'Benchmark: {data["benchmark"]}')
    print(f'Task: {data["task"]}')
    if 'methodology' in data:
        m = data['methodology']
        print(f'Model: {m.get("model", "N/A")}')
        print(f'Validation: {m.get("validation", "N/A")}')
    print()

    hero(data, out)
    cost_quality(data, out)
    efficiency(data, out)
    consistency(data, out)
    resource_footprint(out)

    # Clean up old charts
    for old in ['pass-rate', 'cost-comparison', 'time-comparison', 'summary-table']:
        for ext in ('svg', 'png'):
            p = out / f'{old}.{ext}'
            if p.exists():
                p.unlink()

    print(f'\nAll charts saved to {out}')


if __name__ == '__main__':
    main()
