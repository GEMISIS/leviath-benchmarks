# Event Schema Specification v2.3

## Base Event Structure

All events MUST conform to this envelope:

```json
{
  "event_id": "evt_<tenant_prefix>_<ulid>",
  "tenant_id": "<tenant_id>",
  "event_type": "<category>.<action>",
  "version": "2.3",
  "timestamp": "<ISO-8601 with timezone offset, NOT UTC Z suffix>",
  "source": "<source_system>",
  "correlation_id": "<optional, propagated from upstream>",
  "payload": { ... },
  "metadata": {
    "sdk_version": "<semver>",
    "retry_count": 0,
    "idempotency_key": "<sha256 of tenant_id + event_type + payload>"
  }
}
```

## Tenant ID Format

Tenant IDs use the format: `tn-<region>-<4digit_number>`

Valid regions: `us-east`, `us-west`, `eu-central`, `ap-south`

Examples: `tn-us-east-0042`, `tn-eu-central-1337`

**Important:** Tenant IDs are case-sensitive and must be validated with regex: `^tn-(us-east|us-west|eu-central|ap-south)-\d{4}$`

## Event Type Taxonomy

Event types follow the pattern `<category>.<action>` where:

Categories: `user`, `order`, `payment`, `inventory`, `notification`
Actions: `created`, `updated`, `deleted`, `expired`, `failed`, `retried`

Not all combinations are valid. Valid combinations per tenant tier:

| Tier | Allowed Categories |
|------|-------------------|
| free | user, notification |
| standard | user, order, notification |
| premium | all categories |
| enterprise | all categories + custom events |

Enterprise tenants can define custom event types with prefix `custom.`

## Schema Validation Rules

1. `event_id` must start with `evt_` followed by the first 2 chars of the tenant_id region (e.g., `evt_us_01HQ3...` for us-east tenants)
2. `timestamp` must be within ±5 minutes of server time (clock skew tolerance)
3. `payload` max size: 64KB for free, 256KB for standard, 1MB for premium, 5MB for enterprise
4. `metadata.sdk_version` must be ≥ 2.0.0 (semver comparison, not string)
5. `idempotency_key` is checked against a 24-hour sliding window per tenant
6. Duplicate `idempotency_key` within window returns 409 Conflict, does NOT reprocess
7. `correlation_id` when present must be a valid UUID v4
8. `source` must be registered in the tenant's allowed sources list (see tenant spec)
