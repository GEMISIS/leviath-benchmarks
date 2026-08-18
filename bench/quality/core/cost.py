"""Provider-billed cost from token usage at pinned rates.

One formula for every arm, applied to the usage counters leviath copies
verbatim from the provider response (`meta.json`: prompt_tokens,
completion_tokens, cached_tokens, cache_write_tokens). Rates are pinned
per round in rates.json and never fetched live.

Provider semantics differ and the difference is exactly the kind of bug
that silently corrupts every cost number, so each rates entry must state
it explicitly:

- Anthropic: prompt_tokens is the API's input_tokens, which EXCLUDES
  cache reads and cache writes (verified against the provider source the
  runtime uses: anthropic.rs maps input_tokens -> prompt_tokens and
  cache_read_input_tokens -> cached_tokens separately). Billed input =
  prompt + cached*cache_read_rate + cache_write*cache_write_rate.
- OpenAI-style: prompt_tokens INCLUDES the cached portion; cached tokens
  are billed at the discounted rate instead of the input rate.

rates.json shape:

    {
      "_meta": {"source_url": "...", "captured_utc": "..."},
      "anthropic/claude-x": {
        "input_per_mtok": 3.0, "output_per_mtok": 15.0,
        "cache_read_per_mtok": 0.3, "cache_write_per_mtok": 3.75,
        "prompt_includes_cache_read": false
      }
    }
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

__all__ = ["load_rates", "rates_sha256", "cost_usd", "billed_tokens",
           "cache_hit_rate", "is_pinned"]

_MTOK = 1_000_000


def load_rates(path: Path) -> dict:
    rates = json.loads(Path(path).read_text())
    for model, entry in rates.items():
        if model.startswith("_"):
            continue
        missing = {"input_per_mtok", "output_per_mtok", "cache_read_per_mtok",
                   "cache_write_per_mtok",
                   "prompt_includes_cache_read"} - set(entry)
        if missing:
            raise ValueError(f"rates.json entry {model!r} missing {missing}")
    return rates


def rates_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def is_pinned(rates: dict, model_id: str) -> bool:
    """True only when the model has a real (non-placeholder) rate.

    An all-zero entry is a development placeholder; treating it as a
    price would record every run as free, so it is not priced at all.
    """
    entry = rates.get(model_id)
    if not entry:
        return False
    if entry.get("local"):
        # Local compute: zero is the true provider price, declared
        # explicitly so it can never be confused with a placeholder.
        return True
    return any(entry[k] > 0 for k in ("input_per_mtok", "output_per_mtok",
                                      "cache_read_per_mtok",
                                      "cache_write_per_mtok"))


def _entry(rates: dict, model_id: str) -> dict:
    if model_id not in rates:
        raise KeyError(
            f"no pinned rate for {model_id!r}; add it to rates.json "
            "(never guess a price)")
    return rates[model_id]


def billed_tokens(usage: dict, prompt_includes_cache_read: bool) -> int:
    """Every token the provider bills for, cache reads and writes included."""
    total = (int(usage.get("prompt_tokens", 0))
             + int(usage.get("completion_tokens", 0))
             + int(usage.get("cache_write_tokens", 0)))
    if not prompt_includes_cache_read:
        total += int(usage.get("cached_tokens", 0))
    return total


def cost_usd(usage: dict, model_id: str, rates: dict) -> float:
    r = _entry(rates, model_id)
    prompt = int(usage.get("prompt_tokens", 0))
    cached = int(usage.get("cached_tokens", 0))
    cache_write = int(usage.get("cache_write_tokens", 0))
    completion = int(usage.get("completion_tokens", 0))
    if r["prompt_includes_cache_read"]:
        # Cached portion sits inside prompt_tokens; re-price it at the
        # discounted rate rather than double-charging.
        uncached = max(prompt - cached, 0)
    else:
        uncached = prompt
    usd = (uncached * r["input_per_mtok"]
           + cached * r["cache_read_per_mtok"]
           + cache_write * r["cache_write_per_mtok"]
           + completion * r["output_per_mtok"]) / _MTOK
    return round(usd, 6)


def stagemix_mapping(blueprint_path: Path) -> dict[str, str]:
    """Stage -> provider/model for a blueprint's native mix.

    Native runs resolve each stage to the first configured provider in
    its model list; with every roster provider keyed, that is the first
    entry. The mapping is recorded alongside any cost computed from it
    so the assumption is inspectable.
    """
    import tomllib
    doc = tomllib.loads(Path(blueprint_path).read_text())
    mapping = {}
    for name, stage in doc.get("stages", {}).items():
        models = (stage.get("model") or {}).get("models") or []
        if models:
            mapping[name] = f"{models[0]['provider']}/{models[0]['model']}"
    return mapping


def stagemix_cost(stage_records: list[dict], mapping: dict[str, str],
                  total_usage: dict, rates: dict) -> float | None:
    """Price a native-mix run stage-wise from the per-stage ledger.

    Each stage's prompt/cached/completion tokens are priced at that
    stage's model rate. The ledger does not attribute cache WRITES per
    stage, so the run's total cache-write tokens are priced at the most
    expensive write rate among the stages' models - a deliberate upper
    bound, disclosed via cost_basis on the record. Returns None when
    any stage's model has no pinned rate.
    """
    total = 0.0
    max_write_rate = 0.0
    for srec in stage_records:
        model_id = mapping.get(srec.get("name"))
        if not model_id or not is_pinned(rates, model_id):
            return None
        stage_usage = {
            "prompt_tokens": srec.get("prompt_tokens", 0),
            "completion_tokens": srec.get("completion_tokens", 0),
            "cached_tokens": srec.get("cached_tokens", 0),
            "cache_write_tokens": 0,
        }
        total += cost_usd(stage_usage, model_id, rates)
        max_write_rate = max(max_write_rate,
                             rates[model_id]["cache_write_per_mtok"])
    total += (int(total_usage.get("cache_write_tokens", 0))
              * max_write_rate / _MTOK)
    return round(total, 6)


def cache_hit_rate(usage: dict,
                   prompt_includes_cache_read: bool) -> float | None:
    """Cache reads as a share of all input-side tokens, or None if no input."""
    prompt = int(usage.get("prompt_tokens", 0))
    cached = int(usage.get("cached_tokens", 0))
    cache_write = int(usage.get("cache_write_tokens", 0))
    denom = prompt + cache_write
    if not prompt_includes_cache_read:
        denom += cached
    if denom == 0:
        return None
    return round(cached / denom, 4)
