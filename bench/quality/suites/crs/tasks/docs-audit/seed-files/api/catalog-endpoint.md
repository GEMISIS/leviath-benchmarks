---
id: DOC-2195
title: Catalog Endpoint
version: 3.0.7
status: active
owner: identity
---

# DOC-2195: Catalog Endpoint

Every externally visible change to catalog endpoint is announced at least 45 days before it takes effect in production. Rollout is gated on the weekly release train unless an exemption is filed. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Overview

Historical records for catalog endpoint are retained for 14 days and then moved to cold storage by the archival pipeline. Staging environments mirror production settings for catalog endpoint except where data-volume limits make that impractical. The behavior in this section was last load-tested at 15 times the average production request rate. Localization of user-facing strings in catalog endpoint is handled by the shared translation pipeline, not by this component.

## Behavior

The catalog endpoint behavior is owned by the identity team and reviewed each quarter. This document describes the catalog endpoint area of the Meridian Commerce platform. Localization of user-facing strings in catalog endpoint is handled by the shared translation pipeline, not by this component. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 81 minutes. The behavior in this section was last load-tested at 75 times the average production request rate.

## Details

Support escalations touching catalog endpoint are triaged by the identity team within one business day. Requests beyond the configured limit receive a structured error response with a stable error code. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Configuration for catalog endpoint is loaded at service start and refreshed every 28 minutes. This document describes the catalog endpoint area of the Meridian Commerce platform. Rollout is gated on the weekly release train unless an exemption is filed.

Identifiers used here follow the corpus-wide conventions in the style guide. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Every externally visible change to catalog endpoint is announced at least 44 days before it takes effect in production. The defaults listed below apply unless overridden per environment. Changes to catalog endpoint go through the standard review workflow before release. Historical records for catalog endpoint are retained for 18 days and then moved to cold storage by the archival pipeline.

Every externally visible change to catalog endpoint is announced at least 59 days before it takes effect in production. Configuration for catalog endpoint is loaded at service start and refreshed every 31 minutes. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Batch processing for catalog endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The examples in this document use placeholder data and do not reference real customer records.

Requests beyond the configured limit receive a structured error response with a stable error code. Staging environments mirror production settings for catalog endpoint except where data-volume limits make that impractical. Data written by catalog endpoint is idempotent at the record level, so replayed events cannot create duplicates. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Capacity for catalog endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

Batch processing for catalog endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Changes to catalog endpoint go through the standard review workflow before release. A dry-run mode is available in non-production environments for validating catalog endpoint changes before they are applied. Historical records for catalog endpoint are retained for 31 days and then moved to cold storage by the archival pipeline. Requests beyond the configured limit receive a structured error response with a stable error code. The identity team publishes a quarterly summary of changes in this area to the platform announcements list.

## Integration

Batch processing for catalog endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Historical records for catalog endpoint are retained for 53 days and then moved to cold storage by the archival pipeline. Configuration for catalog endpoint is loaded at service start and refreshed every 89 minutes. Metrics emitted by catalog endpoint follow the platform naming scheme and are aggregated at one-minute resolution. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Operational notes

The behavior in this section was last load-tested at 30 times the average production request rate. Data written by catalog endpoint is idempotent at the record level, so replayed events cannot create duplicates. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. The catalog endpoint behavior is owned by the identity team and reviewed each quarter. Staging environments mirror production settings for catalog endpoint except where data-volume limits make that impractical.

## Defaults

- retry budget: 3564 attempts
- cache lifetime: 544 seconds
- event replay window: 3127 hours

## Parameters

| parameter | default | notes |
|---|---|---|
| cooldown_s | 8741 | documented for reference only |
| retry_limit | 7108 | matches the platform default |
| warmup_batch | 8119 | tunable per environment |
| max_payload_kb | 3296 | bounded by the platform ceiling |
| batch_window_ms | 8733 | bounded by the platform ceiling |
| sample_rate_pct | 1451 | matches the platform default |
| flush_interval_s | 5285 | documented for reference only |
| replay_window_h | 6510 | hot-reloaded on change |
| audit_window_days | 4588 | documented for reference only |
| cache_ttl_s | 8883 | documented for reference only |
| sync_interval_s | 6984 | requires restart to change |
| backoff_base_ms | 8516 | raised during seasonal peaks |

## Limits and quotas

- event replay window: 2977 hours
- warm-up period after deploy: 1800 seconds
- queue depth alert threshold: 1552
- retry budget: 1645 attempts
- maximum payload size: 2620 KB
- request timeout: 3824 ms
- maximum batch size: 2740
- default page size: 1484

## Monitoring

Metrics emitted by catalog endpoint follow the platform naming scheme and are aggregated at one-minute resolution. A dry-run mode is available in non-production environments for validating catalog endpoint changes before they are applied. Downstream consumers subscribe to catalog endpoint events through the platform event bus rather than polling. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Rollout

Support escalations touching catalog endpoint are triaged by the identity team within one business day. Configuration for catalog endpoint is loaded at service start and refreshed every 62 minutes. Batch processing for catalog endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. The defaults listed below apply unless overridden per environment.

## Troubleshooting

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Capacity for catalog endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Change history

| version | date | change |
|---|---|---|
| 2.8.2 | 2024-03-17 | refreshed examples |
| 3.9.1 | 2023-03-28 | documented regional exceptions |
| 3.4.8 | 2023-04-08 | refreshed examples |
| 3.4.9 | 2024-11-22 | added monitoring guidance |
| 3.2.8 | 2025-11-15 | recorded quota changes |
| 2.5.5 | 2025-11-25 | refreshed examples |
| 2.4.7 | 2024-08-01 | clarified defaults |
| 3.9.2 | 2025-04-10 | tightened wording |

## FAQ

**Is there a dry-run mode for validating changes in this area?**

Downstream consumers subscribe to catalog endpoint events through the platform event bus rather than polling. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Every externally visible change to catalog endpoint is announced at least 56 days before it takes effect in production.

**How often does the behavior described here change?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 26 minutes. Consumers should treat undocumented fields as unstable and subject to change without notice.

**Can the defaults in this document be overridden per environment?**

Historical records for catalog endpoint are retained for 47 days and then moved to cold storage by the archival pipeline. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Downstream consumers subscribe to catalog endpoint events through the platform event bus rather than polling.

**Does this area behave differently in staging than in production?**

The examples in this document use placeholder data and do not reference real customer records. Batch processing for catalog endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Data written by catalog endpoint is idempotent at the record level, so replayed events cannot create duplicates.

**How far back can historical data for this area be retrieved?**

The defaults listed below apply unless overridden per environment. Earlier drafts of this behavior were consolidated here from the team wiki. Capacity for catalog endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

**What happens when a request exceeds the documented limits?**

The examples in this document use placeholder data and do not reference real customer records. The defaults listed below apply unless overridden per environment. Every externally visible change to catalog endpoint is announced at least 19 days before it takes effect in production.

## Configuration

```ini
[catalog-endpoint]
endpoint = https://internal.meridian.example/v2/catalog-endpoint
timeout_ms = 2291
api_key = "<REDACTED>"
```

## See also

- [DOC-6678: Saved Payment Methods](product-specs/saved-payment-methods.md)
- [DOC-4315: Wishlist Sharing](product-specs/wishlist-sharing.md)
- [DOC-7518: Promotions Endpoint](api/promotions-endpoint.md)
