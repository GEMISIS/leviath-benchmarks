---
id: DOC-3686
title: Rate Limits
version: 2.4.0
status: active
owner: storefront
---

# DOC-3686: Rate Limits

Consumers should treat undocumented fields as unstable and subject to change without notice. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The rate limits behavior is owned by the storefront team and reviewed each quarter.

## Overview

A dry-run mode is available in non-production environments for validating rate limits changes before they are applied. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 44 minutes. The defaults listed below apply unless overridden per environment. Localization of user-facing strings in rate limits is handled by the shared translation pipeline, not by this component.

## Behavior

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Metrics emitted by rate limits follow the platform naming scheme and are aggregated at one-minute resolution. The behavior in this section was last load-tested at 21 times the average production request rate. The defaults listed below apply unless overridden per environment. Staging environments mirror production settings for rate limits except where data-volume limits make that impractical.

## Details

Changes to rate limits go through the standard review workflow before release. A dry-run mode is available in non-production environments for validating rate limits changes before they are applied. Downstream consumers subscribe to rate limits events through the platform event bus rather than polling. Rollout is gated on the weekly release train unless an exemption is filed. Historical records for rate limits are retained for 38 days and then moved to cold storage by the archival pipeline. Capacity for rate limits is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

Every externally visible change to rate limits is announced at least 14 days before it takes effect in production. The rate limits behavior is owned by the storefront team and reviewed each quarter. The defaults listed below apply unless overridden per environment. Historical records for rate limits are retained for 39 days and then moved to cold storage by the archival pipeline. Identifiers used here follow the corpus-wide conventions in the style guide. Capacity for rate limits is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

Localization of user-facing strings in rate limits is handled by the shared translation pipeline, not by this component. Batch processing for rate limits runs on a fixed schedule and drains its queue completely before the next cycle begins. Capacity for rate limits is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Data written by rate limits is idempotent at the record level, so replayed events cannot create duplicates. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Downstream consumers subscribe to rate limits events through the platform event bus rather than polling.

Localization of user-facing strings in rate limits is handled by the shared translation pipeline, not by this component. The rate limits behavior is owned by the storefront team and reviewed each quarter. Capacity for rate limits is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The behavior in this section was last load-tested at 25 times the average production request rate. Staging environments mirror production settings for rate limits except where data-volume limits make that impractical. Historical records for rate limits are retained for 46 days and then moved to cold storage by the archival pipeline.

Downstream consumers subscribe to rate limits events through the platform event bus rather than polling. Every externally visible change to rate limits is announced at least 45 days before it takes effect in production. Earlier drafts of this behavior were consolidated here from the team wiki. Data written by rate limits is idempotent at the record level, so replayed events cannot create duplicates. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Changes to rate limits go through the standard review workflow before release.

## Integration

Every externally visible change to rate limits is announced at least 56 days before it takes effect in production. Batch processing for rate limits runs on a fixed schedule and drains its queue completely before the next cycle begins. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Historical records for rate limits are retained for 76 days and then moved to cold storage by the archival pipeline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Operational notes

The behavior in this section was last load-tested at 62 times the average production request rate. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Capacity for rate limits is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Clients are expected to implement exponential backoff when a retryable error is returned by this area. This document describes the rate limits area of the Meridian Commerce platform.

## Defaults

- default page size: 500
- retry budget: 30 attempts
- queue depth alert threshold: 2340
- event replay window: 1516 hours

## Parameters

| parameter | default | notes |
|---|---|---|
| cache_ttl_s | 4843 | raised during seasonal peaks |
| sync_interval_s | 4432 | monitored by the owning team |
| retry_limit | 2197 | monitored by the owning team |
| sample_rate_pct | 4295 | requires restart to change |
| drain_timeout_s | 3226 | requires restart to change |
| queue_depth_limit | 8516 | monitored by the owning team |
| lease_ttl_s | 1979 | documented for reference only |
| warmup_batch | 3360 | documented for reference only |
| backoff_base_ms | 3029 | monitored by the owning team |
| connection_limit | 4235 | hot-reloaded on change |
| shard_count | 5913 | hot-reloaded on change |

## Limits and quotas

- concurrent worker ceiling: 1591
- cache lifetime: 2848 seconds
- queue depth alert threshold: 3600
- default page size: 3665
- retry budget: 1964 attempts
- maximum batch size: 777
- burst allowance: 2847 requests

## Monitoring

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 42 minutes. Operational alerts for this area route to the owning team's rotation. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly.

## Rollout

The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Historical records for rate limits are retained for 7 days and then moved to cold storage by the archival pipeline. Downstream consumers subscribe to rate limits events through the platform event bus rather than polling. The behavior in this section was last load-tested at 64 times the average production request rate.

## Troubleshooting

The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Every externally visible change to rate limits is announced at least 23 days before it takes effect in production. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 67 minutes. The rate limits behavior is owned by the storefront team and reviewed each quarter.

## Change history

| version | date | change |
|---|---|---|
| 3.7.0 | 2023-11-21 | documented error codes |
| 3.6.5 | 2024-11-10 | updated escalation contacts |
| 2.5.4 | 2025-07-11 | expanded rollout notes |
| 3.7.3 | 2025-10-16 | refreshed examples |
| 3.9.2 | 2023-04-02 | documented regional exceptions |
| 1.9.6 | 2025-06-24 | aligned terminology with the style guide |
| 3.0.2 | 2024-03-05 | expanded rollout notes |

## FAQ

**Does this area behave differently in staging than in production?**

Capacity for rate limits is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The behavior in this section was last load-tested at 20 times the average production request rate. Staging environments mirror production settings for rate limits except where data-volume limits make that impractical.

**What happens when a request exceeds the documented limits?**

This document describes the rate limits area of the Meridian Commerce platform. Capacity for rate limits is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Downstream consumers subscribe to rate limits events through the platform event bus rather than polling.

**Who should be contacted when the documented defaults look wrong?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Metrics emitted by rate limits follow the platform naming scheme and are aggregated at one-minute resolution. Batch processing for rate limits runs on a fixed schedule and drains its queue completely before the next cycle begins.

**Where are the metrics for this area published?**

The behavior in this section was last load-tested at 27 times the average production request rate. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Operational alerts for this area route to the owning team's rotation.

**Is there a dry-run mode for validating changes in this area?**

Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Requests beyond the configured limit receive a structured error response with a stable error code. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

**How far back can historical data for this area be retrieved?**

Data written by rate limits is idempotent at the record level, so replayed events cannot create duplicates. Batch processing for rate limits runs on a fixed schedule and drains its queue completely before the next cycle begins. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## See also

- [DOC-8616: Tax Rates Endpoint](api/tax-rates-endpoint.md)
- [DOC-7274: Errors Reference](api/errors-reference.md)
- [DOC-7657: Customer Segments](product-specs/customer-segments.md)
