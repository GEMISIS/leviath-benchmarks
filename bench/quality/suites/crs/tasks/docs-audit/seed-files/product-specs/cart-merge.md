---
id: DOC-1266
title: Cart Merge
version: 3.5.4
status: active
owner: storefront
---

# DOC-1266: Cart Merge

Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Localization of user-facing strings in cart merge is handled by the shared translation pipeline, not by this component. Capacity for cart merge is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Overview

Changes to cart merge go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Downstream consumers subscribe to cart merge events through the platform event bus rather than polling.

## Behavior

Clients are expected to implement exponential backoff when a retryable error is returned by this area. The defaults listed below apply unless overridden per environment. The examples in this document use placeholder data and do not reference real customer records. Every externally visible change to cart merge is announced at least 19 days before it takes effect in production. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Details

Batch processing for cart merge runs on a fixed schedule and drains its queue completely before the next cycle begins. The behavior in this section was last load-tested at 77 times the average production request rate. Staging environments mirror production settings for cart merge except where data-volume limits make that impractical. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Every externally visible change to cart merge is announced at least 26 days before it takes effect in production. Localization of user-facing strings in cart merge is handled by the shared translation pipeline, not by this component.

The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Changes to cart merge go through the standard review workflow before release. The examples in this document use placeholder data and do not reference real customer records. Capacity for cart merge is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Downstream consumers subscribe to cart merge events through the platform event bus rather than polling. Historical records for cart merge are retained for 65 days and then moved to cold storage by the archival pipeline.

Requests beyond the configured limit receive a structured error response with a stable error code. The examples in this document use placeholder data and do not reference real customer records. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Capacity for cart merge is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Data written by cart merge is idempotent at the record level, so replayed events cannot create duplicates. Operational alerts for this area route to the owning team's rotation.

Support escalations touching cart merge are triaged by the storefront team within one business day. Localization of user-facing strings in cart merge is handled by the shared translation pipeline, not by this component. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 25 minutes. Capacity for cart merge is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Downstream consumers subscribe to cart merge events through the platform event bus rather than polling.

Rollout is gated on the weekly release train unless an exemption is filed. This document describes the cart merge area of the Meridian Commerce platform. Historical records for cart merge are retained for 76 days and then moved to cold storage by the archival pipeline. Operational alerts for this area route to the owning team's rotation. Support escalations touching cart merge are triaged by the storefront team within one business day. Requests beyond the configured limit receive a structured error response with a stable error code.

## Integration

Downstream consumers subscribe to cart merge events through the platform event bus rather than polling. Requests beyond the configured limit receive a structured error response with a stable error code. Consumers should treat undocumented fields as unstable and subject to change without notice. The defaults listed below apply unless overridden per environment. The examples in this document use placeholder data and do not reference real customer records.

## Operational notes

Identifiers used here follow the corpus-wide conventions in the style guide. Metrics emitted by cart merge follow the platform naming scheme and are aggregated at one-minute resolution. Operational alerts for this area route to the owning team's rotation. The examples in this document use placeholder data and do not reference real customer records. Capacity for cart merge is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Defaults

- retry budget: 1942 attempts
- maximum payload size: 3591 KB
- cache lifetime: 506 seconds
- default page size: 917

## Parameters

| parameter | default | notes |
|---|---|---|
| warmup_batch | 7399 | documented for reference only |
| sample_rate_pct | 111 | monitored by the owning team |
| cache_ttl_s | 7699 | tunable per environment |
| max_payload_kb | 5820 | bounded by the platform ceiling |
| flush_interval_s | 7099 | monitored by the owning team |
| connection_limit | 2498 | bounded by the platform ceiling |
| prefetch_count | 4605 | matches the platform default |
| cooldown_s | 695 | hot-reloaded on change |
| max_concurrency | 2167 | tunable per environment |
| batch_window_ms | 797 | tunable per environment |
| queue_depth_limit | 2303 | bounded by the platform ceiling |
| retry_limit | 4086 | monitored by the owning team |
| audit_window_days | 2352 | matches the platform default |
| replay_window_h | 3070 | hot-reloaded on change |

## Limits and quotas

- maximum payload size: 1553 KB
- event replay window: 1622 hours
- request timeout: 3645 ms
- queue depth alert threshold: 1414
- maximum batch size: 2935
- soft quota per client: 2849 per hour

## Monitoring

The cart merge behavior is owned by the storefront team and reviewed each quarter. Historical records for cart merge are retained for 77 days and then moved to cold storage by the archival pipeline. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 59 minutes. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Rollout

Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. A dry-run mode is available in non-production environments for validating cart merge changes before they are applied. The defaults listed below apply unless overridden per environment. The examples in this document use placeholder data and do not reference real customer records.

## Troubleshooting

Rollout is gated on the weekly release train unless an exemption is filed. Earlier drafts of this behavior were consolidated here from the team wiki. Support escalations touching cart merge are triaged by the storefront team within one business day. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list.

## Change history

| version | date | change |
|---|---|---|
| 2.5.9 | 2025-09-13 | tightened wording |
| 3.5.0 | 2023-02-08 | clarified defaults |
| 3.8.7 | 2023-01-05 | expanded rollout notes |
| 2.3.0 | 2024-12-14 | aligned terminology with the style guide |
| 1.3.9 | 2023-07-04 | documented regional exceptions |
| 3.3.0 | 2023-02-01 | recorded quota changes |
| 2.3.3 | 2023-04-28 | recorded quota changes |
| 3.0.3 | 2024-01-10 | clarified defaults |
| 1.8.2 | 2023-02-13 | recorded quota changes |
| 1.8.5 | 2025-03-06 | updated escalation contacts |
| 3.2.7 | 2023-07-14 | refreshed examples |

## FAQ

**How far back can historical data for this area be retrieved?**

Data written by cart merge is idempotent at the record level, so replayed events cannot create duplicates. The behavior in this section was last load-tested at 7 times the average production request rate. Consumers should treat undocumented fields as unstable and subject to change without notice.

**Who should be contacted when the documented defaults look wrong?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Changes to cart merge go through the standard review workflow before release. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 30 minutes.

**Is there a dry-run mode for validating changes in this area?**

Identifiers used here follow the corpus-wide conventions in the style guide. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Data written by cart merge is idempotent at the record level, so replayed events cannot create duplicates.

**Does this area behave differently in staging than in production?**

Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for cart merge except where data-volume limits make that impractical. Changes to cart merge go through the standard review workflow before release.

## Configuration

```ini
[cart-merge]
endpoint = https://internal.meridian.example/v2/cart-merge
timeout_ms = 8420
api_key = "<REDACTED>"
```

## See also

- [DOC-8879: Notifications Endpoint](api/notifications-endpoint.md)
- [DOC-5661: Postmortem Process](sops/postmortem-process.md)
