# Service Level Agreements (SLA)

## Performance SLAs

### Throughput
- **Target**: 10,000 events per second
- **Measurement**: Rolling 5-minute average
- **Alert threshold**: <8,000 EPS for >5 minutes

### Latency
- **p50**: ≤100ms end-to-end
- **p95**: ≤500ms end-to-end
- **p99**: ≤1000ms end-to-end
- **Measurement**: Time from ingestion to load complete
- **Alert threshold**: p95 >750ms for >10 minutes

### Availability
- **Target**: 99.9% uptime (≤43 minutes downtime per month)
- **Measurement**: Pipeline health check returns 200 OK
- **Alert**: Any health check failure

## Data Quality SLAs

### Error Rate
- **Target**: ≤0.1% of events rejected
- **Measurement**: (rejected_events / total_events) × 100
- **Alert threshold**: >0.5% error rate for >15 minutes

### Data Completeness
- **Target**: 100% of required fields present
- **Measurement**: Schema validation pass rate
- **Alert**: Required field missing rate >0.01%

### Data Freshness
- **Target**: Events processed within 5 minutes of ingestion
- **Measurement**: (current_time - event.timestamp) at load stage
- **Alert threshold**: Average age >10 minutes

## Operational SLAs

### Recovery Time Objective (RTO)
- **Target**: ≤15 minutes to restore pipeline after failure
- **Includes**: Automatic retry, manual intervention if needed

### Recovery Point Objective (RPO)
- **Target**: ≤1 minute of data loss
- **Mechanism**: Checkpoint every 60 seconds

### Monitoring Response
- **Critical alerts**: Page on-call within 2 minutes
- **Warning alerts**: Ticket created within 15 minutes
