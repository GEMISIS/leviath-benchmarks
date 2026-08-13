# Audit & Compliance Specification

## Audit Events

The audit log captures a tamper-evident record of all significant operations.

## Audit Entry Schema

```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    audit_id TEXT UNIQUE NOT NULL,   -- "aud_" + ULID
    timestamp TEXT NOT NULL,
    actor TEXT NOT NULL,              -- API key_id or "system"
    action TEXT NOT NULL,             -- see action list below
    tenant_id TEXT,
    resource_type TEXT NOT NULL,      -- event | tenant | dlq | config
    resource_id TEXT,                 -- the affected resource ID
    severity TEXT NOT NULL,           -- INFO | WARN | ERROR | CRITICAL
    details TEXT,                     -- JSON with action-specific details
    checksum TEXT NOT NULL,           -- SHA-256 of: previous_checksum + timestamp + action + details
    
    CHECK (severity IN ('INFO', 'WARN', 'ERROR', 'CRITICAL'))
);

CREATE INDEX idx_audit_tenant ON audit_log(tenant_id);
CREATE INDEX idx_audit_action ON audit_log(action);
CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);
```

## Checksum Chain

The checksum field creates a hash chain for tamper detection:
- First entry: checksum = SHA-256 of `"genesis" + timestamp + action + details`
- Subsequent: checksum = SHA-256 of `previous_checksum + timestamp + action + details`
- This means audit entries must be written sequentially (use a lock/queue)

## Audited Actions

| Action | Severity | Trigger |
|--------|----------|---------|
| event.received | INFO | Every event received |
| event.processed | INFO | Event successfully processed |
| event.failed | ERROR | Event processing failed |
| event.rejected | WARN | Event rejected (validation/auth) |
| event.deduplicated | INFO | Duplicate event detected |
| dlq.enqueued | WARN | Event sent to DLQ |
| dlq.reprocessed | INFO | DLQ entry reprocessed |
| dlq.discarded | WARN | DLQ entry discarded |
| tenant.source_rejected | WARN | Unregistered source detected |
| circuit_breaker.opened | CRITICAL | Circuit breaker opened |
| circuit_breaker.closed | INFO | Circuit breaker closed |
| api.auth_failed | WARN | Authentication failure |
| config.reloaded | INFO | Tenant config hot-reloaded |

## Performance Constraints

- Audit writes MUST NOT block event processing
- Use an async write queue (capacity: 10,000 entries)
- If queue is full: log at ERROR and drop the audit entry (never block)
- Batch audit writes: up to 100 entries per transaction

## Retention

- Audit log retention: 1 year (365 days)
- Cleanup runs daily at 02:00 UTC
- Cleanup deletes entries older than retention period in batches of 5,000
