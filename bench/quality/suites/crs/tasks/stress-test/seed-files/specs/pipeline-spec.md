# Pipeline Orchestrator Specification

## Processing Stages

Events flow through these stages in order:

1. **Receive** → validate envelope schema
2. **Authenticate** → verify tenant exists and is not decommissioned
3. **Rate Check** → check per-tenant rate limits
4. **Validate** → full schema validation (event type, payload size, sdk version, idempotency)
5. **Transform** → apply tenant transformation rules
6. **Route** → determine handler(s) based on routing table
7. **Handle** → dispatch to handler(s), collect results
8. **Persist** → write to storage with tenant isolation
9. **Audit** → write audit log entry
10. **Webhook** → POST to tenant's webhook URL (async, non-blocking)
11. **Metrics** → emit metrics for this event

## Stage Failure Behavior

Each stage has specific failure handling:

| Stage | On Failure | DLQ? | Retry? | HTTP Response |
|-------|-----------|------|--------|---------------|
| Receive | Reject | No | No | 400 Bad Request |
| Authenticate | Reject | No | No | 401/410 |
| Rate Check | Throttle | No | No | 429 Too Many Requests |
| Validate | Reject | Yes, reason=validation_failed | No | 422 Unprocessable |
| Transform | Skip transform, use raw | Yes, reason=transform_error | Yes, 2x | 200 (degraded) |
| Route | DLQ | Yes, reason=no_route | No | 500 |
| Handle | Partial success possible | Yes (failed handlers only) | Yes, 3x | 207 Multi-Status |
| Persist | Critical failure | Yes, reason=storage_error | Yes, 5x with circuit breaker | 503 |
| Audit | Log error, continue | No | No | N/A (post-response) |
| Webhook | Async retry | No | Yes, per tenant policy | N/A (async) |
| Metrics | Log error, continue | No | No | N/A (post-response) |

## Circuit Breaker (Storage Stage Only)

Parameters:
- **Failure threshold:** 5 consecutive failures
- **Recovery timeout:** 30 seconds
- **Half-open max probes:** 3
- States: CLOSED → OPEN → HALF_OPEN → CLOSED

When circuit is OPEN:
- All events go to DLQ with reason `circuit_open`
- Return 503 Service Unavailable
- After recovery timeout, transition to HALF_OPEN
- In HALF_OPEN, allow up to 3 probe requests
- If any probe fails → back to OPEN
- If all 3 succeed → CLOSED

## Concurrency Model

- Pipeline processes events concurrently per tenant
- Max concurrent events per tenant: `min(rate_limit.events_per_second, 100)`
- Global max concurrent events: 1000
- Use semaphore-based throttling, NOT thread pools
- Events for suspended tenants go to a separate queue (capacity: 10,000 per tenant)

## Idempotency Handling

The idempotency window is 24 hours (86400 seconds). Store idempotency keys in memory with LRU eviction.
- Max entries: 1,000,000 (across all tenants)
- On duplicate within window: return cached response with header `X-Idempotent: true`
- On eviction: accept the risk of reprocessing (log at DEBUG level)

## Response Headers

All responses MUST include:
- `X-Request-ID`: same as event_id if valid, otherwise generate UUID v4
- `X-Tenant-ID`: tenant_id from the event
- `X-Processing-Time-Ms`: wall-clock processing time in milliseconds
- `X-Pipeline-Version`: "2.3"
- `X-Rate-Limit-Remaining`: remaining events in current window
- `X-Rate-Limit-Reset`: Unix timestamp when window resets
