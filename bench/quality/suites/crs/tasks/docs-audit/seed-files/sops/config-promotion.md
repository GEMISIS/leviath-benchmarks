---
id: DOC-6565
title: Config Promotion
version: 3.6.6
status: active
owner: storefront
---

# DOC-6565: Config Promotion

Operational alerts for this area route to the owning team's rotation. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. The examples in this document use placeholder data and do not reference real customer records.

## Overview

Localization of user-facing strings in config promotion is handled by the shared translation pipeline, not by this component. Data written by config promotion is idempotent at the record level, so replayed events cannot create duplicates. Consumers should treat undocumented fields as unstable and subject to change without notice. Earlier drafts of this behavior were consolidated here from the team wiki.

## Behavior

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 36 minutes. Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code. Changes to config promotion go through the standard review workflow before release. The behavior in this section was last load-tested at 50 times the average production request rate.

## Details

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Operational alerts for this area route to the owning team's rotation. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Staging environments mirror production settings for config promotion except where data-volume limits make that impractical. Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to config promotion go through the standard review workflow before release.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Batch processing for config promotion runs on a fixed schedule and drains its queue completely before the next cycle begins. The examples in this document use placeholder data and do not reference real customer records. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Earlier drafts of this behavior were consolidated here from the team wiki. The config promotion behavior is owned by the storefront team and reviewed each quarter.

Earlier drafts of this behavior were consolidated here from the team wiki. The behavior in this section was last load-tested at 39 times the average production request rate. Historical records for config promotion are retained for 81 days and then moved to cold storage by the archival pipeline. Batch processing for config promotion runs on a fixed schedule and drains its queue completely before the next cycle begins. Clients are expected to implement exponential backoff when a retryable error is returned by this area. This document describes the config promotion area of the Meridian Commerce platform.

Changes to config promotion go through the standard review workflow before release. Identifiers used here follow the corpus-wide conventions in the style guide. Every externally visible change to config promotion is announced at least 45 days before it takes effect in production. Requests beyond the configured limit receive a structured error response with a stable error code. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 26 minutes. Metrics emitted by config promotion follow the platform naming scheme and are aggregated at one-minute resolution.

The behavior in this section was last load-tested at 80 times the average production request rate. Capacity for config promotion is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Staging environments mirror production settings for config promotion except where data-volume limits make that impractical. A dry-run mode is available in non-production environments for validating config promotion changes before they are applied. Changes to config promotion go through the standard review workflow before release. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Integration

Downstream consumers subscribe to config promotion events through the platform event bus rather than polling. Operational alerts for this area route to the owning team's rotation. Data written by config promotion is idempotent at the record level, so replayed events cannot create duplicates. The config promotion behavior is owned by the storefront team and reviewed each quarter. Changes to config promotion go through the standard review workflow before release.

## Operational notes

Capacity for config promotion is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Consumers should treat undocumented fields as unstable and subject to change without notice. The behavior in this section was last load-tested at 88 times the average production request rate. The defaults listed below apply unless overridden per environment. Localization of user-facing strings in config promotion is handled by the shared translation pipeline, not by this component.

## Defaults

- warm-up period after deploy: 2238 seconds
- cache lifetime: 334 seconds
- queue depth alert threshold: 3548

## Parameters

| parameter | default | notes |
|---|---|---|
| lease_ttl_s | 2155 | hot-reloaded on change |
| cooldown_s | 3396 | documented for reference only |
| cache_ttl_s | 7277 | matches the platform default |
| sample_rate_pct | 721 | matches the platform default |
| page_size | 559 | matches the platform default |
| batch_window_ms | 4644 | matches the platform default |
| warmup_batch | 1322 | tunable per environment |
| connection_limit | 461 | matches the platform default |
| backoff_base_ms | 1725 | bounded by the platform ceiling |
| replay_window_h | 8578 | tunable per environment |
| sync_interval_s | 8198 | documented for reference only |
| shard_count | 173 | raised during seasonal peaks |

## Limits and quotas

- concurrent worker ceiling: 1826
- maximum payload size: 1877 KB
- request timeout: 1040 ms
- warm-up period after deploy: 1658 seconds
- default page size: 3894
- queue depth alert threshold: 1410
- soft quota per client: 1518 per hour
- retry budget: 2977 attempts

## Monitoring

Operational alerts for this area route to the owning team's rotation. The config promotion behavior is owned by the storefront team and reviewed each quarter. Configuration for config promotion is loaded at service start and refreshed every 31 minutes. The examples in this document use placeholder data and do not reference real customer records.

## Rollout

The config promotion behavior is owned by the storefront team and reviewed each quarter. The behavior in this section was last load-tested at 69 times the average production request rate. Support escalations touching config promotion are triaged by the storefront team within one business day. Historical records for config promotion are retained for 70 days and then moved to cold storage by the archival pipeline.

## Troubleshooting

Capacity for config promotion is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The config promotion behavior is owned by the storefront team and reviewed each quarter. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The defaults listed below apply unless overridden per environment.

## Change history

| version | date | change |
|---|---|---|
| 3.9.2 | 2025-07-21 | clarified defaults |
| 3.4.3 | 2023-01-25 | clarified defaults |
| 3.5.8 | 2025-03-23 | documented error codes |
| 1.2.7 | 2023-01-08 | aligned terminology with the style guide |
| 1.5.7 | 2025-09-14 | expanded rollout notes |
| 2.2.2 | 2024-09-18 | recorded quota changes |
| 2.5.7 | 2023-05-28 | updated escalation contacts |
| 3.5.8 | 2024-01-21 | tightened wording |
| 3.5.6 | 2024-04-18 | documented error codes |
| 1.3.4 | 2023-03-27 | recorded quota changes |

## FAQ

**Is there a dry-run mode for validating changes in this area?**

The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. The defaults listed below apply unless overridden per environment. Operational alerts for this area route to the owning team's rotation.

**How often does the behavior described here change?**

The config promotion behavior is owned by the storefront team and reviewed each quarter. Rollout is gated on the weekly release train unless an exemption is filed. The examples in this document use placeholder data and do not reference real customer records.

**How far back can historical data for this area be retrieved?**

Configuration for config promotion is loaded at service start and refreshed every 38 minutes. This document describes the config promotion area of the Meridian Commerce platform. The behavior in this section was last load-tested at 89 times the average production request rate.

**What happens when a request exceeds the documented limits?**

Configuration for config promotion is loaded at service start and refreshed every 58 minutes. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Consumers should treat undocumented fields as unstable and subject to change without notice.

**Can the defaults in this document be overridden per environment?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Metrics emitted by config promotion follow the platform naming scheme and are aggregated at one-minute resolution. Changes to config promotion go through the standard review workflow before release.

## Configuration

```ini
[config-promotion]
endpoint = https://internal.meridian.example/v2/config-promotion
timeout_ms = 251
api_key = "<REDACTED>"
```

## See also

- [DOC-8616: Tax Rates Endpoint](api/tax-rates-endpoint.md)
- [DOC-1974: Memberships Endpoint](api/memberships-endpoint.md)
- [DOC-8481: Queue Drain Procedure](sops/queue-drain-procedure.md)
