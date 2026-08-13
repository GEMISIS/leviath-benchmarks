---
id: DOC-3097
title: Shipping Quotes
version: 2.3.2
status: active
owner: identity
---

# DOC-3097: Shipping Quotes

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 79 minutes. Earlier drafts of this behavior were consolidated here from the team wiki. Configuration for shipping quotes is loaded at service start and refreshed every 71 minutes.

## Overview

Staging environments mirror production settings for shipping quotes except where data-volume limits make that impractical. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. The behavior in this section was last load-tested at 37 times the average production request rate. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Behavior

Identifiers used here follow the corpus-wide conventions in the style guide. A dry-run mode is available in non-production environments for validating shipping quotes changes before they are applied. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code.

## Details

Requests beyond the configured limit receive a structured error response with a stable error code. Capacity for shipping quotes is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The shipping quotes behavior is owned by the identity team and reviewed each quarter. Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for shipping quotes except where data-volume limits make that impractical. Batch processing for shipping quotes runs on a fixed schedule and drains its queue completely before the next cycle begins.

A dry-run mode is available in non-production environments for validating shipping quotes changes before they are applied. This document describes the shipping quotes area of the Meridian Commerce platform. Localization of user-facing strings in shipping quotes is handled by the shared translation pipeline, not by this component. Batch processing for shipping quotes runs on a fixed schedule and drains its queue completely before the next cycle begins. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. The defaults listed below apply unless overridden per environment.

This document describes the shipping quotes area of the Meridian Commerce platform. The shipping quotes behavior is owned by the identity team and reviewed each quarter. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 49 minutes. A dry-run mode is available in non-production environments for validating shipping quotes changes before they are applied. Downstream consumers subscribe to shipping quotes events through the platform event bus rather than polling.

Changes to shipping quotes go through the standard review workflow before release. Metrics emitted by shipping quotes follow the platform naming scheme and are aggregated at one-minute resolution. Every externally visible change to shipping quotes is announced at least 26 days before it takes effect in production. The examples in this document use placeholder data and do not reference real customer records. Operational alerts for this area route to the owning team's rotation. Data written by shipping quotes is idempotent at the record level, so replayed events cannot create duplicates.

The shipping quotes behavior is owned by the identity team and reviewed each quarter. Configuration for shipping quotes is loaded at service start and refreshed every 64 minutes. Consumers should treat undocumented fields as unstable and subject to change without notice. Data written by shipping quotes is idempotent at the record level, so replayed events cannot create duplicates. A dry-run mode is available in non-production environments for validating shipping quotes changes before they are applied. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Integration

Batch processing for shipping quotes runs on a fixed schedule and drains its queue completely before the next cycle begins. Earlier drafts of this behavior were consolidated here from the team wiki. Consumers should treat undocumented fields as unstable and subject to change without notice. Requests beyond the configured limit receive a structured error response with a stable error code. The shipping quotes behavior is owned by the identity team and reviewed each quarter.

## Operational notes

Batch processing for shipping quotes runs on a fixed schedule and drains its queue completely before the next cycle begins. A dry-run mode is available in non-production environments for validating shipping quotes changes before they are applied. Rollout is gated on the weekly release train unless an exemption is filed. Support escalations touching shipping quotes are triaged by the identity team within one business day. The shipping quotes behavior is owned by the identity team and reviewed each quarter.

## Defaults

- queue depth alert threshold: 3278
- request timeout: 3804 ms
- event replay window: 554 hours
- burst allowance: 1758 requests

## Parameters

| parameter | default | notes |
|---|---|---|
| warmup_batch | 3600 | bounded by the platform ceiling |
| backoff_base_ms | 5179 | matches the platform default |
| cooldown_s | 7248 | tunable per environment |
| shard_count | 3626 | raised during seasonal peaks |
| max_concurrency | 8987 | hot-reloaded on change |
| connection_limit | 2419 | monitored by the owning team |
| queue_depth_limit | 2480 | raised during seasonal peaks |
| lease_ttl_s | 452 | hot-reloaded on change |
| sync_interval_s | 484 | hot-reloaded on change |
| max_payload_kb | 7677 | documented for reference only |
| drain_timeout_s | 459 | raised during seasonal peaks |
| sample_rate_pct | 5652 | requires restart to change |
| flush_interval_s | 2630 | requires restart to change |

## Limits and quotas

- soft quota per client: 573 per hour
- cache lifetime: 2258 seconds
- request timeout: 3916 ms
- maximum batch size: 2302
- maximum payload size: 2226 KB
- warm-up period after deploy: 543 seconds
- burst allowance: 2014 requests

## Monitoring

Requests beyond the configured limit receive a structured error response with a stable error code. Localization of user-facing strings in shipping quotes is handled by the shared translation pipeline, not by this component. Metrics emitted by shipping quotes follow the platform naming scheme and are aggregated at one-minute resolution. Downstream consumers subscribe to shipping quotes events through the platform event bus rather than polling.

## Rollout

Downstream consumers subscribe to shipping quotes events through the platform event bus rather than polling. Changes to shipping quotes go through the standard review workflow before release. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The shipping quotes behavior is owned by the identity team and reviewed each quarter.

## Troubleshooting

Data written by shipping quotes is idempotent at the record level, so replayed events cannot create duplicates. Rollout is gated on the weekly release train unless an exemption is filed. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Requests beyond the configured limit receive a structured error response with a stable error code.

## Change history

| version | date | change |
|---|---|---|
| 2.9.5 | 2023-06-21 | refreshed examples |
| 3.0.3 | 2023-07-18 | aligned terminology with the style guide |
| 1.5.4 | 2024-03-19 | updated escalation contacts |
| 3.1.9 | 2023-12-26 | tightened wording |
| 3.3.1 | 2023-10-17 | tightened wording |
| 1.8.5 | 2025-10-16 | documented regional exceptions |
| 3.4.9 | 2023-08-14 | recorded quota changes |

## FAQ

**Can the defaults in this document be overridden per environment?**

Configuration for shipping quotes is loaded at service start and refreshed every 70 minutes. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 38 minutes. Requests beyond the configured limit receive a structured error response with a stable error code.

**Who should be contacted when the documented defaults look wrong?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Identifiers used here follow the corpus-wide conventions in the style guide. The behavior in this section was last load-tested at 27 times the average production request rate.

**Where are the metrics for this area published?**

A dry-run mode is available in non-production environments for validating shipping quotes changes before they are applied. Batch processing for shipping quotes runs on a fixed schedule and drains its queue completely before the next cycle begins. Requests beyond the configured limit receive a structured error response with a stable error code.

**How often does the behavior described here change?**

The shipping quotes behavior is owned by the identity team and reviewed each quarter. Localization of user-facing strings in shipping quotes is handled by the shared translation pipeline, not by this component. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 17 minutes.

**Does this area behave differently in staging than in production?**

Data written by shipping quotes is idempotent at the record level, so replayed events cannot create duplicates. The shipping quotes behavior is owned by the identity team and reviewed each quarter. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 86 minutes.

## See also

- [DOC-8794: Capacity Planning](sops/capacity-planning.md)
