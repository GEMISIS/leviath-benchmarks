# Task: Build a Multi-Tenant Event Processing Platform

Build a complete event processing platform from the specification documents in the seed files. This is a complex system with multiple interacting components. Read ALL specification files before writing any code.

## System Overview

The platform processes events from multiple tenants, applies transformation rules, routes to appropriate handlers, persists to storage, and exposes metrics. Each component has specific requirements detailed in the spec files.

## Required Components (build in this order)

1. **Event Schema Validator** (`src/schema_validator.py`) — Validates incoming events against tenant-specific schemas
2. **Transformation Engine** (`src/transformer.py`) — Applies per-tenant transformation rules from `config/transforms.yaml`
3. **Router** (`src/router.py`) — Routes events based on routing table in `config/routing.yaml`
4. **Handler Registry** (`src/handlers.py`) — Registers and dispatches to event handlers per the handler spec
5. **Storage Layer** (`src/storage.py`) — Persists events with tenant isolation per the storage spec
6. **Metrics Collector** (`src/metrics.py`) — Tracks metrics defined in the monitoring spec
7. **Dead Letter Queue** (`src/dlq.py`) — Handles failed events per the DLQ spec
8. **Rate Limiter** (`src/rate_limiter.py`) — Per-tenant rate limiting per the rate limit spec
9. **Audit Logger** (`src/audit.py`) — Audit trail per compliance spec
10. **Pipeline Orchestrator** (`src/pipeline.py`) — Ties everything together per the pipeline spec
11. **API Server** (`src/api.py`) — REST API exposing the platform per the API spec

## Critical Rules

- Read ALL spec files before writing any code
- Every configuration value, threshold, timeout, and limit in the specs must be implemented exactly
- Do not hardcode values that are specified in config files — read them at runtime
- Each component must handle errors according to the error handling spec
- All tenant IDs use the format specified in the tenant spec (not UUIDs, not integers)
- The retry backoff algorithm must match the spec exactly (not just "exponential backoff")

## Behavioral Contracts

Your implementation will be tested through the HTTP API. The validation tests verify **behaviors**, not internal architecture. You are free to organize your code however you want internally, as long as the system exhibits these observable behaviors:

### API Endpoint Behaviors

**POST /api/v1/events**
- Accepts a single event with valid schema → returns 200, 201, or 207
- Missing required fields → returns 400
- Invalid API key → returns 401
- Cross-tenant access (wrong tenant_id for API key) → returns 403
- Unknown tenant_id → returns 404
- Duplicate idempotency_key within 24h → returns 409 with `X-Idempotent: true` header
- Decommissioned tenant → returns 410
- Validation errors (bad format, wrong SDK version, disallowed category for tier) → returns 422
- Rate limit exceeded → returns 429 with `Retry-After`, `X-Rate-Limit-*` headers
- Storage circuit breaker open → returns 503

**POST /api/v1/events/batch**
- Accepts up to 100 events → returns 200 or 207
- More than 100 events → returns 400
- Batch always returns 200 at HTTP level with per-event results in body

**GET /api/v1/health**
- No authentication required
- Returns 200 with JSON: `{"status": "healthy|degraded|unhealthy", "version": "2.3", ...}`
- Status logic:
  - `healthy`: storage ok AND circuit breaker closed AND DLQ depth < 10,000
  - `degraded`: storage ok AND (circuit breaker != closed OR DLQ depth >= 10,000)
  - `unhealthy`: storage error

**GET /metrics**
- Prometheus-format text response
- Includes metrics prefixed with `evtplatform`

**GET /api/v1/metrics/summary**
- Requires admin authentication
- Returns JSON with `uptime_seconds`, `total_events_received`, and other metrics

**GET /api/v1/dlq**
- Requires admin authentication (dlq:read permission)
- Non-admin keys → returns 401 or 403

### Event Processing Behaviors

**Validation**
- Event with `sdk_version < 2.0.0` → rejected (400 or 422)
- Invalid `correlation_id` format (not UUID v4) → rejected (422)
- Payload size exceeds tier limit (64KB free, 1MB premium/enterprise) → rejected (400, 413, or 422)
- Disallowed event category for tier (e.g., `order.*` on free tier) → rejected (400, 403, or 422)
- Unregistered source for tenant → sent to DLQ with reason=`unregistered_source`

**Tenant Status**
- Suspended tenant → returns 202 (accepted, queued)
- Decommissioned tenant → returns 410

**Transformation**
- Global transform: timestamps ending in `Z` → converted to `+00:00`
- Acme tenant (tn-us-east-0042): `order.*` events → `payload.currency` uppercased
- EuroTech tenant (tn-eu-central-1337): emails and IP addresses redacted per GDPR transforms

**Rate Limiting**
- Free tier (tn-us-west-0099): 10 events/sec, 500/min, burst capacity 20
- Premium tier (tn-us-east-0042): 500 events/sec, 25,000/min
- Burst requests exceeding token bucket capacity → 429
- Sustained requests exceeding sliding window limit → 429

**Response Headers**
All successful responses include:
- `X-Request-ID`
- `X-Tenant-ID`
- `X-Processing-Time-Ms`
- `X-Pipeline-Version: 2.3`
- `X-Rate-Limit-Remaining`
- `X-Rate-Limit-Reset`

**Error Response Format**
All error responses return JSON with structure:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": { ... },
    "request_id": "..."
  }
}
```
Or flattened:
```json
{
  "error_code": "ERROR_CODE",
  "message": "Human readable message",
  "request_id": "..."
}
```

**Idempotency**
- Same `idempotency_key` within 24h window → 409 Conflict
- Response includes `X-Idempotent: true` header
- Different `idempotency_key` values → independent events

**Dead Letter Queue**
- Storage errors → DLQ with reason=`storage_error`
- Transform errors → DLQ with reason=`transform_error`
- Validation failures → DLQ with reason=`validation_failed` (non-retryable)

**Circuit Breaker**
- Opens after 5 consecutive storage failures
- When open, returns 503

## Algorithm Contracts

Your implementation MUST expose these specific functions for algorithmic testing. These functions test low-level algorithms independent of the full pipeline. You may implement them in any module you choose, but they must be importable.

### Rate Limiting: `compute_backoff(attempt: int, base: float, cap: float) -> float`

**Location:** Any module (e.g., `dlq.py`, `rate_limiter.py`, or a dedicated `backoff.py`)

**Purpose:** Compute the next backoff delay using decorrelated jitter algorithm.

**Algorithm:**
```python
def compute_backoff(attempt: int, base: float, cap: float) -> float:
    """
    Decorrelated jitter backoff: sleep = min(cap, random(base, prev_sleep * 3))
    
    Args:
        attempt: retry attempt number (0-indexed)
        base: base delay in seconds (e.g., 1.0)
        cap: maximum delay in seconds (e.g., 60.0)
    
    Returns:
        float: backoff delay in seconds
    """
    # For attempt 0, return base
    # For attempt 1+, use: min(cap, random.uniform(base, prev_sleep * 3))
    # prev_sleep starts at base for attempt 0
```

**Test expectations:**
- `compute_backoff(0, 1.0, 60.0)` → returns `1.0` (base)
- `compute_backoff(1, 1.0, 60.0)` → returns value in range `[1.0, 3.0]`
- `compute_backoff(5, 1.0, 60.0)` → returns value in range `[1.0, 60.0]`, capped at 60.0
- Result is randomized but stays within `[base, cap]`

### Metrics: DDSketch Percentile Estimation

**Location:** `metrics.py`

**Purpose:** Use DDSketch algorithm for P50/P95/P99 latency estimation with 1% relative accuracy.

**Implementation requirement:** Your metrics module must use a DDSketch-compatible algorithm (not simple histogram). Tests will verify that percentile estimates are within 1% relative accuracy of true values.

**Interface:** Not strictly defined, but your metrics collector should:
- Track processing time distributions per tenant
- Expose percentile queries: `get_percentile(tenant_id, percentile)` → float (milliseconds)

### Circuit Breaker: State Machine

**Location:** Any module (e.g., `pipeline.py`, `storage.py`, or dedicated `circuit_breaker.py`)

**Purpose:** Circuit breaker state machine with CLOSED → OPEN → HALF_OPEN → CLOSED transitions.

**Interface:**
```python
class CircuitBreaker:
    def record_success(self) -> None: ...
    def record_failure(self) -> None: ...
    def is_open(self) -> bool: ...
    def get_state(self) -> str:  # "CLOSED" | "OPEN" | "HALF_OPEN"
```

**Behavior:**
- Starts in CLOSED state
- After 5 consecutive failures → transitions to OPEN
- After 30 seconds in OPEN → transitions to HALF_OPEN
- In HALF_OPEN, allows up to 3 probe requests
  - If any fails → back to OPEN
  - If all 3 succeed → back to CLOSED

### Audit: Hash Chain Checksum

**Location:** `audit.py`

**Purpose:** Compute SHA-256 hash chain for audit log integrity.

**Interface:**
```python
def compute_audit_checksum(previous_checksum: str | None, timestamp: str, action: str, details: dict) -> str:
    """
    Compute SHA-256 hash for audit chain.
    
    First entry: hash('genesis' + timestamp + action + json(details))
    Subsequent: hash(previous_checksum + timestamp + action + json(details))
    
    Returns: hex digest string
    """
```

**Test expectations:**
- First entry (previous_checksum=None): uses "genesis" as prefix
- Subsequent entries: uses previous checksum as prefix
- Same input → same output (deterministic)
- Different input → different output (collision-resistant)

### Storage: Key Format Function

**Location:** `storage.py`

**Purpose:** Generate storage keys in the required format.

**Interface:**
```python
def format_storage_key(tenant_prefix: str, event_type: str, timestamp: str, event_id: str) -> str:
    """
    Format: {prefix}/{category}/{YYYY}/{MM}/{DD}/{HH}/{event_id}
    
    Args:
        tenant_prefix: e.g., "acme"
        event_type: e.g., "user.created" → category is "user"
        timestamp: ISO 8601 timestamp
        event_id: event identifier
    
    Returns: formatted storage key
    """
```

**Test expectations:**
- `format_storage_key("acme", "user.created", "2024-03-15T14:30:00+00:00", "evt_us_ABC123")` 
  → `"acme/user/2024/03/15/14/evt_us_ABC123"`
- Extracts date/time components from ISO timestamp
- Extracts category (part before `.`) from event_type

## Deliverables

- All 11 files listed above
- `requirements.txt` with dependencies
- `README.md` with architecture overview

**Note:** A separate validation test suite will be used to evaluate your implementation.
