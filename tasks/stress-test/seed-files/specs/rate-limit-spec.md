# Rate Limiting Specification

## Algorithm: Token Bucket with Sliding Window Hybrid

Use a combination approach:
1. **Token bucket** for burst allowance (short-term)
2. **Sliding window counter** for sustained rate (long-term)

An event is allowed only if BOTH checks pass.

## Token Bucket Parameters (per tenant)

- Capacity: `tenant.rate_limits.events_per_second * tenant.rate_limits.burst_multiplier`
- Refill rate: `tenant.rate_limits.events_per_second` tokens per second
- Initial tokens: full capacity
- Tokens are refilled continuously (not in discrete intervals)

## Sliding Window Parameters (per tenant)

- Window size: 60 seconds
- Max events in window: `tenant.rate_limits.events_per_minute`
- Use "sliding window log" algorithm (NOT fixed window, NOT sliding window counter approximation)
- Store timestamps of each event, count events in [now - 60s, now]
- Evict timestamps older than 60 seconds

## Rate Limit Response

When rate limited, return:
- HTTP 429 Too Many Requests
- Headers:
  - `Retry-After: <seconds_until_next_token>` (ceiling integer)
  - `X-Rate-Limit-Limit: <events_per_minute>`
  - `X-Rate-Limit-Remaining: <remaining_in_window>`
  - `X-Rate-Limit-Reset: <unix_timestamp_when_window_resets>`
- Body:
```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded for tenant {tenant_id}",
    "details": {
      "limit": 25000,
      "remaining": 0,
      "reset_at": "2024-03-15T14:31:00-05:00",
      "retry_after_seconds": 12
    }
  }
}
```

## Rate Limit Exemptions

- Health check endpoint: never rate limited
- Prometheus metrics endpoint: never rate limited
- Admin API keys: rate limited at 10x the tenant's limit
- DLQ reprocessing: does NOT count against rate limits

## Memory Management

The sliding window log stores event timestamps. To prevent unbounded memory growth:
- Max stored timestamps per tenant: events_per_minute * 2
- When exceeded: switch to approximate counting mode (fixed window) for that tenant
- Log at WARN when switching to approximate mode
- Switch back to exact mode when timestamp count drops below events_per_minute
