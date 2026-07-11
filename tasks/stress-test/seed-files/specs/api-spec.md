# REST API Specification

## Base URL

`http://localhost:8080/api/v1`

## Authentication

All API endpoints (except health check) require an API key in the header:
`Authorization: Bearer <api_key>`

API keys are loaded from `config/api_keys.yaml`. Each key has:
- `key_id`: unique identifier
- `key_hash`: bcrypt hash of the actual key
- `tenant_id`: associated tenant (or `*` for admin keys)
- `permissions`: list of allowed operations
- `rate_limit_override`: optional per-key rate limit

## Endpoints

### POST /api/v1/events
Ingest a single event.

Request body: Event JSON (see event schema spec)
Response: 
- 200: Processed successfully
- 202: Accepted (tenant suspended, queued for later)
- 207: Partially processed (some handlers failed)
- 400: Invalid event envelope
- 401: Invalid/missing API key
- 409: Duplicate event (idempotency)
- 410: Tenant decommissioned
- 422: Validation error
- 429: Rate limited
- 503: Service unavailable (circuit breaker open)

### POST /api/v1/events/batch
Ingest multiple events (max 100 per batch).

Request body: `{"events": [...]}`
Response: `{"results": [{"event_id": "...", "status": 200, "message": "ok"}, ...]}`
- Always returns 200 at HTTP level
- Individual event results in the array

### GET /api/v1/events/{event_id}
Retrieve a single event by ID.
- Must validate tenant_id from API key matches event's tenant_id
- 404 if not found OR if tenant mismatch (don't leak existence)

### GET /api/v1/events
List events with filters.
Query params: `tenant_id`, `event_type`, `start`, `end`, `limit` (default 50, max 1000), `offset`
- Admin keys can query any tenant
- Non-admin keys restricted to their tenant

### GET /api/v1/tenants/{tenant_id}/stats
Get tenant statistics.
Response includes: event counts by type, error rate, avg processing time, current rate limit utilization.

### GET /api/v1/dlq
List DLQ entries.
Query params: `tenant_id`, `reason`, `limit`, `offset`
- Admin only

### POST /api/v1/dlq/{event_id}/reprocess
Reprocess a DLQ entry.
- Removes from DLQ
- Sends through pipeline again
- Updates processing_status to 'reprocessed'
- Admin only

### GET /api/v1/health
No auth required.
Response:
```json
{
  "status": "healthy",     // healthy | degraded | unhealthy
  "version": "2.3",
  "uptime_seconds": 3600,
  "checks": {
    "storage": "ok",       // ok | error
    "circuit_breaker": "closed",
    "dlq_depth": 42,
    "active_tenants": 5
  }
}
```

Status logic:
- `healthy`: storage ok AND circuit_breaker closed AND dlq_depth < 10000
- `degraded`: storage ok AND (circuit_breaker != closed OR dlq_depth >= 10000)
- `unhealthy`: storage error

### GET /metrics
Prometheus-compatible metrics endpoint. No auth required.

### GET /api/v1/metrics/summary
JSON metrics summary. Auth required.

## Error Response Format

All errors return:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable message",
    "details": { ... },   // optional, context-specific
    "request_id": "..."
  }
}
```

Error codes: VALIDATION_ERROR, AUTH_ERROR, RATE_LIMITED, TENANT_DECOMMISSIONED, DUPLICATE_EVENT, STORAGE_ERROR, INTERNAL_ERROR

## CORS

- Allowed origins: `*` (configurable)
- Allowed methods: GET, POST, OPTIONS
- Allowed headers: Authorization, Content-Type, X-Request-ID
- Max age: 3600
