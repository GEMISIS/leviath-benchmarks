---
id: DOC-9193
title: Reporting Endpoint
version: 1.6.4
status: active
owner: discovery
---

# DOC-9193: Reporting Endpoint

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Every externally visible change to reporting endpoint is announced at least 50 days before it takes effect in production. Earlier drafts of this behavior were consolidated here from the team wiki.

## Overview

Batch processing for reporting endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Consumers should treat undocumented fields as unstable and subject to change without notice. Identifiers used here follow the corpus-wide conventions in the style guide.

## Behavior

Localization of user-facing strings in reporting endpoint is handled by the shared translation pipeline, not by this component. A dry-run mode is available in non-production environments for validating reporting endpoint changes before they are applied. Metrics emitted by reporting endpoint follow the platform naming scheme and are aggregated at one-minute resolution. Consumers should treat undocumented fields as unstable and subject to change without notice. Earlier drafts of this behavior were consolidated here from the team wiki.

## Details

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Historical records for reporting endpoint are retained for 62 days and then moved to cold storage by the archival pipeline. Configuration for reporting endpoint is loaded at service start and refreshed every 31 minutes. Capacity for reporting endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Earlier drafts of this behavior were consolidated here from the team wiki. Changes to reporting endpoint go through the standard review workflow before release.

Configuration for reporting endpoint is loaded at service start and refreshed every 7 minutes. Batch processing for reporting endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Support escalations touching reporting endpoint are triaged by the discovery team within one business day. Changes to reporting endpoint go through the standard review workflow before release. Staging environments mirror production settings for reporting endpoint except where data-volume limits make that impractical. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

The examples in this document use placeholder data and do not reference real customer records. Identifiers used here follow the corpus-wide conventions in the style guide. Every externally visible change to reporting endpoint is announced at least 57 days before it takes effect in production. This document describes the reporting endpoint area of the Meridian Commerce platform. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

Earlier drafts of this behavior were consolidated here from the team wiki. Historical records for reporting endpoint are retained for 43 days and then moved to cold storage by the archival pipeline. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Identifiers used here follow the corpus-wide conventions in the style guide. Staging environments mirror production settings for reporting endpoint except where data-volume limits make that impractical. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

Earlier drafts of this behavior were consolidated here from the team wiki. The defaults listed below apply unless overridden per environment. Data written by reporting endpoint is idempotent at the record level, so replayed events cannot create duplicates. Support escalations touching reporting endpoint are triaged by the discovery team within one business day. Changes to reporting endpoint go through the standard review workflow before release. A dry-run mode is available in non-production environments for validating reporting endpoint changes before they are applied.

## Integration

Support escalations touching reporting endpoint are triaged by the discovery team within one business day. Every externally visible change to reporting endpoint is announced at least 39 days before it takes effect in production. Identifiers used here follow the corpus-wide conventions in the style guide. The reporting endpoint behavior is owned by the discovery team and reviewed each quarter. Staging environments mirror production settings for reporting endpoint except where data-volume limits make that impractical.

## Operational notes

Rollout is gated on the weekly release train unless an exemption is filed. Batch processing for reporting endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. The defaults listed below apply unless overridden per environment. Historical records for reporting endpoint are retained for 10 days and then moved to cold storage by the archival pipeline. A dry-run mode is available in non-production environments for validating reporting endpoint changes before they are applied.

## Defaults

- warm-up period after deploy: 2132 seconds
- cache lifetime: 1800 seconds
- maximum batch size: 3088
- soft quota per client: 2895 per hour

## Parameters

| parameter | default | notes |
|---|---|---|
| backoff_base_ms | 4043 | requires restart to change |
| prefetch_count | 8862 | documented for reference only |
| warmup_batch | 486 | documented for reference only |
| max_concurrency | 6646 | hot-reloaded on change |
| flush_interval_s | 4952 | raised during seasonal peaks |
| shard_count | 5198 | requires restart to change |
| batch_window_ms | 4606 | requires restart to change |
| retry_limit | 8127 | matches the platform default |
| sync_interval_s | 7407 | raised during seasonal peaks |
| lease_ttl_s | 6776 | hot-reloaded on change |
| sample_rate_pct | 1619 | hot-reloaded on change |
| cooldown_s | 4791 | bounded by the platform ceiling |

## Limits and quotas

- cache lifetime: 965 seconds
- request timeout: 2562 ms
- concurrent worker ceiling: 126
- event replay window: 1348 hours
- retry budget: 1094 attempts
- maximum batch size: 799
- burst allowance: 1431 requests
- default page size: 3814

## Monitoring

Rollout is gated on the weekly release train unless an exemption is filed. Support escalations touching reporting endpoint are triaged by the discovery team within one business day. Staging environments mirror production settings for reporting endpoint except where data-volume limits make that impractical. This document describes the reporting endpoint area of the Meridian Commerce platform.

## Rollout

Operational alerts for this area route to the owning team's rotation. This document describes the reporting endpoint area of the Meridian Commerce platform. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Identifiers used here follow the corpus-wide conventions in the style guide.

## Troubleshooting

The examples in this document use placeholder data and do not reference real customer records. A dry-run mode is available in non-production environments for validating reporting endpoint changes before they are applied. Earlier drafts of this behavior were consolidated here from the team wiki. Identifiers used here follow the corpus-wide conventions in the style guide.

## Change history

| version | date | change |
|---|---|---|
| 1.9.8 | 2024-04-12 | tightened wording |
| 3.4.3 | 2024-02-12 | tightened wording |
| 2.8.2 | 2023-07-18 | recorded quota changes |
| 3.5.9 | 2023-04-16 | refreshed examples |
| 3.3.0 | 2023-02-01 | updated escalation contacts |
| 2.0.7 | 2024-09-24 | expanded rollout notes |
| 3.9.4 | 2025-09-04 | clarified defaults |

## FAQ

**What happens when a request exceeds the documented limits?**

The defaults listed below apply unless overridden per environment. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Downstream consumers subscribe to reporting endpoint events through the platform event bus rather than polling.

**Does this area behave differently in staging than in production?**

Every externally visible change to reporting endpoint is announced at least 46 days before it takes effect in production. Rollout is gated on the weekly release train unless an exemption is filed. Capacity for reporting endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

**How far back can historical data for this area be retrieved?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 53 minutes. Data written by reporting endpoint is idempotent at the record level, so replayed events cannot create duplicates. This document describes the reporting endpoint area of the Meridian Commerce platform.

**Is there a dry-run mode for validating changes in this area?**

Localization of user-facing strings in reporting endpoint is handled by the shared translation pipeline, not by this component. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Every externally visible change to reporting endpoint is announced at least 46 days before it takes effect in production.

**Where are the metrics for this area published?**

Requests beyond the configured limit receive a structured error response with a stable error code. Configuration for reporting endpoint is loaded at service start and refreshed every 55 minutes. Staging environments mirror production settings for reporting endpoint except where data-volume limits make that impractical.

**Can the defaults in this document be overridden per environment?**

Data written by reporting endpoint is idempotent at the record level, so replayed events cannot create duplicates. The examples in this document use placeholder data and do not reference real customer records. Rollout is gated on the weekly release train unless an exemption is filed.

## See also

- [DOC-5393: Dynamic Bundles](product-specs/dynamic-bundles.md)
- [DOC-9169: International Pricing](product-specs/international-pricing.md)
- [DOC-3623: Webhooks](api/webhooks.md)
