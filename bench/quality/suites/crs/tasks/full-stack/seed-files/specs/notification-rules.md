# Notification Business Rules

## Notification Types

1. **COMMENT** - User receives a comment on their content
   - Priority: MEDIUM
   - Batching: Can batch up to 5 comments into one notification

2. **MENTION** - User is @mentioned
   - Priority: HIGH
   - Batching: Never batch, always send immediately

3. **SYSTEM** - System announcements, maintenance notices
   - Priority: LOW or MEDIUM depending on severity
   - Batching: System messages are never batched

4. **SECURITY** - Login from new device, password changes, etc.
   - Priority: URGENT
   - Batching: Never batch, always send immediately
   - Special: Bypass quiet hours

## Delivery Rules

1. **Quiet Hours**: If user has quiet hours configured, only URGENT priority notifications are delivered during that time. Others are queued and sent when quiet hours end.

2. **User Preferences**: Check `enabled_types` - only send notification types the user has enabled.

3. **Read Status**: Once a notification is marked as read via WebSocket or API, set `read=true` in database.

4. **Retention**: Keep notifications for 30 days, then archive.

5. **Duplicates**: If same notification (same type, same metadata) is generated within 5 minutes, suppress it.

## Real-Time Delivery

- Use WebSocket for real-time push to connected clients
- If user not connected, notifications still stored in DB for later retrieval
- On reconnect, send any unread notifications from last 24 hours
