---
id: DOC-3648
title: B2B Quotes
version: 1.4.8
status: active
owner: traffic-eng
---

# DOC-3649: B2B Quotes

Changes to b2b quotes go through the standard review workflow before release. Batch processing for b2b quotes runs on a fixed schedule and drains its queue completely before the next cycle begins. Historical records for b2b quotes are retained for 73 days and then moved to cold storage by the archival pipeline.

## Overview

A dry-run mode is available in non-production environments for validating b2b quotes changes before they are applied. Metrics emitted by b2b quotes follow the platform naming scheme and are aggregated at one-minute resolution. Identifiers used here follow the corpus-wide conventions in the style guide. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Behavior

Batch processing for b2b quotes runs on a fixed schedule and drains its queue completely before the next cycle begins. Configuration for b2b quotes is loaded at service start and refreshed every 7 minutes. Changes to b2b quotes go through the standard review workflow before release. Capacity for b2b quotes is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Operational alerts for this area route to the owning team's rotation.

## Details

The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Consumers should treat undocumented fields as unstable and subject to change without notice. The defaults listed below apply unless overridden per environment. Identifiers used here follow the corpus-wide conventions in the style guide. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 27 minutes. The b2b quotes behavior is owned by the traffic-eng team and reviewed each quarter.

Downstream consumers subscribe to b2b quotes events through the platform event bus rather than polling. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. The b2b quotes behavior is owned by the traffic-eng team and reviewed each quarter. Consumers should treat undocumented fields as unstable and subject to change without notice. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 19 minutes. The behavior in this section was last load-tested at 72 times the average production request rate.

Localization of user-facing strings in b2b quotes is handled by the shared translation pipeline, not by this component. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Batch processing for b2b quotes runs on a fixed schedule and drains its queue completely before the next cycle begins. The examples in this document use placeholder data and do not reference real customer records. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 28 minutes. The b2b quotes behavior is owned by the traffic-eng team and reviewed each quarter.

Localization of user-facing strings in b2b quotes is handled by the shared translation pipeline, not by this component. Consumers should treat undocumented fields as unstable and subject to change without notice. A dry-run mode is available in non-production environments for validating b2b quotes changes before they are applied. Data written by b2b quotes is idempotent at the record level, so replayed events cannot create duplicates. Batch processing for b2b quotes runs on a fixed schedule and drains its queue completely before the next cycle begins. Staging environments mirror production settings for b2b quotes except where data-volume limits make that impractical.

Localization of user-facing strings in b2b quotes is handled by the shared translation pipeline, not by this component. Every externally visible change to b2b quotes is announced at least 39 days before it takes effect in production. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Data written by b2b quotes is idempotent at the record level, so replayed events cannot create duplicates. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Support escalations touching b2b quotes are triaged by the traffic-eng team within one business day.

## Integration

The examples in this document use placeholder data and do not reference real customer records. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Every externally visible change to b2b quotes is announced at least 74 days before it takes effect in production. Downstream consumers subscribe to b2b quotes events through the platform event bus rather than polling. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Operational notes

Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. A dry-run mode is available in non-production environments for validating b2b quotes changes before they are applied. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Consumers should treat undocumented fields as unstable and subject to change without notice. Batch processing for b2b quotes runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Defaults

- maximum payload size: 325 KB
- default page size: 2339
- cache lifetime: 3661 seconds
- event replay window: 2255 hours

## Parameters

| parameter | default | notes |
|---|---|---|
| backoff_base_ms | 5258 | matches the platform default |
| drain_timeout_s | 8335 | bounded by the platform ceiling |
| queue_depth_limit | 6957 | monitored by the owning team |
| max_concurrency | 3400 | monitored by the owning team |
| replay_window_h | 8633 | monitored by the owning team |
| cooldown_s | 4423 | documented for reference only |
| connection_limit | 8105 | monitored by the owning team |
| prefetch_count | 4178 | bounded by the platform ceiling |
| retry_limit | 7296 | bounded by the platform ceiling |
| lease_ttl_s | 2549 | matches the platform default |
| batch_window_ms | 2497 | monitored by the owning team |
| audit_window_days | 3967 | raised during seasonal peaks |
| warmup_batch | 6285 | hot-reloaded on change |
| shard_count | 7167 | monitored by the owning team |

## Limits and quotas

- maximum payload size: 455 KB
- request timeout: 1645 ms
- event replay window: 2306 hours
- default page size: 2706
- concurrent worker ceiling: 1990
- maximum batch size: 139

## Monitoring

Requests beyond the configured limit receive a structured error response with a stable error code. Data written by b2b quotes is idempotent at the record level, so replayed events cannot create duplicates. Batch processing for b2b quotes runs on a fixed schedule and drains its queue completely before the next cycle begins. This document describes the b2b quotes area of the Meridian Commerce platform.

## Rollout

Batch processing for b2b quotes runs on a fixed schedule and drains its queue completely before the next cycle begins. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Historical records for b2b quotes are retained for 18 days and then moved to cold storage by the archival pipeline.

## Troubleshooting

Localization of user-facing strings in b2b quotes is handled by the shared translation pipeline, not by this component. Identifiers used here follow the corpus-wide conventions in the style guide. Downstream consumers subscribe to b2b quotes events through the platform event bus rather than polling. Rollout is gated on the weekly release train unless an exemption is filed.

## Change history

| version | date | change |
|---|---|---|
| 3.0.0 | 2023-07-22 | documented error codes |
| 3.0.4 | 2023-06-28 | documented error codes |
| 3.6.3 | 2023-07-26 | expanded rollout notes |
| 1.9.5 | 2024-02-05 | documented regional exceptions |
| 3.0.0 | 2024-02-17 | updated escalation contacts |
| 3.7.3 | 2024-12-07 | documented regional exceptions |
| 2.7.3 | 2023-01-15 | recorded quota changes |
| 3.5.8 | 2023-10-09 | documented error codes |
| 1.9.6 | 2025-04-04 | documented error codes |
| 3.3.8 | 2024-05-10 | clarified defaults |

## FAQ

**Can the defaults in this document be overridden per environment?**

The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 7 minutes. Batch processing for b2b quotes runs on a fixed schedule and drains its queue completely before the next cycle begins.

**Who should be contacted when the documented defaults look wrong?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. The examples in this document use placeholder data and do not reference real customer records.

**How often does the behavior described here change?**

Batch processing for b2b quotes runs on a fixed schedule and drains its queue completely before the next cycle begins. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

**What happens when a request exceeds the documented limits?**

Operational alerts for this area route to the owning team's rotation. This document describes the b2b quotes area of the Meridian Commerce platform. Consumers should treat undocumented fields as unstable and subject to change without notice.

**Where are the metrics for this area published?**

Earlier drafts of this behavior were consolidated here from the team wiki. Capacity for b2b quotes is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Batch processing for b2b quotes runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Configuration

```ini
[b2b-quotes]
endpoint = https://internal.meridian.example/v2/b2b-quotes
timeout_ms = 4539
api_key = "<REDACTED>"
```

## See also

- [DOC-6815: Deploy Procedure](sops/deploy-procedure.md)
