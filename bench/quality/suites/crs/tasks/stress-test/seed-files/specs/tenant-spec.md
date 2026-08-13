# Tenant Configuration Specification

## Tenant Registry

Tenants are loaded from `config/tenants.yaml` at startup. Hot-reload every 30 seconds.

## Tenant Object Schema

```yaml
tenant_id: tn-us-east-0042
name: "Acme Corp"
tier: premium              # free | standard | premium | enterprise
status: active             # active | suspended | migrating | decommissioned
created_at: 2024-01-15T00:00:00-05:00
allowed_sources:
  - "web-app"
  - "mobile-ios"
  - "mobile-android"
  - "batch-import"
rate_limits:
  events_per_second: 500
  events_per_minute: 25000
  burst_multiplier: 2.5     # burst = events_per_second * burst_multiplier
isolation:
  storage_prefix: "acme"    # prefix for storage keys
  queue_name: "acme-events" # dedicated queue name
  encryption_key_id: "kms-key-acme-2024"  # KMS key reference
custom_transforms: []       # only enterprise tier
webhook_url: "https://acme.example.com/webhooks/events"
webhook_secret: "whsec_acme_prod_k3y..."
webhook_retry_policy:
  max_retries: 5
  backoff_base_ms: 1000
  backoff_max_ms: 60000
  backoff_algorithm: "decorrelated_jitter"  # NOT standard exponential!
```

## Webhook Retry: Decorrelated Jitter Algorithm

This is critical — do NOT use standard exponential backoff.

The decorrelated jitter algorithm works as follows:
```
sleep = min(backoff_max_ms, random_between(backoff_base_ms, previous_sleep * 3))
```

Where `previous_sleep` starts at `backoff_base_ms` for the first retry.

This is AWS-style decorrelated jitter, NOT full jitter or equal jitter.

## Tenant Status Behavior

- `active`: Process events normally
- `suspended`: Accept events but queue them (do NOT process). Return 202 Accepted with header `X-Tenant-Status: suspended`
- `migrating`: Accept events, process with both old AND new pipeline config, compare results. Log discrepancies but use OLD pipeline result.
- `decommissioned`: Reject all events with 410 Gone

## Source Validation

Each tenant has an `allowed_sources` list. Events from unregistered sources are:
1. Logged to audit with severity `WARN`
2. Sent to DLQ with reason `unregistered_source`
3. NOT processed (but still counted against rate limits)

## Tenant Isolation Requirements

- Storage MUST use tenant-specific prefixes (no cross-tenant data access)
- Metrics MUST be tagged with tenant_id
- Logs MUST include tenant_id in structured fields
- Rate limits are per-tenant (not global)
- DLQ is shared but events are tagged with tenant_id
