---
id: DOC-9735
title: Partial Shipments
version: 2.3.0
status: active
owner: storefront
---

# DOC-9735: Partial Shipments

Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. This document describes the partial shipments area of the Meridian Commerce platform.

## Overview

Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code. Historical records for partial shipments are retained for 44 days and then moved to cold storage by the archival pipeline. Downstream consumers subscribe to partial shipments events through the platform event bus rather than polling.

## Behavior

The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Changes to partial shipments go through the standard review workflow before release. Batch processing for partial shipments runs on a fixed schedule and drains its queue completely before the next cycle begins. Capacity for partial shipments is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly.

## Details

The partial shipments behavior is owned by the storefront team and reviewed each quarter. Requests beyond the configured limit receive a structured error response with a stable error code. Rollout is gated on the weekly release train unless an exemption is filed. Metrics emitted by partial shipments follow the platform naming scheme and are aggregated at one-minute resolution. A dry-run mode is available in non-production environments for validating partial shipments changes before they are applied. Support escalations touching partial shipments are triaged by the storefront team within one business day.

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Localization of user-facing strings in partial shipments is handled by the shared translation pipeline, not by this component. Earlier drafts of this behavior were consolidated here from the team wiki. Metrics emitted by partial shipments follow the platform naming scheme and are aggregated at one-minute resolution. Requests beyond the configured limit receive a structured error response with a stable error code. The partial shipments behavior is owned by the storefront team and reviewed each quarter.

Earlier drafts of this behavior were consolidated here from the team wiki. The behavior in this section was last load-tested at 33 times the average production request rate. Rollout is gated on the weekly release train unless an exemption is filed. Downstream consumers subscribe to partial shipments events through the platform event bus rather than polling. Operational alerts for this area route to the owning team's rotation. Support escalations touching partial shipments are triaged by the storefront team within one business day.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Downstream consumers subscribe to partial shipments events through the platform event bus rather than polling. Operational alerts for this area route to the owning team's rotation. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 88 minutes. Configuration for partial shipments is loaded at service start and refreshed every 66 minutes.

The partial shipments behavior is owned by the storefront team and reviewed each quarter. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 53 minutes. Localization of user-facing strings in partial shipments is handled by the shared translation pipeline, not by this component. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Rollout is gated on the weekly release train unless an exemption is filed. Every externally visible change to partial shipments is announced at least 45 days before it takes effect in production.

## Integration

Earlier drafts of this behavior were consolidated here from the team wiki. Downstream consumers subscribe to partial shipments events through the platform event bus rather than polling. The defaults listed below apply unless overridden per environment. Batch processing for partial shipments runs on a fixed schedule and drains its queue completely before the next cycle begins. Data written by partial shipments is idempotent at the record level, so replayed events cannot create duplicates.

## Operational notes

Earlier drafts of this behavior were consolidated here from the team wiki. Support escalations touching partial shipments are triaged by the storefront team within one business day. This document describes the partial shipments area of the Meridian Commerce platform. Metrics emitted by partial shipments follow the platform naming scheme and are aggregated at one-minute resolution. The partial shipments behavior is owned by the storefront team and reviewed each quarter.

## Defaults

- default page size: 1971
- queue depth alert threshold: 3474
- burst allowance: 1694 requests

## Parameters

| parameter | default | notes |
|---|---|---|
| drain_timeout_s | 5708 | matches the platform default |
| replay_window_h | 1978 | matches the platform default |
| flush_interval_s | 1120 | tunable per environment |
| queue_depth_limit | 283 | hot-reloaded on change |
| warmup_batch | 7812 | raised during seasonal peaks |
| retry_limit | 1524 | documented for reference only |
| lease_ttl_s | 8616 | raised during seasonal peaks |
| max_concurrency | 6553 | raised during seasonal peaks |
| max_payload_kb | 7540 | tunable per environment |
| prefetch_count | 154 | requires restart to change |

## Limits and quotas

- maximum payload size: 2563 KB
- request timeout: 3931 ms
- concurrent worker ceiling: 1537
- warm-up period after deploy: 314 seconds
- burst allowance: 482 requests
- event replay window: 117 hours
- cache lifetime: 1728 seconds

## Monitoring

This document describes the partial shipments area of the Meridian Commerce platform. Earlier drafts of this behavior were consolidated here from the team wiki. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly.

## Rollout

This document describes the partial shipments area of the Meridian Commerce platform. Data written by partial shipments is idempotent at the record level, so replayed events cannot create duplicates. Changes to partial shipments go through the standard review workflow before release. Historical records for partial shipments are retained for 53 days and then moved to cold storage by the archival pipeline.

## Troubleshooting

Localization of user-facing strings in partial shipments is handled by the shared translation pipeline, not by this component. Consumers should treat undocumented fields as unstable and subject to change without notice. Staging environments mirror production settings for partial shipments except where data-volume limits make that impractical. Support escalations touching partial shipments are triaged by the storefront team within one business day.

## Change history

| version | date | change |
|---|---|---|
| 2.4.3 | 2025-05-20 | documented regional exceptions |
| 1.5.4 | 2024-11-23 | added monitoring guidance |
| 1.1.7 | 2024-03-10 | expanded rollout notes |
| 1.2.0 | 2023-09-06 | expanded rollout notes |
| 2.0.1 | 2024-05-11 | added monitoring guidance |
| 3.0.9 | 2023-09-01 | expanded rollout notes |
| 2.1.3 | 2024-06-27 | recorded quota changes |
| 1.3.6 | 2024-04-04 | recorded quota changes |
| 1.7.3 | 2025-02-03 | recorded quota changes |

## FAQ

**Does this area behave differently in staging than in production?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 69 minutes. Rollout is gated on the weekly release train unless an exemption is filed. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly.

**What happens when a request exceeds the documented limits?**

A dry-run mode is available in non-production environments for validating partial shipments changes before they are applied. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 23 minutes.

**Who should be contacted when the documented defaults look wrong?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Historical records for partial shipments are retained for 20 days and then moved to cold storage by the archival pipeline. Batch processing for partial shipments runs on a fixed schedule and drains its queue completely before the next cycle begins.

**How far back can historical data for this area be retrieved?**

The defaults listed below apply unless overridden per environment. Operational alerts for this area route to the owning team's rotation. A dry-run mode is available in non-production environments for validating partial shipments changes before they are applied.

## See also

- [DOC-4256: Pagination Rules](api/pagination-rules.md)
