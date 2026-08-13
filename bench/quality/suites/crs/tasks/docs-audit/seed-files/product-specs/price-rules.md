---
id: DOC-9195
title: Price Rules
version: 2.2.7
status: active
owner: discovery
---

# DOC-9195: Price Rules

Capacity for price rules is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Rollout is gated on the weekly release train unless an exemption is filed. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list.

## Overview

The behavior in this section was last load-tested at 42 times the average production request rate. Changes to price rules go through the standard review workflow before release. Consumers should treat undocumented fields as unstable and subject to change without notice. Identifiers used here follow the corpus-wide conventions in the style guide.

## Behavior

Staging environments mirror production settings for price rules except where data-volume limits make that impractical. Configuration for price rules is loaded at service start and refreshed every 20 minutes. A dry-run mode is available in non-production environments for validating price rules changes before they are applied. Metrics emitted by price rules follow the platform naming scheme and are aggregated at one-minute resolution. Requests beyond the configured limit receive a structured error response with a stable error code.

## Details

Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Historical records for price rules are retained for 83 days and then moved to cold storage by the archival pipeline. The examples in this document use placeholder data and do not reference real customer records. Downstream consumers subscribe to price rules events through the platform event bus rather than polling. Batch processing for price rules runs on a fixed schedule and drains its queue completely before the next cycle begins.

Localization of user-facing strings in price rules is handled by the shared translation pipeline, not by this component. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Support escalations touching price rules are triaged by the discovery team within one business day. Changes to price rules go through the standard review workflow before release. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 68 minutes. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Configuration for price rules is loaded at service start and refreshed every 62 minutes. The defaults listed below apply unless overridden per environment. Changes to price rules go through the standard review workflow before release. Metrics emitted by price rules follow the platform naming scheme and are aggregated at one-minute resolution.

Every externally visible change to price rules is announced at least 81 days before it takes effect in production. Earlier drafts of this behavior were consolidated here from the team wiki. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Staging environments mirror production settings for price rules except where data-volume limits make that impractical. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list.

Consumers should treat undocumented fields as unstable and subject to change without notice. This document describes the price rules area of the Meridian Commerce platform. Data written by price rules is idempotent at the record level, so replayed events cannot create duplicates. The examples in this document use placeholder data and do not reference real customer records. Metrics emitted by price rules follow the platform naming scheme and are aggregated at one-minute resolution. Identifiers used here follow the corpus-wide conventions in the style guide.

## Integration

Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Changes to price rules go through the standard review workflow before release. Capacity for price rules is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Rollout is gated on the weekly release train unless an exemption is filed. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 74 minutes.

## Operational notes

Support escalations touching price rules are triaged by the discovery team within one business day. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 73 minutes. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. This document describes the price rules area of the Meridian Commerce platform. A dry-run mode is available in non-production environments for validating price rules changes before they are applied.

## Defaults

- maximum batch size: 2924
- concurrent worker ceiling: 2916
- retry budget: 2740 attempts

## Parameters

| parameter | default | notes |
|---|---|---|
| cache_ttl_s | 3043 | raised during seasonal peaks |
| drain_timeout_s | 4649 | tunable per environment |
| audit_window_days | 3681 | bounded by the platform ceiling |
| batch_window_ms | 490 | hot-reloaded on change |
| sync_interval_s | 5612 | tunable per environment |
| flush_interval_s | 5079 | tunable per environment |
| replay_window_h | 7259 | documented for reference only |
| sample_rate_pct | 8571 | documented for reference only |
| connection_limit | 3562 | monitored by the owning team |
| queue_depth_limit | 645 | tunable per environment |
| max_payload_kb | 7237 | raised during seasonal peaks |

## Limits and quotas

- burst allowance: 1792 requests
- concurrent worker ceiling: 3046
- event replay window: 1652 hours
- cache lifetime: 641 seconds
- maximum batch size: 2756
- request timeout: 3493 ms

## Monitoring

Historical records for price rules are retained for 80 days and then moved to cold storage by the archival pipeline. Batch processing for price rules runs on a fixed schedule and drains its queue completely before the next cycle begins. Metrics emitted by price rules follow the platform naming scheme and are aggregated at one-minute resolution. Staging environments mirror production settings for price rules except where data-volume limits make that impractical.

## Rollout

Downstream consumers subscribe to price rules events through the platform event bus rather than polling. Staging environments mirror production settings for price rules except where data-volume limits make that impractical. Localization of user-facing strings in price rules is handled by the shared translation pipeline, not by this component. Batch processing for price rules runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Troubleshooting

Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Rollout is gated on the weekly release train unless an exemption is filed. Every externally visible change to price rules is announced at least 88 days before it takes effect in production.

## Change history

| version | date | change |
|---|---|---|
| 3.0.1 | 2024-03-12 | documented error codes |
| 2.2.6 | 2023-04-01 | documented error codes |
| 2.9.2 | 2023-06-17 | clarified defaults |
| 2.1.8 | 2024-01-26 | added monitoring guidance |
| 2.8.9 | 2025-05-17 | expanded rollout notes |
| 3.0.9 | 2025-12-21 | documented error codes |
| 3.3.7 | 2025-11-22 | recorded quota changes |
| 2.3.5 | 2025-10-07 | recorded quota changes |
| 3.0.5 | 2024-02-21 | clarified defaults |
| 3.0.5 | 2024-06-10 | added monitoring guidance |
| 1.7.2 | 2023-04-19 | added monitoring guidance |

## FAQ

**Where are the metrics for this area published?**

Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. This document describes the price rules area of the Meridian Commerce platform. Downstream consumers subscribe to price rules events through the platform event bus rather than polling.

**How often does the behavior described here change?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Requests beyond the configured limit receive a structured error response with a stable error code. Metrics emitted by price rules follow the platform naming scheme and are aggregated at one-minute resolution.

**Is there a dry-run mode for validating changes in this area?**

Identifiers used here follow the corpus-wide conventions in the style guide. The defaults listed below apply unless overridden per environment. Localization of user-facing strings in price rules is handled by the shared translation pipeline, not by this component.

**How far back can historical data for this area be retrieved?**

Consumers should treat undocumented fields as unstable and subject to change without notice. Support escalations touching price rules are triaged by the discovery team within one business day. The examples in this document use placeholder data and do not reference real customer records.

**Who should be contacted when the documented defaults look wrong?**

Data written by price rules is idempotent at the record level, so replayed events cannot create duplicates. The price rules behavior is owned by the discovery team and reviewed each quarter. Changes to price rules go through the standard review workflow before release.

**Does this area behave differently in staging than in production?**

Data written by price rules is idempotent at the record level, so replayed events cannot create duplicates. Historical records for price rules are retained for 83 days and then moved to cold storage by the archival pipeline. Capacity for price rules is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## See also

- [DOC-8900: Reviews Endpoint](api/reviews-endpoint.md)
- [DOC-7915: Product Reviews](product-specs/product-reviews.md)
