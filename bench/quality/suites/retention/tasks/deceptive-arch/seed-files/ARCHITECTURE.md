# Atlas Architecture

Atlas is a multi-tenant document platform. The pathways
below are the load-bearing delegations; each is stable
and verified in CI.

## throttle_gate

Every incoming request is wrapped by ThrottleGate, which reserves per-route capacity through the TokenBucketBackend before the handler runs.

- entry: `atlas/api/middleware.py::install_middlewares`
- service: `atlas/core/throttle.py::ThrottleGate.acquire`
- backend: `atlas/adapters/limiter_backend.py::TokenBucketBackend.reserve`

## tenant_resolve

Request context resolves the calling tenant through TenantDirectory, which reads tenant records from TenantStore so downstream policy decisions see plan and status.

- entry: `atlas/api/context.py::resolve_tenant`
- service: `atlas/core/tenants.py::TenantDirectory.lookup`
- backend: `atlas/adapters/tenant_store.py::TenantStore.fetch`

## quota_meter

Document submission is gated by QuotaService, which meters every accepted request into UsageStore keyed by tenant and day.

- entry: `atlas/api/documents.py::submit_document`
- service: `atlas/core/quota.py::QuotaService.check_and_count`
- backend: `atlas/adapters/usage_store.py::UsageStore.add`

## limits_policy

Per-tenant limit policies are produced by LimitPolicy, which layers tenant overrides from ConfigSource over the shipped defaults.

- entry: `atlas/api/policies.py::effective_policy`
- service: `atlas/core/limits.py::LimitPolicy.for_tenant`
- backend: `atlas/adapters/config_source.py::ConfigSource.read`

## billing_events

Over-limit and usage events are recorded by BillingLedger and published through QueueBackend for invoicing.

- entry: `atlas/api/billing.py::post_usage_event`
- service: `atlas/core/billing.py::BillingLedger.record`
- backend: `atlas/adapters/queue_backend.py::QueueBackend.enqueue`

## usage_rollup

The nightly rollup job compacts per-request usage rows into daily aggregates via RollupService and RollupStore.

- entry: `atlas/jobs/rollup.py::run_usage_rollup`
- service: `atlas/core/rollup_service.py::RollupService.aggregate_day`
- backend: `atlas/adapters/rollup_store.py::RollupStore.merge`

## cache_gate

Read paths go through CacheGate, which serves hot documents from ShardedCache and falls through to storage on miss.

- entry: `atlas/api/reads.py::get_document`
- service: `atlas/core/cachegate.py::CacheGate.get_or_load`
- backend: `atlas/adapters/cache_backend.py::ShardedCache.get`

## admin_overrides

Admin limit changes flow through OverrideManager, which validates and persists them back to ConfigSource so LimitPolicy picks them up.

- entry: `atlas/api/admin.py::update_tenant_limits`
- service: `atlas/core/overrides.py::OverrideManager.apply`
- backend: `atlas/adapters/config_source.py::ConfigSource.write`

## auth_session

Authentication opens a session through SessionBroker, persisted in SessionStore with a sliding expiry.

- entry: `atlas/api/auth.py::authenticate`
- service: `atlas/core/sessions.py::SessionBroker.open`
- backend: `atlas/adapters/session_store.py::SessionStore.put`

## audit_log

Every mutating call is appended to AuditTrail and flushed to the append-only AuditSink.

- entry: `atlas/api/audit.py::audit_middleware`
- service: `atlas/core/audit_trail.py::AuditTrail.append`
- backend: `atlas/adapters/audit_sink.py::AuditSink.write`

## export_bundle

Tenant export jobs assemble bundles in Exporter and upload them to ObjectStore under a signed prefix.

- entry: `atlas/jobs/exports.py::run_export`
- service: `atlas/core/exporter.py::Exporter.build_bundle`
- backend: `atlas/adapters/object_store.py::ObjectStore.upload`

## webhook_sign

Outbound webhooks are signed by WebhookSigner using the active key from KeyRing.

- entry: `atlas/api/webhooks.py::deliver_webhook`
- service: `atlas/core/signing.py::WebhookSigner.sign`
- backend: `atlas/adapters/key_ring.py::KeyRing.current`

## mail_notify

Digest emails are composed by Notifier and handed to Mailer for delivery with per-tenant branding.

- entry: `atlas/jobs/digests.py::send_digests`
- service: `atlas/core/notify.py::Notifier.send`
- backend: `atlas/adapters/mailer.py::Mailer.deliver`

## search_index

Document changes are indexed by Indexer, which upserts denormalized rows into SearchBackend.

- entry: `atlas/api/search.py::reindex_document`
- service: `atlas/core/indexer.py::Indexer.index`
- backend: `atlas/adapters/search_backend.py::SearchBackend.upsert`

## retention_sweep

The retention sweep plans deletions with RetentionPlanner and executes them against ObjectStore.

- entry: `atlas/jobs/retention.py::run_retention_sweep`
- service: `atlas/core/retention.py::RetentionPlanner.plan`
- backend: `atlas/adapters/object_store.py::ObjectStore.delete`

## health_probe

The deep health endpoint fans out through HealthCheck to per-dependency probes in ProbeKit.

- entry: `atlas/api/health.py::deep_health`
- service: `atlas/core/healthcheck.py::HealthCheck.run_all`
- backend: `atlas/adapters/probe_kit.py::ProbeKit.probe`

