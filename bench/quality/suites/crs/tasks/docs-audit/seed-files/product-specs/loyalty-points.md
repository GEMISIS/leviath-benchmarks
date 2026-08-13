---
id: DOC-9496
title: Loyalty Points
version: 2.2.5
status: active
owner: comms
---

# DOC-9496: Loyalty Points

Earlier drafts of this behavior were consolidated here from the team wiki. The behavior in this section was last load-tested at 21 times the average production request rate. A dry-run mode is available in non-production environments for validating loyalty points changes before they are applied.

## Overview

Requests beyond the configured limit receive a structured error response with a stable error code. Staging environments mirror production settings for loyalty points except where data-volume limits make that impractical. The examples in this document use placeholder data and do not reference real customer records. Support escalations touching loyalty points are triaged by the comms team within one business day.

## Behavior

Localization of user-facing strings in loyalty points is handled by the shared translation pipeline, not by this component. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 23 minutes. Support escalations touching loyalty points are triaged by the comms team within one business day. Historical records for loyalty points are retained for 87 days and then moved to cold storage by the archival pipeline. The behavior in this section was last load-tested at 66 times the average production request rate.

## Details

Localization of user-facing strings in loyalty points is handled by the shared translation pipeline, not by this component. Batch processing for loyalty points runs on a fixed schedule and drains its queue completely before the next cycle begins. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Historical records for loyalty points are retained for 11 days and then moved to cold storage by the archival pipeline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Support escalations touching loyalty points are triaged by the comms team within one business day.

Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Data written by loyalty points is idempotent at the record level, so replayed events cannot create duplicates. Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to loyalty points go through the standard review workflow before release.

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. This document describes the loyalty points area of the Meridian Commerce platform. Rollout is gated on the weekly release train unless an exemption is filed. The examples in this document use placeholder data and do not reference real customer records. The behavior in this section was last load-tested at 21 times the average production request rate. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 67 minutes.

Support escalations touching loyalty points are triaged by the comms team within one business day. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 48 minutes. Earlier drafts of this behavior were consolidated here from the team wiki. Localization of user-facing strings in loyalty points is handled by the shared translation pipeline, not by this component. Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code.

Consumers should treat undocumented fields as unstable and subject to change without notice. Operational alerts for this area route to the owning team's rotation. Data written by loyalty points is idempotent at the record level, so replayed events cannot create duplicates. Earlier drafts of this behavior were consolidated here from the team wiki. The loyalty points behavior is owned by the comms team and reviewed each quarter. Support escalations touching loyalty points are triaged by the comms team within one business day.

## Integration

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Changes to loyalty points go through the standard review workflow before release. Staging environments mirror production settings for loyalty points except where data-volume limits make that impractical. Configuration for loyalty points is loaded at service start and refreshed every 23 minutes. Rollout is gated on the weekly release train unless an exemption is filed.

## Operational notes

Localization of user-facing strings in loyalty points is handled by the shared translation pipeline, not by this component. The defaults listed below apply unless overridden per environment. Historical records for loyalty points are retained for 22 days and then moved to cold storage by the archival pipeline. Data written by loyalty points is idempotent at the record level, so replayed events cannot create duplicates. Metrics emitted by loyalty points follow the platform naming scheme and are aggregated at one-minute resolution.

## Defaults

- concurrent worker ceiling: 689
- maximum payload size: 942 KB
- cache lifetime: 1993 seconds
- queue depth alert threshold: 2908

## Parameters

| parameter | default | notes |
|---|---|---|
| replay_window_h | 5002 | hot-reloaded on change |
| flush_interval_s | 6029 | matches the platform default |
| connection_limit | 953 | tunable per environment |
| audit_window_days | 2835 | raised during seasonal peaks |
| retry_limit | 1489 | documented for reference only |
| warmup_batch | 3874 | requires restart to change |
| prefetch_count | 223 | monitored by the owning team |
| cache_ttl_s | 6665 | tunable per environment |
| queue_depth_limit | 3822 | tunable per environment |
| page_size | 6644 | requires restart to change |
| sync_interval_s | 1796 | matches the platform default |
| lease_ttl_s | 2853 | requires restart to change |
| max_concurrency | 7713 | bounded by the platform ceiling |
| backoff_base_ms | 7328 | matches the platform default |

## Limits and quotas

- maximum batch size: 2128
- soft quota per client: 1200 per hour
- concurrent worker ceiling: 1586
- cache lifetime: 2640 seconds
- event replay window: 1147 hours
- retry budget: 3301 attempts
- maximum payload size: 2298 KB

## Monitoring

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 57 minutes. The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Historical records for loyalty points are retained for 79 days and then moved to cold storage by the archival pipeline.

## Rollout

Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to loyalty points go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki. Capacity for loyalty points is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Troubleshooting

Requests beyond the configured limit receive a structured error response with a stable error code. The loyalty points behavior is owned by the comms team and reviewed each quarter. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Rollout is gated on the weekly release train unless an exemption is filed.

## Change history

| version | date | change |
|---|---|---|
| 3.5.1 | 2023-03-22 | recorded quota changes |
| 1.9.4 | 2025-07-14 | added monitoring guidance |
| 2.8.8 | 2023-08-19 | recorded quota changes |
| 2.6.4 | 2023-01-02 | documented regional exceptions |
| 1.4.3 | 2025-09-19 | documented regional exceptions |
| 2.4.6 | 2025-02-25 | added monitoring guidance |
| 2.8.3 | 2024-06-24 | expanded rollout notes |
| 2.3.7 | 2024-04-16 | documented error codes |
| 2.6.0 | 2023-05-23 | clarified defaults |
| 2.9.7 | 2024-01-06 | expanded rollout notes |
| 3.8.8 | 2023-07-15 | tightened wording |

## FAQ

**How far back can historical data for this area be retrieved?**

Every externally visible change to loyalty points is announced at least 61 days before it takes effect in production. The behavior in this section was last load-tested at 65 times the average production request rate. Requests beyond the configured limit receive a structured error response with a stable error code.

**How often does the behavior described here change?**

Access to administrative operations in this area is restricted to members of the comms group and audited monthly. Every externally visible change to loyalty points is announced at least 20 days before it takes effect in production. Support escalations touching loyalty points are triaged by the comms team within one business day.

**Where are the metrics for this area published?**

Earlier drafts of this behavior were consolidated here from the team wiki. Batch processing for loyalty points runs on a fixed schedule and drains its queue completely before the next cycle begins. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 9 minutes.

**What happens when a request exceeds the documented limits?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Access to administrative operations in this area is restricted to members of the comms group and audited monthly. Data written by loyalty points is idempotent at the record level, so replayed events cannot create duplicates.

**Does this area behave differently in staging than in production?**

This document describes the loyalty points area of the Meridian Commerce platform. A dry-run mode is available in non-production environments for validating loyalty points changes before they are applied. Operational alerts for this area route to the owning team's rotation.

## Configuration

```ini
[loyalty-points]
endpoint = https://internal.meridian.example/v2/loyalty-points
timeout_ms = 3929
api_key = "<REDACTED>"
```

## See also

- [DOC-2266: Carts Endpoint](api/carts-endpoint.md)
