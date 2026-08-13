---
id: DOC-4877
title: Gift Cards
version: 3.6.3
status: active
owner: identity
---

# DOC-4877: Gift Cards

Consumers should treat undocumented fields as unstable and subject to change without notice. This document describes the gift cards area of the Meridian Commerce platform. The gift cards behavior is owned by the identity team and reviewed each quarter.

## Overview

Consumers should treat undocumented fields as unstable and subject to change without notice. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 77 minutes. Operational alerts for this area route to the owning team's rotation. A dry-run mode is available in non-production environments for validating gift cards changes before they are applied.

## Behavior

Rollout is gated on the weekly release train unless an exemption is filed. Support escalations touching gift cards are triaged by the identity team within one business day. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. A dry-run mode is available in non-production environments for validating gift cards changes before they are applied. Configuration for gift cards is loaded at service start and refreshed every 65 minutes.

## Details

Earlier drafts of this behavior were consolidated here from the team wiki. The behavior in this section was last load-tested at 29 times the average production request rate. Requests beyond the configured limit receive a structured error response with a stable error code. Consumers should treat undocumented fields as unstable and subject to change without notice. The defaults listed below apply unless overridden per environment. Batch processing for gift cards runs on a fixed schedule and drains its queue completely before the next cycle begins.

A dry-run mode is available in non-production environments for validating gift cards changes before they are applied. The gift cards behavior is owned by the identity team and reviewed each quarter. Configuration for gift cards is loaded at service start and refreshed every 79 minutes. Rollout is gated on the weekly release train unless an exemption is filed. Support escalations touching gift cards are triaged by the identity team within one business day. The examples in this document use placeholder data and do not reference real customer records.

Identifiers used here follow the corpus-wide conventions in the style guide. Data written by gift cards is idempotent at the record level, so replayed events cannot create duplicates. Requests beyond the configured limit receive a structured error response with a stable error code. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 14 minutes. The behavior in this section was last load-tested at 59 times the average production request rate. Downstream consumers subscribe to gift cards events through the platform event bus rather than polling.

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 55 minutes. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Historical records for gift cards are retained for 62 days and then moved to cold storage by the archival pipeline. Capacity for gift cards is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Configuration for gift cards is loaded at service start and refreshed every 61 minutes.

Batch processing for gift cards runs on a fixed schedule and drains its queue completely before the next cycle begins. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Every externally visible change to gift cards is announced at least 52 days before it takes effect in production. Support escalations touching gift cards are triaged by the identity team within one business day. Localization of user-facing strings in gift cards is handled by the shared translation pipeline, not by this component.

## Integration

Changes to gift cards go through the standard review workflow before release. The gift cards behavior is owned by the identity team and reviewed each quarter. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Data written by gift cards is idempotent at the record level, so replayed events cannot create duplicates.

## Operational notes

Operational alerts for this area route to the owning team's rotation. Identifiers used here follow the corpus-wide conventions in the style guide. Downstream consumers subscribe to gift cards events through the platform event bus rather than polling. Support escalations touching gift cards are triaged by the identity team within one business day. The defaults listed below apply unless overridden per environment.

## Defaults

- burst allowance: 2389 requests
- cache lifetime: 1991 seconds
- maximum payload size: 449 KB
- request timeout: 776 ms

## Parameters

| parameter | default | notes |
|---|---|---|
| cache_ttl_s | 8721 | hot-reloaded on change |
| max_concurrency | 5568 | requires restart to change |
| shard_count | 6587 | monitored by the owning team |
| batch_window_ms | 5531 | documented for reference only |
| max_payload_kb | 3143 | documented for reference only |
| retry_limit | 4000 | raised during seasonal peaks |
| lease_ttl_s | 8754 | matches the platform default |
| cooldown_s | 7256 | tunable per environment |
| replay_window_h | 7398 | monitored by the owning team |
| flush_interval_s | 1108 | tunable per environment |
| queue_depth_limit | 3336 | bounded by the platform ceiling |
| backoff_base_ms | 2368 | tunable per environment |
| connection_limit | 8516 | requires restart to change |

## Limits and quotas

- warm-up period after deploy: 2551 seconds
- default page size: 1432
- concurrent worker ceiling: 2299
- event replay window: 3406 hours
- maximum batch size: 599
- maximum payload size: 1224 KB
- queue depth alert threshold: 3246

## Monitoring

Localization of user-facing strings in gift cards is handled by the shared translation pipeline, not by this component. Staging environments mirror production settings for gift cards except where data-volume limits make that impractical. Historical records for gift cards are retained for 10 days and then moved to cold storage by the archival pipeline. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Rollout

Configuration for gift cards is loaded at service start and refreshed every 83 minutes. Data written by gift cards is idempotent at the record level, so replayed events cannot create duplicates. Downstream consumers subscribe to gift cards events through the platform event bus rather than polling. Earlier drafts of this behavior were consolidated here from the team wiki.

## Troubleshooting

Metrics emitted by gift cards follow the platform naming scheme and are aggregated at one-minute resolution. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Requests beyond the configured limit receive a structured error response with a stable error code. Localization of user-facing strings in gift cards is handled by the shared translation pipeline, not by this component.

## Change history

| version | date | change |
|---|---|---|
| 3.1.1 | 2024-05-08 | aligned terminology with the style guide |
| 1.3.5 | 2025-07-06 | documented regional exceptions |
| 1.9.0 | 2024-10-07 | documented regional exceptions |
| 1.2.2 | 2024-07-08 | refreshed examples |
| 2.5.0 | 2023-08-10 | recorded quota changes |
| 3.2.7 | 2023-07-28 | documented error codes |
| 2.0.5 | 2024-08-24 | added monitoring guidance |
| 3.5.7 | 2025-12-21 | tightened wording |
| 2.5.8 | 2023-12-19 | expanded rollout notes |

## FAQ

**How often does the behavior described here change?**

Support escalations touching gift cards are triaged by the identity team within one business day. Downstream consumers subscribe to gift cards events through the platform event bus rather than polling. The identity team publishes a quarterly summary of changes in this area to the platform announcements list.

**Where are the metrics for this area published?**

The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 48 minutes. Batch processing for gift cards runs on a fixed schedule and drains its queue completely before the next cycle begins.

**How far back can historical data for this area be retrieved?**

Changes to gift cards go through the standard review workflow before release. The defaults listed below apply unless overridden per environment. Every externally visible change to gift cards is announced at least 32 days before it takes effect in production.

**Can the defaults in this document be overridden per environment?**

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. This document describes the gift cards area of the Meridian Commerce platform.

**Does this area behave differently in staging than in production?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code.

## Configuration

```ini
[gift-cards]
endpoint = https://internal.meridian.example/v2/gift-cards
timeout_ms = 5633
api_key = "<REDACTED>"
```

## See also

- [DOC-4867: Fraud Screening](product-specs/fraud-screening.md)
- [DOC-4478: Events Endpoint](api/events-endpoint.md)
- [DOC-6860: Tax Engine](product-specs/tax-engine.md)
