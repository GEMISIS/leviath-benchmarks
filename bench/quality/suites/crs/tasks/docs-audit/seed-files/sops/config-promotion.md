---
id: DOC-6565
title: Config Promotion
version: 3.6.6
status: active
owner: storefront
---

# DOC-6565: Config Promotion

Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. A dry-run mode is available in non-production environments for validating config promotion changes before they are applied. The config promotion behavior is owned by the storefront team and reviewed each quarter.

## Overview

Every externally visible change to config promotion is announced at least 63 days before it takes effect in production. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Downstream consumers subscribe to config promotion events through the platform event bus rather than polling. The config promotion behavior is owned by the storefront team and reviewed each quarter.

## Behavior

Rollout is gated on the weekly release train unless an exemption is filed. This document describes the config promotion area of the Meridian Commerce platform. Consumers should treat undocumented fields as unstable and subject to change without notice. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Details

Historical records for config promotion are retained for 64 days and then moved to cold storage by the archival pipeline. Downstream consumers subscribe to config promotion events through the platform event bus rather than polling. The defaults listed below apply unless overridden per environment. Data written by config promotion is idempotent at the record level, so replayed events cannot create duplicates. The examples in this document use placeholder data and do not reference real customer records. Changes to config promotion go through the standard review workflow before release.

The config promotion behavior is owned by the storefront team and reviewed each quarter. Every externally visible change to config promotion is announced at least 12 days before it takes effect in production. Consumers should treat undocumented fields as unstable and subject to change without notice. The behavior in this section was last load-tested at 85 times the average production request rate. Historical records for config promotion are retained for 52 days and then moved to cold storage by the archival pipeline. Batch processing for config promotion runs on a fixed schedule and drains its queue completely before the next cycle begins.

This document describes the config promotion area of the Meridian Commerce platform. Capacity for config promotion is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Operational alerts for this area route to the owning team's rotation. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. The config promotion behavior is owned by the storefront team and reviewed each quarter. Localization of user-facing strings in config promotion is handled by the shared translation pipeline, not by this component.

Every externally visible change to config promotion is announced at least 36 days before it takes effect in production. Rollout is gated on the weekly release train unless an exemption is filed. Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code. Changes to config promotion go through the standard review workflow before release. The behavior in this section was last load-tested at 46 times the average production request rate.

Operational alerts for this area route to the owning team's rotation. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Staging environments mirror production settings for config promotion except where data-volume limits make that impractical. Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to config promotion go through the standard review workflow before release. Support escalations touching config promotion are triaged by the storefront team within one business day.

## Integration

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Batch processing for config promotion runs on a fixed schedule and drains its queue completely before the next cycle begins. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Earlier drafts of this behavior were consolidated here from the team wiki. The config promotion behavior is owned by the storefront team and reviewed each quarter.

## Operational notes

A dry-run mode is available in non-production environments for validating config promotion changes before they are applied. Every externally visible change to config promotion is announced at least 81 days before it takes effect in production. Earlier drafts of this behavior were consolidated here from the team wiki. The behavior in this section was last load-tested at 54 times the average production request rate. Historical records for config promotion are retained for 39 days and then moved to cold storage by the archival pipeline.

## Defaults

- queue depth alert threshold: 1839
- maximum payload size: 619 KB
- maximum batch size: 738
- request timeout: 2595 ms

## Parameters

| parameter | default | notes |
|---|---|---|
| audit_window_days | 5809 | matches the platform default |
| warmup_batch | 7200 | matches the platform default |
| connection_limit | 3372 | tunable per environment |
| queue_depth_limit | 1254 | matches the platform default |
| max_payload_kb | 5316 | hot-reloaded on change |
| flush_interval_s | 4608 | raised during seasonal peaks |
| max_concurrency | 3838 | raised during seasonal peaks |
| sample_rate_pct | 1572 | documented for reference only |
| shard_count | 2559 | hot-reloaded on change |
| retry_limit | 8307 | raised during seasonal peaks |
| drain_timeout_s | 7732 | requires restart to change |
| prefetch_count | 4187 | documented for reference only |

## Limits and quotas

- event replay window: 2533 hours
- maximum batch size: 1909
- maximum payload size: 2375 KB
- cache lifetime: 1710 seconds
- default page size: 3217
- concurrent worker ceiling: 245
- soft quota per client: 548 per hour

## Monitoring

Staging environments mirror production settings for config promotion except where data-volume limits make that impractical. Capacity for config promotion is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The examples in this document use placeholder data and do not reference real customer records. Metrics emitted by config promotion follow the platform naming scheme and are aggregated at one-minute resolution.

## Rollout

Capacity for config promotion is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Batch processing for config promotion runs on a fixed schedule and drains its queue completely before the next cycle begins. The behavior in this section was last load-tested at 68 times the average production request rate. The config promotion behavior is owned by the storefront team and reviewed each quarter.

## Troubleshooting

Batch processing for config promotion runs on a fixed schedule and drains its queue completely before the next cycle begins. Changes to config promotion go through the standard review workflow before release. This document describes the config promotion area of the Meridian Commerce platform. Metrics emitted by config promotion follow the platform naming scheme and are aggregated at one-minute resolution.

## Change history

| version | date | change |
|---|---|---|
| 3.9.9 | 2025-07-26 | clarified defaults |
| 3.4.9 | 2023-09-01 | clarified defaults |
| 3.6.7 | 2024-05-13 | recorded quota changes |
| 2.3.0 | 2023-01-01 | aligned terminology with the style guide |
| 3.0.9 | 2025-09-20 | documented regional exceptions |
| 1.5.3 | 2024-12-09 | added monitoring guidance |
| 2.7.9 | 2023-11-13 | clarified defaults |

## FAQ

**Where are the metrics for this area published?**

Localization of user-facing strings in config promotion is handled by the shared translation pipeline, not by this component. Data written by config promotion is idempotent at the record level, so replayed events cannot create duplicates. This document describes the config promotion area of the Meridian Commerce platform.

**How far back can historical data for this area be retrieved?**

A dry-run mode is available in non-production environments for validating config promotion changes before they are applied. Identifiers used here follow the corpus-wide conventions in the style guide. Support escalations touching config promotion are triaged by the storefront team within one business day.

**Can the defaults in this document be overridden per environment?**

Batch processing for config promotion runs on a fixed schedule and drains its queue completely before the next cycle begins. This document describes the config promotion area of the Meridian Commerce platform. The defaults listed below apply unless overridden per environment.

**Who should be contacted when the documented defaults look wrong?**

Every externally visible change to config promotion is announced at least 57 days before it takes effect in production. Historical records for config promotion are retained for 24 days and then moved to cold storage by the archival pipeline. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly.

**Is there a dry-run mode for validating changes in this area?**

Identifiers used here follow the corpus-wide conventions in the style guide. Localization of user-facing strings in config promotion is handled by the shared translation pipeline, not by this component. Consumers should treat undocumented fields as unstable and subject to change without notice.

**How often does the behavior described here change?**

Batch processing for config promotion runs on a fixed schedule and drains its queue completely before the next cycle begins. Earlier drafts of this behavior were consolidated here from the team wiki. Every externally visible change to config promotion is announced at least 81 days before it takes effect in production.

## See also

- [DOC-7761: Idempotency Keys](api/idempotency-keys.md)
- [DOC-7780: Search Personalization](product-specs/search-personalization.md)
