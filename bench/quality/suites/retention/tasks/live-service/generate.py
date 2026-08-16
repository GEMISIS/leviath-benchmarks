#!/usr/bin/env python3
"""Generate the live-service corpus (retention suite, depth task).

The corpus is not a pile of files - it is a SERVICE. The workdir ships
a small deterministic order-processing server the agent must start,
poke, load, reconfigure and observe. Interactive state kills every
static shortcut: the fault only manifests under traffic the agent
itself generates, /metrics only shows a sliding window so history must
be observed (and remembered) as it happens, and the mitigation can
only be proven by applying it and watching the recovery. Every poke is
a tool call at depth, which is the point: this task exists to carry
the retention curve past 150 calls.

The injected fault chain, registered by the generator:

1. POST /orders for any item in the fault CATEGORY silently also
   decrements a RELATED item in a different category (a packing
   consumable, per the seeded link table). The response says ok; only
   /inventory diffs reveal the drain.
2. When the related item's stock crosses the seeded threshold, the
   restock worker enters a retry loop (supplier backorder): a per-tick
   retry counter climbs in /metrics and the service log.
3. While the worker retries, every order's reported latency degrades -
   the customer-visible symptom.
4. Setting the TRUE mitigation config key to "exponential" via
   PUT /config backs the worker off and latency recovers. The shipped
   runbook documents this mitigation under a WRONG key name; the true
   name is discoverable via GET /config (or the rejection message).

Two hard constraints, as everywhere in this repo:

- Determinism: the emitted tree is a pure function of --seed
  (--check verifies byte-identity), and the SERVICE is a pure function
  of seed.json plus the request sequence it receives - a logical
  clock, no wall time, no runtime RNG. Same requests, same bytes back.
- Self-supporting key: the self-test imports the emitted srv.py and
  drives a full scripted diagnosis in-process - baseline, reproduce,
  observe, wrong-key rejection, true-key mitigation, recovery -
  asserting every registered answer and counting the calls a diligent
  diagnosis costs (the task's depth demand, asserted >= 120).

Usage:
    python3 generate.py [--seed N] [--out DIR] [--check]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import random
import sys
import tempfile
from pathlib import Path

DEFAULT_SEED = 8117
MAX_FILE_BYTES = 60_000
MIN_DEPTH = 120

CATEGORIES = ["beverage", "perishable", "frozen", "dry-goods",
              "household"]
# The related item is always a packing consumable - a category of its
# own so the drain is never explainable by the item's own orders.
CONSUMABLES = [("chill-pack", "insulated chill pack"),
               ("crate-liner", "vented crate liner"),
               ("seal-wrap", "tamper seal wrap")]

ITEM_NAMES = ["arabica beans", "oat milk", "rye loaf", "goat cheese",
              "orange juice", "frozen peas", "gyoza tray", "rice 5kg",
              "olive oil", "paper towels", "dish soap", "lentils",
              "kombucha", "butter block", "berry mix"]

METRIC_KEYS = ["restock_retry_count", "restock_retries_total",
               "worker_retry_count"]
TRUE_KEYS = ["restock_backoff_mode", "restock_retry_policy",
             "restock_backoff_strategy"]
WRONG_KEYS = ["restock_backoff", "retry_backoff_mode",
              "restock_policy"]

# ---------------------------------------------------------------------
# Fixed service source. Nothing seeded lives here: every varying fact
# is read from seed.json at startup, so probes may quote this file and
# --check stays trivially byte-stable across seeds.
# ---------------------------------------------------------------------

SRV_PY = r'''#!/usr/bin/env python3
"""Order-processing service (benchmark fixture).

Deterministic by construction: behavior is a pure function of
seed.json and the request sequence. A logical clock advances once per
handled request; no wall time or randomness is ever consulted for
behavior (a wall-clock TTL exists only as a self-destruct so an
abandoned server cannot outlive its benchmark run).

Run:  python3 srv.py [--port N]        (0 = pick a free port)
The chosen port is written to port.txt beside this file. The runtime
log is appended to service.log beside this file.
"""
import argparse
import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS_WINDOW = 20   # ticks of history /metrics reports
ORDER_QTY_CAP = 3     # larger orders are rejected


class Service:
    def __init__(self, seed_path):
        self.seed = json.loads(Path(seed_path).read_text())
        self.tick = 0
        self.items = {i["id"]: dict(i) for i in self.seed["items"]}
        self.config = dict(self.seed["config"])
        self.orders = []
        self.latencies = []      # (tick, ms)
        self.retry_events = []   # ticks a retry happened
        self.retries_total = 0
        self.orders_processed = 0
        self.log_path = HERE / "service.log"

    # -- internals ----------------------------------------------------

    def _log(self, msg):
        with open(self.log_path, "a") as f:
            f.write("[t%05d] %s\n" % (self.tick, msg))

    def _fault(self):
        return self.seed["fault"]

    def _related_id(self):
        return self.seed["items"][self._fault()["rel"]]["id"]

    def _worker_should_retry(self):
        rel = self.items[self._related_id()]
        low = rel["stock"] < self._fault()["thr"]
        mitigated = self.config.get(
            self.seed["mitigation"]["key"]) == \
            self.seed["mitigation"]["value"]
        return low and not mitigated

    def _advance(self):
        self.tick += 1
        if self._worker_should_retry():
            self.retries_total += 1
            self.retry_events.append(self.tick)
            self._log("restock worker retry #%d for %s: supplier "
                      "backorder" % (self.retries_total,
                                     self._related_id()))
        elif self.retry_events and \
                self.retry_events[-1] == self.tick - 1:
            self._log("restock worker idle")

    def _latency_ms(self):
        lo, hi = self.seed["latency"]["base"]
        span = max(hi - lo, 1)
        val = lo + ((self.tick * 7919) % (span * 10)) / 10.0
        if self.retry_events and self.retry_events[-1] >= \
                self.tick - 1:
            val = val * self.seed["latency"]["degraded_multiplier"] \
                + (self.tick * 104729) % 120
        return round(val, 1)

    # -- request handling --------------------------------------------

    def handle(self, method, path, body):
        self._advance()
        if method == "GET" and path == "/health":
            return 200, {"status": "ok", "tick": self.tick}
        if method == "GET" and path == "/inventory":
            return 200, {i["id"]: self.items[i["id"]]["stock"]
                         for i in self.seed["items"]}
        if method == "GET" and path == "/config":
            return 200, dict(self.config)
        if method == "PUT" and path == "/config":
            body = body or {}
            unknown = [k for k in body if k not in self.config]
            if unknown:
                return 400, {"error": "unknown config key(s): %s"
                             % ", ".join(sorted(unknown)),
                             "valid_keys": sorted(self.config)}
            self.config.update(body)
            self._log("config updated: %s" % json.dumps(
                body, sort_keys=True))
            return 200, {"ok": True, "config": dict(self.config)}
        if method == "GET" and path == "/orders":
            return 200, {"recent": self.orders[-10:],
                         "orders_processed": self.orders_processed}
        if method == "POST" and path == "/orders":
            body = body or {}
            item = self.items.get(body.get("item"))
            qty = int(body.get("qty", 1))
            if item is None:
                return 404, {"error": "no such item"}
            if qty < 1 or qty > ORDER_QTY_CAP:
                return 400, {"error": "qty must be 1..%d"
                             % ORDER_QTY_CAP}
            if item["stock"] < qty:
                return 409, {"error": "insufficient stock"}
            item["stock"] -= qty
            fault = self._fault()
            if item["cat"] == fault["cat"]:
                rel = self.items[self._related_id()]
                rel["stock"] = max(rel["stock"] - qty, 0)
            ms = self._latency_ms()
            self.latencies.append((self.tick, ms))
            self.orders_processed += 1
            entry = {"tick": self.tick, "item": item["id"],
                     "qty": qty, "latency_ms": ms}
            self.orders.append(entry)
            self._log("order %s x%d served in %sms"
                      % (item["id"], qty, ms))
            return 200, entry
        if method == "GET" and path == "/metrics":
            floor = self.tick - METRICS_WINDOW
            window_lat = [ms for t, ms in self.latencies
                          if t > floor]
            retries = sum(1 for t in self.retry_events if t > floor)
            avg = round(sum(window_lat) / len(window_lat), 1) \
                if window_lat else 0.0
            return 200, {
                "tick": self.tick,
                "window_ticks": METRICS_WINDOW,
                "orders_in_window": len(window_lat),
                "avg_latency_ms_window": avg,
                self.seed["metrics"]["retry_key"]: retries,
            }
        if method == "GET" and path == "/admin/workers":
            state = "retrying" if self._worker_should_retry() \
                else "idle"
            return 200, {"restock_worker": state,
                         "retries_total": self.retries_total}
        if method == "GET" and path == "/admin/state":
            return 200, {
                "tick": self.tick,
                "orders_processed": self.orders_processed,
                "retries_total": self.retries_total,
                "inventory": {i["id"]: self.items[i["id"]]["stock"]
                              for i in self.seed["items"]},
                "config": dict(self.config),
            }
        if method == "POST" and path == "/admin/shutdown":
            return 200, {"ok": True, "shutting_down": True}
        return 404, {"error": "no such endpoint"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=0)
    ap.add_argument("--seed-path", default=str(HERE / "seed.json"))
    ap.add_argument("--ttl-seconds", type=int, default=7200,
                    help="wall-clock self destruct (safety only; "
                         "never consulted for behavior)")
    args = ap.parse_args()
    svc = Service(args.seed_path)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _serve(self, method):
            length = int(self.headers.get("Content-Length") or 0)
            body = None
            if length:
                try:
                    body = json.loads(self.rfile.read(length))
                except ValueError:
                    body = None
            status, payload = svc.handle(method, self.path, body)
            data = json.dumps(payload).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            if self.path == "/admin/shutdown" and method == "POST":
                threading.Thread(target=server.shutdown,
                                 daemon=True).start()

        def do_GET(self):
            self._serve("GET")

        def do_POST(self):
            self._serve("POST")

        def do_PUT(self):
            self._serve("PUT")

    server = HTTPServer(("127.0.0.1", args.port), Handler)
    (HERE / "port.txt").write_text(str(server.server_address[1]))
    threading.Thread(target=lambda: (time.sleep(args.ttl_seconds),
                                     server.shutdown()),
                     daemon=True).start()
    print("live-service listening on port %d"
          % server.server_address[1])
    server.serve_forever()


if __name__ == "__main__":
    main()
'''

API_MD = """\
# Order Service - API notes (rev 4)

The service listens on the port written to `service/port.txt` after
startup. All bodies are JSON. It keeps a runtime log in
`service/service.log`.

| endpoint | verbs | notes |
|---|---|---|
| /health | GET | liveness + logical tick |
| /orders | POST, GET | place an order {"item", "qty"} (qty 1..3); GET lists recent |
| /inventory | GET | current stock per item |
| /config | GET, PUT | live keys; PUT rejects unknown keys and lists valid ones |
| /metrics | GET | sliding window over the last 20 ticks only |
| /admin/workers | GET | background worker status |
| /admin/state | GET | full state dump (diagnostics) |
| /admin/shutdown | POST | stop the service |

Every handled request advances the service's logical clock by one
tick. `/metrics` reports ONLY the trailing 20-tick window - history
you did not observe is history you no longer have.
"""

RUNBOOK_TMPL = """\
# On-call runbook - slow orders (rev 2)

1. Confirm the symptom: place a few orders and read the reported
   `latency_ms` against the recent average in `/metrics`.
2. Check `/admin/workers`. A worker stuck retrying is the usual
   suspect when latency degrades across ALL order categories.
3. Known mitigation for restock retry storms: set `{wrong_key}` to
   `exponential` via `PUT /config`. This backs the worker off and
   lets order latency recover while supply catches up.
4. Verify recovery with fresh orders and `/metrics` before closing
   the incident.
"""


def build(seed: int) -> tuple[dict[str, str], dict]:
    """Return ({relative_path: text}, registration dict)."""
    for attempt in range(64):
        rng = random.Random(f"{seed}:{attempt}")
        out = _try_build(rng)
        if out is not None:
            return out
    raise SystemExit(f"no valid draw within 64 attempts of seed {seed}")


def _try_build(rng: random.Random):
    fault_cat = rng.randrange(len(CATEGORIES))
    con_id, con_name = rng.choice(CONSUMABLES)

    names = rng.sample(ITEM_NAMES, 12)
    items = []
    for name in names:
        items.append({
            "id": "itm-%04d" % rng.randrange(1000, 9900),
            "name": name,
            "cat": rng.randrange(len(CATEGORIES)),
            "stock": rng.randrange(120, 400),
        })
    if len({i["id"] for i in items}) != len(items):
        return None
    # Guarantee the fault category has real order targets.
    for i in items[:3]:
        i["cat"] = fault_cat
    # The related consumable: its own category index is None-like (-1)
    # so no order can ever target the fault path through it.
    rel_stock = rng.randrange(42, 56)
    items.append({"id": "itm-%04d" % rng.randrange(1000, 9900),
                  "name": con_name, "cat": -1, "stock": rel_stock,
                  "consumable": con_id})
    rel_index = len(items) - 1
    if items[rel_index]["id"] in {i["id"] for i in items[:-1]}:
        return None

    threshold = rng.randrange(12, 19)
    metric_key = rng.choice(METRIC_KEYS)
    true_key = rng.choice(TRUE_KEYS)
    wrong_key = rng.choice(WRONG_KEYS)
    if wrong_key == true_key:
        return None

    seed_json = {
        "items": items,
        "categories": CATEGORIES,
        "fault": {"cat": fault_cat, "rel": rel_index,
                  "thr": threshold},
        "metrics": {"retry_key": metric_key},
        "mitigation": {"key": true_key, "value": "exponential"},
        "config": {true_key: "fixed",
                   "order_qty_cap": 3,
                   "metrics_window_ticks": 20},
        "latency": {"base": [35, 70], "degraded_multiplier":
                    rng.choice([6, 7, 8])},
    }

    corpus = {
        "service/srv.py": SRV_PY,
        "service/seed.json": json.dumps(seed_json, indent=1) + "\n",
        "docs/api.md": API_MD,
        "docs/runbook.md": RUNBOOK_TMPL.format(wrong_key=wrong_key),
    }

    reg = {
        "fault_category": CATEGORIES[fault_cat],
        "related_item": items[rel_index]["id"],
        "metric_key": metric_key,
        "true_key": true_key,
        "wrong_key": wrong_key,
        "threshold": threshold,
        "rel_stock": rel_stock,
        "vocab": {
            "metric_keys": [metric_key, "avg_latency_ms_window",
                            "orders_in_window", "window_ticks",
                            "tick"],
            "config_keys": sorted(seed_json["config"]),
            "item_ids": sorted(i["id"] for i in items),
            "categories": CATEGORIES,
        },
    }
    answers = [
        "/orders category=%s" % CATEGORIES[fault_cat],
        items[rel_index]["id"],
        metric_key,
        "%s=exponential" % true_key,
        "runbook says %s, actual %s" % (wrong_key, true_key),
        "",   # line 6 is verified against the agent's own state dump
    ]
    return corpus, {"answers": answers, "reg": reg,
                    "seed_json": seed_json}


# ---------------------------------------------------------------------
# Self-test: import the emitted srv.py and run a full scripted
# diagnosis in-process, asserting the chain, the mitigation, the
# runbook lie, and the depth a diligent diagnosis costs.
# ---------------------------------------------------------------------


def self_test(corpus: dict[str, str], built: dict) -> int:
    reg = built["reg"]
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel, text in corpus.items():
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(text.encode())
        spec = importlib.util.spec_from_file_location(
            "srv_fixture", root / "service" / "srv.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        svc = mod.Service(root / "service" / "seed.json")

        calls = 0

        def call(method, path, body=None):
            nonlocal calls
            calls += 1
            return svc.handle(method, path, body)

        # -- exploration ---------------------------------------------
        for path in ("/health", "/config", "/inventory", "/metrics",
                     "/admin/workers", "/orders"):
            status, _ = call("GET", path)
            assert status == 200, path
        _, cfg = call("GET", "/config")
        assert reg["true_key"] in cfg, "true key not discoverable"
        assert reg["wrong_key"] not in cfg, "runbook key must be wrong"

        # -- baseline: non-fault orders stay in the base band --------
        _, inv = call("GET", "/inventory")
        fault_cat = built["seed_json"]["fault"]["cat"]
        items = built["seed_json"]["items"]
        normal = next(i["id"] for i in items
                      if i["cat"] not in (fault_cat, -1))
        trigger = [i["id"] for i in items if i["cat"] == fault_cat]
        lo, hi = built["seed_json"]["latency"]["base"]
        for _ in range(10):
            status, o = call("POST", "/orders",
                             {"item": normal, "qty": 1})
            assert status == 200 and lo <= o["latency_ms"] <= hi + 1
        _, m = call("GET", "/metrics")
        assert m[reg["metric_key"]] == 0, "retries before repro"

        # -- reproduce: fault-category load drains the related item --
        rel_id = reg["related_item"]
        start_rel = svc.items[rel_id]["stock"]
        degraded_seen = 0
        polls = 0
        while svc.items[rel_id]["stock"] >= reg["threshold"] or \
                degraded_seen < 5:
            for tid in trigger[:3]:
                status, o = call("POST", "/orders",
                                 {"item": tid, "qty": 1})
                assert status == 200
                if o["latency_ms"] > hi * 3:
                    degraded_seen += 1
            call("GET", "/inventory")
            _, m = call("GET", "/metrics")
            call("GET", "/admin/workers")
            polls += 1
            assert polls < 200, "fault chain never manifested"
        assert svc.items[rel_id]["stock"] < start_rel, \
            "related item never drained"

        # -- attribution: non-fault orders must NOT drain the
        # related item (the diligence step that separates "correlated"
        # from "caused", and a few more calls of honest depth)
        rel_before = svc.items[rel_id]["stock"]
        for _ in range(3):
            status, _o = call("POST", "/orders",
                              {"item": normal, "qty": 1})
            assert status == 200
        _, inv2 = call("GET", "/inventory")
        assert inv2[rel_id] == rel_before, \
            "non-fault orders drained the related item"
        _, w = call("GET", "/admin/workers")
        assert w["restock_worker"] == "retrying"
        _, m = call("GET", "/metrics")
        assert m[reg["metric_key"]] > 0, "retry metric silent"

        # -- the runbook lie -----------------------------------------
        status, resp = call("PUT", "/config",
                            {reg["wrong_key"]: "exponential"})
        assert status == 400 and reg["true_key"] in \
            resp.get("valid_keys", []), "wrong key not rejected"

        # -- mitigation + recovery -----------------------------------
        status, _ = call("PUT", "/config",
                         {reg["true_key"]: "exponential"})
        assert status == 200
        recovered = 0
        for _ in range(12):
            status, o = call("POST", "/orders",
                             {"item": normal, "qty": 1})
            assert status == 200
            if o["latency_ms"] <= hi + 1:
                recovered += 1
            call("GET", "/metrics")
        assert recovered >= 10, "latency did not recover"
        _, w = call("GET", "/admin/workers")
        assert w["restock_worker"] == "idle"

        _, state = call("GET", "/admin/state")
        assert state["orders_processed"] == svc.orders_processed

        for rel, text in corpus.items():
            assert len(text.encode()) <= MAX_FILE_BYTES, rel
        assert calls >= MIN_DEPTH, \
            f"diligent diagnosis took only {calls} calls"
        return calls


# ---------------------------------------------------------------------
# Output + --check (repo conventions)
# ---------------------------------------------------------------------


def write_out(out_dir: Path, corpus: dict[str, str], built: dict,
              seed: int, depth: int) -> None:
    for rel, text in sorted(corpus.items()):
        path = out_dir / "seed-files" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
    reg = built["reg"]
    (out_dir / "answers.json").write_bytes(json.dumps({
        "seed": seed,
        "answers": built["answers"],
        "prior_traps": {
            "4": {"corpus": "%s=exponential" % reg["true_key"],
                  "prior": "%s=exponential" % reg["wrong_key"]},
        },
        "vocab": reg["vocab"],
        "registration": {k: reg[k] for k in
                         ("fault_category", "related_item",
                          "metric_key", "true_key", "wrong_key",
                          "threshold")},
        "expected_depth": depth,
    }, indent=2).encode("utf-8") + b"\n")


def _tree(root: Path) -> dict[str, bytes]:
    return {str(p.relative_to(root)): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def run_check(task_dir: Path, seed: int) -> int:
    corpus, built = build(seed)
    depth = self_test(corpus, built)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        write_out(tmp_dir, corpus, built, seed, depth)
        fresh = _tree(tmp_dir)
    committed = {k: v for k, v in _tree(task_dir).items()
                 if k == "answers.json" or k.startswith("seed-files/")}
    problems = []
    for rel in sorted(set(fresh) | set(committed)):
        if rel not in committed:
            problems.append(f"missing from committed corpus: {rel}")
        elif rel not in fresh:
            problems.append(f"stale committed file: {rel}")
        elif fresh[rel] != committed[rel]:
            problems.append(f"byte mismatch: {rel}")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        print(f"check FAILED for seed {seed}", file=sys.stderr)
        return 1
    print(f"check OK: {len(fresh)} files byte-identical for "
          f"seed {seed}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out",
                        default=str(Path(__file__).resolve().parent))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    task_dir = Path(args.out)
    if args.check:
        return run_check(task_dir, args.seed)
    corpus, built = build(args.seed)
    depth = self_test(corpus, built)
    write_out(task_dir, corpus, built, args.seed, depth)
    reg = built["reg"]
    print(f"seed {args.seed}: {len(corpus)} files")
    print(f"  fault: /orders category={reg['fault_category']} "
          f"drains {reg['related_item']} (threshold "
          f"{reg['threshold']})")
    print(f"  metric={reg['metric_key']} true_key={reg['true_key']} "
          f"runbook_key={reg['wrong_key']}")
    print(f"  scripted diligent diagnosis: {depth} service calls")
    print("self-test OK: chain, lie, mitigation and recovery all "
          "re-derived in-process")
    return 0


if __name__ == "__main__":
    sys.exit(main())
