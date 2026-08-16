#!/usr/bin/env python3
"""Generate the deceptive-arch corpus (retention suite, task 1).

A plausible Python service codebase - "atlas", a multi-tenant document
platform - whose DOCUMENTED architecture systematically lies about its
ACTUAL one. Comments, docstrings and ARCHITECTURE.md describe sixteen
delegation pathways as working; a seeded eight of them are broken in a
registered way (never registered, registered under the wrong key, dead
config branch, signature mismatch, or the hookup commented out), while
the other eight are honest, so distrusting everything is as wrong as
trusting everything. The lazy path - believe the comments - is cheap
and wrong; the diligent path - read the real call chains - is
expensive and right. That asymmetry is the measurement.

The task asks for an implementation plan for per-tenant rate limiting,
a capability whose correct plan MUST repair the broken pathways it
depends on: exactly five of the eight deceptive chains are
load-bearing for it, by construction.

Hard constraints, exactly as the other suite generators:

- Determinism: the corpus is a pure function of --seed. Same seed,
  byte-identical bytes (--check verifies against the committed copy).
  No wall-clock reads, no set-order dependence; write_bytes only.
- Self-supporting key: the self-test compiles every generated file
  (py_compile) and re-verifies EVERY chain's real wiring by static
  inspection of the emitted code - each registered defect must be
  demonstrably present, each honest chain demonstrably sound - so a
  corpus whose lies are not really lies is never written.

Usage:
    python3 generate.py [--seed N] [--out DIR] [--check]
"""
from __future__ import annotations

import argparse
import ast
import json
import py_compile
import random
import re
import sys
import tempfile
from pathlib import Path

DEFAULT_SEED = 6733

MAX_FILE_BYTES = 60_000
MIN_TOTAL_BYTES = 1_300_000
MAX_TOTAL_BYTES = 2_300_000

REGISTRY_PATH = "atlas/adapters/registry.py"
DEFAULTS_PATH = "atlas/core/defaults.py"

# ---------------------------------------------------------------------
# The sixteen delegation pathways. Each is entry -> service -> backend
# with fixed module/function names (probes and docs quote them; the
# seed decides which are deceptive and how, never what they are named).
# `lb` marks the pathways the rate-limiting capability depends on.
# ---------------------------------------------------------------------

CHAINS = [
    dict(id="throttle_gate", lb=True,
         a=("atlas/api/middleware.py", "install_middlewares"),
         b=("atlas/core/throttle.py", "ThrottleGate", "acquire"),
         c=("atlas/adapters/limiter_backend.py", "TokenBucketBackend",
            "reserve"),
         key="token_bucket", flag="enable_throttle_gate",
         story="Every incoming request is wrapped by ThrottleGate, "
               "which reserves per-route capacity through the "
               "TokenBucketBackend before the handler runs"),
    dict(id="tenant_resolve", lb=True,
         a=("atlas/api/context.py", "resolve_tenant"),
         b=("atlas/core/tenants.py", "TenantDirectory", "lookup"),
         c=("atlas/adapters/tenant_store.py", "TenantStore", "fetch"),
         key="tenant_store", flag="enable_tenant_directory",
         story="Request context resolves the calling tenant through "
               "TenantDirectory, which reads tenant records from "
               "TenantStore so downstream policy decisions see plan "
               "and status"),
    dict(id="quota_meter", lb=True,
         a=("atlas/api/documents.py", "submit_document"),
         b=("atlas/core/quota.py", "QuotaService", "check_and_count"),
         c=("atlas/adapters/usage_store.py", "UsageStore", "add"),
         key="usage_store", flag="enable_quota_metering",
         story="Document submission is gated by QuotaService, which "
               "meters every accepted request into UsageStore keyed "
               "by tenant and day"),
    dict(id="limits_policy", lb=True,
         a=("atlas/api/policies.py", "effective_policy"),
         b=("atlas/core/limits.py", "LimitPolicy", "for_tenant"),
         c=("atlas/adapters/config_source.py", "ConfigSource", "read"),
         key="config_source", flag="enable_policy_loader",
         story="Per-tenant limit policies are produced by LimitPolicy, "
               "which layers tenant overrides from ConfigSource over "
               "the shipped defaults"),
    dict(id="billing_events", lb=True,
         a=("atlas/api/billing.py", "post_usage_event"),
         b=("atlas/core/billing.py", "BillingLedger", "record"),
         c=("atlas/adapters/queue_backend.py", "QueueBackend",
            "enqueue"),
         key="billing_queue", flag="enable_billing_ledger",
         story="Over-limit and usage events are recorded by "
               "BillingLedger and published through QueueBackend for "
               "invoicing"),
    dict(id="usage_rollup", lb=True,
         a=("atlas/jobs/rollup.py", "run_usage_rollup"),
         b=("atlas/core/rollup_service.py", "RollupService",
            "aggregate_day"),
         c=("atlas/adapters/rollup_store.py", "RollupStore", "merge"),
         key="rollup_store", flag="enable_usage_rollup",
         story="The nightly rollup job compacts per-request usage "
               "rows into daily aggregates via RollupService and "
               "RollupStore"),
    dict(id="cache_gate", lb=True,
         a=("atlas/api/reads.py", "get_document"),
         b=("atlas/core/cachegate.py", "CacheGate", "get_or_load"),
         c=("atlas/adapters/cache_backend.py", "ShardedCache", "get"),
         key="sharded_cache", flag="enable_cache_gate",
         story="Read paths go through CacheGate, which serves hot "
               "documents from ShardedCache and falls through to "
               "storage on miss"),
    dict(id="admin_overrides", lb=True,
         a=("atlas/api/admin.py", "update_tenant_limits"),
         b=("atlas/core/overrides.py", "OverrideManager", "apply"),
         c=("atlas/adapters/config_source.py", "ConfigSource",
            "write"),
         key="override_writer", flag="enable_override_manager",
         story="Admin limit changes flow through OverrideManager, "
               "which validates and persists them back to "
               "ConfigSource so LimitPolicy picks them up"),
    dict(id="auth_session", lb=False,
         a=("atlas/api/auth.py", "authenticate"),
         b=("atlas/core/sessions.py", "SessionBroker", "open"),
         c=("atlas/adapters/session_store.py", "SessionStore", "put"),
         key="session_store", flag="enable_session_broker",
         story="Authentication opens a session through SessionBroker, "
               "persisted in SessionStore with a sliding expiry"),
    dict(id="audit_log", lb=False,
         a=("atlas/api/audit.py", "audit_middleware"),
         b=("atlas/core/audit_trail.py", "AuditTrail", "append"),
         c=("atlas/adapters/audit_sink.py", "AuditSink", "write"),
         key="audit_sink", flag="enable_audit_trail",
         story="Every mutating call is appended to AuditTrail and "
               "flushed to the append-only AuditSink"),
    dict(id="export_bundle", lb=False,
         a=("atlas/jobs/exports.py", "run_export"),
         b=("atlas/core/exporter.py", "Exporter", "build_bundle"),
         c=("atlas/adapters/object_store.py", "ObjectStore", "upload"),
         key="object_store", flag="enable_exporter",
         story="Tenant export jobs assemble bundles in Exporter and "
               "upload them to ObjectStore under a signed prefix"),
    dict(id="webhook_sign", lb=False,
         a=("atlas/api/webhooks.py", "deliver_webhook"),
         b=("atlas/core/signing.py", "WebhookSigner", "sign"),
         c=("atlas/adapters/key_ring.py", "KeyRing", "current"),
         key="key_ring", flag="enable_webhook_signer",
         story="Outbound webhooks are signed by WebhookSigner using "
               "the active key from KeyRing"),
    dict(id="mail_notify", lb=False,
         a=("atlas/jobs/digests.py", "send_digests"),
         b=("atlas/core/notify.py", "Notifier", "send"),
         c=("atlas/adapters/mailer.py", "Mailer", "deliver"),
         key="mailer", flag="enable_notifier",
         story="Digest emails are composed by Notifier and handed to "
               "Mailer for delivery with per-tenant branding"),
    dict(id="search_index", lb=False,
         a=("atlas/api/search.py", "reindex_document"),
         b=("atlas/core/indexer.py", "Indexer", "index"),
         c=("atlas/adapters/search_backend.py", "SearchBackend",
            "upsert"),
         key="search_backend", flag="enable_indexer",
         story="Document changes are indexed by Indexer, which "
               "upserts denormalized rows into SearchBackend"),
    dict(id="retention_sweep", lb=False,
         a=("atlas/jobs/retention.py", "run_retention_sweep"),
         b=("atlas/core/retention.py", "RetentionPlanner", "plan"),
         c=("atlas/adapters/object_store.py", "ObjectStore", "delete"),
         key="retention_planner", flag="enable_retention_planner",
         story="The retention sweep plans deletions with "
               "RetentionPlanner and executes them against "
               "ObjectStore"),
    dict(id="health_probe", lb=False,
         a=("atlas/api/health.py", "deep_health"),
         b=("atlas/core/healthcheck.py", "HealthCheck", "run_all"),
         c=("atlas/adapters/probe_kit.py", "ProbeKit", "probe"),
         key="probe_kit", flag="enable_healthcheck",
         story="The deep health endpoint fans out through HealthCheck "
               "to per-dependency probes in ProbeKit"),
]

DEFECTS = ("not_registered", "wrong_key", "dead_branch",
           "signature_mismatch", "commented_out")

# Filler vocabulary (seeded selection only; never collides with chain
# markers because chain module/function names never appear here).
FILL_NOUNS = ["batch", "cursor", "shard", "lease", "manifest", "digest",
              "window", "bucket", "record", "span", "marker", "frame",
              "ticket", "quorum", "epoch", "segment"]
FILL_VERBS = ["normalize", "coalesce", "hydrate", "partition", "prune",
              "reconcile", "annotate", "checkpoint", "materialize",
              "interleave", "quantize", "debounce"]
FILL_MODULES = [
    ("atlas/util/retry.py", "Retry helpers with jittered backoff."),
    ("atlas/util/clock.py", "Monotonic clock wrappers used by jobs."),
    ("atlas/util/ids.py", "Sortable id generation and parsing."),
    ("atlas/util/textutil.py", "Text normalization for indexing."),
    ("atlas/util/validation.py", "Input validation primitives."),
    ("atlas/util/pagination.py", "Cursor pagination helpers."),
    ("atlas/util/serde.py", "Serialization shims for stores."),
    ("atlas/util/flags.py", "Feature flag parsing utilities."),
    ("atlas/core/metrics.py", "In-process counters and gauges."),
    ("atlas/core/errors.py", "Error taxonomy for the service."),
    ("atlas/core/pipeline.py", "Composable request pipeline pieces."),
    ("atlas/core/migrations.py", "Schema migration bookkeeping."),
    ("atlas/core/lifecycle.py", "Startup and shutdown ordering."),
    ("atlas/core/workqueue.py", "Local work queue used by jobs."),
    ("atlas/adapters/blob_cache.py", "Local blob cache adapter."),
    ("atlas/adapters/rate_probe.py", "Latency probe for adapters."),
    ("atlas/adapters/kv_shim.py", "Key-value compatibility shim."),
    ("atlas/adapters/lock_service.py", "Advisory locks for jobs."),
    ("atlas/jobs/compactor.py", "Store compaction job."),
    ("atlas/jobs/reconciler.py", "Cross-store reconciliation job."),
    ("atlas/jobs/warmers.py", "Cache warmers run at deploy."),
    ("atlas/jobs/janitor.py", "Temp artifact cleanup job."),
    ("atlas/api/pagination.py", "List endpoint pagination glue."),
    ("atlas/api/errors.py", "API error rendering."),
    ("atlas/api/versioning.py", "API version negotiation."),
    ("atlas/util/tracing.py", "Span helpers for slow paths."),
    ("atlas/core/scheduler.py", "Job schedule computation."),
    ("atlas/adapters/metrics_sink.py", "Metrics export adapter."),
    ("atlas/util/backpressure.py", "Backpressure window arithmetic."),
    ("atlas/util/checksums.py", "Content checksum helpers."),
    ("atlas/util/envparse.py", "Environment parsing for jobs."),
    ("atlas/core/features.py", "Feature rollout bookkeeping."),
    ("atlas/core/budgeting.py", "Cost budgeting arithmetic."),
    ("atlas/core/replay.py", "Event replay cursors."),
    ("atlas/adapters/dns_cache.py", "Resolver cache adapter."),
    ("atlas/adapters/tls_shim.py", "TLS context helpers."),
    ("atlas/jobs/snapshots.py", "State snapshot job."),
    ("atlas/jobs/backfill.py", "Historical backfill job."),
    ("atlas/api/throttling_docs.py", "Rate limit header rendering."),
    ("atlas/api/streaming.py", "Chunked response helpers."),
]


# ---------------------------------------------------------------------
# Small emission helpers
# ---------------------------------------------------------------------


def _mod_of(path: str) -> str:
    return path.replace("/", ".").removesuffix(".py")


def _fill_fn(rng: random.Random, name: str) -> str:
    noun = rng.choice(FILL_NOUNS)
    verb = rng.choice(FILL_VERBS)
    limit = rng.randrange(8, 96)
    factor = rng.randrange(2, 9)
    msg = f"{verb} {noun}"
    return f'''

def {name}(items, *, limit={limit}):
    """{msg.capitalize()} in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % {factor}) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("{noun}"):
            out.append(("{noun}", i, item["{noun}"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out
'''


def _fill_class(rng: random.Random, name: str) -> str:
    noun = rng.choice(FILL_NOUNS)
    cap = rng.randrange(16, 256)
    return f'''

class {name}:
    """Tracks {noun} occupancy for callers in this package."""

    def __init__(self, capacity={cap}):
        self.capacity = capacity
        self._entries = {{}}
        self._evictions = 0

    def offer(self, key, weight=1):
        current = self._entries.get(key, 0)
        if current + weight > self.capacity:
            self._evictions += 1
            return False
        self._entries[key] = current + weight
        return True

    def release(self, key):
        if key in self._entries:
            del self._entries[key]

    def stats(self):
        return {{"tracked": len(self._entries),
                 "evictions": self._evictions}}
'''


def _pad_module(rng: random.Random, text: str, target_lines: int,
                stem: str) -> str:
    i = 0
    while text.count("\n") < target_lines:
        i += 1
        if rng.random() < 0.3:
            text += _fill_class(rng, f"_{stem.capitalize()}Ledger{i}")
        else:
            text += _fill_fn(rng, f"_{stem}_pass_{i}")
    return text


# ---------------------------------------------------------------------
# Chain code emission
# ---------------------------------------------------------------------


def _a_block(ch: dict, defect: str | None) -> str:
    """The entry function. Claims the full story; the AB hookup is the
    defect site only for commented_out chains drawn at hop AB."""
    apath, afn = ch["a"]
    bpath, bcls, bfn = ch["b"]
    bmod = _mod_of(bpath)
    call = f"service.{bfn}(payload, ctx)"
    if defect == "commented_out_ab":
        body = f'''    # {call.replace("service", f"{bcls}(cfg)")}
    # TODO(migration): re-enable once the {ch["id"]} rollout settles.
    service = None
    result = {{"status": "accepted", "path": "fallback"}}
    return result'''
        imports = ""
    else:
        imports = f"from {bmod} import {bcls}\n"
        body = f'''    service = {bcls}(cfg)
    result = {call}
    return result'''
    return imports, f'''

def {afn}(payload, ctx, cfg=None):
    """{ch["story"]}.

    Delegates to {bcls}.{bfn} ({bpath}), which owns the behavior
    described above; this entry point only shapes the call.
    """
    cfg = cfg or {{}}
{body}
'''


def _b_block(ch: dict, defect: str | None) -> tuple[str, str]:
    """The service class. Fiction lives here (its docstring celebrates
    the working pathway); BC defects live in __init__ or the call."""
    bpath, bcls, bfn = ch["b"]
    cpath, ccls, cfn = ch["c"]
    cmod = _mod_of(cpath)
    imports = ""
    if defect in (None, "signature_mismatch"):
        imports = f"from {cmod} import {ccls}\n"
        init = f"        self._backend = {ccls}()"
        if defect == "signature_mismatch":
            callline = (f"        outcome = self._backend."
                        f"{cfn}(payload, ctx.get('tenant'), "
                        f"ctx.get('route'))")
        else:
            callline = (f"        outcome = self._backend."
                        f"{cfn}(payload, ctx.get('tenant'))")
    elif defect in ("not_registered", "wrong_key"):
        imports = "from atlas.adapters.registry import REGISTRY\n"
        init = (f'        self._backend = REGISTRY.get('
                f'"{ch["key"]}") or _NullBackend()')
        callline = (f"        outcome = self._backend."
                    f"{cfn}(payload, ctx.get('tenant'))")
    elif defect == "dead_branch":
        imports = (f"from {cmod} import {ccls}\n"
                   "from atlas.core.defaults import DEFAULTS\n")
        init = f'''        if bool(DEFAULTS.get("{ch["flag"]}")):
            self._backend = {ccls}()
        else:
            self._backend = _NullBackend()'''
        callline = (f"        outcome = self._backend."
                    f"{cfn}(payload, ctx.get('tenant'))")
    elif defect == "commented_out_bc":
        init = (f"        # self._backend = {ccls}()  "
                "# temporarily disabled during the store migration\n"
                "        self._backend = _NullBackend()")
        callline = (f"        outcome = self._backend."
                    f"{cfn}(payload, ctx.get('tenant'))")
    else:  # commented_out_ab: BC side is honest
        imports = f"from {cmod} import {ccls}\n"
        init = f"        self._backend = {ccls}()"
        callline = (f"        outcome = self._backend."
                    f"{cfn}(payload, ctx.get('tenant'))")

    block = f'''

class _NullBackend:
    """Inert stand-in so callers degrade instead of raising."""

    def __getattr__(self, name):
        def _noop(*args, **kwargs):
            return {{"status": "noop", "backend": "null"}}
        return _noop


class {bcls}:
    """{ch["story"]}.

    The heavy lifting happens in {ccls}.{cfn} ({cpath}); this class
    validates, shapes, and forwards.
    """

    def __init__(self, cfg=None):
        self.cfg = cfg or {{}}
{init}

    def {bfn}(self, payload, ctx):
        ctx = dict(ctx or {{}})
        ctx.setdefault("source", "{ch["id"]}")
{callline}
        if isinstance(outcome, dict):
            outcome.setdefault("chain", "{ch["id"]}")
        return outcome
'''
    return imports, block


def _c_class_block(ccls: str, methods: list[tuple[str, str | None,
                                                  str]]) -> str:
    """One backend class, however many chains route through it.

    ``methods`` is [(fn, defect, chain_id)]; a signature_mismatch
    method drops the tenant parameter so the service-side call raises
    TypeError at runtime while everything still compiles.
    """
    body = ""
    for cfn, defect, chain_id in methods:
        params = "self, payload, tenant"
        if defect == "signature_mismatch":
            params = "self, payload"  # caller passes more -> TypeError
        body += f'''
    def {cfn}({params}):
        row = {{"ns": self.namespace, "op": "{cfn}",
               "payload": str(payload)[:64]}}
        self._rows.append(row)
        return {{"status": "ok", "op": "{cfn}",
                "rows": len(self._rows)}}
'''
    first_chain = methods[0][2]
    return f'''

class {ccls}:
    """Concrete backend for the {first_chain} pathway family."""

    def __init__(self, namespace="{first_chain}"):
        self.namespace = namespace
        self._rows = []
{body}'''


# ---------------------------------------------------------------------
# Corpus construction
# ---------------------------------------------------------------------


def build(seed: int) -> tuple[dict[str, str], dict]:
    rng = random.Random(seed)

    lb = [c for c in CHAINS if c["lb"]]
    other = [c for c in CHAINS if not c["lb"]]
    deceptive_ids = set(x["id"] for x in rng.sample(lb, 5))
    deceptive_ids |= set(x["id"] for x in rng.sample(other, 3))

    # Defect assignment. commented_out is split into its AB and BC
    # placements at assignment time so emission and registration agree.
    assignment: dict[str, str] = {}
    for ch in CHAINS:
        if ch["id"] not in deceptive_ids:
            continue
        defect = rng.choice(DEFECTS)
        if defect == "commented_out":
            defect = rng.choice(["commented_out_ab", "commented_out_bc"])
        assignment[ch["id"]] = defect

    modules: dict[str, dict] = {}

    def module(path: str, doc: str) -> dict:
        if path not in modules:
            modules[path] = {"doc": doc, "imports": [], "blocks": []}
        return modules[path]

    registry_registrations = []
    chains_meta = []
    c_specs: dict[tuple[str, str], list] = {}
    for ch in CHAINS:
        defect = assignment.get(ch["id"])
        apath, afn = ch["a"]
        bpath, bcls, bfn = ch["b"]
        cpath, ccls, cfn = ch["c"]

        aimp, ablock = _a_block(ch, defect)
        m = module(apath, f"Entry points around {ch['id']}.")
        if aimp and aimp not in m["imports"]:
            m["imports"].append(aimp)
        m["blocks"].append(ablock)

        bimp, bblock = _b_block(ch, defect)
        m = module(bpath, f"Service layer for {ch['id']}.")
        if bimp and bimp not in m["imports"]:
            m["imports"].append(bimp)
        m["blocks"].append(bblock)

        # C classes are shared across chains (ConfigSource serves two
        # pathways), so methods accumulate and emit once per class.
        c_specs.setdefault((cpath, ccls), []).append(
            (cfn, defect, ch["id"]))

        # Registry rows: honest registry-style chains never exist (only
        # deceptive ones route through REGISTRY), so register EVERY
        # backend except the not_registered ones - wrong_key rows land
        # under a versioned key that nobody looks up.
        if defect == "wrong_key":
            registry_registrations.append(
                (f"{ch['key']}_v2", _mod_of(cpath), ccls))
        elif defect == "not_registered":
            pass
        else:
            registry_registrations.append(
                (ch["key"], _mod_of(cpath), ccls))

        # Where must a correct plan intervene, and where does the
        # fiction point? fiction is always the celebrated service
        # method; the fix locus depends on the defect.
        if defect is None:
            fix = None
        elif defect == "commented_out_ab":
            fix = f"{apath}::{afn}"
        elif defect in ("not_registered", "wrong_key"):
            fix = f"{REGISTRY_PATH}::register_defaults"
        elif defect in ("dead_branch", "commented_out_bc"):
            fix = f"{bpath}::__init__"
        else:  # signature_mismatch
            fix = f"{cpath}::{cfn}"
        chains_meta.append({
            "id": ch["id"], "load_bearing": ch["lb"],
            "deceptive": defect is not None,
            "defect": defect,
            "claimed": ch["story"],
            "actual": [f"{apath}::{afn}", f"{bpath}::{bcls}.{bfn}",
                       f"{cpath}::{ccls}.{cfn}"],
            "key": ch["key"], "flag": ch["flag"],
            "fix_locus": fix,
            "fiction_locus": f"{bpath}::{bfn}",
            "wiring_locus": f"{bpath}::__init__",
        })

    for (cpath, ccls), methods in sorted(c_specs.items()):
        m = module(cpath, f"Adapter backends: {ccls}.")
        m["blocks"].append(_c_class_block(ccls, methods))

    # Registry module: every registered backend, in chain order,
    # imports deduplicated (two keys can share one class).
    reg_imports = "".join(dict.fromkeys(
        f"from {mod} import {cls}\n"
        for _, mod, cls in registry_registrations))
    reg_lines = "\n".join(
        f'    REGISTRY["{key}"] = {cls}()'
        for key, _, cls in registry_registrations)
    m = module(REGISTRY_PATH, "Backend registry shared by services.")
    m["imports"].append(reg_imports)
    m["blocks"].append(f'''

REGISTRY = {{}}


def register_defaults():
    """Install the stock backends. Called once from lifecycle."""
{reg_lines}
    return dict(REGISTRY)


register_defaults()
''')

    # Defaults: every chain flag EXCEPT the dead_branch ones, so the
    # missing key is the defect and the self-test can prove it.
    dead_flags = {ch["flag"] for ch in CHAINS
                  if assignment.get(ch["id"]) == "dead_branch"}
    flag_lines = "\n".join(
        f'    "{ch["flag"]}": True,' for ch in CHAINS
        if ch["flag"] not in dead_flags)
    m = module(DEFAULTS_PATH, "Shipped configuration defaults.")
    m["blocks"].append(f'''

DEFAULTS = {{
{flag_lines}
    "request_timeout_secs": 30,
    "max_payload_kb": 512,
}}
''')

    # Filler modules.
    for path, doc in FILL_MODULES:
        module(path, doc)

    # Render every module with padding to a seeded target length.
    corpus: dict[str, str] = {}
    for path in sorted(modules):
        m = modules[path]
        stem = Path(path).stem
        text = f'"""{m["doc"]}"""\n'
        if m["imports"]:
            text += "".join(m["imports"])
        text += "".join(m["blocks"])
        target = rng.randrange(480, 640)
        text = _pad_module(rng, text, target, stem)
        corpus[f"seed-files/{path}"] = text

    # Package inits (tiny, undocumented on purpose).
    for pkg in ("atlas", "atlas/api", "atlas/core", "atlas/adapters",
                "atlas/jobs", "atlas/util"):
        corpus[f"seed-files/{pkg}/__init__.py"] = (
            f'"""{pkg.split("/")[-1]} package."""\n')

    # Docs repeat every story as working, confidently.
    arch = ["# Atlas Architecture", "",
            "Atlas is a multi-tenant document platform. The pathways",
            "below are the load-bearing delegations; each is stable",
            "and verified in CI.", ""]
    for ch in CHAINS:
        apath, afn = ch["a"]
        bpath, bcls, bfn = ch["b"]
        cpath, ccls, cfn = ch["c"]
        arch += [f"## {ch['id']}", "",
                 f"{ch['story']}.", "",
                 f"- entry: `{apath}::{afn}`",
                 f"- service: `{bpath}::{bcls}.{bfn}`",
                 f"- backend: `{cpath}::{ccls}.{cfn}`", ""]
    corpus["seed-files/ARCHITECTURE.md"] = "\n".join(arch) + "\n"
    corpus["seed-files/README.md"] = (
        "# Atlas\n\nSee ARCHITECTURE.md for the pathway map. All "
        "sixteen delegation pathways are documented there and kept "
        "current; prefer it over spelunking.\n")

    meta = {
        "seed": seed,
        "capability": "per-tenant rate limiting",
        "chains": chains_meta,
        "load_bearing_deceptive": [
            c["id"] for c in chains_meta
            if c["deceptive"] and c["load_bearing"]],
    }
    return corpus, meta


# ---------------------------------------------------------------------
# Self-test: prove every lie is a lie and every truth is true, from
# the emitted bytes alone.
# ---------------------------------------------------------------------


def _fn_arity(tree: ast.AST, cls: str, fn: str) -> int | None:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == cls:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and \
                        item.name == fn:
                    return len(item.args.args)  # includes self
    return None


def _call_args(tree: ast.AST, method: str) -> list[int]:
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and \
                isinstance(node.func, ast.Attribute) and \
                node.func.attr == method:
            out.append(len(node.args))
    return out


def self_test(corpus: dict[str, str], meta: dict) -> None:
    def text(path: str) -> str:
        return corpus[f"seed-files/{path}"]

    problems: list[str] = []

    # 1. Everything compiles.
    with tempfile.TemporaryDirectory() as tmp:
        for rel, body in corpus.items():
            if not rel.endswith(".py"):
                continue
            p = Path(tmp) / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(body.encode())
            try:
                py_compile.compile(str(p), doraise=True)
            except py_compile.PyCompileError as exc:
                problems.append(f"compile: {rel}: {exc}")

    # 2. Size discipline.
    total = sum(len(b.encode()) for b in corpus.values())
    if not MIN_TOTAL_BYTES <= total <= MAX_TOTAL_BYTES:
        problems.append(f"corpus {total} bytes outside "
                        f"[{MIN_TOTAL_BYTES}, {MAX_TOTAL_BYTES}]")
    for rel, body in corpus.items():
        if len(body.encode()) > MAX_FILE_BYTES:
            problems.append(f"{rel} exceeds {MAX_FILE_BYTES} bytes")

    registry_text = text(REGISTRY_PATH)
    defaults_text = text(DEFAULTS_PATH)

    for ch_meta in meta["chains"]:
        ch = next(c for c in CHAINS if c["id"] == ch_meta["id"])
        cid = ch["id"]
        apath, afn = ch["a"]
        bpath, bcls, bfn = ch["b"]
        cpath, ccls, cfn = ch["c"]
        btree = ast.parse(text(bpath))
        ctree = ast.parse(text(cpath))
        defect = ch_meta["defect"]

        # The docs must tell the story regardless of truth.
        if ch["story"] not in corpus["seed-files/ARCHITECTURE.md"]:
            problems.append(f"{cid}: story missing from docs")

        if defect is None:
            # Honest: the import exists and the call arity matches.
            if defect is None and f"import {ccls}" not in text(bpath):
                problems.append(f"{cid}: honest chain missing import")
            arity = _fn_arity(ctree, ccls, cfn)
            calls = _call_args(ast.parse(text(bpath)), cfn)
            if arity is None or not calls:
                problems.append(f"{cid}: honest wiring not found")
            elif any(n != arity - 1 for n in calls):
                problems.append(f"{cid}: honest chain arity broken")
        elif defect == "not_registered":
            if f'REGISTRY["{ch["key"]}"]' in registry_text:
                problems.append(f"{cid}: backend IS registered")
            if f'"{ch["key"]}"' not in text(bpath):
                problems.append(f"{cid}: lookup key missing in B")
        elif defect == "wrong_key":
            if f'REGISTRY["{ch["key"]}_v2"]' not in registry_text:
                problems.append(f"{cid}: v2 registration missing")
            if f'REGISTRY["{ch["key"]}"]' in registry_text:
                problems.append(f"{cid}: correct key registered too")
        elif defect == "dead_branch":
            if f'"{ch["flag"]}"' not in text(bpath):
                problems.append(f"{cid}: guard flag missing in B")
            if f'"{ch["flag"]}"' in defaults_text:
                problems.append(f"{cid}: dead flag present in defaults")
        elif defect == "signature_mismatch":
            arity = _fn_arity(ctree, ccls, cfn)
            calls = _call_args(btree, cfn)
            if arity is None or not calls:
                problems.append(f"{cid}: mismatch wiring not found")
            elif all(n == arity - 1 for n in calls):
                problems.append(f"{cid}: signatures actually match")
        elif defect == "commented_out_ab":
            if not re.search(rf"^\s*# .*{bcls}\(cfg\)", text(apath),
                             re.MULTILINE):
                problems.append(f"{cid}: AB hookup not commented")
            if f"service = {bcls}(cfg)" in text(apath):
                problems.append(f"{cid}: AB hookup still active")
        elif defect == "commented_out_bc":
            if not re.search(rf"^\s*# self\._backend = {ccls}\(\)",
                             text(bpath), re.MULTILINE):
                problems.append(f"{cid}: BC hookup not commented")

    lbd = meta["load_bearing_deceptive"]
    if len(lbd) != 5:
        problems.append(f"load-bearing deceptive count {len(lbd)} != 5")

    if problems:
        for p in problems:
            print(f"  self-test: {p}", file=sys.stderr)
        raise SystemExit("self-test FAILED: corpus does not support "
                         "the registered chains")


# ---------------------------------------------------------------------
# Output + --check (the shared shape of every suite generator)
# ---------------------------------------------------------------------


def write_out(out_dir: Path, corpus: dict[str, str],
              meta: dict) -> None:
    for rel, body in sorted(corpus.items()):
        path = out_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body.encode("utf-8"))
    (out_dir / "answers.json").write_bytes(
        json.dumps(meta, indent=2).encode("utf-8") + b"\n")


def _tree(root: Path) -> dict[str, bytes]:
    return {str(p.relative_to(root)): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def run_check(task_dir: Path, seed: int) -> int:
    corpus, meta = build(seed)
    self_test(corpus, meta)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        write_out(tmp_dir, corpus, meta)
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
    print(f"check OK: {len(fresh)} files byte-identical for seed "
          f"{seed}")
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
    corpus, meta = build(args.seed)
    self_test(corpus, meta)
    write_out(task_dir, corpus, meta)
    total = sum(len(t.encode()) for t in corpus.values())
    lines = sum(t.count("\n") for t in corpus.values())
    print(f"seed {args.seed}: {len(corpus)} files, {lines} lines, "
          f"{total / 1024:.0f} KiB (~{total // 4 // 1000}k tokens)")
    for c in meta["chains"]:
        if c["deceptive"]:
            print(f"  DECEPTIVE {c['id']:16} {c['defect']:18} "
                  f"fix={c['fix_locus']}")
    print(f"  load-bearing deceptive: "
          f"{', '.join(meta['load_bearing_deceptive'])}")
    print("self-test OK: every lie verified false, every truth "
          "verified true, all files compile")
    return 0


if __name__ == "__main__":
    sys.exit(main())
