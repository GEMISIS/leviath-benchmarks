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

## Deliverables

- All 11 files listed above
- `requirements.txt` with dependencies
- `README.md` with architecture overview

**Note:** A separate validation test suite will be used to evaluate your implementation.
