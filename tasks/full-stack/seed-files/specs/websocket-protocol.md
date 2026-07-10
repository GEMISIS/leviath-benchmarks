# WebSocket Protocol Specification

## Connection

**Endpoint**: `ws://localhost:8000/ws/notifications?token=<jwt>`

Authentication via JWT token in query parameter (for WebSocket compatibility).

## Message Format

All messages are JSON matching the `WebSocketMessage` type from `shared/types.ts`:

```json
{
  "type": "notification" | "notification_read" | "ping" | "pong",
  "payload": {},
  "timestamp": "2024-01-15T10:30:45.123Z"
}
```

## Message Types

### Server → Client: notification

```json
{
  "type": "notification",
  "payload": {
    "id": "notif-123",
    "user_id": 456,
    "type": "mention",
    "priority": "high",
    "title": "You were mentioned",
    "message": "Alice mentioned you in a comment",
    "link": "/posts/789",
    "read": false,
    "created_at": "2024-01-15T10:30:45.123Z"
  },
  "timestamp": "2024-01-15T10:30:45.123Z"
}
```

### Client → Server: notification_read

```json
{
  "type": "notification_read",
  "payload": {
    "notification_id": "notif-123"
  },
  "timestamp": "2024-01-15T10:31:00.000Z"
}
```

### Heartbeat: ping/pong

Client sends `ping` every 30 seconds:
```json
{"type": "ping", "payload": {}, "timestamp": "..."}
```

Server responds with `pong`:
```json
{"type": "pong", "payload": {}, "timestamp": "..."}
```

## Reconnection

- Client should attempt reconnection with exponential backoff: 1s, 2s, 4s, 8s, max 30s
- On reconnect, server sends missed unread notifications (last 24h)
- Client should handle duplicate notifications gracefully (use notification.id)
