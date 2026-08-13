---
id: DOC-3928
title: Vendor Dropship
version: 1.5.3
status: active
owner: payments-platform
---

# DOC-3928: Vendor Dropship

The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Support escalations touching vendor dropship are triaged by the payments-platform team within one business day. Identifiers used here follow the corpus-wide conventions in the style guide.

## Overview

Identifiers used here follow the corpus-wide conventions in the style guide. Metrics emitted by vendor dropship follow the platform naming scheme and are aggregated at one-minute resolution. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. The vendor dropship behavior is owned by the payments-platform team and reviewed each quarter.

## Behavior

Requests beyond the configured limit receive a structured error response with a stable error code. Metrics emitted by vendor dropship follow the platform naming scheme and are aggregated at one-minute resolution. Configuration for vendor dropship is loaded at service start and refreshed every 37 minutes. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 62 minutes.

## Details

Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Localization of user-facing strings in vendor dropship is handled by the shared translation pipeline, not by this component. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. This document describes the vendor dropship area of the Meridian Commerce platform. Downstream consumers subscribe to vendor dropship events through the platform event bus rather than polling.

Changes to vendor dropship go through the standard review workflow before release. Support escalations touching vendor dropship are triaged by the payments-platform team within one business day. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 65 minutes. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Historical records for vendor dropship are retained for 67 days and then moved to cold storage by the archival pipeline. The examples in this document use placeholder data and do not reference real customer records.

Historical records for vendor dropship are retained for 87 days and then moved to cold storage by the archival pipeline. Localization of user-facing strings in vendor dropship is handled by the shared translation pipeline, not by this component. This document describes the vendor dropship area of the Meridian Commerce platform. A dry-run mode is available in non-production environments for validating vendor dropship changes before they are applied. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Rollout is gated on the weekly release train unless an exemption is filed.

Batch processing for vendor dropship runs on a fixed schedule and drains its queue completely before the next cycle begins. Rollout is gated on the weekly release train unless an exemption is filed. Support escalations touching vendor dropship are triaged by the payments-platform team within one business day. Staging environments mirror production settings for vendor dropship except where data-volume limits make that impractical. Downstream consumers subscribe to vendor dropship events through the platform event bus rather than polling. This document describes the vendor dropship area of the Meridian Commerce platform.

Requests beyond the configured limit receive a structured error response with a stable error code. The defaults listed below apply unless overridden per environment. Earlier drafts of this behavior were consolidated here from the team wiki. Capacity for vendor dropship is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Configuration for vendor dropship is loaded at service start and refreshed every 68 minutes. The behavior in this section was last load-tested at 22 times the average production request rate.

## Integration

Requests beyond the configured limit receive a structured error response with a stable error code. Rollout is gated on the weekly release train unless an exemption is filed. Historical records for vendor dropship are retained for 49 days and then moved to cold storage by the archival pipeline. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. Data written by vendor dropship is idempotent at the record level, so replayed events cannot create duplicates.

## Operational notes

Batch processing for vendor dropship runs on a fixed schedule and drains its queue completely before the next cycle begins. Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for vendor dropship except where data-volume limits make that impractical. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 6 minutes.

## Defaults

- event replay window: 668 hours
- burst allowance: 2501 requests
- warm-up period after deploy: 1387 seconds
- maximum batch size: 1806

## Parameters

| parameter | default | notes |
|---|---|---|
| batch_window_ms | 6583 | raised during seasonal peaks |
| max_concurrency | 7845 | matches the platform default |
| warmup_batch | 3755 | tunable per environment |
| cache_ttl_s | 1368 | raised during seasonal peaks |
| page_size | 7310 | bounded by the platform ceiling |
| lease_ttl_s | 5756 | hot-reloaded on change |
| sample_rate_pct | 5064 | raised during seasonal peaks |
| sync_interval_s | 1008 | documented for reference only |
| audit_window_days | 4051 | hot-reloaded on change |
| backoff_base_ms | 7980 | tunable per environment |
| retry_limit | 6018 | monitored by the owning team |
| max_payload_kb | 8375 | raised during seasonal peaks |

## Limits and quotas

- default page size: 243
- cache lifetime: 330 seconds
- maximum batch size: 3985
- queue depth alert threshold: 1493
- soft quota per client: 1092 per hour
- retry budget: 1251 attempts
- concurrent worker ceiling: 135
- event replay window: 979 hours

## Monitoring

Changes to vendor dropship go through the standard review workflow before release. The defaults listed below apply unless overridden per environment. Support escalations touching vendor dropship are triaged by the payments-platform team within one business day. The behavior in this section was last load-tested at 30 times the average production request rate.

## Rollout

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Historical records for vendor dropship are retained for 55 days and then moved to cold storage by the archival pipeline. The defaults listed below apply unless overridden per environment.

## Troubleshooting

Localization of user-facing strings in vendor dropship is handled by the shared translation pipeline, not by this component. Data written by vendor dropship is idempotent at the record level, so replayed events cannot create duplicates. Historical records for vendor dropship are retained for 32 days and then moved to cold storage by the archival pipeline. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list.

## Change history

| version | date | change |
|---|---|---|
| 1.3.0 | 2024-09-07 | clarified defaults |
| 3.3.2 | 2023-07-06 | recorded quota changes |
| 1.6.2 | 2025-02-06 | documented regional exceptions |
| 3.3.4 | 2024-10-27 | documented regional exceptions |
| 2.6.0 | 2023-04-05 | documented regional exceptions |
| 2.9.2 | 2025-04-04 | expanded rollout notes |
| 1.9.2 | 2024-04-04 | expanded rollout notes |
| 2.2.9 | 2023-10-26 | recorded quota changes |

## FAQ

**How far back can historical data for this area be retrieved?**

Data written by vendor dropship is idempotent at the record level, so replayed events cannot create duplicates. Downstream consumers subscribe to vendor dropship events through the platform event bus rather than polling. Rollout is gated on the weekly release train unless an exemption is filed.

**Is there a dry-run mode for validating changes in this area?**

The examples in this document use placeholder data and do not reference real customer records. Localization of user-facing strings in vendor dropship is handled by the shared translation pipeline, not by this component. Requests beyond the configured limit receive a structured error response with a stable error code.

**What happens when a request exceeds the documented limits?**

Support escalations touching vendor dropship are triaged by the payments-platform team within one business day. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. Metrics emitted by vendor dropship follow the platform naming scheme and are aggregated at one-minute resolution.

**Who should be contacted when the documented defaults look wrong?**

The defaults listed below apply unless overridden per environment. Consumers should treat undocumented fields as unstable and subject to change without notice. Downstream consumers subscribe to vendor dropship events through the platform event bus rather than polling.

## Configuration

```ini
[vendor-dropship]
endpoint = https://internal.meridian.example/v2/vendor-dropship
timeout_ms = 5538
api_key = "<REDACTED>"
```

## See also

- [DOC-1233: Returns Portal](product-specs/returns-portal.md)
- [DOC-3761: Shipping Endpoint](api/shipping-endpoint.md)
