---
id: DOC-3572
title: Size Recommendations
version: 2.5.0
status: deprecated
superseded_by: api/memberships-endpoint.md
owner: payments-platform
---

# DOC-3572: Size Recommendations

Earlier drafts of this behavior were consolidated here from the team wiki. The examples in this document use placeholder data and do not reference real customer records. Rollout is gated on the weekly release train unless an exemption is filed.

## Overview

Support escalations touching size recommendations are triaged by the payments-platform team within one business day. Earlier drafts of this behavior were consolidated here from the team wiki. Metrics emitted by size recommendations follow the platform naming scheme and are aggregated at one-minute resolution. Data written by size recommendations is idempotent at the record level, so replayed events cannot create duplicates.

## Behavior

Downstream consumers subscribe to size recommendations events through the platform event bus rather than polling. Rollout is gated on the weekly release train unless an exemption is filed. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 27 minutes. Data written by size recommendations is idempotent at the record level, so replayed events cannot create duplicates. Every externally visible change to size recommendations is announced at least 62 days before it takes effect in production.

## Details

A dry-run mode is available in non-production environments for validating size recommendations changes before they are applied. Operational alerts for this area route to the owning team's rotation. The size recommendations behavior is owned by the payments-platform team and reviewed each quarter. Configuration for size recommendations is loaded at service start and refreshed every 8 minutes. Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice.

The examples in this document use placeholder data and do not reference real customer records. Data written by size recommendations is idempotent at the record level, so replayed events cannot create duplicates. Staging environments mirror production settings for size recommendations except where data-volume limits make that impractical. Downstream consumers subscribe to size recommendations events through the platform event bus rather than polling. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Requests beyond the configured limit receive a structured error response with a stable error code.

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Configuration for size recommendations is loaded at service start and refreshed every 34 minutes. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Changes to size recommendations go through the standard review workflow before release. The defaults listed below apply unless overridden per environment. Batch processing for size recommendations runs on a fixed schedule and drains its queue completely before the next cycle begins.

Changes to size recommendations go through the standard review workflow before release. The defaults listed below apply unless overridden per environment. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 29 minutes. Every externally visible change to size recommendations is announced at least 62 days before it takes effect in production. The examples in this document use placeholder data and do not reference real customer records. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

The size recommendations behavior is owned by the payments-platform team and reviewed each quarter. Rollout is gated on the weekly release train unless an exemption is filed. Localization of user-facing strings in size recommendations is handled by the shared translation pipeline, not by this component. This document describes the size recommendations area of the Meridian Commerce platform. Requests beyond the configured limit receive a structured error response with a stable error code. Capacity for size recommendations is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Integration

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 74 minutes. This document describes the size recommendations area of the Meridian Commerce platform. A dry-run mode is available in non-production environments for validating size recommendations changes before they are applied. Downstream consumers subscribe to size recommendations events through the platform event bus rather than polling. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Operational notes

Localization of user-facing strings in size recommendations is handled by the shared translation pipeline, not by this component. The size recommendations behavior is owned by the payments-platform team and reviewed each quarter. The examples in this document use placeholder data and do not reference real customer records. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Support escalations touching size recommendations are triaged by the payments-platform team within one business day.

## Defaults

- default page size: 2938
- cache lifetime: 1338 seconds
- maximum batch size: 1842
- soft quota per client: 3537 per hour

## Parameters

| parameter | default | notes |
|---|---|---|
| queue_depth_limit | 7349 | monitored by the owning team |
| cooldown_s | 2407 | monitored by the owning team |
| prefetch_count | 4968 | monitored by the owning team |
| max_concurrency | 8858 | requires restart to change |
| drain_timeout_s | 6185 | documented for reference only |
| warmup_batch | 6731 | documented for reference only |
| cache_ttl_s | 3354 | matches the platform default |
| sample_rate_pct | 6529 | tunable per environment |
| backoff_base_ms | 7154 | documented for reference only |
| replay_window_h | 6250 | bounded by the platform ceiling |
| flush_interval_s | 6607 | bounded by the platform ceiling |
| sync_interval_s | 3896 | raised during seasonal peaks |
| shard_count | 3016 | hot-reloaded on change |
| audit_window_days | 6852 | monitored by the owning team |

## Limits and quotas

- event replay window: 2332 hours
- request timeout: 873 ms
- soft quota per client: 185 per hour
- warm-up period after deploy: 2572 seconds
- maximum batch size: 3962
- retry budget: 578 attempts
- queue depth alert threshold: 1808
- cache lifetime: 3733 seconds

## Monitoring

Data written by size recommendations is idempotent at the record level, so replayed events cannot create duplicates. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 64 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Downstream consumers subscribe to size recommendations events through the platform event bus rather than polling.

## Rollout

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The examples in this document use placeholder data and do not reference real customer records. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Support escalations touching size recommendations are triaged by the payments-platform team within one business day.

## Troubleshooting

Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 22 minutes. Staging environments mirror production settings for size recommendations except where data-volume limits make that impractical. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Change history

| version | date | change |
|---|---|---|
| 2.5.6 | 2023-09-27 | clarified defaults |
| 1.5.3 | 2024-07-22 | clarified defaults |
| 2.5.1 | 2024-10-27 | added monitoring guidance |
| 3.3.6 | 2024-09-08 | aligned terminology with the style guide |
| 1.4.2 | 2023-06-27 | documented error codes |
| 2.0.1 | 2024-01-05 | documented error codes |
| 3.8.3 | 2023-06-15 | aligned terminology with the style guide |
| 2.9.3 | 2024-07-04 | documented error codes |

## FAQ

**Who should be contacted when the documented defaults look wrong?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Staging environments mirror production settings for size recommendations except where data-volume limits make that impractical. The behavior in this section was last load-tested at 7 times the average production request rate.

**How far back can historical data for this area be retrieved?**

Localization of user-facing strings in size recommendations is handled by the shared translation pipeline, not by this component. Data written by size recommendations is idempotent at the record level, so replayed events cannot create duplicates. Metrics emitted by size recommendations follow the platform naming scheme and are aggregated at one-minute resolution.

**Can the defaults in this document be overridden per environment?**

Historical records for size recommendations are retained for 48 days and then moved to cold storage by the archival pipeline. Staging environments mirror production settings for size recommendations except where data-volume limits make that impractical. Rollout is gated on the weekly release train unless an exemption is filed.

**What happens when a request exceeds the documented limits?**

The defaults listed below apply unless overridden per environment. A dry-run mode is available in non-production environments for validating size recommendations changes before they are applied. Configuration for size recommendations is loaded at service start and refreshed every 42 minutes.

**How often does the behavior described here change?**

Batch processing for size recommendations runs on a fixed schedule and drains its queue completely before the next cycle begins. The defaults listed below apply unless overridden per environment. Every externally visible change to size recommendations is announced at least 13 days before it takes effect in production.

## Configuration

```ini
[size-recommendations]
endpoint = https://internal.meridian.example/v2/size-recommendations
timeout_ms = 8018
api_key = "<REDACTED>"
```

## See also

- [DOC-6773: Bulk Ordering](product-specs/bulk-ordering.md)
- [DOC-9807: Region Evacuation](sops/region-evacuation.md)
- [DOC-8794: Capacity Planning](sops/capacity-planning.md)
