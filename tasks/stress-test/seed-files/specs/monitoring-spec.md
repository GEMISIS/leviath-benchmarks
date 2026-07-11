# Monitoring & Metrics Specification

## Metric Types

All metrics use a prefix of `evtplatform.` and are tagged with `tenant_id`.

### Counters (monotonically increasing)
- `evtplatform.events.received` — total events received, tags: [tenant_id, event_type]
- `evtplatform.events.processed` — successfully processed, tags: [tenant_id, event_type]
- `evtplatform.events.failed` — failed at any stage, tags: [tenant_id, event_type, stage, error_code]
- `evtplatform.events.rejected` — rejected (validation/auth), tags: [tenant_id, reason]
- `evtplatform.events.throttled` — rate limited, tags: [tenant_id]
- `evtplatform.events.deduplicated` — idempotency hits, tags: [tenant_id]
- `evtplatform.dlq.enqueued` — sent to DLQ, tags: [tenant_id, reason]
- `evtplatform.dlq.reprocessed` — reprocessed from DLQ, tags: [tenant_id]
- `evtplatform.webhook.sent` — webhooks dispatched, tags: [tenant_id]
- `evtplatform.webhook.failed` — webhook delivery failures, tags: [tenant_id, status_code]
- `evtplatform.storage.writes` — storage write operations, tags: [tenant_id]
- `evtplatform.storage.write_failures` — storage write failures, tags: [tenant_id]
- `evtplatform.circuit_breaker.opened` — circuit breaker open events
- `evtplatform.circuit_breaker.closed` — circuit breaker close events

### Histograms (distribution of values)
- `evtplatform.processing.duration_ms` — end-to-end processing time, tags: [tenant_id, event_type]
  - Bucket boundaries: [1, 5, 10, 25, 50, 100, 250, 500, 1000, 5000]
- `evtplatform.payload.size_bytes` — payload size distribution, tags: [tenant_id]
  - Bucket boundaries: [256, 1024, 4096, 16384, 65536, 262144, 1048576]
- `evtplatform.transform.duration_ms` — transform stage duration, tags: [tenant_id]
  - Bucket boundaries: [0.1, 0.5, 1, 5, 10, 50, 100]
- `evtplatform.storage.batch_size` — events per storage batch, tags: [tenant_id]
  - Bucket boundaries: [1, 5, 10, 25, 50, 100]

### Gauges (current values)
- `evtplatform.rate_limiter.utilization` — current rate / limit ratio, tags: [tenant_id]
- `evtplatform.suspended_queue.size` — events queued for suspended tenants, tags: [tenant_id]
- `evtplatform.idempotency_cache.size` — current idempotency cache entries
- `evtplatform.concurrent.events` — currently processing events, tags: [tenant_id]
- `evtplatform.circuit_breaker.state` — 0=closed, 1=open, 2=half_open

## Metric Emission

Metrics are stored in-memory and exposed via:
1. `GET /metrics` endpoint (Prometheus-compatible text format)
2. `GET /api/metrics/summary` endpoint (JSON, for the UI)

The JSON summary endpoint returns:
```json
{
  "uptime_seconds": 3600,
  "total_events_received": 150000,
  "total_events_processed": 149500,
  "total_events_failed": 500,
  "events_per_second_1m": 42.3,
  "events_per_second_5m": 38.7,
  "p50_processing_ms": 12.5,
  "p95_processing_ms": 87.3,
  "p99_processing_ms": 234.1,
  "active_tenants": 15,
  "circuit_breaker_state": "closed",
  "dlq_depth": 127
}
```

## Percentile Calculation

Use the DDSketch algorithm for streaming percentile estimation.
- Relative accuracy: 1% (alpha = 0.01)
- This is NOT t-digest, NOT simple sorting, NOT reservoir sampling
- DDSketch chosen because it's mergeable across time windows

## Alert Thresholds (for monitoring, not implementation)

These are documented here for test validation:
- Error rate > 5% for 5 minutes → WARN
- Error rate > 15% for 1 minute → CRITICAL
- p99 processing > 5000ms for 3 minutes → WARN
- Circuit breaker OPEN for > 2 minutes → CRITICAL
- DLQ depth > 10,000 → WARN
