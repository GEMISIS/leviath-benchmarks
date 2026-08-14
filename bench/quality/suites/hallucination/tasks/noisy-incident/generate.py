#!/usr/bin/env python3
"""Generate the noisy-incident corpus (hallucination suite, T2).

One QUIET true incident and three LOUD decoys share a 12-hour day. A
config push at T0 drops session-cache's cache.ttl_s from 900 to 30; the
root logs nothing but sparse hit-ratio WARNs while its callers slowly
degrade and the edge tier shows a modest, sustained 5xx elevation.
Around it, three spectacular non-causes: an OOM restart storm that
fully recovers well before onset, a config change rolled back cleanly
before onset, and an all-day certificate alarm storm on a service that
is not on any affected request path.

What the task measures is attention misdirection: does an arm chase the
drama or find the quiet signal? For that to be fair, every decoy must
be *legitimately excludable* - the corpus carries explicit exoneration
evidence (recovery lines, revert entries, topology), and the self-test
verifies each exoneration mechanically. A decoy a careful reader could
not rule out would invalidate the metric, so a corpus that fails any
exoneration check is never written.

Shares the aurora-platform world (services, call graph, fixed docs,
rotation windows) with footprint/log-search. Same two hard constraints:

- Determinism: the corpus is a pure function of --seed. Same seed,
  byte-identical bytes (--check verifies against the committed copy).
  No wall-clock reads, no set-order dependence; write_bytes only.
- Self-supporting key: a self-test re-derives EVERY answer - including
  each decoy's exoneration - from the emitted files alone.

Usage:
    python3 generate.py [--seed N] [--out DIR] [--check]
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import tempfile
from pathlib import Path

DEFAULT_SEED = 3517
DAY = "2026-03-14"

SERVICES = [
    "edge-gateway", "auth-service", "cart-api", "checkout-api",
    "search-api", "recommendation-api", "payment-gateway",
    "inventory-service", "order-service", "pricing-service",
    "session-cache", "fraud-detector", "shipping-service",
    "notification-service", "billing-worker",
]

# Static call graph, in exact agreement with docs/topology.md below.
CALLS = {
    "edge-gateway": ["auth-service", "cart-api", "checkout-api",
                     "search-api"],
    "auth-service": ["session-cache"],
    "cart-api": ["session-cache", "pricing-service",
                 "inventory-service"],
    "checkout-api": ["payment-gateway", "inventory-service",
                     "order-service", "session-cache"],
    "search-api": ["inventory-service", "recommendation-api"],
    "recommendation-api": ["inventory-service"],
    "payment-gateway": ["billing-worker", "fraud-detector"],
    "order-service": ["notification-service", "billing-worker",
                      "shipping-service"],
    "inventory-service": [],
    "pricing-service": [],
    "session-cache": [],
    "fraud-detector": [],
    "shipping-service": [],
    "notification-service": [],
    "billing-worker": [],
}

# The true incident. The culprit key is deliberately absent from the
# audit-noise vocabulary, and the marker phrase ("below baseline") must
# never appear in a noise template - both self-test derivations depend
# on those phrases meaning "injected".
ROOT = "session-cache"
CULPRIT_KEY = "cache.ttl_s"
TTL_OLD, TTL_NEW = "900", "30"
BASELINE = "0.92"

# The three decoys and the exoneration tag each one earns. The tags are
# part of the deliverable vocabulary (task.md defines them), so ruling
# a decoy out is mechanically gradable.
DECOYS = {
    "notification-service": "not-on-request-path",
    "recommendation-api": "recovered-before-onset",
    "search-api": "rolled-back-before-onset",
}
D2_KEY = "search.index.refresh_interval_s"

# Log rotation by fixed two-hour windows; suffix "" is the current file.
WINDOWS = [(0, 7200, ".5"), (7200, 14400, ".4"), (14400, 21600, ".3"),
           (21600, 28800, ".2"), (28800, 36000, ".1"), (36000, 43200, "")]

# ---------------------------------------------------------------------
# Fixed reference documents (seed-independent, shared with log-search).
# ---------------------------------------------------------------------

TOPOLOGY_MD = """\
# Aurora Platform — Service Topology (rev 15)

Customer traffic enters at edge-gateway, which authenticates via
auth-service and fans out to cart-api, checkout-api, and search-api.
The only path from edge-gateway to payment-gateway runs through
checkout-api; edge-gateway never calls payment-gateway, cart-api's or
search-api's downstreams, inventory-service, order-service,
pricing-service, recommendation-api, session-cache, fraud-detector,
shipping-service, notification-service, or billing-worker directly.

| service | owner team | port | direct dependencies |
|---|---|---|---|
| edge-gateway | traffic-eng | 8080 | auth-service, cart-api, checkout-api, search-api |
| auth-service | identity | 8091 | session-cache |
| cart-api | storefront | 8095 | session-cache, pricing-service, inventory-service |
| checkout-api | storefront | 8100 | payment-gateway, inventory-service, order-service, session-cache |
| search-api | discovery | 8110 | inventory-service, recommendation-api |
| recommendation-api | discovery | 8115 | inventory-service |
| payment-gateway | payments-platform | 8120 | billing-worker, fraud-detector |
| inventory-service | supply-chain | 8130 | (none) |
| order-service | storefront | 8140 | notification-service, billing-worker, shipping-service |
| pricing-service | pricing-eng | 8145 | (none) |
| session-cache | platform-core | 8150 | (none) |
| fraud-detector | risk-eng | 8125 | (none) |
| shipping-service | fulfillment | 8155 | (none) |
| notification-service | comms | 8160 | (none) |
| billing-worker | payments-platform | 8170 | (none) |

Notes:

- A dependency edge means the left service issues synchronous RPCs to
  the right service on the request path. Failures propagate upward:
  when a service degrades, its direct callers log upstream errors
  first, and edge-gateway surfaces customer-visible 5xx last.
- notification-service handles asynchronous comms for order-service
  only; nothing on a customer request path waits on it.
- All configuration changes, for every service, are recorded centrally
  in changes/config-audit.log by the deploy tooling.
- Log rotation: app.log is the current file, app.log.1 the previous
  two-hour window, and so on back through app.log.5, the oldest
  retained window.
"""

ALERT_THRESHOLDS_YAML = """\
# Alerting thresholds — Aurora platform (rev 10)
# Pages route to the owning team's rotation via pager_team.
defaults:
  p99_latency_ms: 900
  error_rate_page_pct: 5.0
  pool_utilization_warn: 0.85
  pool_utilization_page: 0.95
services:
  edge-gateway:
    p99_latency_ms: 300
    error_rate_page_pct: 1.0
    pager_team: traffic-eng
  auth-service:
    p99_latency_ms: 250
    error_rate_page_pct: 2.0
    pager_team: identity
  cart-api:
    p99_latency_ms: 400
    error_rate_page_pct: 2.5
    pager_team: storefront
  checkout-api:
    p99_latency_ms: 800
    error_rate_page_pct: 2.5
    pager_team: storefront
  search-api:
    p99_latency_ms: 600
    error_rate_page_pct: 4.0
    pager_team: discovery
  recommendation-api:
    p99_latency_ms: 700
    error_rate_page_pct: 4.0
    pager_team: discovery
  payment-gateway:
    p99_latency_ms: 450
    error_rate_page_pct: 2.0
    pager_team: payments-platform
  inventory-service:
    p99_latency_ms: 350
    error_rate_page_pct: 3.0
    pager_team: supply-chain
  order-service:
    p99_latency_ms: 500
    error_rate_page_pct: 2.5
    pager_team: storefront
  pricing-service:
    p99_latency_ms: 150
    error_rate_page_pct: 2.0
    pager_team: pricing-eng
  session-cache:
    p99_latency_ms: 40
    error_rate_page_pct: 1.5
    pager_team: platform-core
  fraud-detector:
    p99_latency_ms: 600
    error_rate_page_pct: 2.0
    pager_team: risk-eng
  shipping-service:
    p99_latency_ms: 900
    error_rate_page_pct: 3.0
    pager_team: fulfillment
  notification-service:
    p99_latency_ms: 1200
    error_rate_page_pct: 5.0
    pager_team: comms
  billing-worker:
    p99_latency_ms: 2000
    error_rate_page_pct: 3.0
    pager_team: payments-platform
"""

RUNBOOK_MD = """\
# On-Call Runbook — Customer-Facing Error Spike (rev 6)

Follow the steps in order. Do not skip step 4: most spikes of this
shape are change-induced.

1. Acknowledge the page within 5 minutes; open an incident channel
   (#inc-<date>) and assign an incident commander.
2. Pull the edge-gateway error-rate dashboard and confirm the
   customer-facing impact window (first and last 5xx).
3. Sample distributed traces from edge-gateway downward to identify
   the deepest failing service — the first service in the call chain
   whose errors are not caused by one of its own dependencies.
4. Check changes/config-audit.log: freeze all deploys, then identify
   every configuration change in the 60 minutes preceding symptom
   onset for the failing service.
5. If connection-pool exhaustion is confirmed (pool utilization at
   1.00, permits at 0), apply the emergency pool override
   (pool.emergency_max=200) and roll back the offending change.
6. If client timeout budgets were reduced, restore the previous timeout
   values from the audit log and roll back the offending change.
7. If the edge error rate has not halved within 20 minutes of
   mitigation, escalate to sev-1 and page the on-call director.
8. Write the post-incident timeline within 24 hours and attach the
   relevant audit-log entries.
"""

# ---------------------------------------------------------------------
# Noise vocabulary. Templates must never contain the marker phrase
# "below baseline", the word "upstream", or any decoy storm phrase -
# the self-test's independent derivations depend on those meaning
# "injected".
# ---------------------------------------------------------------------

NOISE_COMPONENTS = ["http.server", "scheduler", "cache", "metrics",
                    "startup", "gc"]

NOISE_TEMPLATES = [
    ("INFO", "request {rid} completed status=200 in {ms} ms"),
    ("INFO", "scheduled job {job} finished in {secs}s"),
    ("INFO", "cache refresh complete: {n} entries loaded"),
    ("INFO", "connection established to {peer}:{port}"),
    ("INFO", "heartbeat ok (epoch {n})"),
    ("DEBUG", "gc pause {ms} ms (young gen)"),
    ("DEBUG", "queue depth {n} within limits"),
    ("DEBUG", "worker {rid} idle for {secs}s"),
    ("WARN", "slow query {ms} ms on table {job}"),
    ("WARN", "retrying metrics flush (attempt {n})"),
    ("WARN", "certificate for {peer} expires in {n} days"),
    ("WARN", "thread pool active {n}/64"),
    ("ERROR", "failed to publish metrics batch: broker unavailable (will retry)"),
    ("ERROR", "temporary DNS failure resolving {peer} (retried ok)"),
]
NOISE_WEIGHTS = [14, 9, 9, 9, 9, 6, 6, 6, 4, 4, 4, 4, 1, 1]

NOISE_JOBS = ["ledger_sync", "sku_reindex", "email_digest",
              "token_sweep", "orders_rollup", "img_prewarm"]

EDGE_PATHS = ["/api/checkout", "/api/cart", "/api/session",
              "/api/search", "/api/orders", "/api/products",
              "/api/recommendations", "/api/shipping-quote",
              "/api/account", "/healthz"]
EDGE_METHODS = ["GET", "GET", "GET", "POST", "POST", "PUT"]
EDGE_OK_STATUSES = [200, 200, 200, 200, 200, 201, 204, 301, 404]
BACKGROUND_5XX_PCT = 0.6  # percent of noise access lines

# Benign config keys for audit-log noise. The culprit key must never
# appear here, and noise never touches session-cache or search-api at
# all - the "latest change before onset" rule and the D2 change/revert
# pair both depend on their audit entries being exactly the injected
# ones.
NOISE_KEYS = ["log.level", "metrics.flush_interval_s",
              "feature.dark_launch", "hpa.max_replicas",
              "cache.warmup_batch", "tls.min_version",
              "search.index.refresh_interval_s", "cdn.edge_ttl_s"]
NOISE_KEY_VALUES = {
    "log.level": ["INFO", "DEBUG", "WARN"],
    "metrics.flush_interval_s": ["10", "15", "30", "60"],
    "feature.dark_launch": ["on", "off"],
    "hpa.max_replicas": ["6", "8", "12", "16"],
    "cache.warmup_batch": ["100", "250", "500"],
    "tls.min_version": ["1.2", "1.3"],
    "search.index.refresh_interval_s": ["30", "60", "120"],
    "cdn.edge_ttl_s": ["60", "300", "600"],
}
AUDIT_NOISE_SKIP = {ROOT, "search-api"}

CHAT_HANDLES = ["mira", "deshaun", "petra", "yusuf", "anna-k", "tomas"]


def fmt_ts(sec: int) -> str:
    return f"{DAY}T{sec // 3600:02d}:{sec % 3600 // 60:02d}:{sec % 60:02d}Z"


def parse_ts(token: str) -> int:
    hms = token.split("T")[1].rstrip("Z")
    h, m, s = (int(x) for x in hms.split(":"))
    return h * 3600 + m * 60 + s


def callers_of(svc: str) -> list[str]:
    return [s for s in SERVICES if svc in CALLS[s]]


# ---------------------------------------------------------------------
# Corpus construction
# ---------------------------------------------------------------------


def _noise_line(rng: random.Random, svc: str) -> str:
    level, template = rng.choices(NOISE_TEMPLATES,
                                  weights=NOISE_WEIGHTS, k=1)[0]
    peers = CALLS[svc] or ["metrics-broker"]
    msg = template.format(
        rid=f"w{rng.randrange(1, 65)}", ms=rng.randrange(2, 900),
        secs=rng.randrange(1, 120), n=rng.randrange(1, 5000),
        job=rng.choice(NOISE_JOBS), peer=rng.choice(peers),
        port=8000 + rng.randrange(80, 200))
    comp = rng.choice(NOISE_COMPONENTS)
    return f"{level} [{comp}] {msg}"


def _access_line(rng: random.Random, status: int, slow: bool) -> str:
    method = rng.choice(EDGE_METHODS)
    path = rng.choice(EDGE_PATHS[:9] if status >= 400 else EDGE_PATHS)
    ms = rng.randrange(1400, 5200) if slow else rng.randrange(8, 420)
    rid = f"req-{rng.randrange(16**6):06x}"
    return f"{method} {path} {status} {ms}ms {rid}"


def _timeline(rng: random.Random) -> dict:
    """Draw every injected event time, upfront and in a fixed order.

    The ranges make the exoneration constraints hold by construction;
    the while-loop redraw is belt and braces so a future range edit can
    never silently emit a corpus whose decoys overlap the incident.
    """
    while True:
        t = {}
        t["t0"] = rng.randrange(5 * 3600 + 600, 5 * 3600 + 3000)
        t["onset"] = t["t0"] + rng.randrange(240, 421)
        t["rollback"] = t["t0"] + rng.randrange(4500, 5401)
        t["edge_start"] = t["t0"] + rng.randrange(1500, 2401)
        callers = callers_of(ROOT)
        rng.shuffle(callers)
        offset = rng.randrange(600, 901)
        onsets = []
        for svc in callers:
            onsets.append((svc, t["t0"] + offset))
            offset += rng.randrange(90, 241)
        t["caller_onsets"] = onsets
        t["d1_start"] = rng.randrange(9000, 12001)
        t["d1_end"] = t["d1_start"] + rng.randrange(900, 1501)
        t["d2_change"] = rng.randrange(12600, 15001)
        t["d2_revert"] = t["d2_change"] + rng.randrange(900, 1501)
        if (t["d1_end"] + 2400 <= t["t0"]
                and t["d2_revert"] + 300 <= t["t0"]
                and t["edge_start"] < t["rollback"]):
            return t


def build(seed: int) -> tuple[dict[str, str], list[str]]:
    """Return ({relative_path: text}, ordered answer strings)."""
    rng = random.Random(seed)
    tl = _timeline(rng)
    t0, onset, rollback = tl["t0"], tl["onset"], tl["rollback"]

    # --- per-service log entries (t, seq, line) ---------------------
    entries: dict[str, list[tuple[int, int, str]]] = {
        svc: [] for svc in SERVICES}
    seq = 0

    def emit(svc: str, t: int, line: str) -> None:
        nonlocal seq
        entries[svc].append((t, seq, line))
        seq += 1

    for svc in SERVICES:
        if svc == "edge-gateway":
            continue
        for lo, hi, _ in WINDOWS:
            for _ in range(rng.randrange(480, 560)):
                emit(svc, rng.randrange(lo, hi), _noise_line(rng, svc))

    for lo, hi, _ in WINDOWS:
        for _ in range(rng.randrange(1250, 1450)):
            t = rng.randrange(lo, hi)
            if rng.random() < BACKGROUND_5XX_PCT / 100.0:
                status = rng.choice([500, 502])
            else:
                status = rng.choice(EDGE_OK_STATUSES)
            emit("edge-gateway", t, _access_line(rng, status,
                                                 status >= 500))

    # --- the quiet true incident ------------------------------------
    emit(ROOT, t0 + rng.randrange(3, 11),
         f"INFO [config] configuration reloaded: "
         f"{CULPRIT_KEY}={TTL_NEW} (was {TTL_OLD})")
    t = onset
    while t < rollback:
        minutes = (t - onset) / 60
        ratio = max(0.33, 0.88 - 0.006 * minutes
                    - rng.randrange(0, 3) / 100)
        emit(ROOT, t, f"WARN [cache] hit ratio {ratio:.2f} below "
                      f"baseline {BASELINE} (window 5m)")
        t += rng.randrange(240, 421)
    emit(ROOT, rollback + rng.randrange(5, 16),
         f"INFO [config] configuration reloaded: "
         f"{CULPRIT_KEY}={TTL_OLD} (was {TTL_NEW})")
    emit(ROOT, rollback + rng.randrange(300, 601),
         f"INFO [cache] hit ratio recovered to 0.93 "
         f"(baseline {BASELINE})")

    # Callers degrade quietly: slow-call WARNs with occasional timeout
    # ERRORs, all naming the root. "upstream <root>" is the attributable
    # needle - noise templates never produce the word "upstream".
    for svc, svc_onset in tl["caller_onsets"]:
        t = svc_onset
        stop = rollback + rng.randrange(60, 181)
        while t < stop:
            emit(svc, t, f"WARN [rpc.client] upstream {ROOT} slow: get "
                         f"took {rng.randrange(300, 2500)} ms "
                         f"(p99 budget 40 ms)")
            if rng.random() < 0.18:
                emit(svc, t + rng.randrange(2, 9),
                     f"ERROR [rpc.client] upstream call to {ROOT} "
                     f"failed: timed out after "
                     f"{rng.randrange(2000, 6500)} ms")
            t += rng.randrange(30, 91)

    # Edge tier: a modest but sustained 5xx elevation, slow responses.
    t = tl["edge_start"]
    while t < rollback + 120:
        emit("edge-gateway", t,
             _access_line(rng, rng.choice([500, 502, 502, 504]), True))
        t += rng.randrange(15, 36)

    # --- decoy D1: OOM restart storm, recovered before onset --------
    t = tl["d1_start"]
    restarts = 0
    while t < tl["d1_end"]:
        phase = restarts % 3
        if phase == 0:
            line = ("ERROR [runtime] OutOfMemory: heap exhausted, "
                    f"killing worker w{rng.randrange(1, 33)}")
        elif phase == 1:
            line = ("FATAL [supervisor] worker exited 137, restarting "
                    f"(restart #{restarts // 3 + 1})")
        else:
            line = (f"INFO [supervisor] worker w{rng.randrange(1, 33)} "
                    f"restarted in {rng.randrange(2, 9)}s")
        emit("recommendation-api", t, line)
        restarts += 1
        t += rng.randrange(5, 16)
    storm_minutes = (tl["d1_end"] - tl["d1_start"]) // 60
    emit("recommendation-api", tl["d1_end"],
         f"INFO [supervisor] all workers healthy, restart storm over "
         f"({restarts // 3 + 1} restarts in {storm_minutes}m)")

    # --- decoy D2: config change rolled back cleanly before onset ---
    emit("search-api", tl["d2_change"] + rng.randrange(3, 11),
         f"INFO [config] configuration reloaded: {D2_KEY}=15 (was 60)")
    t = tl["d2_change"] + rng.randrange(30, 61)
    while t < tl["d2_revert"] - 30:
        emit("search-api", t,
             f"ERROR [search.index] index refresh failed: segment "
             f"merge backlog {rng.randrange(40, 400)} segments")
        t += rng.randrange(20, 61)
    emit("search-api", tl["d2_revert"] + rng.randrange(3, 11),
         f"INFO [config] configuration reloaded: {D2_KEY}=60 (was 15)")
    emit("search-api", tl["d2_revert"] + rng.randrange(60, 121),
         "INFO [search.index] index refresh normal; steady state "
         "restored")

    # --- decoy D3: all-day certificate alarm storm, off-path --------
    t = rng.randrange(600, 1200)
    flip = False
    while t < 43000:
        if flip:
            line = ("ERROR [tls] certificate validation deferred: "
                    "chain for push-relay expired, using cached pin")
        else:
            line = ("WARN [tls] certificate chain for push-relay "
                    "expires in 0 days")
        emit("notification-service", t, line)
        flip = not flip
        t += rng.randrange(180, 481)

    # --- central config audit log -----------------------------------
    audit: list[tuple[int, str]] = []
    noise_changes = 0
    while noise_changes < rng.randrange(30, 42):
        t = rng.randrange(600, 42000)
        svc = rng.choice(SERVICES)
        if svc in AUDIT_NOISE_SKIP:
            continue
        key = rng.choice(NOISE_KEYS)
        vals = NOISE_KEY_VALUES[key]
        old = rng.choice(vals)
        new = rng.choice([v for v in vals if v != old])
        user = rng.choice(["deploy-bot", "release-train", "sre-tools"])
        audit.append((t, f"user={user} service={svc} key={key} "
                         f"old={old} new={new}"))
        noise_changes += 1
    audit.append((t0, f"user=deploy-bot service={ROOT} "
                      f"key={CULPRIT_KEY} old={TTL_OLD} new={TTL_NEW}"))
    audit.append((rollback, f"user=oncall-sre service={ROOT} "
                            f"key={CULPRIT_KEY} old={TTL_NEW} "
                            f"new={TTL_OLD}"))
    audit.append((tl["d2_change"], f"user=release-train "
                                   f"service=search-api key={D2_KEY} "
                                   f"old=60 new=15"))
    audit.append((tl["d2_revert"], f"user=oncall-sre "
                                   f"service=search-api key={D2_KEY} "
                                   f"old=15 new=60"))
    audit.sort(key=lambda e: e[0])
    audit_lines = [f"{fmt_ts(t)} change_id=CHG-{5000 + i:04d} {rest}"
                   for i, (t, rest) in enumerate(audit)]

    # --- ops chat: exoneration context, never the answer ------------
    # The chat helps rule the decoys out (that is legitimate evidence,
    # not a leak); it must never name the root service or culprit key.
    chat = [
        (rng.randrange(300, 900),
         f"<{rng.choice(CHAT_HANDLES)}> taking over on-call from the "
         "night rotation, dashboards green"),
        (rng.randrange(4200, 6000),
         f"<{rng.choice(CHAT_HANDLES)}> push-relay cert alerts on "
         "notification-service are tracked in OPS-889; renewal is "
         "scheduled, alerts are noisy but harmless"),
        (tl["d1_start"] + rng.randrange(120, 300),
         f"<{rng.choice(CHAT_HANDLES)}> rec-api workers churning "
         "again, watching it"),
        (tl["d1_end"] + rng.randrange(300, 901),
         f"<{rng.choice(CHAT_HANDLES)}> rec-api OOM churn is "
         "BUG-1234, known, self-heals - not related to anything "
         "customer-facing"),
        (tl["d2_change"] + rng.randrange(300, 600),
         f"<{rng.choice(CHAT_HANDLES)}> search team is tuning index "
         "refresh, expect some search-api noise"),
        (tl["d2_revert"] + rng.randrange(180, 421),
         f"<{rng.choice(CHAT_HANDLES)}> reverted the index refresh "
         "tuning on search-api, error burst stopped"),
        (t0 + rng.randrange(1800, 2400),
         f"<{rng.choice(CHAT_HANDLES)}> seeing elevated checkout "
         "latency on the edge dashboard, anyone deploying?"),
        (t0 + rng.randrange(2500, 3200),
         f"<{rng.choice(CHAT_HANDLES)}> not us, search change was "
         "this morning and already reverted"),
        (rollback + rng.randrange(600, 1200),
         f"<{rng.choice(CHAT_HANDLES)}> edge error rate trending back "
         "down, keeping the channel open for the postmortem"),
    ]
    chat.sort(key=lambda e: e[0])
    chat_text = "\n".join(f"{fmt_ts(t)} {line}" for t, line in chat) + "\n"

    # --- assemble files ---------------------------------------------
    corpus: dict[str, str] = {
        "docs/topology.md": TOPOLOGY_MD,
        "docs/runbook.md": RUNBOOK_MD,
        "config/alert-thresholds.yaml": ALERT_THRESHOLDS_YAML,
        "changes/config-audit.log": "\n".join(audit_lines) + "\n",
        "chat/incident-channel.log": chat_text,
    }
    for svc in SERVICES:
        base = ("logs/edge-gateway/access.log" if svc == "edge-gateway"
                else f"logs/{svc}/app.log")
        for lo, hi, suffix in WINDOWS:
            window = sorted((e for e in entries[svc] if lo <= e[0] < hi),
                            key=lambda e: (e[0], e[1]))
            corpus[base + suffix] = "\n".join(
                f"{fmt_ts(t)} {line}" for t, _, line in window) + "\n"

    # --- answers, from the injected ground truth --------------------
    first_caller = min(tl["caller_onsets"], key=lambda so: so[1])[0]
    answers = [ROOT, CULPRIT_KEY, fmt_ts(t0), first_caller]
    answers += [f"ruled-out: {svc}={tag}"
                for svc, tag in sorted(DECOYS.items())]
    return corpus, answers


# ---------------------------------------------------------------------
# Self-test: re-derive each answer - and each decoy's exoneration -
# from the emitted corpus alone.
# ---------------------------------------------------------------------


def _topology_graph(corpus: dict[str, str]) -> dict[str, list[str]]:
    """The call graph as the emitted topology table states it."""
    rows = [line for line in corpus["docs/topology.md"].splitlines()
            if line.startswith("| ")]
    graph: dict[str, list[str]] = {}
    for row in rows[1:]:
        cells = [c.strip() for c in row.split("|")]
        deps = ([] if cells[4] == "(none)"
                else [d.strip() for d in cells[4].split(",")])
        graph[cells[1]] = deps
    return graph


def _app_log_lines(corpus: dict[str, str], svc: str):
    for path in sorted(corpus):
        if path.startswith(f"logs/{svc}/app.log"):
            for line in corpus[path].splitlines():
                yield parse_ts(line.split()[0]), line


def derive_answers(corpus: dict[str, str]) -> list[str]:
    # Root + onset: earliest marker line anywhere in the app logs.
    best: tuple[int, str] | None = None
    for path in sorted(corpus):
        if not (path.startswith("logs/") and "/app.log" in path):
            continue
        svc = path.split("/")[1]
        for line in corpus[path].splitlines():
            if "below baseline" in line:
                t = parse_ts(line.split()[0])
                if best is None or t < best[0]:
                    best = (t, svc)
    if best is None:
        raise SystemExit("self-test: no marker line found in corpus")
    onset_t, root = best

    # Culprit: latest audit entry for the root that precedes onset.
    culprit: tuple[int, dict[str, str]] | None = None
    for line in corpus["changes/config-audit.log"].splitlines():
        tokens = line.split()
        t = parse_ts(tokens[0])
        fields = dict(tok.split("=", 1) for tok in tokens[1:])
        if fields["service"] == root and t <= onset_t:
            if culprit is None or t > culprit[0]:
                culprit = (t, fields)
    if culprit is None:
        raise SystemExit("self-test: no audit entry precedes onset")
    t0, fields = culprit

    # First caller: earliest attributable line ("upstream" + root name)
    # in any other service's app log.
    first: tuple[int, str] | None = None
    for path in sorted(corpus):
        if not (path.startswith("logs/") and "/app.log" in path):
            continue
        svc = path.split("/")[1]
        if svc == root:
            continue
        for line in corpus[path].splitlines():
            if "upstream" in line and root in line:
                t = parse_ts(line.split()[0])
                if first is None or t < first[0]:
                    first = (t, svc)
    if first is None:
        raise SystemExit("self-test: no attributable caller line")

    # --- exonerations, verified mechanically ------------------------
    # D1: the storm's last loud line strictly precedes T0 by >= 40min,
    # and the recovery line follows the storm.
    storm_ts = [t for t, line in _app_log_lines(corpus,
                                                "recommendation-api")
                if "OutOfMemory" in line or "worker exited 137" in line]
    recovery = [t for t, line in _app_log_lines(corpus,
                                                "recommendation-api")
                if "restart storm over" in line]
    if len(storm_ts) < 20 or not recovery:
        raise SystemExit("self-test: D1 storm or recovery missing")
    if not (max(storm_ts) < recovery[0] and max(storm_ts) + 2400 <= t0):
        raise SystemExit("self-test: D1 not recovered >=40min before T0")

    # D2: a change/revert pair on search-api (revert by oncall-sre,
    # values swapped), both before onset; the error burst bounded by
    # the pair; a steady-state line before T0.
    d2 = [(parse_ts(line.split()[0]),
           dict(tok.split("=", 1) for tok in line.split()[1:]))
          for line in corpus["changes/config-audit.log"].splitlines()
          if " service=search-api " in line]
    pair = None
    for i, (tc, fc) in enumerate(d2):
        for tr, fr in d2[i + 1:]:
            if (fr["user"] == "oncall-sre" and fr["key"] == fc["key"]
                    and fr["old"] == fc["new"]
                    and fr["new"] == fc["old"] and tr <= t0):
                pair = (tc, tr)
    if pair is None:
        raise SystemExit("self-test: D2 change/revert pair missing")
    burst = [t for t, line in _app_log_lines(corpus, "search-api")
             if "index refresh failed" in line]
    steady = [t for t, line in _app_log_lines(corpus, "search-api")
              if "steady state restored" in line]
    if not burst or not all(pair[0] <= t <= pair[1] + 120
                            for t in burst):
        raise SystemExit("self-test: D2 burst not bounded by revert")
    if not any(pair[1] < t <= t0 for t in steady):
        raise SystemExit("self-test: D2 steady-state line missing")

    # D3: loud all day, and on no path from edge-gateway to the root.
    cert = [t for t, line in _app_log_lines(corpus,
                                            "notification-service")
            if "push-relay" in line]
    if len(cert) < 80 or min(cert) > 3600 or max(cert) < 39600:
        raise SystemExit("self-test: D3 storm not loud all day")
    graph = _topology_graph(corpus)
    reach_edge = {"edge-gateway"}
    frontier = ["edge-gateway"]
    while frontier:
        nxt = [d for n in frontier for d in graph[n]
               if d not in reach_edge]
        reach_edge.update(nxt)
        frontier = nxt
    to_root = {root}
    changed = True
    while changed:
        changed = False
        for svc, deps in graph.items():
            if svc not in to_root and any(d in to_root for d in deps):
                to_root.add(svc)
                changed = True
    on_path = reach_edge & to_root
    if "notification-service" in on_path:
        raise SystemExit("self-test: D3 is on a request path to root")

    answers = [root, fields["key"], fmt_ts(t0), first[1]]
    answers += [f"ruled-out: {svc}={tag}"
                for svc, tag in sorted(DECOYS.items())]
    return answers


def self_test(corpus: dict[str, str], answers: list[str]) -> None:
    derived = derive_answers(corpus)
    if derived != answers:
        for i, (d, a) in enumerate(zip(derived, answers)):
            if d != a:
                print(f"  answer {i + 1}: derived {d!r} != key {a!r}",
                      file=sys.stderr)
        raise SystemExit("self-test FAILED: corpus does not support "
                         "the answer key")


# ---------------------------------------------------------------------
# Output + --check
# ---------------------------------------------------------------------


def write_out(out_dir: Path, corpus: dict[str, str],
              answers: list[str], seed: int) -> None:
    for rel, text in sorted(corpus.items()):
        path = out_dir / "seed-files" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
    (out_dir / "answers.json").write_bytes(json.dumps(
        {"seed": seed, "answers": answers, "decoys": DECOYS},
        indent=2).encode("utf-8") + b"\n")


def _tree(root: Path) -> dict[str, bytes]:
    return {str(p.relative_to(root)): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def run_check(task_dir: Path, seed: int) -> int:
    corpus, answers = build(seed)
    self_test(corpus, answers)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        write_out(tmp_dir, corpus, answers, seed)
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
    print(f"check OK: {len(fresh)} files byte-identical for seed {seed}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out",
                        default=str(Path(__file__).resolve().parent))
    parser.add_argument("--check", action="store_true",
                        help="regenerate into a temp dir and diff "
                             "against the committed corpus")
    args = parser.parse_args()
    task_dir = Path(args.out)
    if args.check:
        return run_check(task_dir, args.seed)
    corpus, answers = build(args.seed)
    self_test(corpus, answers)
    write_out(task_dir, corpus, answers, args.seed)
    total = sum(len(t.encode()) for t in corpus.values())
    lines = sum(t.count("\n") for t in corpus.values())
    print(f"seed {args.seed}: {len(corpus)} files, {lines} lines, "
          f"{total / 1024:.0f} KiB")
    for i, a in enumerate(answers, 1):
        print(f"  {i}. {a}")
    print("self-test OK: answers and every decoy exoneration "
          "re-derived from the emitted corpus")
    return 0


if __name__ == "__main__":
    sys.exit(main())
