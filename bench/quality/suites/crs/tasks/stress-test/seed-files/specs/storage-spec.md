# Storage Layer Specification

## Backend

Use SQLite with WAL mode enabled. Database file: `data/events.db`

## Schema

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT UNIQUE NOT NULL,
    tenant_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    version TEXT NOT NULL DEFAULT '2.3',
    timestamp TEXT NOT NULL,
    source TEXT NOT NULL,
    correlation_id TEXT,
    payload TEXT NOT NULL,  -- JSON string
    metadata TEXT NOT NULL, -- JSON string
    storage_key TEXT NOT NULL, -- tenant_prefix + "/" + event_type + "/" + YYYY/MM/DD/HH + "/" + event_id
    processing_status TEXT NOT NULL DEFAULT 'processed', -- processed | failed | reprocessed
    handler_results TEXT, -- JSON array of handler results
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f+00:00', 'now')),
    
    CHECK (processing_status IN ('processed', 'failed', 'reprocessed'))
);

CREATE INDEX idx_events_tenant ON events(tenant_id);
CREATE INDEX idx_events_type ON events(tenant_id, event_type);
CREATE INDEX idx_events_timestamp ON events(tenant_id, timestamp);
CREATE INDEX idx_events_storage_key ON events(storage_key);
CREATE INDEX idx_events_correlation ON events(correlation_id) WHERE correlation_id IS NOT NULL;
```

## Storage Key Format

CRITICAL: The storage key format MUST be exactly:
```
{tenant_storage_prefix}/{event_category}/{YYYY}/{MM}/{DD}/{HH}/{event_id}
```

Example: `acme/user/2024/03/15/14/evt_us_01HQ3ABC123`

Note: Use `event_category` (the part before the dot in event_type), NOT the full event_type.

## Write Semantics

1. All writes use INSERT OR REPLACE (upsert on event_id)
2. Batch writes: accumulate up to 50 events OR 500ms, whichever comes first
3. Batch size is configurable per tenant (override in tenant config, default 50)
4. On write failure: retry 3 times with 100ms, 500ms, 2000ms delays
5. After 3 failures: circuit breaker opens (see pipeline spec)

## Read Operations

- `get_event(event_id)` → single event
- `list_events(tenant_id, event_type, start_time, end_time, limit=100, offset=0)` → paginated
- `count_events(tenant_id, event_type, start_time, end_time)` → count
- All reads MUST filter by tenant_id (enforce tenant isolation)
- Maximum `limit` value: 1000
- Results sorted by timestamp DESC (newest first)

## Data Retention

- Default retention: 90 days
- Premium/Enterprise: 365 days
- Free tier: 30 days
- Cleanup runs every 6 hours via background task
- Cleanup deletes in batches of 1000 rows (to avoid long locks)
