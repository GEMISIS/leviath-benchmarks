#!/usr/bin/env python3
"""Run one quality suite for leviath and write raw results.

The quality track scores real task outcomes on external suites with
deterministic verifiers, under three context arms per suite:

- flat-pinned:        flat-context blueprint, one pinned model
- structured-pinned:  structured blueprint, the same pinned model
- structured-stagemix: structured blueprint, its native per-stage models

Everything is recorded raw - one JSON per run including failures,
timeouts, and budget cap-outs - and summaries are medians with min/max
and every underlying point. Counted rounds require a qbench-* freeze tag
on a clean tree; --unsafe-smoke bypasses that but stamps every record
UNFROZEN-SMOKE, which the renderer refuses for publishable output.

Usage:
    python3 bench/quality/run_quality.py --suite loganalysis \
        --arms flat-pinned,structured-pinned --models "Claude Sonnet 5" \
        --reps 3 [--subset suites/loganalysis/subsets/r1.json] \
        [--unsafe-smoke] [--budget-usd 50]

Outputs land under results/<UTC-stamp>_<hostname>/quality/<suite>/ in
the same results tree the performance track uses.
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import socket
import subprocess
import sys
import datetime as dt
from datetime import datetime, timezone
from pathlib import Path

QUALITY_DIR = Path(__file__).resolve().parent
BENCH_DIR = QUALITY_DIR.parent
REPO_DIR = BENCH_DIR.parent
sys.path.insert(0, str(QUALITY_DIR))
sys.path.insert(0, str(BENCH_DIR))

import machine_specs  # noqa: E402
from core import cost as cost_mod  # noqa: E402
from core import freeze, record, runner, scrub, stats, subset  # noqa: E402
from core import throughput as throughput_mod  # noqa: E402
from core.levctl import QualityHome  # noqa: E402

DEFAULT_TIMEOUT_SECS = 1800


def load_dotenv(path: Path) -> None:
    """Load KEY=VALUE lines from the repo's gitignored .env.

    Real environment variables always win; empty values are skipped.
    Keys reach provider SDKs through the process environment only and
    are never written into results (scrub.py enforces that end-side).
    """
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if value and key not in os.environ:
            os.environ[key] = value


def require_result_capable(lev: str) -> None:
    """Gate on capability, not version number.

    The quality track's answer-capture contract is `lev result`; any
    build that has it works - mainline, an alpha, or whatever release
    the user installed. A version gate would wrongly reject source
    builds, so we probe the subcommand instead.
    """
    try:
        probe = subprocess.run([lev, "result", "--help"],
                               capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        sys.exit(f"could not run {lev!r}; pass --lev /path/to/lev")
    if probe.returncode != 0:
        sys.exit(
            "the quality track needs a lev with the `result` subcommand "
            "(mainline, or v0.3.0+ once released). The lev at "
            f"{lev!r} does not have it - build from source "
            "(cargo build --release -p leviath-cli) or install a newer "
            "build, then point --lev at it.")
# Comparisons are pre-registered: arm a is hypothesized to pass MORE and
# bill FEWER tokens than arm b.
COMPARISONS = [
    ("structured-pinned", "flat-pinned"),
    # CRS pre-registered comparisons: the Leviath arm is the composed
    # flagship (the configuration the runtime actually recommends), read
    # against the strong flat baseline first and the plain one second.
    ("structured-mix-flagship", "flat-compacting"),
    ("flat-compacting", "flat-pinned"),
]


# Roster recency (METHODOLOGY.md): the roster carries models released
# within roughly two months of the round. Past this many days a model
# is reported as aged - the round still runs, and the age travels into
# round.json so a reader can judge it instead of guessing.
RECENCY_DAYS = 75


def load_arms_config(path: Path) -> dict:
    cfg = json.loads(path.read_text())
    for name, entry in cfg["models"].items():
        if not {"id", "tier"} <= set(entry):
            raise ValueError(f"arms.json model {name!r} needs id + tier")
        if entry["tier"] != "smoke" and not entry.get("released"):
            raise ValueError(f"arms.json model {name!r} needs a released "
                             "date (YYYY-MM-DD) for the recency rule")
    return cfg


def roster_ages(cfg: dict, as_of: dt.date) -> dict:
    """Age in days of every real roster model, as of the round start."""
    ages = {}
    for name, entry in cfg["models"].items():
        if entry["tier"] == "smoke":
            continue
        released = dt.date.fromisoformat(entry["released"])
        ages[name] = {"released": entry["released"],
                      "age_days": (as_of - released).days}
    return ages


def resolve_arms(cfg: dict, arm_names: list[str],
                 model_labels: list[str]) -> list[dict]:
    """Expand $sweep arms over the selected roster entries."""
    roster = cfg["models"]
    unknown = set(model_labels) - set(roster)
    if unknown:
        raise ValueError(f"models not in arms.json roster: {sorted(unknown)}")
    resolved = []
    for arm in cfg["arms"]:
        if arm["name"] not in arm_names:
            continue
        if arm["model"] == "$sweep":
            for label in model_labels:
                # A swept arm may still name a variant: that is how a
                # layout change is compared against the same model
                # rather than against a different one.
                resolved.append({"name": arm["name"], "role": arm["role"],
                                 "model_label": label,
                                 "model_id": roster[label]["id"],
                                 "variant": arm.get("variant")})
        elif arm["model"] is None:
            # A mixed arm runs the blueprint's own per-stage assignment;
            # `variant` picks which generated mix that is.
            resolved.append({"name": arm["name"], "role": arm["role"],
                             "model_label": None, "model_id": None,
                             "variant": arm.get("variant")})
        else:
            resolved.append({"name": arm["name"], "role": arm["role"],
                             "model_label": arm["model"],
                             "model_id": roster[arm["model"]]["id"]})
    if not resolved:
        raise ValueError(f"no arms matched {arm_names}")
    return resolved


def comparisons_block(records_list: list[dict], seed: int = 0) -> list[dict]:
    """p-values for every pre-registered arm pair, per model.

    Exact enumeration where it fits, a seeded random-permutation test
    where it cannot (whole-suite cells run to C(72,36) and beyond); each
    entry records which was used, with the resample count and seed.
    Only cells that produced a measurement are compared - a cap-out or a
    crash is a non-completion in the pass rate, but it has no token
    total to rank, so including it would compare a zero against real
    work.
    """
    out = []
    for arm_a, arm_b in COMPARISONS:
        models = sorted({r["model_label"] for r in records_list
                         if r["arm"] in (arm_a, arm_b)})
        for model in models:
            a = [r for r in records_list
                 if r["arm"] == arm_a and r["model_label"] == model]
            b = [r for r in records_list
                 if r["arm"] == arm_b and r["model_label"] == model]
            if not a or not b:
                continue
            entry = {"a": arm_a, "b": arm_b, "model_label": model,
                     "hypothesis": "a passes more and bills fewer tokens",
                     "n_a": len(a), "n_b": len(b)}
            entry["pass"] = stats.pass_rate_test(
                [bool(r["score"] and r["score"].get("passed")) for r in a],
                [bool(r["score"] and r["score"].get("passed")) for r in b],
                seed=seed)
            measured_a = [r for r in a if r["status"] == "complete"]
            measured_b = [r for r in b if r["status"] == "complete"]
            entry["tokens_n_a"] = len(measured_a)
            entry["tokens_n_b"] = len(measured_b)
            if measured_a and measured_b:
                entry["tokens"] = stats.rank_sum_test(
                    [float(r["billed_tokens"]) for r in measured_a],
                    [float(r["billed_tokens"]) for r in measured_b],
                    seed=seed)
            else:
                entry["tokens"] = None
                entry["tokens_note"] = ("no completed runs on one side; "
                                        "nothing to rank")
            out.append(entry)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--suite", required=True,
                        help="suite plugin name under suites/")
    parser.add_argument("--lev", default="lev", help="path to the lev binary")
    parser.add_argument("--arms", default="flat-pinned,structured-pinned",
                        help="comma-separated arm names from arms.json")
    parser.add_argument("--models", default=None,
                        help="comma-separated roster labels to sweep "
                             "(default: every roster entry)")
    parser.add_argument("--reps", type=int, default=1)
    parser.add_argument("--subset", default=None,
                        help="subset file (default: the suite's full "
                             "task list)")
    parser.add_argument("--out", default=None,
                        help="results dir (default: results/<stamp>_<host>)")
    parser.add_argument("--budget-usd", type=float, default=None)
    parser.add_argument("--per-run-max-tokens", type=int,
                        default=3_000_000,
                        help="mid-run billed-token ceiling per run; the "
                             "run is cancelled and recorded as 'cap' "
                             "when exceeded (0 disables)")
    parser.add_argument("--task-timeout", type=float,
                        default=DEFAULT_TIMEOUT_SECS)
    parser.add_argument("--concurrency", type=int, default=1,
                        help="cells to run at once. The host handles "
                             "hundreds of agents; the provider is the real "
                             "ceiling, so raise this alongside the rate "
                             "limits in arms.json. Wall-clock is only "
                             "comparable between rounds run at the same "
                             "level, and every record carries it")
    parser.add_argument("--window-tokens", type=int, default=None,
                        help="pin every roster model's context window to "
                             "min(native, N) for this invocation - the "
                             "declared independent variable of the CRS "
                             "window sweep. Model labels get an @<N>k "
                             "suffix so tiers coexist in one results "
                             "dir, and window_tokens lands in round.json "
                             "and every record")
    parser.add_argument("--seed", type=int, default=1,
                        help="interleaving order seed (recorded)")
    parser.add_argument("--provider-config", default=None,
                        help="config.toml text file installed into the "
                             "isolated home (smoke/mock runs)")
    parser.add_argument("--providers-dir", default=None,
                        help="script-provider dir to install (mock runs)")
    parser.add_argument("--keep-context", action="store_true")
    parser.add_argument("--unsafe-smoke", action="store_true",
                        help="run without a freeze tag; records are "
                             "stamped UNFROZEN-SMOKE")
    args = parser.parse_args()

    load_dotenv(REPO_DIR / ".env")
    require_result_capable(args.lev)

    if args.unsafe_smoke:
        freeze_tag = freeze.SMOKE_TAG
    else:
        try:
            freeze_tag = freeze.require_frozen(REPO_DIR)
        except RuntimeError as exc:
            sys.exit(str(exc))

    suite_mod = importlib.import_module(f"suites.{args.suite}.suite")
    suite = suite_mod.Suite()

    missing = {name: why
               for name, why in getattr(suite, "requires_env", {}).items()
               if not os.environ.get(name)}
    if missing:
        for name, why in missing.items():
            print(f"{suite.name} requires {name}: {why}", file=sys.stderr)
        return 2

    arms_cfg = load_arms_config(QUALITY_DIR / "arms.json")
    if args.window_tokens:
        # The window sweep: every model in the round runs under
        # min(native, N). Region budgets are percentages of the window,
        # so this shrinks every region proportionally - the same agent
        # under a smaller deployment, which is the declared variable.
        for entry in arms_cfg["models"].values():
            if entry.get("tier") == "smoke":
                continue
            native = entry.get("context_window") or args.window_tokens
            # Pin ONLY the window. Overrides apply field-by-field since
            # #338, so every capability flag stays the runtime's own -
            # inventing flags here is how a model that refuses
            # `temperature` gets sent one and 400s every call.
            cap = dict(entry.get("capability_override") or {})
            cap["max_context_tokens"] = min(native, args.window_tokens)
            entry["capability_override"] = cap
            entry["context_window"] = min(native, args.window_tokens)
    model_labels = (args.models.split(",") if args.models
                    else list(arms_cfg["models"]))
    arms = resolve_arms(arms_cfg, args.arms.split(","),
                        [m.strip() for m in model_labels])
    if args.window_tokens:
        suffix = f"@{args.window_tokens // 1000}k"
        for arm in arms:
            arm["window_tokens"] = args.window_tokens
            arm["model_label"] = (f"{arm['model_label'] or 'native'} "
                                  f"{suffix}")

    ages = roster_ages(arms_cfg, dt.datetime.now(timezone.utc).date())
    for label in sorted({a["model_label"] for a in arms} & set(ages)):
        if ages[label]["age_days"] > RECENCY_DAYS:
            print(f"note: {label} was released {ages[label]['released']}, "
                  f"{ages[label]['age_days']} days ago - past the "
                  f"{RECENCY_DAYS}-day roster recency rule", file=sys.stderr)

    rates = cost_mod.load_rates(QUALITY_DIR / "rates.json")
    rates_sha = cost_mod.rates_sha256(QUALITY_DIR / "rates.json")

    subset_record = None
    if args.subset:
        subset_record = subset.load_subset(Path(args.subset))
    tasks = suite.load_tasks(subset_record)
    if not tasks:
        print("no tasks to run", file=sys.stderr)
        return 2

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_root = Path(args.out) if args.out else (
        REPO_DIR / "results" / f"{stamp}_{socket.gethostname()}")
    suite_dir = out_root / "quality" / suite.name
    runs_dir = suite_dir / "runs"
    suite_dir.mkdir(parents=True, exist_ok=True)
    specs_path = out_root / "specs.json"
    if not specs_path.exists():
        specs_path.write_text(
            json.dumps(machine_specs.gather(args.lev), indent=2) + "\n")

    home = QualityHome(args.lev)
    blueprints_dir = QUALITY_DIR / "blueprints"
    config_text = (Path(args.provider_config).read_text()
                   if args.provider_config else
                   "# leviath-benchmarks quality isolated home (generated)\n")
    # Every model's context window, pinned: it is what region budgets
    # are a percentage of, so it belongs in the frozen inputs rather
    # than in whatever the runtime's model table happens to know.
    windows = QualityHome.capability_overrides(arms_cfg["models"])
    if windows:
        config_text = f"{config_text}\n{windows}"
    # Daemon lanes and provider pacing for the concurrency asked for.
    config_text = (f"{config_text}\n"
                   + QualityHome.concurrency_config(
                       args.concurrency, arms_cfg.get("rate_limits", {})))
    # Anthropic cache entries default to a 5-minute TTL, which a staged
    # run outlives between writing a prefix and re-reading it; the hour
    # TTL costs nothing extra on hits and is part of what a structured
    # arm is claimed to be able to do. Native Anthropic provider only.
    config_text += '\n[providers]\nanthropic_cache_ttl = "1h"\n'
    # Blueprint tool_permissions are a ceiling by default (only
    # web_search/web_fetch may loosen); --yolo masks that by
    # auto-approving. The ask tests run attended so the ask tools
    # survive - without this, every shell call parks on an approval
    # the scripted user must rubber-stamp (~35 round trips per run).
    # The home is hermetic and every other cell runs --yolo, so this
    # only makes attended cells behave like the rest of the matrix.
    config_text += '\n[security]\nallow_blueprint_permissions = true\n'
    home.install(blueprints_dir, config_text,
                 providers_dir=(Path(args.providers_dir)
                                if args.providers_dir else None))

    blueprint_shas = freeze.manifest_sha256s(
        [p for p in sorted(blueprints_dir.iterdir()) if p.is_dir()])
    blueprint_shas = {Path(k).name: v for k, v in blueprint_shas.items()}

    lev_info = {"version": home.version(),
                "sha256": machine_specs._sha256(args.lev)}

    round_meta = {
        "freeze_tag": freeze_tag,
        "suite": suite.name,
        "seed": args.seed,
        "window_tokens": args.window_tokens,
        "reps": args.reps,
        "budget_usd": args.budget_usd,
        "per_run_max_tokens": args.per_run_max_tokens or None,
        "concurrency": args.concurrency,
        "rate_limits": arms_cfg.get("rate_limits", {}),
        "task_timeout_secs": args.task_timeout,
        "arms": arms,
        "roster": arms_cfg["models"],
        "roster_ages": ages,
        "context_windows": {n: e.get("context_window")
                            for n, e in arms_cfg["models"].items()},
        # One mapping per mixed arm in the round: with several mixes,
        # "which models, on which stages" has more than one answer.
        "stagemix_mapping": {
            a["name"]: cost_mod.stagemix_mapping(
                blueprints_dir / suite.agent_for(a)[0] / "agent.leviath")
            for a in arms if a["model_id"] is None},
        "subset": subset_record,
        "rates_sha256": rates_sha,
        "blueprints": blueprint_shas,
        "lev": lev_info,
        "records_schema": record.SCHEMA,
    }
    round_path = out_root / "quality" / "round.json"
    round_path.write_text(json.dumps(round_meta, indent=2) + "\n")

    # Mock smoke runs simulate inference latency the way the perf track
    # does (LEVMOCK_LATENCY_MS + the local sleep server). Instant mock
    # inference is also unrealistically fast for the persistence lane,
    # so smoke runs should always set a nonzero latency.
    latency_proc = None
    if os.environ.get("LEVMOCK_LATENCY_MS"):
        latency_proc = subprocess.Popen(
            [sys.executable, str(BENCH_DIR / "latency_server.py")],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import time as _time
        _time.sleep(1.0)

    home.start_daemon()
    try:
        written = runner.run_matrix(
            home, suite, tasks, arms, args.reps, rates, runs_dir,
            runs_dir, freeze_tag, lev_info, blueprint_shas, rates_sha,
            args.seed, args.task_timeout, args.budget_usd,
            args.keep_context,
            per_run_max_tokens=args.per_run_max_tokens or None,
            concurrency=args.concurrency)
    finally:
        home.stop_daemon()
        if latency_proc is not None:
            latency_proc.terminate()

    summary = {
        "suite": suite.name,
        "freeze_tag": freeze_tag,
        "aggregate": record.aggregate(written),
        "comparisons": comparisons_block(written, seed=args.seed),
        "throughput": throughput_mod.throughput(written, args.concurrency),
    }
    (suite_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n")

    findings = scrub.scan(out_root)
    if findings:
        for f in findings:
            print(f"SECRET LEAK: {f['kind']} in {f['file']}",
                  file=sys.stderr)
        print("results tree contains secrets - fix before committing",
              file=sys.stderr)
        return 3
    print(f"results: {suite_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
