# Task: Real-Time Notification System

Implement a full-stack real-time notification feature across frontend and backend with WebSocket integration.

## Requirements

### Backend (Python/FastAPI)

1. **WebSocket Server**: Implement WebSocket endpoint for real-time notifications
2. **REST API**: CRUD endpoints for notification preferences (see `specs/backend-api.yaml`)
3. **Database**: Use schema from `specs/database-schema.sql`
4. **Business Logic**: Implement notification rules from `specs/notification-rules.md`
5. **Integration**: Connect to mock external service (endpoints in `specs/external-service.md`)

### Frontend (React/TypeScript)

1. **Components**: Notification bell, toast notifications, preferences panel (see `specs/ui-mockups.png`)
2. **WebSocket Client**: Connect to backend WS endpoint, handle reconnection
3. **State Management**: Use shared types from `shared/types.ts`
4. **Styling**: Match design system in `specs/design-tokens.json`

### Shared Types

1. **Type Definitions**: All types defined in `shared/types.ts` must be used on both frontend and backend
2. **Validation**: Frontend and backend must validate against same schema

### Integration Tests

1. **End-to-End**: Tests that verify frontend → backend → database flow
2. **WebSocket**: Test connection, reconnection, and message delivery
3. **Type Safety**: Ensure shared types are used correctly

## Constraints

- Frontend and backend must agree on all interfaces (use shared/types.ts)
- WebSocket messages must match format in specs/websocket-protocol.md
- All notification types from specs/notification-rules.md must be supported
- Must handle offline/reconnection gracefully

## Deliverables

- Backend implementation in `backend/`
- Frontend implementation in `frontend/`
- Integration tests in `tests/integration/`
- Shared types remain in `shared/types.ts` (update as needed but keep both sides in sync)
