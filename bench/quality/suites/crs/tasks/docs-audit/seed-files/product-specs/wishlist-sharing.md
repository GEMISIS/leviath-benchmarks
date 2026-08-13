---
id: DOC-4315
title: Wishlist Sharing
version: 1.0.7
status: active
owner: platform-core
---

# DOC-4315: Wishlist Sharing

Rollout is gated on the weekly release train unless an exemption is filed. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 13 minutes. Earlier drafts of this behavior were consolidated here from the team wiki.

## Overview

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 73 minutes. Historical records for wishlist sharing are retained for 77 days and then moved to cold storage by the archival pipeline. A dry-run mode is available in non-production environments for validating wishlist sharing changes before they are applied.

## Behavior

Batch processing for wishlist sharing runs on a fixed schedule and drains its queue completely before the next cycle begins. Identifiers used here follow the corpus-wide conventions in the style guide. Earlier drafts of this behavior were consolidated here from the team wiki. The defaults listed below apply unless overridden per environment. Every externally visible change to wishlist sharing is announced at least 27 days before it takes effect in production.

## Details

Changes to wishlist sharing go through the standard review workflow before release. Batch processing for wishlist sharing runs on a fixed schedule and drains its queue completely before the next cycle begins. This document describes the wishlist sharing area of the Meridian Commerce platform. Operational alerts for this area route to the owning team's rotation. Identifiers used here follow the corpus-wide conventions in the style guide. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

Capacity for wishlist sharing is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Data written by wishlist sharing is idempotent at the record level, so replayed events cannot create duplicates. Earlier drafts of this behavior were consolidated here from the team wiki. Changes to wishlist sharing go through the standard review workflow before release. Localization of user-facing strings in wishlist sharing is handled by the shared translation pipeline, not by this component. Every externally visible change to wishlist sharing is announced at least 54 days before it takes effect in production.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The defaults listed below apply unless overridden per environment. The behavior in this section was last load-tested at 88 times the average production request rate. The examples in this document use placeholder data and do not reference real customer records. Requests beyond the configured limit receive a structured error response with a stable error code.

Support escalations touching wishlist sharing are triaged by the platform-core team within one business day. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Consumers should treat undocumented fields as unstable and subject to change without notice. Downstream consumers subscribe to wishlist sharing events through the platform event bus rather than polling. Capacity for wishlist sharing is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

Every externally visible change to wishlist sharing is announced at least 71 days before it takes effect in production. A dry-run mode is available in non-production environments for validating wishlist sharing changes before they are applied. Configuration for wishlist sharing is loaded at service start and refreshed every 80 minutes. Changes to wishlist sharing go through the standard review workflow before release. The behavior in this section was last load-tested at 23 times the average production request rate. Requests beyond the configured limit receive a structured error response with a stable error code.

## Integration

Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for wishlist sharing is loaded at service start and refreshed every 65 minutes. Rollout is gated on the weekly release train unless an exemption is filed. Metrics emitted by wishlist sharing follow the platform naming scheme and are aggregated at one-minute resolution. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 87 minutes.

## Operational notes

The behavior in this section was last load-tested at 41 times the average production request rate. The examples in this document use placeholder data and do not reference real customer records. Batch processing for wishlist sharing runs on a fixed schedule and drains its queue completely before the next cycle begins. The defaults listed below apply unless overridden per environment. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Defaults

- maximum batch size: 3343
- maximum payload size: 2261 KB
- request timeout: 3357 ms
- concurrent worker ceiling: 1045

## Parameters

| parameter | default | notes |
|---|---|---|
| batch_window_ms | 3762 | hot-reloaded on change |
| drain_timeout_s | 1042 | bounded by the platform ceiling |
| sync_interval_s | 8745 | hot-reloaded on change |
| shard_count | 3204 | bounded by the platform ceiling |
| page_size | 6118 | monitored by the owning team |
| audit_window_days | 489 | raised during seasonal peaks |
| lease_ttl_s | 4741 | tunable per environment |
| queue_depth_limit | 5500 | requires restart to change |
| retry_limit | 5243 | documented for reference only |
| flush_interval_s | 7044 | hot-reloaded on change |
| replay_window_h | 7796 | tunable per environment |

## Limits and quotas

- event replay window: 2051 hours
- concurrent worker ceiling: 1669
- warm-up period after deploy: 1442 seconds
- maximum payload size: 556 KB
- default page size: 1803
- maximum batch size: 1114
- cache lifetime: 537 seconds
- burst allowance: 1923 requests

## Monitoring

Batch processing for wishlist sharing runs on a fixed schedule and drains its queue completely before the next cycle begins. Configuration for wishlist sharing is loaded at service start and refreshed every 69 minutes. Localization of user-facing strings in wishlist sharing is handled by the shared translation pipeline, not by this component. The wishlist sharing behavior is owned by the platform-core team and reviewed each quarter.

## Rollout

The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Downstream consumers subscribe to wishlist sharing events through the platform event bus rather than polling. Changes to wishlist sharing go through the standard review workflow before release.

## Troubleshooting

The defaults listed below apply unless overridden per environment. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. Earlier drafts of this behavior were consolidated here from the team wiki. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 21 minutes.

## Change history

| version | date | change |
|---|---|---|
| 1.5.7 | 2025-01-26 | added monitoring guidance |
| 3.9.2 | 2025-11-25 | documented regional exceptions |
| 1.3.2 | 2023-03-20 | expanded rollout notes |
| 2.1.8 | 2025-06-13 | refreshed examples |
| 2.0.5 | 2024-01-03 | updated escalation contacts |
| 3.3.5 | 2023-04-07 | documented error codes |
| 2.6.4 | 2023-04-25 | refreshed examples |
| 3.1.3 | 2025-04-23 | added monitoring guidance |
| 3.2.9 | 2025-12-10 | recorded quota changes |
| 2.3.2 | 2024-12-18 | updated escalation contacts |
| 1.1.2 | 2023-01-28 | recorded quota changes |

## FAQ

**How often does the behavior described here change?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Downstream consumers subscribe to wishlist sharing events through the platform event bus rather than polling. Data written by wishlist sharing is idempotent at the record level, so replayed events cannot create duplicates.

**Does this area behave differently in staging than in production?**

Requests beyond the configured limit receive a structured error response with a stable error code. Capacity for wishlist sharing is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

**Who should be contacted when the documented defaults look wrong?**

Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. The behavior in this section was last load-tested at 55 times the average production request rate. This document describes the wishlist sharing area of the Meridian Commerce platform.

**Where are the metrics for this area published?**

A dry-run mode is available in non-production environments for validating wishlist sharing changes before they are applied. Localization of user-facing strings in wishlist sharing is handled by the shared translation pipeline, not by this component. Metrics emitted by wishlist sharing follow the platform naming scheme and are aggregated at one-minute resolution.

**How far back can historical data for this area be retrieved?**

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 61 minutes.

**Can the defaults in this document be overridden per environment?**

Earlier drafts of this behavior were consolidated here from the team wiki. The wishlist sharing behavior is owned by the platform-core team and reviewed each quarter. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Configuration

```ini
[wishlist-sharing]
endpoint = https://internal.meridian.example/v2/wishlist-sharing
timeout_ms = 4661
api_key = "<REDACTED>"
```

## See also

- [DOC-6815: Deploy Procedure](sops/deploy-procedure.md)
- [DOC-9290: Products Endpoint](api/products-endpoint.md)
