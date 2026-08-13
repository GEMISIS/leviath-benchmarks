#!/usr/bin/env python3
"""Generate the incident-forensics corpus.

A multi-service production incident on 2026-03-14: a config push at T0
degrades one service, the failure cascades to that service's callers,
and the edge tier surfaces 5xx to customers. The generator buries the
causal chain in seeded background noise and computes the answer key
from what it injected; a self-test then re-derives every answer from
the emitted files alone, so the corpus provably supports the key.

Two hard constraints shape this file:

- Determinism: the corpus is a pure function of --seed. Same seed,
  byte-identical bytes (--check verifies against the committed copy).
  No wall-clock reads, no filesystem-order or set-order dependence;
  files are written with write_bytes so platform newline translation
  can never leak in.
- Stable reference docs: docs/topology.md, docs/runbook.md and
  config/alert-thresholds.yaml are constants, independent of the seed.
  probes.json quotes facts from them, so they must never vary; only
  the injected incident and the noise around it do.

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

DEFAULT_SEED = 1134
DAY = "2026-03-14"

SERVICES = [
    "edge-gateway", "auth-service", "checkout-api", "search-api",
    "payment-gateway", "inventory-service", "order-service",
    "session-cache", "notification-service", "billing-worker",
]

# Static call graph. Kept in exact agreement with docs/topology.md
# below; the cascade (who logs upstream failures when the root-cause
# service degrades) is derived from this map, never hand-listed.
CALLS = {
    "edge-gateway": ["auth-service", "checkout-api", "search-api"],
    "auth-service": ["session-cache"],
    "checkout-api": ["payment-gateway", "inventory-service",
                     "order-service", "session-cache"],
    "search-api": ["inventory-service"],
    "payment-gateway": ["billing-worker"],
    "order-service": ["notification-service", "billing-worker"],
    "inventory-service": [],
    "session-cache": [],
    "notification-service": [],
    "billing-worker": [],
}

# Failure modes the seed chooses between. "roots" lists services whose
# role makes the mode plausible (a timeout-budget cut only bites a
# service that calls someone). "marker" is the phrase the self-test
# uses to find symptom onset independently of the injection bookkeeping;
# noise templates must never contain it. "mitigation" is the phrase
# that locates the containment step inside the (fixed) runbook.
MODES = {
    "pool": {
        "key": "db.pool.max_connections", "old": "120", "new": "15",
        "roots": ["payment-gateway", "inventory-service",
                  "order-service", "session-cache"],
        "marker": "connection pool exhausted",
        "mitigation": "emergency pool override",
    },
    "timeout": {
        "key": "http.client.timeout_ms", "old": "2500", "new": "250",
        "roots": ["payment-gateway", "order-service"],
        "marker": "client timeout budget",
        "mitigation": "restore the previous timeout",
    },
}

# Log rotation is by fixed two-hour windows; suffix "" is the current
# file. T0 is always drawn from 02:10-03:20 so the incident lives in
# the .1 file - an agent that only reads the current file misses it.
WINDOWS = [(0, 7200, ".2"), (7200, 14400, ".1"), (14400, 21600, "")]

IMPACT_WINDOW_SECS = 900

# ---------------------------------------------------------------------
# Fixed reference documents (seed-independent; see module docstring).
# ---------------------------------------------------------------------

TOPOLOGY_MD = """\
# Aurora Platform — Service Topology (rev 14)

Customer traffic enters at edge-gateway, which authenticates via
auth-service and fans out to checkout-api and search-api. The only
path from edge-gateway to payment-gateway runs through checkout-api;
edge-gateway never calls payment-gateway, inventory-service,
order-service, session-cache, notification-service, or billing-worker
directly.

| service | owner team | port | direct dependencies |
|---|---|---|---|
| edge-gateway | traffic-eng | 8080 | auth-service, checkout-api, search-api |
| auth-service | identity | 8091 | session-cache |
| checkout-api | storefront | 8100 | payment-gateway, inventory-service, order-service, session-cache |
| search-api | discovery | 8110 | inventory-service |
| payment-gateway | payments-platform | 8120 | billing-worker |
| inventory-service | supply-chain | 8130 | (none) |
| order-service | storefront | 8140 | notification-service, billing-worker |
| session-cache | platform-core | 8150 | (none) |
| notification-service | comms | 8160 | (none) |
| billing-worker | payments-platform | 8170 | (none) |

Notes:

- A dependency edge means the left service issues synchronous RPCs to
  the right service on the request path. Failures propagate upward:
  when a service degrades, its direct callers log upstream errors
  first, and edge-gateway surfaces customer-visible 5xx last.
- All configuration changes, for every service, are recorded centrally
  in changes/config-audit.log by the deploy tooling.
- Log rotation: app.log is the current file, app.log.1 the previous
  two-hour window, app.log.2 the one before that.
"""

ALERT_THRESHOLDS_YAML = """\
# Alerting thresholds — Aurora platform (rev 9)
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
  checkout-api:
    p99_latency_ms: 800
    error_rate_page_pct: 2.5
    pager_team: storefront
  search-api:
    p99_latency_ms: 600
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
  session-cache:
    p99_latency_ms: 40
    error_rate_page_pct: 1.5
    pager_team: platform-core
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
# Noise vocabulary. Templates must never contain a mode marker or the
# cascade phrase "upstream call to" - the self-test's independent
# derivation depends on those phrases meaning "injected incident".
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
NOISE_WEIGHTS = [14, 9, 9, 9, 9, 6, 6, 6, 4, 4, 4, 4, 2, 2]

NOISE_JOBS = ["ledger_sync", "sku_reindex", "email_digest",
              "token_sweep", "orders_rollup", "img_prewarm"]

EDGE_PATHS = ["/api/checkout", "/api/cart", "/api/session",
              "/api/search", "/api/orders", "/api/products",
              "/api/account", "/healthz"]
EDGE_METHODS = ["GET", "GET", "GET", "POST", "POST", "PUT"]
EDGE_OK_STATUSES = [200, 200, 200, 200, 200, 201, 204, 301, 404]
BACKGROUND_5XX_PCT = 0.6  # percent of noise access lines

# Benign config keys for audit-log noise. Neither mode key may ever
# appear here: the culprit entry must be the only change of its key.
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
    path = rng.choice(EDGE_PATHS[:7] if status >= 400 else EDGE_PATHS)
    ms = rng.randrange(1400, 5200) if slow else rng.randrange(8, 420)
    rid = f"req-{rng.randrange(16**6):06x}"
    return f"{method} {path} {status} {ms}ms {rid}"


def build(seed: int) -> tuple[dict[str, str], list[str]]:
    """Return ({relative_path: text}, ordered answer strings)."""
    rng = random.Random(seed)

    # --- pick the incident ------------------------------------------
    mode_name = rng.choice(sorted(MODES))
    mode = MODES[mode_name]
    root = rng.choice(mode["roots"])
    t0 = rng.randrange(2 * 3600 + 600, 3 * 3600 + 1200)
    onset = t0 + rng.randrange(20, 61)

    caller_order = callers_of(root)
    rng.shuffle(caller_order)
    caller_onsets = []
    cur = onset
    for svc in caller_order:
        cur += rng.randrange(25, 71)
        caller_onsets.append((svc, cur))
    edge_start = cur + rng.randrange(30, 91)
    rollback_t = t0 + 1800
    end = rollback_t + rng.randrange(20, 61)

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
            for _ in range(rng.randrange(66, 90)):
                emit(svc, rng.randrange(lo, hi), _noise_line(rng, svc))

    # Edge access-log noise, with a low background 5xx rate that the
    # impact count deliberately includes - the answer is "5xx in the
    # window", not "5xx we injected", and both derivations count the
    # same emitted lines.
    for lo, hi, _ in WINDOWS:
        for _ in range(rng.randrange(240, 300)):
            t = rng.randrange(lo, hi)
            if rng.random() < BACKGROUND_5XX_PCT / 100.0:
                status = rng.choice([500, 502])
            else:
                status = rng.choice(EDGE_OK_STATUSES)
            emit("edge-gateway", t, _access_line(rng, status,
                                                 status >= 500))

    # --- the injected chain -----------------------------------------
    emit(root, t0 + rng.randrange(3, 11),
         f"INFO [config] configuration reloaded: "
         f"{mode['key']}={mode['new']} (was {mode['old']})")

    t = onset
    while t < end:
        if mode_name == "pool":
            msg = (f"connection pool exhausted: 0 of {mode['new']} "
                   f"permits available, queue depth "
                   f"{rng.randrange(40, 400)}, request waited "
                   f"{rng.randrange(3000, 9000)} ms then failed")
            comp = "db.pool"
        else:
            callee = rng.choice(CALLS[root])
            msg = (f"request aborted: client timeout budget "
                   f"{mode['new']} ms exceeded contacting {callee} "
                   f"(attempt {rng.randrange(1, 4)})")
            comp = "http.client"
        emit(root, t, f"ERROR [{comp}] {msg}")
        if rng.random() < 0.12:
            emit(root, t + 1, "WARN [db.pool] pool utilization 1.00 "
                              "(page threshold 0.95)")
        t += rng.randrange(8, 21)

    for svc, svc_onset in caller_onsets:
        t = svc_onset
        first = True
        while t < end:
            emit(svc, t,
                 f"ERROR [rpc.client] upstream call to {root} failed: "
                 f"timed out after {rng.randrange(2000, 6500)} ms")
            if first and rng.random() < 0.8:
                emit(svc, t + rng.randrange(20, 60),
                     f"WARN [rpc.client] circuit breaker for {root} "
                     f"transitioned to OPEN")
            first = False
            t += rng.randrange(10, 26)

    t = edge_start
    while t < end:
        emit("edge-gateway", t,
             _access_line(rng, rng.choice([502, 502, 504, 500]), True))
        t += rng.randrange(3, 9)

    emit(root, rollback_t + rng.randrange(5, 16),
         f"INFO [config] configuration reloaded: "
         f"{mode['key']}={mode['old']} (was {mode['new']})")
    emit(root, end + rng.randrange(30, 90),
         "INFO [http.server] error rate back below threshold; "
         "steady state restored")

    # --- central config audit log -----------------------------------
    audit: list[tuple[int, str]] = []
    noise_changes = 0
    while noise_changes < rng.randrange(10, 15):
        t = rng.randrange(600, 20400)
        svc = rng.choice(SERVICES)
        # Nothing near the culprit for the root service: the audit
        # answer is "latest change to the root service before onset",
        # and that must be the injected push under any seed.
        if svc == root and abs(t - t0) < 3600:
            continue
        key = rng.choice(NOISE_KEYS)
        vals = NOISE_KEY_VALUES[key]
        old = rng.choice(vals)
        new = rng.choice([v for v in vals if v != old])
        user = rng.choice(["deploy-bot", "release-train", "sre-tools"])
        audit.append((t, f"user={user} service={svc} key={key} "
                         f"old={old} new={new}"))
        noise_changes += 1
    audit.append((t0, f"user=deploy-bot service={root} "
                      f"key={mode['key']} old={mode['old']} "
                      f"new={mode['new']}"))
    audit.append((rollback_t, f"user=oncall-sre service={root} "
                              f"key={mode['key']} old={mode['new']} "
                              f"new={mode['old']}"))
    audit.sort(key=lambda e: e[0])
    audit_lines = [f"{fmt_ts(t)} change_id=CHG-{5000 + i:04d} {rest}"
                   for i, (t, rest) in enumerate(audit)]

    # --- assemble files ---------------------------------------------
    corpus: dict[str, str] = {
        "docs/topology.md": TOPOLOGY_MD,
        "docs/runbook.md": RUNBOOK_MD,
        "config/alert-thresholds.yaml": ALERT_THRESHOLDS_YAML,
        "changes/config-audit.log": "\n".join(audit_lines) + "\n",
    }
    for svc in SERVICES:
        base = ("logs/edge-gateway/access.log" if svc == "edge-gateway"
                else f"logs/{svc}/app.log")
        for lo, hi, suffix in WINDOWS:
            window = sorted((e for e in entries[svc] if lo <= e[0] < hi),
                            key=lambda e: (e[0], e[1]))
            corpus[base + suffix] = "\n".join(
                f"{fmt_ts(t)} {line}" for t, _, line in window) + "\n"

    # --- answers, computed from the injected ground truth -----------
    impacted = sum(
        1 for t, _, line in entries["edge-gateway"]
        if t0 <= t < t0 + IMPACT_WINDOW_SECS
        and 500 <= int(line.split()[2]) < 600)
    step = _runbook_step(mode["mitigation"])
    propagation = ",".join([root] + [svc for svc, _ in caller_onsets]
                           + ["edge-gateway"])
    answers = [root, mode["key"], fmt_ts(t0), propagation,
               str(impacted), str(step)]
    return corpus, answers


def _runbook_step(mitigation_phrase: str) -> int:
    """The containment answer comes from the runbook text itself, so a
    reworded runbook cannot silently orphan the answer key."""
    step = None
    for line in RUNBOOK_MD.splitlines():
        stripped = line.strip()
        if stripped[:1].isdigit() and ". " in stripped:
            step = int(stripped.split(".", 1)[0])
        if mitigation_phrase in line:
            if step is None:
                break
            return step
    raise SystemExit(f"runbook lost the phrase {mitigation_phrase!r}")


# ---------------------------------------------------------------------
# Self-test: re-derive each answer from the emitted corpus alone.
# ---------------------------------------------------------------------


def derive_answers(corpus: dict[str, str]) -> list[str]:
    # Symptom onset: earliest mode-marker line anywhere in the app logs.
    best: tuple[int, str, str] | None = None
    for path in sorted(corpus):
        if not (path.startswith("logs/") and "/app.log" in path):
            continue
        svc = path.split("/")[1]
        for line in corpus[path].splitlines():
            for mode_name in sorted(MODES):
                if MODES[mode_name]["marker"] in line:
                    t = parse_ts(line.split()[0])
                    if best is None or t < best[0]:
                        best = (t, svc, mode_name)
    if best is None:
        raise SystemExit("self-test: no symptom marker found in corpus")
    onset_t, root, mode_name = best

    # Triggering change: latest audit entry for the root service that
    # precedes symptom onset.
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

    # Propagation: first cascade error per caller, ordered by time.
    cascade: list[tuple[int, str]] = []
    needle = f"upstream call to {root} failed"
    for path in sorted(corpus):
        if not (path.startswith("logs/") and "/app.log" in path):
            continue
        svc = path.split("/")[1]
        for line in corpus[path].splitlines():
            if needle in line:
                cascade.append((parse_ts(line.split()[0]), svc))
    firsts: dict[str, int] = {}
    for t, svc in sorted(cascade):
        firsts.setdefault(svc, t)
    ordered = [svc for svc, _ in sorted(firsts.items(),
                                        key=lambda kv: kv[1])]
    propagation = ",".join([root] + ordered + ["edge-gateway"])

    # Customer impact: 5xx access lines inside [T0, T0 + window).
    impacted = 0
    for path in sorted(corpus):
        if "edge-gateway/access.log" not in path:
            continue
        for line in corpus[path].splitlines():
            tokens = line.split()
            t = parse_ts(tokens[0])
            if t0 <= t < t0 + IMPACT_WINDOW_SECS and \
                    500 <= int(tokens[3]) < 600:
                impacted += 1

    step = None
    current = None
    for line in corpus["docs/runbook.md"].splitlines():
        stripped = line.strip()
        if stripped[:1].isdigit() and ". " in stripped:
            current = int(stripped.split(".", 1)[0])
        if MODES[mode_name]["mitigation"] in line:
            step = current
    if step is None:
        raise SystemExit("self-test: mitigation step not in runbook")

    return [root, fields["key"], fmt_ts(t0), propagation,
            str(impacted), str(step)]


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
        {"seed": seed, "answers": answers},
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
    print(f"  root={answers[0]} key={answers[1]} t0={answers[2]}")
    print(f"  propagation={answers[3]}")
    print(f"  impacted={answers[4]} runbook_step={answers[5]}")
    print("self-test OK: all answers re-derived from the emitted corpus")
    return 0


if __name__ == "__main__":
    sys.exit(main())
