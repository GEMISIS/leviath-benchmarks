---
id: DOC-6678
title: Saved Payment Methods
version: 1.8.3
status: active
owner: traffic-eng
---

# DOC-6678: Saved Payment Methods

A dry-run mode is available in non-production environments for validating saved payment methods changes before they are applied. Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for saved payment methods is loaded at service start and refreshed every 24 minutes.

## Overview

Metrics emitted by saved payment methods follow the platform naming scheme and are aggregated at one-minute resolution. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Capacity for saved payment methods is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. This document describes the saved payment methods area of the Meridian Commerce platform.

## Behavior

Consumers should treat undocumented fields as unstable and subject to change without notice. The defaults listed below apply unless overridden per environment. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. This document describes the saved payment methods area of the Meridian Commerce platform. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list.

## Details

This document describes the saved payment methods area of the Meridian Commerce platform. Support escalations touching saved payment methods are triaged by the traffic-eng team within one business day. Earlier drafts of this behavior were consolidated here from the team wiki. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Batch processing for saved payment methods runs on a fixed schedule and drains its queue completely before the next cycle begins. Configuration for saved payment methods is loaded at service start and refreshed every 56 minutes.

Localization of user-facing strings in saved payment methods is handled by the shared translation pipeline, not by this component. The examples in this document use placeholder data and do not reference real customer records. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 76 minutes. Historical records for saved payment methods are retained for 77 days and then moved to cold storage by the archival pipeline. Every externally visible change to saved payment methods is announced at least 27 days before it takes effect in production. Consumers should treat undocumented fields as unstable and subject to change without notice.

Support escalations touching saved payment methods are triaged by the traffic-eng team within one business day. The defaults listed below apply unless overridden per environment. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Rollout is gated on the weekly release train unless an exemption is filed. A dry-run mode is available in non-production environments for validating saved payment methods changes before they are applied. Metrics emitted by saved payment methods follow the platform naming scheme and are aggregated at one-minute resolution.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Configuration for saved payment methods is loaded at service start and refreshed every 63 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Localization of user-facing strings in saved payment methods is handled by the shared translation pipeline, not by this component. Rollout is gated on the weekly release train unless an exemption is filed. A dry-run mode is available in non-production environments for validating saved payment methods changes before they are applied.

Identifiers used here follow the corpus-wide conventions in the style guide. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Capacity for saved payment methods is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Earlier drafts of this behavior were consolidated here from the team wiki. This document describes the saved payment methods area of the Meridian Commerce platform. A dry-run mode is available in non-production environments for validating saved payment methods changes before they are applied.

## Integration

Historical records for saved payment methods are retained for 28 days and then moved to cold storage by the archival pipeline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Every externally visible change to saved payment methods is announced at least 12 days before it takes effect in production. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Configuration for saved payment methods is loaded at service start and refreshed every 52 minutes.

## Operational notes

Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice. The behavior in this section was last load-tested at 50 times the average production request rate. Earlier drafts of this behavior were consolidated here from the team wiki. The defaults listed below apply unless overridden per environment.

## Defaults

- warm-up period after deploy: 1264 seconds
- maximum payload size: 3799 KB
- soft quota per client: 1146 per hour

## Parameters

| parameter | default | notes |
|---|---|---|
| batch_window_ms | 5725 | documented for reference only |
| cache_ttl_s | 4873 | matches the platform default |
| page_size | 7079 | monitored by the owning team |
| flush_interval_s | 7467 | monitored by the owning team |
| shard_count | 828 | matches the platform default |
| queue_depth_limit | 8755 | hot-reloaded on change |
| sample_rate_pct | 6769 | matches the platform default |
| lease_ttl_s | 2237 | raised during seasonal peaks |
| prefetch_count | 3794 | monitored by the owning team |
| connection_limit | 5809 | matches the platform default |
| warmup_batch | 5533 | raised during seasonal peaks |

## Limits and quotas

- request timeout: 1924 ms
- cache lifetime: 155 seconds
- retry budget: 1074 attempts
- maximum batch size: 1757
- burst allowance: 2944 requests
- maximum payload size: 3215 KB
- warm-up period after deploy: 2483 seconds
- soft quota per client: 3168 per hour

## Monitoring

The saved payment methods behavior is owned by the traffic-eng team and reviewed each quarter. The behavior in this section was last load-tested at 58 times the average production request rate. Localization of user-facing strings in saved payment methods is handled by the shared translation pipeline, not by this component. A dry-run mode is available in non-production environments for validating saved payment methods changes before they are applied.

## Rollout

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Every externally visible change to saved payment methods is announced at least 54 days before it takes effect in production. Changes to saved payment methods go through the standard review workflow before release. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 18 minutes.

## Troubleshooting

Changes to saved payment methods go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki. Configuration for saved payment methods is loaded at service start and refreshed every 59 minutes. Historical records for saved payment methods are retained for 52 days and then moved to cold storage by the archival pipeline.

## Change history

| version | date | change |
|---|---|---|
| 3.9.4 | 2024-02-09 | tightened wording |
| 3.8.9 | 2025-11-19 | refreshed examples |
| 2.9.0 | 2025-11-17 | refreshed examples |
| 2.9.1 | 2023-11-24 | documented regional exceptions |
| 1.8.0 | 2024-11-11 | added monitoring guidance |
| 1.8.5 | 2025-07-01 | documented regional exceptions |
| 3.6.1 | 2025-03-15 | documented regional exceptions |
| 1.3.0 | 2025-02-11 | added monitoring guidance |
| 2.2.6 | 2025-09-13 | clarified defaults |
| 2.9.9 | 2024-08-25 | documented regional exceptions |

## FAQ

**Who should be contacted when the documented defaults look wrong?**

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Configuration for saved payment methods is loaded at service start and refreshed every 40 minutes. Data written by saved payment methods is idempotent at the record level, so replayed events cannot create duplicates.

**Where are the metrics for this area published?**

A dry-run mode is available in non-production environments for validating saved payment methods changes before they are applied. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The examples in this document use placeholder data and do not reference real customer records.

**Can the defaults in this document be overridden per environment?**

Changes to saved payment methods go through the standard review workflow before release. Metrics emitted by saved payment methods follow the platform naming scheme and are aggregated at one-minute resolution. The behavior in this section was last load-tested at 25 times the average production request rate.

**How far back can historical data for this area be retrieved?**

Changes to saved payment methods go through the standard review workflow before release. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Localization of user-facing strings in saved payment methods is handled by the shared translation pipeline, not by this component.

## Configuration

```ini
[saved-payment-methods]
endpoint = https://internal.meridian.example/v2/saved-payment-methods
timeout_ms = 7171
api_key = "<REDACTED>"
```

## See also

- [DOC-8356: Search Endpoint](api/search-endpoint.md)
- [DOC-6231: Cdn Failover](sops/cdn-failover.md)
