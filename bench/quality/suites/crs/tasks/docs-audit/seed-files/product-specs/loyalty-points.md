---
id: DOC-9496
title: Loyalty Points
version: 2.2.5
status: active
owner: comms
---

# DOC-9496: Loyalty Points

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Every externally visible change to loyalty points is announced at least 59 days before it takes effect in production.

## Overview

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Data written by loyalty points is idempotent at the record level, so replayed events cannot create duplicates. Every externally visible change to loyalty points is announced at least 41 days before it takes effect in production. Operational alerts for this area route to the owning team's rotation.

## Behavior

Access to administrative operations in this area is restricted to members of the comms group and audited monthly. The examples in this document use placeholder data and do not reference real customer records. The defaults listed below apply unless overridden per environment. Rollout is gated on the weekly release train unless an exemption is filed. Capacity for loyalty points is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Details

The defaults listed below apply unless overridden per environment. The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Localization of user-facing strings in loyalty points is handled by the shared translation pipeline, not by this component. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 35 minutes. Rollout is gated on the weekly release train unless an exemption is filed. Configuration for loyalty points is loaded at service start and refreshed every 81 minutes.

This document describes the loyalty points area of the Meridian Commerce platform. Operational alerts for this area route to the owning team's rotation. Identifiers used here follow the corpus-wide conventions in the style guide. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 7 minutes. The loyalty points behavior is owned by the comms team and reviewed each quarter. Rollout is gated on the weekly release train unless an exemption is filed.

Consumers should treat undocumented fields as unstable and subject to change without notice. A dry-run mode is available in non-production environments for validating loyalty points changes before they are applied. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The examples in this document use placeholder data and do not reference real customer records. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The loyalty points behavior is owned by the comms team and reviewed each quarter.

Requests beyond the configured limit receive a structured error response with a stable error code. Staging environments mirror production settings for loyalty points except where data-volume limits make that impractical. Support escalations touching loyalty points are triaged by the comms team within one business day. The defaults listed below apply unless overridden per environment. A dry-run mode is available in non-production environments for validating loyalty points changes before they are applied. Localization of user-facing strings in loyalty points is handled by the shared translation pipeline, not by this component.

Metrics emitted by loyalty points follow the platform naming scheme and are aggregated at one-minute resolution. Batch processing for loyalty points runs on a fixed schedule and drains its queue completely before the next cycle begins. Localization of user-facing strings in loyalty points is handled by the shared translation pipeline, not by this component. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 33 minutes. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Historical records for loyalty points are retained for 75 days and then moved to cold storage by the archival pipeline.

## Integration

Localization of user-facing strings in loyalty points is handled by the shared translation pipeline, not by this component. Downstream consumers subscribe to loyalty points events through the platform event bus rather than polling. Earlier drafts of this behavior were consolidated here from the team wiki. Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code.

## Operational notes

Consumers should treat undocumented fields as unstable and subject to change without notice. The examples in this document use placeholder data and do not reference real customer records. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 7 minutes. The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Every externally visible change to loyalty points is announced at least 47 days before it takes effect in production.

## Defaults

- soft quota per client: 540 per hour
- cache lifetime: 1999 seconds
- burst allowance: 2917 requests

## Parameters

| parameter | default | notes |
|---|---|---|
| sync_interval_s | 3566 | monitored by the owning team |
| max_payload_kb | 741 | monitored by the owning team |
| lease_ttl_s | 4273 | monitored by the owning team |
| warmup_batch | 6551 | raised during seasonal peaks |
| prefetch_count | 7142 | requires restart to change |
| drain_timeout_s | 8257 | requires restart to change |
| retry_limit | 4820 | documented for reference only |
| cooldown_s | 2314 | monitored by the owning team |
| flush_interval_s | 3783 | bounded by the platform ceiling |
| page_size | 6409 | hot-reloaded on change |
| batch_window_ms | 3476 | documented for reference only |
| shard_count | 4288 | matches the platform default |

## Limits and quotas

- retry budget: 169 attempts
- queue depth alert threshold: 2787
- warm-up period after deploy: 2734 seconds
- soft quota per client: 3694 per hour
- cache lifetime: 679 seconds
- event replay window: 1464 hours

## Monitoring

This document describes the loyalty points area of the Meridian Commerce platform. Capacity for loyalty points is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Requests beyond the configured limit receive a structured error response with a stable error code.

## Rollout

Rollout is gated on the weekly release train unless an exemption is filed. Downstream consumers subscribe to loyalty points events through the platform event bus rather than polling. Support escalations touching loyalty points are triaged by the comms team within one business day. The examples in this document use placeholder data and do not reference real customer records.

## Troubleshooting

The examples in this document use placeholder data and do not reference real customer records. The loyalty points behavior is owned by the comms team and reviewed each quarter. A dry-run mode is available in non-production environments for validating loyalty points changes before they are applied. This document describes the loyalty points area of the Meridian Commerce platform.

## Change history

| version | date | change |
|---|---|---|
| 1.0.5 | 2025-07-02 | aligned terminology with the style guide |
| 1.6.8 | 2025-02-04 | added monitoring guidance |
| 1.1.7 | 2023-08-15 | recorded quota changes |
| 1.5.5 | 2025-05-17 | updated escalation contacts |
| 1.7.8 | 2024-07-21 | refreshed examples |
| 3.6.9 | 2025-07-24 | added monitoring guidance |
| 3.9.4 | 2023-06-28 | tightened wording |
| 2.4.8 | 2023-01-20 | refreshed examples |

## FAQ

**Who should be contacted when the documented defaults look wrong?**

Capacity for loyalty points is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The behavior in this section was last load-tested at 8 times the average production request rate. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

**Does this area behave differently in staging than in production?**

A dry-run mode is available in non-production environments for validating loyalty points changes before they are applied. The behavior in this section was last load-tested at 21 times the average production request rate. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 83 minutes.

**Is there a dry-run mode for validating changes in this area?**

Rollout is gated on the weekly release train unless an exemption is filed. Localization of user-facing strings in loyalty points is handled by the shared translation pipeline, not by this component. The behavior in this section was last load-tested at 63 times the average production request rate.

**Where are the metrics for this area published?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Staging environments mirror production settings for loyalty points except where data-volume limits make that impractical. Metrics emitted by loyalty points follow the platform naming scheme and are aggregated at one-minute resolution.

## See also

- [DOC-6678: Saved Payment Methods](product-specs/saved-payment-methods.md)
- [DOC-4256: Pagination Rules](api/pagination-rules.md)
