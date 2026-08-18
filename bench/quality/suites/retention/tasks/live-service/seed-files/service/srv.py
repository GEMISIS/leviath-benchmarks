#!/usr/bin/env python3
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
