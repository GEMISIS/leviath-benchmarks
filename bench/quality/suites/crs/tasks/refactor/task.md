# Task: Refactor Legacy Payment Processor

Refactor a legacy payment processing system to use the new architecture while keeping all tests passing.

## Requirements

1. **Migration Path**: Follow the architecture documented in `docs/new-architecture.md`
2. **Test Compatibility**: All existing tests in `tests/` must pass after refactoring
3. **Pattern**: Migrate from procedural code to the strategy pattern for payment methods
4. **Validation**: Use the validation rules from `docs/validation-rules.md`
5. **Database**: Update schema per `docs/schema-migration.sql` but keep data compatibility

## Current System

See `src/legacy/` for existing implementation:
- `payment_processor.py` - Main processor (procedural, 500 lines)
- `validators.py` - Input validation
- `database.py` - SQLite operations

## Deliverables

- Refactored code in `src/` with new architecture
- All existing tests passing (don't modify test logic, only test imports if needed)
- Migration script in `migrate.py`
- Keep backward compatibility for API - external interface must remain unchanged

## Constraints

- Cannot break existing API contracts (see `docs/api-contract.md`)
- Must maintain 100% test coverage
- All transaction processing logic must match existing behavior exactly
