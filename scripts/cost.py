#!/usr/bin/env python3
"""The ONE cost formula for every benchmark arm, chart, and report.

Costs are computed exclusively from API-reported usage fields (Anthropic
semantics: `input_tokens` EXCLUDES cache reads/writes, which are billed
separately) at the per-model rates pinned in the round's `rates.json`:

    {
      "pinned_at": "YYYY-MM-DD",
      "source": "<pricing page URL captured at freeze time>",
      "models": {
        "<model-id>": {
          "input_per_mtok": 3.0,
          "output_per_mtok": 15.0,
          "cache_write_per_mtok": 3.75,
          "cache_read_per_mtok": 0.30
        }
      }
    }

rates.json is written at freeze time from the provider's current price list —
never from memory — and committed with the round. There is deliberately no
default rates table in this file.

CLI: cost.py <rates.json> <model> <input> <output> <cache_write> <cache_read>
"""
import json
import sys
from pathlib import Path


def load_rates(path):
    rates = json.loads(Path(path).read_text())
    for key in ("pinned_at", "source", "models"):
        if key not in rates:
            sys.exit(f"rates file {path} missing '{key}' — pin rates at freeze time")
    return rates


def compute_cost(usage, model, rates):
    try:
        r = rates["models"][model]
    except KeyError:
        sys.exit(f"no pinned rates for model '{model}' — add it to rates.json")
    return (
        usage["input_tokens"] * r["input_per_mtok"]
        + usage["output_tokens"] * r["output_per_mtok"]
        + usage["cache_creation_input_tokens"] * r["cache_write_per_mtok"]
        + usage["cache_read_input_tokens"] * r["cache_read_per_mtok"]
    ) / 1_000_000


if __name__ == "__main__":
    if len(sys.argv) != 7:
        sys.exit(__doc__)
    rates = load_rates(sys.argv[1])
    usage = dict(zip(
        ("input_tokens", "output_tokens",
         "cache_creation_input_tokens", "cache_read_input_tokens"),
        map(int, sys.argv[3:7]),
    ))
    print(f"{compute_cost(usage, sys.argv[2], rates):.4f}")
