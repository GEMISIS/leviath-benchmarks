# Dead Letter Queue Specification

## DLQ Storage

Uses SQLite (same database as events, different table):

```sql
CREATE TABLE dead_letter_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL,
    tenant_id TEXT NOT NULL,
    event_data TEXT NOT NULL,      -- full original event JSON
    reason TEXT NOT NULL,          -- validation_failed | transform_error | no_route | storage_error | circuit_open | unregistered_source | handler_error
    error_details TEXT,            -- detailed error message/traceback
    stage TEXT NOT NULL,           -- pipeline stage that failed
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    next_retry_at TEXT,            -- ISO-8601 timestamp
    status TEXT DEFAULT 'pending', -- pending | retrying | exhausted | reprocessed | discarded
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f+00:00', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f+00:00', 'now')),
    
    CHECK (status IN ('pending', 'retrying', 'exhausted', 'reprocessed', 'discarded'))
);

CREATE INDEX idx_dlq_tenant ON dead_letter_queue(tenant_id);
CREATE INDEX idx_dlq_status ON dead_letter_queue(status);
CREATE INDEX idx_dlq_next_retry ON dead_letter_queue(next_retry_at) WHERE status = 'pending';
```

## Retry Behavior

NOT all DLQ entries are retried. Retry eligibility by reason:

| Reason | Retryable? | Max Retries | Backoff |
|--------|-----------|-------------|---------|
| validation_failed | No | 0 | N/A |
| transform_error | Yes | 2 | 5s, 30s |
| no_route | No | 0 | N/A |
| storage_error | Yes | 5 | 1s, 5s, 25s, 125s, 625s (5x multiplier) |
| circuit_open | Yes | 10 | 30s fixed (wait for circuit recovery) |
| unregistered_source | No | 0 | N/A |
| handler_error | Yes | 3 | 10s, 60s, 300s |

## Auto-Retry Process

A background worker runs every 10 seconds:
1. Query: `SELECT * FROM dead_letter_queue WHERE status = 'pending' AND next_retry_at <= NOW() ORDER BY created_at LIMIT 50`
2. For each entry:
   a. Set status = 'retrying'
   b. Re-submit event through pipeline (from the FAILED stage, not from beginning)
   c. On success: set status = 'reprocessed', update events table
   d. On failure: increment retry_count
      - If retry_count >= max_retries: set status = 'exhausted'
      - Else: calculate next_retry_at based on backoff table, set status = 'pending'

## Important: Stage Re-entry

When retrying from DLQ, the event re-enters the pipeline at the FAILED STAGE, not the beginning.
- If transform failed: retry from transform stage
- If storage failed: retry from storage stage
- This prevents redundant validation and handler execution

Exception: circuit_open retries always start from the persist stage.

## DLQ Depth Limits

- Maximum DLQ depth per tenant: 50,000 entries
- When limit reached: new DLQ entries for that tenant are logged and discarded (status = 'discarded')
- Log at ERROR level: "DLQ depth limit exceeded for tenant {tenant_id}"

## Manual Operations

Via API (admin only):
- Reprocess single entry: `POST /api/v1/dlq/{event_id}/reprocess`
- Discard entry: `DELETE /api/v1/dlq/{event_id}`
- Bulk discard by reason: `DELETE /api/v1/dlq?reason=validation_failed&tenant_id=...`
