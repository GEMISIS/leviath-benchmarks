---
id: DOC-3928
title: Vendor Dropship
version: 1.5.3
status: active
owner: payments-platform
---

# DOC-3928: Vendor Dropship

Metrics emitted by vendor dropship follow the platform naming scheme and are aggregated at one-minute resolution. Capacity for vendor dropship is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Overview

Rollout is gated on the weekly release train unless an exemption is filed. Batch processing for vendor dropship runs on a fixed schedule and drains its queue completely before the next cycle begins. Support escalations touching vendor dropship are triaged by the payments-platform team within one business day. Staging environments mirror production settings for vendor dropship except where data-volume limits make that impractical.

## Behavior

The vendor dropship behavior is owned by the payments-platform team and reviewed each quarter. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. This document describes the vendor dropship area of the Meridian Commerce platform. Downstream consumers subscribe to vendor dropship events through the platform event bus rather than polling. The examples in this document use placeholder data and do not reference real customer records.

## Details

Configuration for vendor dropship is loaded at service start and refreshed every 68 minutes. The behavior in this section was last load-tested at 22 times the average production request rate. A dry-run mode is available in non-production environments for validating vendor dropship changes before they are applied. The defaults listed below apply unless overridden per environment. Downstream consumers subscribe to vendor dropship events through the platform event bus rather than polling. Historical records for vendor dropship are retained for 73 days and then moved to cold storage by the archival pipeline.

Requests beyond the configured limit receive a structured error response with a stable error code. The examples in this document use placeholder data and do not reference real customer records. Data written by vendor dropship is idempotent at the record level, so replayed events cannot create duplicates. Identifiers used here follow the corpus-wide conventions in the style guide. Operational alerts for this area route to the owning team's rotation. Earlier drafts of this behavior were consolidated here from the team wiki.

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 6 minutes. A dry-run mode is available in non-production environments for validating vendor dropship changes before they are applied. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Staging environments mirror production settings for vendor dropship except where data-volume limits make that impractical.

Identifiers used here follow the corpus-wide conventions in the style guide. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Every externally visible change to vendor dropship is announced at least 86 days before it takes effect in production. Rollout is gated on the weekly release train unless an exemption is filed. Configuration for vendor dropship is loaded at service start and refreshed every 71 minutes.

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 41 minutes. The examples in this document use placeholder data and do not reference real customer records. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Capacity for vendor dropship is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Every externally visible change to vendor dropship is announced at least 66 days before it takes effect in production. Configuration for vendor dropship is loaded at service start and refreshed every 34 minutes.

## Integration

Clients are expected to implement exponential backoff when a retryable error is returned by this area. The vendor dropship behavior is owned by the payments-platform team and reviewed each quarter. Changes to vendor dropship go through the standard review workflow before release. Capacity for vendor dropship is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Rollout is gated on the weekly release train unless an exemption is filed.

## Operational notes

Capacity for vendor dropship is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Rollout is gated on the weekly release train unless an exemption is filed. The vendor dropship behavior is owned by the payments-platform team and reviewed each quarter. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. Staging environments mirror production settings for vendor dropship except where data-volume limits make that impractical.

## Defaults

- event replay window: 3776 hours
- soft quota per client: 3709 per hour
- warm-up period after deploy: 3968 seconds

## Parameters

| parameter | default | notes |
|---|---|---|
| prefetch_count | 1283 | monitored by the owning team |
| connection_limit | 4330 | raised during seasonal peaks |
| retry_limit | 503 | bounded by the platform ceiling |
| sample_rate_pct | 1370 | bounded by the platform ceiling |
| cache_ttl_s | 5196 | documented for reference only |
| flush_interval_s | 3260 | documented for reference only |
| backoff_base_ms | 3859 | bounded by the platform ceiling |
| queue_depth_limit | 6438 | matches the platform default |
| sync_interval_s | 6150 | matches the platform default |
| replay_window_h | 3465 | bounded by the platform ceiling |
| drain_timeout_s | 3784 | tunable per environment |
| page_size | 3548 | tunable per environment |

## Limits and quotas

- warm-up period after deploy: 486 seconds
- retry budget: 1583 attempts
- default page size: 657
- event replay window: 1297 hours
- concurrent worker ceiling: 189
- burst allowance: 1634 requests
- maximum batch size: 3473

## Monitoring

Requests beyond the configured limit receive a structured error response with a stable error code. Data written by vendor dropship is idempotent at the record level, so replayed events cannot create duplicates. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. Configuration for vendor dropship is loaded at service start and refreshed every 35 minutes.

## Rollout

Localization of user-facing strings in vendor dropship is handled by the shared translation pipeline, not by this component. Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice. Historical records for vendor dropship are retained for 7 days and then moved to cold storage by the archival pipeline.

## Troubleshooting

Configuration for vendor dropship is loaded at service start and refreshed every 57 minutes. Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly.

## Change history

| version | date | change |
|---|---|---|
| 1.2.0 | 2025-03-12 | aligned terminology with the style guide |
| 1.2.6 | 2023-10-03 | updated escalation contacts |
| 2.3.8 | 2024-08-08 | refreshed examples |
| 2.5.7 | 2023-03-14 | documented error codes |
| 3.8.8 | 2023-08-08 | refreshed examples |
| 2.8.0 | 2025-06-25 | documented error codes |
| 1.9.0 | 2024-06-03 | tightened wording |
| 3.9.5 | 2023-11-17 | updated escalation contacts |

## FAQ

**Who should be contacted when the documented defaults look wrong?**

Capacity for vendor dropship is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. A dry-run mode is available in non-production environments for validating vendor dropship changes before they are applied. This document describes the vendor dropship area of the Meridian Commerce platform.

**Does this area behave differently in staging than in production?**

The vendor dropship behavior is owned by the payments-platform team and reviewed each quarter. Configuration for vendor dropship is loaded at service start and refreshed every 26 minutes. Downstream consumers subscribe to vendor dropship events through the platform event bus rather than polling.

**Can the defaults in this document be overridden per environment?**

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Support escalations touching vendor dropship are triaged by the payments-platform team within one business day. Staging environments mirror production settings for vendor dropship except where data-volume limits make that impractical.

**How often does the behavior described here change?**

The behavior in this section was last load-tested at 41 times the average production request rate. Batch processing for vendor dropship runs on a fixed schedule and drains its queue completely before the next cycle begins. Earlier drafts of this behavior were consolidated here from the team wiki.

## Configuration

```ini
[vendor-dropship]
endpoint = https://internal.meridian.example/v2/vendor-dropship
timeout_ms = 6241
api_key = "<REDACTED>"
```

## See also

- [DOC-7780: Search Personalization](product-specs/search-personalization.md)
- [DOC-8544: Webhook Retries](api/webhook-retries.md)
- [DOC-3067: Curbside Pickup](product-specs/curbside-pickup.md)
