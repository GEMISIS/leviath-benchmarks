---
id: DOC-4315
title: Wishlist Sharing
version: 1.0.7
status: active
owner: platform-core
---

# DOC-4315: Wishlist Sharing

Every externally visible change to wishlist sharing is announced at least 86 days before it takes effect in production. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. The behavior in this section was last load-tested at 86 times the average production request rate.

## Overview

A dry-run mode is available in non-production environments for validating wishlist sharing changes before they are applied. The examples in this document use placeholder data and do not reference real customer records. Downstream consumers subscribe to wishlist sharing events through the platform event bus rather than polling. Rollout is gated on the weekly release train unless an exemption is filed.

## Behavior

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 77 minutes. Historical records for wishlist sharing are retained for 79 days and then moved to cold storage by the archival pipeline. A dry-run mode is available in non-production environments for validating wishlist sharing changes before they are applied. Batch processing for wishlist sharing runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Details

Earlier drafts of this behavior were consolidated here from the team wiki. The defaults listed below apply unless overridden per environment. Every externally visible change to wishlist sharing is announced at least 27 days before it takes effect in production. The behavior in this section was last load-tested at 15 times the average production request rate. The wishlist sharing behavior is owned by the platform-core team and reviewed each quarter. Metrics emitted by wishlist sharing follow the platform naming scheme and are aggregated at one-minute resolution.

Operational alerts for this area route to the owning team's rotation. Identifiers used here follow the corpus-wide conventions in the style guide. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Localization of user-facing strings in wishlist sharing is handled by the shared translation pipeline, not by this component. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Requests beyond the configured limit receive a structured error response with a stable error code.

Localization of user-facing strings in wishlist sharing is handled by the shared translation pipeline, not by this component. Every externally visible change to wishlist sharing is announced at least 54 days before it takes effect in production. Configuration for wishlist sharing is loaded at service start and refreshed every 84 minutes. Changes to wishlist sharing go through the standard review workflow before release. Operational alerts for this area route to the owning team's rotation. Metrics emitted by wishlist sharing follow the platform naming scheme and are aggregated at one-minute resolution.

Requests beyond the configured limit receive a structured error response with a stable error code. A dry-run mode is available in non-production environments for validating wishlist sharing changes before they are applied. Configuration for wishlist sharing is loaded at service start and refreshed every 37 minutes. Identifiers used here follow the corpus-wide conventions in the style guide. Metrics emitted by wishlist sharing follow the platform naming scheme and are aggregated at one-minute resolution. Historical records for wishlist sharing are retained for 38 days and then moved to cold storage by the archival pipeline.

Staging environments mirror production settings for wishlist sharing except where data-volume limits make that impractical. Identifiers used here follow the corpus-wide conventions in the style guide. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The wishlist sharing behavior is owned by the platform-core team and reviewed each quarter. Data written by wishlist sharing is idempotent at the record level, so replayed events cannot create duplicates. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 46 minutes.

## Integration

Historical records for wishlist sharing are retained for 74 days and then moved to cold storage by the archival pipeline. Downstream consumers subscribe to wishlist sharing events through the platform event bus rather than polling. This document describes the wishlist sharing area of the Meridian Commerce platform. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 42 minutes. Requests beyond the configured limit receive a structured error response with a stable error code.

## Operational notes

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 67 minutes. Historical records for wishlist sharing are retained for 87 days and then moved to cold storage by the archival pipeline. Batch processing for wishlist sharing runs on a fixed schedule and drains its queue completely before the next cycle begins. The defaults listed below apply unless overridden per environment. Downstream consumers subscribe to wishlist sharing events through the platform event bus rather than polling.

## Defaults

- cache lifetime: 1341 seconds
- retry budget: 492 attempts
- default page size: 2524
- soft quota per client: 2782 per hour

## Parameters

| parameter | default | notes |
|---|---|---|
| max_payload_kb | 1804 | requires restart to change |
| drain_timeout_s | 3265 | bounded by the platform ceiling |
| sample_rate_pct | 2159 | requires restart to change |
| replay_window_h | 3463 | hot-reloaded on change |
| batch_window_ms | 3204 | bounded by the platform ceiling |
| shard_count | 6118 | monitored by the owning team |
| warmup_batch | 489 | raised during seasonal peaks |
| cooldown_s | 4741 | tunable per environment |
| lease_ttl_s | 5500 | requires restart to change |
| page_size | 5243 | documented for reference only |
| queue_depth_limit | 7044 | hot-reloaded on change |

## Limits and quotas

- default page size: 882
- maximum payload size: 2051 KB
- warm-up period after deploy: 1669 seconds
- concurrent worker ceiling: 1442
- event replay window: 556 hours
- maximum batch size: 1803
- cache lifetime: 1114 seconds

## Monitoring

Requests beyond the configured limit receive a structured error response with a stable error code. Every externally visible change to wishlist sharing is announced at least 33 days before it takes effect in production. Batch processing for wishlist sharing runs on a fixed schedule and drains its queue completely before the next cycle begins. Configuration for wishlist sharing is loaded at service start and refreshed every 73 minutes.

## Rollout

Identifiers used here follow the corpus-wide conventions in the style guide. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Downstream consumers subscribe to wishlist sharing events through the platform event bus rather than polling.

## Troubleshooting

The behavior in this section was last load-tested at 50 times the average production request rate. Consumers should treat undocumented fields as unstable and subject to change without notice. The defaults listed below apply unless overridden per environment. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list.

## Change history

| version | date | change |
|---|---|---|
| 3.1.5 | 2025-11-16 | updated escalation contacts |
| 1.7.9 | 2023-11-25 | documented regional exceptions |
| 1.3.2 | 2023-03-20 | expanded rollout notes |
| 2.1.8 | 2025-06-13 | refreshed examples |
| 2.0.5 | 2024-01-03 | updated escalation contacts |
| 3.3.5 | 2023-04-07 | documented error codes |
| 2.6.4 | 2023-04-25 | refreshed examples |
| 3.1.3 | 2025-04-23 | added monitoring guidance |

## FAQ

**Does this area behave differently in staging than in production?**

The examples in this document use placeholder data and do not reference real customer records. Operational alerts for this area route to the owning team's rotation. Identifiers used here follow the corpus-wide conventions in the style guide.

**Where are the metrics for this area published?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 28 minutes. The defaults listed below apply unless overridden per environment. Configuration for wishlist sharing is loaded at service start and refreshed every 5 minutes.

**How far back can historical data for this area be retrieved?**

Capacity for wishlist sharing is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly.

**Is there a dry-run mode for validating changes in this area?**

Consumers should treat undocumented fields as unstable and subject to change without notice. Localization of user-facing strings in wishlist sharing is handled by the shared translation pipeline, not by this component. Operational alerts for this area route to the owning team's rotation.

**Can the defaults in this document be overridden per environment?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Downstream consumers subscribe to wishlist sharing events through the platform event bus rather than polling. Data written by wishlist sharing is idempotent at the record level, so replayed events cannot create duplicates.

**Who should be contacted when the documented defaults look wrong?**

Requests beyond the configured limit receive a structured error response with a stable error code. Capacity for wishlist sharing is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## See also

- [DOC-8092: Alert Triage](sops/alert-triage.md)
