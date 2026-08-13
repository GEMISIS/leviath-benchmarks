---
id: DOC-3686
title: Rate Limits
version: 2.4.0
status: active
owner: storefront
---

# DOC-3686: Rate Limits

Metrics emitted by rate limits follow the platform naming scheme and are aggregated at one-minute resolution. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Rollout is gated on the weekly release train unless an exemption is filed.

## Overview

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 63 minutes. Staging environments mirror production settings for rate limits except where data-volume limits make that impractical. Identifiers used here follow the corpus-wide conventions in the style guide. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Behavior

The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Batch processing for rate limits runs on a fixed schedule and drains its queue completely before the next cycle begins. Downstream consumers subscribe to rate limits events through the platform event bus rather than polling. This document describes the rate limits area of the Meridian Commerce platform.

## Details

Every externally visible change to rate limits is announced at least 39 days before it takes effect in production. Data written by rate limits is idempotent at the record level, so replayed events cannot create duplicates. Rollout is gated on the weekly release train unless an exemption is filed. Identifiers used here follow the corpus-wide conventions in the style guide. Operational alerts for this area route to the owning team's rotation. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list.

Metrics emitted by rate limits follow the platform naming scheme and are aggregated at one-minute resolution. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. This document describes the rate limits area of the Meridian Commerce platform. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Requests beyond the configured limit receive a structured error response with a stable error code. Changes to rate limits go through the standard review workflow before release.

This document describes the rate limits area of the Meridian Commerce platform. Rollout is gated on the weekly release train unless an exemption is filed. Every externally visible change to rate limits is announced at least 83 days before it takes effect in production. The examples in this document use placeholder data and do not reference real customer records. Downstream consumers subscribe to rate limits events through the platform event bus rather than polling. Batch processing for rate limits runs on a fixed schedule and drains its queue completely before the next cycle begins.

Requests beyond the configured limit receive a structured error response with a stable error code. A dry-run mode is available in non-production environments for validating rate limits changes before they are applied. The defaults listed below apply unless overridden per environment. Localization of user-facing strings in rate limits is handled by the shared translation pipeline, not by this component. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Rollout is gated on the weekly release train unless an exemption is filed. Above the sustained rate, bursts are tolerated up to 75 requests in any single second.

Data written by rate limits is idempotent at the record level, so replayed events cannot create duplicates. A dry-run mode is available in non-production environments for validating rate limits changes before they are applied. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Consumers should treat undocumented fields as unstable and subject to change without notice. The behavior in this section was last load-tested at 44 times the average production request rate. Support escalations touching rate limits are triaged by the storefront team within one business day.

## Integration

Rollout is gated on the weekly release train unless an exemption is filed. Staging environments mirror production settings for rate limits except where data-volume limits make that impractical. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Consumers should treat undocumented fields as unstable and subject to change without notice. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 9 minutes.

## Operational notes

The examples in this document use placeholder data and do not reference real customer records. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 14 minutes. The defaults listed below apply unless overridden per environment. Historical records for rate limits are retained for 7 days and then moved to cold storage by the archival pipeline. Identifiers used here follow the corpus-wide conventions in the style guide.

## Defaults

- cache lifetime: 2216 seconds
- queue depth alert threshold: 3278
- warm-up period after deploy: 3648 seconds

## Parameters

| parameter | default | notes |
|---|---|---|
| cache_ttl_s | 8746 | hot-reloaded on change |
| audit_window_days | 6172 | monitored by the owning team |
| warmup_batch | 7261 | monitored by the owning team |
| backoff_base_ms | 6663 | requires restart to change |
| retry_limit | 5216 | matches the platform default |
| max_concurrency | 8040 | hot-reloaded on change |
| flush_interval_s | 5139 | matches the platform default |
| sample_rate_pct | 7802 | documented for reference only |
| connection_limit | 5322 | documented for reference only |
| cooldown_s | 1394 | requires restart to change |
| queue_depth_limit | 7026 | documented for reference only |

## Limits and quotas

- default page size: 908
- queue depth alert threshold: 2056
- cache lifetime: 248 seconds
- soft quota per client: 500 per hour
- request timeout: 30 ms
- maximum batch size: 2340
- retry budget: 1516 attempts
- event replay window: 689 hours

## Monitoring

Changes to rate limits go through the standard review workflow before release. Operational alerts for this area route to the owning team's rotation. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 52 minutes. The rate limits behavior is owned by the storefront team and reviewed each quarter.

## Rollout

Clients are expected to implement exponential backoff when a retryable error is returned by this area. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Troubleshooting

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to rate limits go through the standard review workflow before release. Operational alerts for this area route to the owning team's rotation.

## Change history

| version | date | change |
|---|---|---|
| 3.5.1 | 2025-07-07 | tightened wording |
| 1.8.8 | 2025-06-09 | expanded rollout notes |
| 2.2.5 | 2025-12-09 | added monitoring guidance |
| 1.3.3 | 2023-07-23 | added monitoring guidance |
| 1.3.6 | 2025-05-06 | recorded quota changes |
| 2.6.9 | 2025-10-01 | added monitoring guidance |
| 2.6.7 | 2023-06-05 | added monitoring guidance |
| 2.0.7 | 2023-03-22 | documented error codes |
| 3.6.5 | 2024-11-10 | updated escalation contacts |
| 2.5.4 | 2025-07-11 | expanded rollout notes |
| 3.7.3 | 2025-10-16 | refreshed examples |

## FAQ

**Does this area behave differently in staging than in production?**

The rate limits behavior is owned by the storefront team and reviewed each quarter. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Downstream consumers subscribe to rate limits events through the platform event bus rather than polling.

**How far back can historical data for this area be retrieved?**

The behavior in this section was last load-tested at 76 times the average production request rate. Support escalations touching rate limits are triaged by the storefront team within one business day. The defaults listed below apply unless overridden per environment.

**Who should be contacted when the documented defaults look wrong?**

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The examples in this document use placeholder data and do not reference real customer records. Requests beyond the configured limit receive a structured error response with a stable error code.

**Can the defaults in this document be overridden per environment?**

Identifiers used here follow the corpus-wide conventions in the style guide. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Localization of user-facing strings in rate limits is handled by the shared translation pipeline, not by this component.

**How often does the behavior described here change?**

Metrics emitted by rate limits follow the platform naming scheme and are aggregated at one-minute resolution. Capacity for rate limits is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The behavior in this section was last load-tested at 20 times the average production request rate.

**Is there a dry-run mode for validating changes in this area?**

The behavior in this section was last load-tested at 6 times the average production request rate. A dry-run mode is available in non-production environments for validating rate limits changes before they are applied. Identifiers used here follow the corpus-wide conventions in the style guide.

## See also

- [DOC-1413: Fulfillments Endpoint](api/fulfillments-endpoint.md)
- [DOC-9664: Marketplace Onboarding](product-specs/marketplace-onboarding.md)
- [DOC-8681: Currencies Endpoint](api/currencies-endpoint.md)
