# Monitoring Specification

## Metrics to Collect

### Throughput Metrics
```
pipeline_events_processed_total{stage, event_type}
  Type: Counter
  Labels: stage (ingestion|validation|transformation|load), event_type
  Description: Total events processed by stage

pipeline_events_per_second{stage}
  Type: Gauge
  Labels: stage
  Description: Current events per second throughput
```

### Latency Metrics
```
pipeline_latency_seconds{stage, quantile}
  Type: Summary
  Labels: stage, quantile (0.5|0.95|0.99)
  Description: Processing latency by stage

pipeline_end_to_end_latency_seconds{quantile}
  Type: Summary
  Labels: quantile
  Description: Total end-to-end latency
```

### Error Metrics
```
pipeline_errors_total{stage, error_type}
  Type: Counter
  Labels: stage, error_type (validation|transformation|transient|critical)
  Description: Total errors by stage and type

pipeline_error_rate{stage}
  Type: Gauge
  Labels: stage
  Description: Current error rate (errors/events)
```

### Resource Metrics
```
pipeline_memory_usage_bytes{stage}
  Type: Gauge
  Labels: stage
  Description: Memory usage per stage

pipeline_cpu_usage_percent{stage}
  Type: Gauge
  Labels: stage
  Description: CPU usage per stage

pipeline_batch_size{stage}
  Type: Histogram
  Labels: stage
  Description: Batch size distribution
```

## Health Check Endpoint

**Endpoint**: GET `/health`

**Response** (200 OK when healthy):
```json
{
  "status": "healthy",
  "stages": {
    "ingestion": {"status": "ok", "last_event_processed": "2024-01-15T10:30:45Z"},
    "validation": {"status": "ok", "error_rate": 0.0001},
    "transformation": {"status": "ok", "throughput_eps": 12450},
    "load": {"status": "ok", "last_write": "2024-01-15T10:30:46Z"}
  },
  "uptime_seconds": 86400,
  "version": "1.0.0"
}
```

**Response** (503 Service Unavailable when unhealthy):
```json
{
  "status": "unhealthy",
  "errors": ["transformation stage stalled for 5 minutes"],
  "stages": {...}
}
```

## Alert Rules

1. **High Error Rate**: error_rate > 0.005 for 15 minutes → Page
2. **Low Throughput**: eps < 8000 for 5 minutes → Page
3. **High Latency**: p95 > 750ms for 10 minutes → Page
4. **Stage Stalled**: No events processed for 2 minutes → Page
5. **Memory High**: memory > 8GB for 10 minutes → Warn
