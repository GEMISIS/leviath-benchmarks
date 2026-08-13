# Handler Registry Specification

## Handler Types

Handlers are functions that process events after routing. Multiple handlers can process the same event.

### Built-in Handlers

1. **LogHandler** — Logs event to structured logger
   - Config: `log_level` (default: INFO), `include_payload` (default: false for free tier, true for others)
   - Always registered for all event types

2. **WebhookHandler** — POSTs event to tenant's webhook URL
   - Uses tenant's webhook_url and webhook_secret
   - Signs payload with HMAC-SHA256 using webhook_secret
   - Signature header: `X-Webhook-Signature: sha256=<hex_digest>`
   - Signature computed over: `timestamp.payload_json` (timestamp is Unix epoch seconds)
   - Timeout: 10 seconds per attempt
   - Retries: per tenant's webhook_retry_policy

3. **AnalyticsHandler** — Aggregates event counts for analytics
   - Maintains 1-minute, 5-minute, and 1-hour sliding window counts per event_type per tenant
   - Windows use "jumping window" semantics (NOT tumbling, NOT sliding)
   - That means: align to calendar boundaries (minute 0, minute 5, minute 10, etc.)

4. **NotificationHandler** — For notification.* events only
   - Extracts `payload.channel` (email | sms | push | in_app)
   - Extracts `payload.recipient_id` and `payload.template_id`
   - Validates that template_id matches regex: `tmpl_[a-z0-9]{8}`
   - Queues notification for delivery (mock implementation: just log it)

5. **InventoryHandler** — For inventory.* events only (premium/enterprise)
   - On `inventory.updated`: check `payload.quantity` against `payload.reorder_threshold`
   - If quantity <= reorder_threshold: emit synthetic `notification.created` event with channel=email
   - The synthetic event MUST go through the full pipeline (not bypass validation)

## Handler Registration

Handlers register for specific event type patterns:
```python
registry.register("*.*", LogHandler())           # all events
registry.register("*.*", WebhookHandler())        # all events
registry.register("*.*", AnalyticsHandler())      # all events
registry.register("notification.*", NotificationHandler())
registry.register("inventory.*", InventoryHandler())
```

Pattern matching: `*` matches any single segment. `*.created` matches `user.created`, `order.created`, etc.

## Handler Result

Each handler returns a HandlerResult:
```python
@dataclass
class HandlerResult:
    handler_name: str
    success: bool
    duration_ms: float
    error: Optional[str] = None
    metadata: Optional[dict] = None  # handler-specific output
```

When multiple handlers process an event:
- ALL handlers execute (failures don't stop other handlers)
- Results are collected in a list
- If ANY handler fails: HTTP 207 Multi-Status
- If ALL succeed: HTTP 200 OK
- Handler results are stored with the event in storage
