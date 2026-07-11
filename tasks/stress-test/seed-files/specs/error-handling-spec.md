# Error Handling Specification

## Error Hierarchy

```
PlatformError (base)
├── ValidationError (400/422)
│   ├── SchemaValidationError
│   ├── PayloadSizeError
│   ├── IdempotencyError (409)
│   └── TenantValidationError
├── AuthenticationError (401)
├── AuthorizationError (403)
├── TenantError
│   ├── TenantNotFoundError (404)
│   ├── TenantSuspendedError (202)
│   ├── TenantDecommissionedError (410)
│   └── TenantMigratingError (200, with warning header)
├── RateLimitError (429)
├── ProcessingError (500)
│   ├── TransformError
│   ├── HandlerError
│   └── RoutingError
├── StorageError (503)
│   └── CircuitBreakerOpenError
└── WebhookError (non-user-facing, async)
```

## Error Context

Every error MUST include:
- `error_code`: machine-readable code (SCREAMING_SNAKE_CASE)
- `message`: human-readable description
- `tenant_id`: if known
- `event_id`: if known
- `stage`: pipeline stage where error occurred
- `timestamp`: ISO-8601

## Logging Levels

| Error Type | Log Level | Audit? |
|-----------|-----------|--------|
| ValidationError | WARN | Yes |
| AuthenticationError | WARN | Yes |
| AuthorizationError | WARN | Yes |
| RateLimitError | INFO | No (too noisy) |
| TenantSuspendedError | INFO | Yes |
| TenantDecommissionedError | INFO | Yes |
| TransformError | ERROR | Yes |
| HandlerError | ERROR | Yes |
| StorageError | CRITICAL | Yes |
| CircuitBreakerOpenError | CRITICAL | Yes |
| WebhookError | WARN | No |

## Structured Log Format

All log entries use JSON format:
```json
{
  "timestamp": "2024-03-15T14:30:00.123-05:00",
  "level": "ERROR",
  "logger": "evtplatform.pipeline",
  "message": "Transform failed for event",
  "tenant_id": "tn-us-east-0042",
  "event_id": "evt_us_01HQ3ABC123",
  "stage": "transform",
  "error_code": "TRANSFORM_ERROR",
  "error_details": "KeyError: 'missing_field'",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "duration_ms": 12.5
}
```

## Panic Recovery

If an unhandled exception occurs during event processing:
1. Log at CRITICAL level
2. Send event to DLQ with reason `internal_error`
3. Return 500 Internal Server Error
4. Increment `evtplatform.events.failed` counter with error_code=`INTERNAL_ERROR`
5. Do NOT crash the process — recover and continue processing other events
