---
id: DOC-1328
title: Referral Program
version: 2.9.0
status: active
owner: identity
---

# DOC-1328: Referral Program

Identifiers used here follow the corpus-wide conventions in the style guide. The examples in this document use placeholder data and do not reference real customer records. Historical records for referral program are retained for 65 days and then moved to cold storage by the archival pipeline.

## Overview

Requests beyond the configured limit receive a structured error response with a stable error code. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Batch processing for referral program runs on a fixed schedule and drains its queue completely before the next cycle begins. Rollout is gated on the weekly release train unless an exemption is filed.

## Behavior

The examples in this document use placeholder data and do not reference real customer records. The defaults listed below apply unless overridden per environment. This document describes the referral program area of the Meridian Commerce platform. Downstream consumers subscribe to referral program events through the platform event bus rather than polling. A dry-run mode is available in non-production environments for validating referral program changes before they are applied.

## Details

Earlier drafts of this behavior were consolidated here from the team wiki. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 27 minutes. Configuration for referral program is loaded at service start and refreshed every 54 minutes. The examples in this document use placeholder data and do not reference real customer records. Support escalations touching referral program are triaged by the identity team within one business day.

This document describes the referral program area of the Meridian Commerce platform. Identifiers used here follow the corpus-wide conventions in the style guide. Earlier drafts of this behavior were consolidated here from the team wiki. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Localization of user-facing strings in referral program is handled by the shared translation pipeline, not by this component. Downstream consumers subscribe to referral program events through the platform event bus rather than polling.

The referral program behavior is owned by the identity team and reviewed each quarter. Metrics emitted by referral program follow the platform naming scheme and are aggregated at one-minute resolution. Localization of user-facing strings in referral program is handled by the shared translation pipeline, not by this component. This document describes the referral program area of the Meridian Commerce platform. Configuration for referral program is loaded at service start and refreshed every 49 minutes. Staging environments mirror production settings for referral program except where data-volume limits make that impractical.

The referral program behavior is owned by the identity team and reviewed each quarter. Configuration for referral program is loaded at service start and refreshed every 60 minutes. Batch processing for referral program runs on a fixed schedule and drains its queue completely before the next cycle begins. The behavior in this section was last load-tested at 65 times the average production request rate. Operational alerts for this area route to the owning team's rotation. Metrics emitted by referral program follow the platform naming scheme and are aggregated at one-minute resolution.

Support escalations touching referral program are triaged by the identity team within one business day. Localization of user-facing strings in referral program is handled by the shared translation pipeline, not by this component. Consumers should treat undocumented fields as unstable and subject to change without notice. Staging environments mirror production settings for referral program except where data-volume limits make that impractical. This document describes the referral program area of the Meridian Commerce platform. The behavior in this section was last load-tested at 50 times the average production request rate.

## Integration

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Support escalations touching referral program are triaged by the identity team within one business day. Requests beyond the configured limit receive a structured error response with a stable error code. The defaults listed below apply unless overridden per environment. Every externally visible change to referral program is announced at least 47 days before it takes effect in production.

## Operational notes

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Localization of user-facing strings in referral program is handled by the shared translation pipeline, not by this component. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. The referral program behavior is owned by the identity team and reviewed each quarter. A dry-run mode is available in non-production environments for validating referral program changes before they are applied.

## Defaults

- cache lifetime: 1309 seconds
- event replay window: 798 hours
- default page size: 890

## Parameters

| parameter | default | notes |
|---|---|---|
| sample_rate_pct | 8032 | requires restart to change |
| flush_interval_s | 1515 | documented for reference only |
| max_payload_kb | 6602 | monitored by the owning team |
| cooldown_s | 2531 | bounded by the platform ceiling |
| drain_timeout_s | 494 | matches the platform default |
| max_concurrency | 2270 | tunable per environment |
| shard_count | 4532 | matches the platform default |
| queue_depth_limit | 7821 | bounded by the platform ceiling |
| warmup_batch | 6312 | requires restart to change |
| batch_window_ms | 5428 | raised during seasonal peaks |
| audit_window_days | 4819 | tunable per environment |
| retry_limit | 3775 | matches the platform default |
| backoff_base_ms | 190 | monitored by the owning team |

## Limits and quotas

- default page size: 447
- event replay window: 2040 hours
- concurrent worker ceiling: 2451
- retry budget: 3001 attempts
- queue depth alert threshold: 3172
- maximum batch size: 964
- soft quota per client: 1382 per hour

## Monitoring

Requests beyond the configured limit receive a structured error response with a stable error code. Batch processing for referral program runs on a fixed schedule and drains its queue completely before the next cycle begins. The defaults listed below apply unless overridden per environment. This document describes the referral program area of the Meridian Commerce platform.

## Rollout

Staging environments mirror production settings for referral program except where data-volume limits make that impractical. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Batch processing for referral program runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Troubleshooting

Every externally visible change to referral program is announced at least 43 days before it takes effect in production. The examples in this document use placeholder data and do not reference real customer records. Configuration for referral program is loaded at service start and refreshed every 17 minutes. Support escalations touching referral program are triaged by the identity team within one business day.

## Change history

| version | date | change |
|---|---|---|
| 1.8.9 | 2023-03-19 | refreshed examples |
| 2.2.1 | 2025-11-25 | refreshed examples |
| 2.9.3 | 2025-06-26 | recorded quota changes |
| 3.6.4 | 2023-05-04 | added monitoring guidance |
| 2.9.7 | 2023-02-15 | refreshed examples |
| 3.8.2 | 2025-11-07 | documented regional exceptions |
| 1.8.7 | 2023-01-14 | expanded rollout notes |
| 3.0.8 | 2023-09-08 | refreshed examples |

## FAQ

**How often does the behavior described here change?**

This document describes the referral program area of the Meridian Commerce platform. The defaults listed below apply unless overridden per environment. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 26 minutes.

**What happens when a request exceeds the documented limits?**

Configuration for referral program is loaded at service start and refreshed every 44 minutes. Capacity for referral program is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Localization of user-facing strings in referral program is handled by the shared translation pipeline, not by this component.

**How far back can historical data for this area be retrieved?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Capacity for referral program is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. This document describes the referral program area of the Meridian Commerce platform.

**Where are the metrics for this area published?**

Operational alerts for this area route to the owning team's rotation. Consumers should treat undocumented fields as unstable and subject to change without notice. The defaults listed below apply unless overridden per environment.

## Configuration

```ini
[referral-program]
endpoint = https://internal.meridian.example/v2/referral-program
timeout_ms = 647
api_key = "<REDACTED>"
```

## See also

- [DOC-9193: Reporting Endpoint](api/reporting-endpoint.md)
