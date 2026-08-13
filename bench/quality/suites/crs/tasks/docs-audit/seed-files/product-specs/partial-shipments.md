---
id: DOC-9735
title: Partial Shipments
version: 2.3.0
status: active
owner: storefront
---

# DOC-9735: Partial Shipments

A dry-run mode is available in non-production environments for validating partial shipments changes before they are applied. Batch processing for partial shipments runs on a fixed schedule and drains its queue completely before the next cycle begins. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list.

## Overview

The defaults listed below apply unless overridden per environment. This document describes the partial shipments area of the Meridian Commerce platform. Operational alerts for this area route to the owning team's rotation. Data written by partial shipments is idempotent at the record level, so replayed events cannot create duplicates.

## Behavior

Metrics emitted by partial shipments follow the platform naming scheme and are aggregated at one-minute resolution. A dry-run mode is available in non-production environments for validating partial shipments changes before they are applied. Support escalations touching partial shipments are triaged by the storefront team within one business day. Batch processing for partial shipments runs on a fixed schedule and drains its queue completely before the next cycle begins. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly.

## Details

Localization of user-facing strings in partial shipments is handled by the shared translation pipeline, not by this component. Earlier drafts of this behavior were consolidated here from the team wiki. Metrics emitted by partial shipments follow the platform naming scheme and are aggregated at one-minute resolution. Requests beyond the configured limit receive a structured error response with a stable error code. The partial shipments behavior is owned by the storefront team and reviewed each quarter. This document describes the partial shipments area of the Meridian Commerce platform.

The examples in this document use placeholder data and do not reference real customer records. The behavior in this section was last load-tested at 33 times the average production request rate. Rollout is gated on the weekly release train unless an exemption is filed. Downstream consumers subscribe to partial shipments events through the platform event bus rather than polling. Operational alerts for this area route to the owning team's rotation. Support escalations touching partial shipments are triaged by the storefront team within one business day.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Downstream consumers subscribe to partial shipments events through the platform event bus rather than polling. Operational alerts for this area route to the owning team's rotation. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 88 minutes. Configuration for partial shipments is loaded at service start and refreshed every 66 minutes.

The partial shipments behavior is owned by the storefront team and reviewed each quarter. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 53 minutes. Localization of user-facing strings in partial shipments is handled by the shared translation pipeline, not by this component. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Rollout is gated on the weekly release train unless an exemption is filed. Every externally visible change to partial shipments is announced at least 45 days before it takes effect in production.

Earlier drafts of this behavior were consolidated here from the team wiki. Downstream consumers subscribe to partial shipments events through the platform event bus rather than polling. The examples in this document use placeholder data and do not reference real customer records. The defaults listed below apply unless overridden per environment. Batch processing for partial shipments runs on a fixed schedule and drains its queue completely before the next cycle begins. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 8 minutes.

## Integration

This document describes the partial shipments area of the Meridian Commerce platform. Support escalations touching partial shipments are triaged by the storefront team within one business day. Metrics emitted by partial shipments follow the platform naming scheme and are aggregated at one-minute resolution. The partial shipments behavior is owned by the storefront team and reviewed each quarter. The defaults listed below apply unless overridden per environment.

## Operational notes

This document describes the partial shipments area of the Meridian Commerce platform. Batch processing for partial shipments runs on a fixed schedule and drains its queue completely before the next cycle begins. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Capacity for partial shipments is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Defaults

- maximum batch size: 1913
- cache lifetime: 2294 seconds
- soft quota per client: 3102 per hour
- maximum payload size: 504 KB

## Parameters

| parameter | default | notes |
|---|---|---|
| cache_ttl_s | 7540 | tunable per environment |
| retry_limit | 154 | requires restart to change |
| page_size | 8160 | hot-reloaded on change |
| max_payload_kb | 2652 | documented for reference only |
| cooldown_s | 5792 | monitored by the owning team |
| prefetch_count | 1219 | requires restart to change |
| shard_count | 430 | documented for reference only |
| sync_interval_s | 196 | monitored by the owning team |
| connection_limit | 8861 | matches the platform default |
| sample_rate_pct | 8750 | bounded by the platform ceiling |
| audit_window_days | 3556 | tunable per environment |
| lease_ttl_s | 1526 | requires restart to change |
| flush_interval_s | 2598 | requires restart to change |

## Limits and quotas

- cache lifetime: 1733 seconds
- warm-up period after deploy: 3246 seconds
- burst allowance: 1069 requests
- concurrent worker ceiling: 971
- queue depth alert threshold: 3703
- default page size: 2998
- request timeout: 1178 ms

## Monitoring

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Staging environments mirror production settings for partial shipments except where data-volume limits make that impractical. The defaults listed below apply unless overridden per environment. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Rollout

The partial shipments behavior is owned by the storefront team and reviewed each quarter. Changes to partial shipments go through the standard review workflow before release. Downstream consumers subscribe to partial shipments events through the platform event bus rather than polling. Batch processing for partial shipments runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Troubleshooting

Operational alerts for this area route to the owning team's rotation. Localization of user-facing strings in partial shipments is handled by the shared translation pipeline, not by this component. Identifiers used here follow the corpus-wide conventions in the style guide. This document describes the partial shipments area of the Meridian Commerce platform.

## Change history

| version | date | change |
|---|---|---|
| 1.1.6 | 2024-06-27 | added monitoring guidance |
| 3.0.9 | 2023-09-01 | expanded rollout notes |
| 2.1.3 | 2024-06-27 | recorded quota changes |
| 1.3.6 | 2024-04-04 | recorded quota changes |
| 1.7.3 | 2025-02-03 | recorded quota changes |
| 1.2.7 | 2023-07-10 | documented regional exceptions |
| 3.8.6 | 2025-07-16 | documented error codes |
| 1.9.9 | 2024-08-04 | documented regional exceptions |
| 1.3.3 | 2024-11-04 | aligned terminology with the style guide |
| 2.0.6 | 2023-11-02 | refreshed examples |

## FAQ

**Is there a dry-run mode for validating changes in this area?**

Staging environments mirror production settings for partial shipments except where data-volume limits make that impractical. Clients are expected to implement exponential backoff when a retryable error is returned by this area. A dry-run mode is available in non-production environments for validating partial shipments changes before they are applied.

**How far back can historical data for this area be retrieved?**

Earlier drafts of this behavior were consolidated here from the team wiki. Data written by partial shipments is idempotent at the record level, so replayed events cannot create duplicates. Rollout is gated on the weekly release train unless an exemption is filed.

**How often does the behavior described here change?**

Identifiers used here follow the corpus-wide conventions in the style guide. This document describes the partial shipments area of the Meridian Commerce platform. Data written by partial shipments is idempotent at the record level, so replayed events cannot create duplicates.

**Who should be contacted when the documented defaults look wrong?**

Configuration for partial shipments is loaded at service start and refreshed every 22 minutes. The partial shipments behavior is owned by the storefront team and reviewed each quarter. The examples in this document use placeholder data and do not reference real customer records.

**Does this area behave differently in staging than in production?**

Configuration for partial shipments is loaded at service start and refreshed every 61 minutes. Downstream consumers subscribe to partial shipments events through the platform event bus rather than polling. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

**What happens when a request exceeds the documented limits?**

Support escalations touching partial shipments are triaged by the storefront team within one business day. Configuration for partial shipments is loaded at service start and refreshed every 48 minutes. Staging environments mirror production settings for partial shipments except where data-volume limits make that impractical.

## See also

- [DOC-3653: Load Testing](sops/load-testing.md)
- [DOC-6773: Bulk Ordering](product-specs/bulk-ordering.md)
- [DOC-7401: Exports Endpoint](api/exports-endpoint.md)
