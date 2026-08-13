---
id: DOC-1417
title: Multi Currency
version: 1.5.3
status: active
owner: storefront
---

# DOC-1417: Multi Currency

Every externally visible change to multi currency is announced at least 32 days before it takes effect in production. Data written by multi currency is idempotent at the record level, so replayed events cannot create duplicates. Batch processing for multi currency runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Overview

Changes to multi currency go through the standard review workflow before release. A dry-run mode is available in non-production environments for validating multi currency changes before they are applied. Data written by multi currency is idempotent at the record level, so replayed events cannot create duplicates. Metrics emitted by multi currency follow the platform naming scheme and are aggregated at one-minute resolution.

## Behavior

Changes to multi currency go through the standard review workflow before release. Data written by multi currency is idempotent at the record level, so replayed events cannot create duplicates. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 65 minutes. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Details

The examples in this document use placeholder data and do not reference real customer records. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Metrics emitted by multi currency follow the platform naming scheme and are aggregated at one-minute resolution. Data written by multi currency is idempotent at the record level, so replayed events cannot create duplicates. The behavior in this section was last load-tested at 76 times the average production request rate. Configuration for multi currency is loaded at service start and refreshed every 20 minutes.

Downstream consumers subscribe to multi currency events through the platform event bus rather than polling. Consumers should treat undocumented fields as unstable and subject to change without notice. Historical records for multi currency are retained for 56 days and then moved to cold storage by the archival pipeline. Data written by multi currency is idempotent at the record level, so replayed events cannot create duplicates. The defaults listed below apply unless overridden per environment. Batch processing for multi currency runs on a fixed schedule and drains its queue completely before the next cycle begins.

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Data written by multi currency is idempotent at the record level, so replayed events cannot create duplicates. Every externally visible change to multi currency is announced at least 25 days before it takes effect in production. This document describes the multi currency area of the Meridian Commerce platform. A dry-run mode is available in non-production environments for validating multi currency changes before they are applied. Metrics emitted by multi currency follow the platform naming scheme and are aggregated at one-minute resolution.

Batch processing for multi currency runs on a fixed schedule and drains its queue completely before the next cycle begins. Consumers should treat undocumented fields as unstable and subject to change without notice. The defaults listed below apply unless overridden per environment. Rollout is gated on the weekly release train unless an exemption is filed. The examples in this document use placeholder data and do not reference real customer records. Capacity for multi currency is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

Earlier drafts of this behavior were consolidated here from the team wiki. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Capacity for multi currency is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The defaults listed below apply unless overridden per environment. Consumers should treat undocumented fields as unstable and subject to change without notice. The examples in this document use placeholder data and do not reference real customer records.

## Integration

Operational alerts for this area route to the owning team's rotation. Capacity for multi currency is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Support escalations touching multi currency are triaged by the storefront team within one business day. Rollout is gated on the weekly release train unless an exemption is filed. Batch processing for multi currency runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Operational notes

The defaults listed below apply unless overridden per environment. Operational alerts for this area route to the owning team's rotation. Configuration for multi currency is loaded at service start and refreshed every 54 minutes. Every externally visible change to multi currency is announced at least 67 days before it takes effect in production. Localization of user-facing strings in multi currency is handled by the shared translation pipeline, not by this component.

## Defaults

- concurrent worker ceiling: 986
- maximum payload size: 3134 KB
- maximum batch size: 3510
- event replay window: 1939 hours

## Parameters

| parameter | default | notes |
|---|---|---|
| batch_window_ms | 714 | tunable per environment |
| retry_limit | 8373 | matches the platform default |
| flush_interval_s | 3188 | raised during seasonal peaks |
| warmup_batch | 5876 | hot-reloaded on change |
| max_payload_kb | 7093 | bounded by the platform ceiling |
| lease_ttl_s | 2179 | tunable per environment |
| sync_interval_s | 3195 | matches the platform default |
| sample_rate_pct | 1559 | hot-reloaded on change |
| page_size | 5033 | tunable per environment |
| shard_count | 7096 | tunable per environment |
| backoff_base_ms | 6382 | matches the platform default |

## Limits and quotas

- default page size: 299
- retry budget: 374 attempts
- request timeout: 2987 ms
- soft quota per client: 3330 per hour
- burst allowance: 3971 requests
- cache lifetime: 501 seconds
- event replay window: 1744 hours

## Monitoring

Operational alerts for this area route to the owning team's rotation. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The behavior in this section was last load-tested at 39 times the average production request rate. Metrics emitted by multi currency follow the platform naming scheme and are aggregated at one-minute resolution.

## Rollout

Configuration for multi currency is loaded at service start and refreshed every 38 minutes. Batch processing for multi currency runs on a fixed schedule and drains its queue completely before the next cycle begins. A dry-run mode is available in non-production environments for validating multi currency changes before they are applied. The behavior in this section was last load-tested at 73 times the average production request rate.

## Troubleshooting

Capacity for multi currency is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Requests beyond the configured limit receive a structured error response with a stable error code. Operational alerts for this area route to the owning team's rotation. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Change history

| version | date | change |
|---|---|---|
| 3.1.5 | 2024-01-01 | documented regional exceptions |
| 2.5.5 | 2023-07-24 | tightened wording |
| 2.2.0 | 2024-11-24 | documented regional exceptions |
| 3.4.5 | 2023-01-09 | aligned terminology with the style guide |
| 1.0.7 | 2024-06-26 | clarified defaults |
| 3.9.2 | 2023-03-12 | recorded quota changes |
| 1.4.6 | 2023-04-04 | aligned terminology with the style guide |
| 3.1.2 | 2025-08-24 | tightened wording |
| 3.3.9 | 2023-06-12 | recorded quota changes |
| 2.9.3 | 2024-03-26 | expanded rollout notes |
| 1.1.8 | 2023-07-07 | aligned terminology with the style guide |

## FAQ

**What happens when a request exceeds the documented limits?**

The behavior in this section was last load-tested at 61 times the average production request rate. Support escalations touching multi currency are triaged by the storefront team within one business day. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

**Who should be contacted when the documented defaults look wrong?**

This document describes the multi currency area of the Meridian Commerce platform. Historical records for multi currency are retained for 31 days and then moved to cold storage by the archival pipeline. Staging environments mirror production settings for multi currency except where data-volume limits make that impractical.

**Can the defaults in this document be overridden per environment?**

Downstream consumers subscribe to multi currency events through the platform event bus rather than polling. Staging environments mirror production settings for multi currency except where data-volume limits make that impractical. This document describes the multi currency area of the Meridian Commerce platform.

**How often does the behavior described here change?**

Historical records for multi currency are retained for 19 days and then moved to cold storage by the archival pipeline. A dry-run mode is available in non-production environments for validating multi currency changes before they are applied. The examples in this document use placeholder data and do not reference real customer records.

**Where are the metrics for this area published?**

Consumers should treat undocumented fields as unstable and subject to change without notice. This document describes the multi currency area of the Meridian Commerce platform. Every externally visible change to multi currency is announced at least 78 days before it takes effect in production.

**How far back can historical data for this area be retrieved?**

The multi currency behavior is owned by the storefront team and reviewed each quarter. Downstream consumers subscribe to multi currency events through the platform event bus rather than polling. The defaults listed below apply unless overridden per environment.

## See also

- [DOC-1413: Fulfillments Endpoint](api/fulfillments-endpoint.md)
- [DOC-9922: Checkout Flow](product-specs/checkout-flow.md)
- [DOC-9195: Price Rules](product-specs/price-rules.md)
