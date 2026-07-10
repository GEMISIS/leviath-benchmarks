# Task: Build a User Management REST API

Build a production-ready REST API for user management with the following requirements:

## Requirements

1. **Authentication**: JWT tokens with RS256 signing (use existing keys in `keys/` directory)
2. **Endpoints**:
   - `POST /api/users` - Create user (admin only)
   - `GET /api/users/:id` - Get user details
   - `PUT /api/users/:id` - Update user (owner or admin)
   - `DELETE /api/users/:id` - Delete user (admin only)
   - `POST /api/auth/login` - Authenticate and get JWT
   - `GET /api/health` - Health check
3. **Validation**: All inputs must be validated per the schema in `schema.sql`
4. **Error Handling**: Return proper HTTP status codes and JSON error responses
5. **Database**: Use SQLite with schema from `schema.sql`
6. **Framework**: Use only the HTTP framework specified in `requirements.txt` - no other external dependencies beyond standard library
7. **Tests**: Write integration tests that cover all endpoints

## Constraints

- No external dependencies beyond: standard library + the web framework in requirements.txt + JWT library
- All passwords must be bcrypt hashed
- JWT tokens expire after 24 hours
- Rate limiting: 100 requests per minute per IP (implement using in-memory store)

## Deliverables

- Complete API implementation in `src/` directory
- Integration tests in `tests/` directory
- README with setup and usage instructions
