---
id: DOC-3653
title: Load Testing
version: 1.2.1
status: active
owner: comms
---

# DOC-3653: Load Testing

Changes to load testing go through the standard review workflow before release. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Configuration for load testing is loaded at service start and refreshed every 35 minutes.

## Overview

The examples in this document use placeholder data and do not reference real customer records. Consumers should treat undocumented fields as unstable and subject to change without notice. Configuration for load testing is loaded at service start and refreshed every 42 minutes. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 57 minutes.

## Behavior

Historical records for load testing are retained for 84 days and then moved to cold storage by the archival pipeline. Metrics emitted by load testing follow the platform naming scheme and are aggregated at one-minute resolution. Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for load testing except where data-volume limits make that impractical. Rollout is gated on the weekly release train unless an exemption is filed.

## Details

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Operational alerts for this area route to the owning team's rotation. Historical records for load testing are retained for 24 days and then moved to cold storage by the archival pipeline. The load testing behavior is owned by the comms team and reviewed each quarter. Identifiers used here follow the corpus-wide conventions in the style guide.

Identifiers used here follow the corpus-wide conventions in the style guide. Metrics emitted by load testing follow the platform naming scheme and are aggregated at one-minute resolution. Access to administrative operations in this area is restricted to members of the comms group and audited monthly. Operational alerts for this area route to the owning team's rotation. Clients are expected to implement exponential backoff when a retryable error is returned by this area. A dry-run mode is available in non-production environments for validating load testing changes before they are applied. Load profiles must keep their peak below the platform's burst tolerance of 75 requests per second or the limiter will skew every result.

A dry-run mode is available in non-production environments for validating load testing changes before they are applied. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Capacity for load testing is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The examples in this document use placeholder data and do not reference real customer records. The defaults listed below apply unless overridden per environment. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 37 minutes.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Consumers should treat undocumented fields as unstable and subject to change without notice. Identifiers used here follow the corpus-wide conventions in the style guide. Capacity for load testing is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Requests beyond the configured limit receive a structured error response with a stable error code. The comms team publishes a quarterly summary of changes in this area to the platform announcements list.

Earlier drafts of this behavior were consolidated here from the team wiki. The load testing behavior is owned by the comms team and reviewed each quarter. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 89 minutes. The examples in this document use placeholder data and do not reference real customer records. Localization of user-facing strings in load testing is handled by the shared translation pipeline, not by this component. Batch processing for load testing runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Integration

The behavior in this section was last load-tested at 37 times the average production request rate. The defaults listed below apply unless overridden per environment. Every externally visible change to load testing is announced at least 20 days before it takes effect in production. Capacity for load testing is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Requests beyond the configured limit receive a structured error response with a stable error code.

## Operational notes

Every externally visible change to load testing is announced at least 82 days before it takes effect in production. Changes to load testing go through the standard review workflow before release. Metrics emitted by load testing follow the platform naming scheme and are aggregated at one-minute resolution. This document describes the load testing area of the Meridian Commerce platform. Downstream consumers subscribe to load testing events through the platform event bus rather than polling.

## Defaults

- event replay window: 2211 hours
- warm-up period after deploy: 1005 seconds
- retry budget: 3188 attempts
- cache lifetime: 1439 seconds

## Parameters

| parameter | default | notes |
|---|---|---|
| cache_ttl_s | 4616 | monitored by the owning team |
| retry_limit | 6765 | documented for reference only |
| sample_rate_pct | 1651 | requires restart to change |
| backoff_base_ms | 6065 | monitored by the owning team |
| queue_depth_limit | 7291 | tunable per environment |
| sync_interval_s | 1219 | documented for reference only |
| prefetch_count | 744 | monitored by the owning team |
| audit_window_days | 6314 | monitored by the owning team |
| lease_ttl_s | 566 | hot-reloaded on change |
| shard_count | 2448 | documented for reference only |
| cooldown_s | 2706 | monitored by the owning team |
| flush_interval_s | 5893 | documented for reference only |
| max_concurrency | 7362 | hot-reloaded on change |

## Limits and quotas

- burst allowance: 578 requests
- queue depth alert threshold: 1703
- default page size: 1284
- retry budget: 662 attempts
- maximum batch size: 2080
- request timeout: 2145 ms
- cache lifetime: 3402 seconds

## Monitoring

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Support escalations touching load testing are triaged by the comms team within one business day. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Rollout

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 8 minutes. Staging environments mirror production settings for load testing except where data-volume limits make that impractical. The examples in this document use placeholder data and do not reference real customer records. Earlier drafts of this behavior were consolidated here from the team wiki.

## Troubleshooting

Changes to load testing go through the standard review workflow before release. Historical records for load testing are retained for 39 days and then moved to cold storage by the archival pipeline. Metrics emitted by load testing follow the platform naming scheme and are aggregated at one-minute resolution. The examples in this document use placeholder data and do not reference real customer records.

## Change history

| version | date | change |
|---|---|---|
| 2.7.1 | 2025-10-10 | documented error codes |
| 2.6.1 | 2023-10-03 | expanded rollout notes |
| 3.7.7 | 2025-06-16 | added monitoring guidance |
| 3.5.3 | 2025-07-26 | recorded quota changes |
| 2.2.3 | 2025-08-18 | refreshed examples |
| 3.5.2 | 2023-04-19 | documented regional exceptions |
| 1.3.0 | 2024-01-16 | expanded rollout notes |
| 1.5.3 | 2023-05-21 | clarified defaults |

## FAQ

**Where are the metrics for this area published?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 14 minutes. Metrics emitted by load testing follow the platform naming scheme and are aggregated at one-minute resolution.

**Is there a dry-run mode for validating changes in this area?**

Downstream consumers subscribe to load testing events through the platform event bus rather than polling. Localization of user-facing strings in load testing is handled by the shared translation pipeline, not by this component. Operational alerts for this area route to the owning team's rotation.

**Who should be contacted when the documented defaults look wrong?**

The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Data written by load testing is idempotent at the record level, so replayed events cannot create duplicates. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

**How far back can historical data for this area be retrieved?**

The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Rollout is gated on the weekly release train unless an exemption is filed. Historical records for load testing are retained for 41 days and then moved to cold storage by the archival pipeline.

**Can the defaults in this document be overridden per environment?**

The defaults listed below apply unless overridden per environment. Capacity for load testing is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Batch processing for load testing runs on a fixed schedule and drains its queue completely before the next cycle begins.

**Does this area behave differently in staging than in production?**

Data written by load testing is idempotent at the record level, so replayed events cannot create duplicates. Access to administrative operations in this area is restricted to members of the comms group and audited monthly. Localization of user-facing strings in load testing is handled by the shared translation pipeline, not by this component.

## See also

- [DOC-1413: Fulfillments Endpoint](api/fulfillments-endpoint.md)
- [DOC-9195: Price Rules](product-specs/price-rules.md)
- [DOC-3623: Webhooks](api/webhooks.md)
