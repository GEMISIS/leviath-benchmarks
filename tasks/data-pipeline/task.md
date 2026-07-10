# Task: Event Analytics ETL Pipeline

Build a production-grade ETL pipeline for processing event data with multiple stages, error handling, and monitoring.

## Requirements

### Pipeline Stages

1. **Ingestion** - Read from multiple sources (see `sources/` directory for examples)
   - JSON event files
   - CSV exports
   - Parquet data dumps

2. **Validation** - Validate against schema in `schemas/event-schema.json`
   - Reject malformed events
   - Log validation errors to `errors/validation-{date}.log`
   - Continue processing valid events

3. **Transformation** - Apply transformations from `transformations/rules.yaml`
   - Enrich with user metadata (lookup from `reference-data/users.csv`)
   - Aggregate by time windows (1 hour, 1 day)
   - Compute derived metrics per `transformations/metrics.yaml`

4. **Load** - Write to output destinations
   - Parquet files partitioned by date
   - Summary statistics to `output/stats.json`
   - Monitoring metrics to `output/metrics.json`

### Error Handling

Per `docs/error-handling.md`:
- **Transient errors**: Retry up to 3 times with exponential backoff
- **Permanent errors**: Log to error file, continue processing
- **Critical errors**: Stop pipeline, alert via configured webhook
- All errors must include: timestamp, stage, event_id, error_type, message

### Monitoring

Implement metrics from `docs/monitoring-spec.md`:
- Events processed per second (EPS)
- Error rate by stage
- Processing latency (p50, p95, p99)
- Memory usage per stage
- Pipeline health check endpoint (for orchestrator)

### SLA Requirements (from `docs/sla.md`)

- **Throughput**: Must process ≥10,000 events/second
- **Latency**: End-to-end p95 latency ≤500ms
- **Availability**: Pipeline uptime ≥99.9%
- **Data Quality**: Error rate ≤0.1%

### Configuration

Use config from `config/pipeline.yaml`:
- Source paths
- Output paths
- Batch sizes
- Worker threads
- Retry policies
- Monitoring endpoints

## Deliverables

- Complete pipeline implementation in `pipeline/` directory
- Unit tests for each stage in `tests/unit/`
- Integration tests in `tests/integration/`
- Monitoring dashboard config in `monitoring/` (Prometheus format)
- README with deployment and operations guide

## Constraints

- Must handle datasets up to 100GB
- Must be resumable after failures (checkpoint/recovery)
- Must support both batch and streaming modes
- Python 3.10+ with standard data processing libraries (pandas, pyarrow)
