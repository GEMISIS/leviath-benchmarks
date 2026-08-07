"""The generic task -> run -> collect -> grade loop.

Suites are plugins (duck-typed):

    class Suite:
        name: str
        agent_for(arm) -> (blueprint_name, extra_cli_args)
        load_tasks(subset_record) -> list[Task]     # Task: dict with "id"
        prepare(task, workdir) -> str               # returns prompt text
        collect(task, workdir, run_dir, answer) -> submission (any)
        grade(task, submission) -> dict | None      # {"passed": bool, ...}
                                                    # None = graded later

The runner owns everything else: fresh per-run workdirs, launch/poll via
levctl, the status taxonomy, seeded arm interleaving, the budget guard,
and writing one raw record per cell no matter what happened.

Known gap, deliberate: a mixed-models arm (model_policy null) has no
single rate to price its aggregate usage, and meta.json does not break
usage down per model. Its cost_usd is recorded as null until per-model
usage harvesting is wired; its token counters are still exact.
"""
from __future__ import annotations

import gzip
import random
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from . import cost as cost_mod
from . import record as record_mod

__all__ = ["run_matrix"]


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _usage_of(meta: dict | None) -> dict:
    meta = meta or {}
    return {k: int(meta.get(k, 0) or 0)
            for k in ("prompt_tokens", "completion_tokens", "cached_tokens",
                      "cache_write_tokens")}


def run_matrix(home, suite, tasks: list[dict], arms: list[dict],
               reps: int, rates: dict, runs_dir: Path, artifacts_root: Path,
               freeze_tag: str, lev_info: dict, blueprint_shas: dict,
               rates_sha: str, seed: int, task_timeout_secs: float,
               budget_usd: float | None, keep_context: bool,
               per_run_max_tokens: int | None = None,
               log=print) -> list[dict]:
    """Run every (task x arm x rep) cell and return the written records.

    ``arms`` entries: {"name", "role", "model_label", "model_id"} where
    role is "structured" or "flat" (the suite maps it to its blueprint)
    and model_id is None for a native stage-mix arm.
    """
    cells = [(t, a, rep)
             for t in tasks for a in arms for rep in range(1, reps + 1)]
    # Interleave arms/models so provider drift and time-of-day effects
    # never load onto one arm.
    random.Random(seed).shuffle(cells)

    spent = 0.0
    records = []
    for i, (task, arm, rep) in enumerate(cells, 1):
        blueprint, extra_cli = suite.agent_for(arm)
        # Per-task output spec (lev run --output-format/--output-
        # instructions) is applied to every arm identically, so the
        # answer-shape guidance rides the runtime's own mechanism
        # rather than fighting a blueprint's output-stage prompt.
        if hasattr(suite, "task_cli"):
            extra_cli = list(extra_cli) + list(suite.task_cli(task))
        label = (f"{suite.name}/{task['id']} {arm['name']} "
                 f"[{arm['model_label'] or 'native'}] rep{rep}")
        base = {
            "schema": record_mod.SCHEMA,
            "freeze_tag": freeze_tag,
            "suite": suite.name,
            "task_id": task["id"],
            "arm": arm["name"],
            "model_label": arm["model_label"] or "native",
            "model_policy": arm["model_id"],
            "rep": rep,
            "blueprint": {"name": blueprint,
                          "sha256": blueprint_shas.get(blueprint)},
            "lev": lev_info,
            "rates_sha256": rates_sha,
        }

        if budget_usd is not None and spent >= budget_usd:
            log(f"[{i}/{len(cells)}] {label}: BUDGET CAP "
                f"(${spent:.2f} >= ${budget_usd:.2f})")
            records.append(_finish(base, runs_dir, status="cap",
                                   started=_utcnow(), ended=_utcnow(),
                                   wall=0.0, meta=None, arm=arm,
                                   rates=rates, score={"passed": False,
                                                       "detail": "budget cap"}))
            continue

        log(f"[{i}/{len(cells)}] {label}")
        workdir = home.home / "work" / record_mod.record_filename(
            task["id"], arm["name"], arm["model_label"] or "native",
            rep).removesuffix(".json")
        shutil.rmtree(workdir, ignore_errors=True)
        workdir.mkdir(parents=True)

        started = _utcnow()
        t0 = time.time()
        status, meta, answer = "error", None, None
        stage_records: list[dict] = []
        try:
            prompt = suite.prepare(task, workdir)
            run_id = home.launch(blueprint, prompt, workdir,
                                 model=arm["model_id"],
                                 extra_args=extra_cli)
            should_cancel = None
            if per_run_max_tokens:
                # Model-agnostic mid-run ceiling on billed tokens; the
                # cancelled run is recorded as "cap" with its spend.
                should_cancel = (lambda m: cost_mod.billed_tokens(
                    _usage_of(m), False) > per_run_max_tokens)
            status, meta = home.wait(run_id, task_timeout_secs,
                                     should_cancel=should_cancel)
            stage_records = home.stages(run_id)
            if status == "complete":
                answer = home.result(run_id)
                if answer is None:
                    status = "no_answer"
            # Suites over gated datasets never write context replays:
            # a replay embeds task text and attachment contents, which
            # their terms forbid storing in a public repository.
            if keep_context and not getattr(suite, "contains_gated_data",
                                            False):
                dump = home.context_dump(run_id)
                if dump:
                    art = _artifacts_dir(artifacts_root, base)
                    (art / "context.json.gz").write_bytes(
                        gzip.compress(dump.encode()))
        except Exception as exc:  # recorded, never skipped
            log(f"  run errored: {exc}")
            status = "error" if status not in ("timeout",) else status
        wall = round(time.time() - t0, 1)

        score = None
        if status in ("complete",):
            art = _artifacts_dir(artifacts_root, base)
            try:
                submission = suite.collect(task, workdir, art, answer)
                score = suite.grade(task, submission)
            except Exception as exc:
                log(f"  grading errored: {exc}")
                score = {"passed": False, "detail": f"grade error: {exc}"}
        if score is None and status != "complete":
            score = {"passed": False, "detail": f"status {status}"}

        mix_mapping = None
        if arm["model_id"] is None:
            blueprint_toml = (home.home / ".leviath" / "agents"
                              / blueprint / "agent.leviath")
            try:
                mix_mapping = cost_mod.stagemix_mapping(blueprint_toml)
            except Exception:
                mix_mapping = None
        rec = _finish(base, runs_dir, status=status, started=started,
                      ended=_utcnow(), wall=wall, meta=meta, arm=arm,
                      rates=rates, score=score,
                      stage_records=stage_records,
                      mix_mapping=mix_mapping)
        if isinstance(rec.get("cost_usd"), (int, float)):
            spent += rec["cost_usd"]
        records.append(rec)
    log(f"done: {len(records)} records, ~${spent:.2f} priced spend")
    return records


def _artifacts_dir(artifacts_root: Path, base: dict) -> Path:
    stem = record_mod.record_filename(
        base["task_id"], base["arm"], base["model_label"],
        base["rep"]).removesuffix(".json")
    path = artifacts_root / f"{stem}.artifacts"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _finish(base: dict, runs_dir: Path, status: str, started: str,
            ended: str, wall: float, meta: dict | None, arm: dict,
            rates: dict, score: dict | None,
            stage_records: list[dict] | None = None,
            mix_mapping: dict | None = None) -> dict:
    usage = _usage_of(meta)
    model_id = arm["model_id"]
    priced = model_id is not None and cost_mod.is_pinned(rates, model_id)
    includes = (rates[model_id]["prompt_includes_cache_read"]
                if model_id in rates else False)
    record = dict(base)
    record.update({
        "status": status,
        "started_utc": started,
        "ended_utc": ended,
        "wall_clock_secs": wall,
        "usage": usage,
        "billed_tokens": cost_mod.billed_tokens(usage, includes),
        "cache_hit_rate": cost_mod.cache_hit_rate(usage, includes),
        "tool_calls": int((meta or {}).get("tool_calls", 0) or 0),
        "iterations": (meta or {}).get("iteration"),
        "final_stage": (meta or {}).get("current_stage"),
        "cost_usd": (cost_mod.cost_usd(usage, model_id, rates)
                     if priced else None),
        "score": score,
    })
    if model_id is None and stage_records and mix_mapping:
        # Native mix: price per stage from the stage ledger. Cache
        # writes are unattributed in the ledger and priced at the most
        # expensive stage model's write rate - an upper bound, so the
        # mix is never flattered.
        mix_cost = cost_mod.stagemix_cost(stage_records, mix_mapping,
                                          usage, rates)
        if mix_cost is not None:
            record["cost_usd"] = mix_cost
            record["cost_basis"] = "stagewise_estimate_upper_bound"
            record["stage_models"] = mix_mapping
            record["usage_by_stage"] = [
                {k: s.get(k) for k in ("name", "prompt_tokens",
                                       "completion_tokens",
                                       "cached_tokens")}
                for s in stage_records]
    record_mod.write_record(runs_dir, record)
    return record
