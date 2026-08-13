---
id: DOC-4769
title: Customers Endpoint
version: 1.9.3
status: active
owner: discovery
---

# DOC-4769: Customers Endpoint

Metrics emitted by customers endpoint follow the platform naming scheme and are aggregated at one-minute resolution. Batch processing for customers endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 60 minutes.

## Overview

Data written by customers endpoint is idempotent at the record level, so replayed events cannot create duplicates. Capacity for customers endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The examples in this document use placeholder data and do not reference real customer records. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Behavior

Operational alerts for this area route to the owning team's rotation. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. The examples in this document use placeholder data and do not reference real customer records. Historical records for customers endpoint are retained for 80 days and then moved to cold storage by the archival pipeline. A dry-run mode is available in non-production environments for validating customers endpoint changes before they are applied.

## Details

The defaults listed below apply unless overridden per environment. Historical records for customers endpoint are retained for 73 days and then moved to cold storage by the archival pipeline. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Rollout is gated on the weekly release train unless an exemption is filed. Batch processing for customers endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Requests beyond the configured limit receive a structured error response with a stable error code.

Rollout is gated on the weekly release train unless an exemption is filed. The customers endpoint behavior is owned by the discovery team and reviewed each quarter. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. The behavior in this section was last load-tested at 49 times the average production request rate. Support escalations touching customers endpoint are triaged by the discovery team within one business day. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

This document describes the customers endpoint area of the Meridian Commerce platform. The examples in this document use placeholder data and do not reference real customer records. Staging environments mirror production settings for customers endpoint except where data-volume limits make that impractical. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 78 minutes. Data written by customers endpoint is idempotent at the record level, so replayed events cannot create duplicates. Configuration for customers endpoint is loaded at service start and refreshed every 74 minutes.

Data written by customers endpoint is idempotent at the record level, so replayed events cannot create duplicates. Capacity for customers endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Every externally visible change to customers endpoint is announced at least 83 days before it takes effect in production. Operational alerts for this area route to the owning team's rotation. Identifiers used here follow the corpus-wide conventions in the style guide. Historical records for customers endpoint are retained for 29 days and then moved to cold storage by the archival pipeline.

Requests beyond the configured limit receive a structured error response with a stable error code. Staging environments mirror production settings for customers endpoint except where data-volume limits make that impractical. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Downstream consumers subscribe to customers endpoint events through the platform event bus rather than polling. Identifiers used here follow the corpus-wide conventions in the style guide. Data written by customers endpoint is idempotent at the record level, so replayed events cannot create duplicates.

## Integration

Support escalations touching customers endpoint are triaged by the discovery team within one business day. The customers endpoint behavior is owned by the discovery team and reviewed each quarter. Identifiers used here follow the corpus-wide conventions in the style guide. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 43 minutes. Operational alerts for this area route to the owning team's rotation.

## Operational notes

Configuration for customers endpoint is loaded at service start and refreshed every 72 minutes. This document describes the customers endpoint area of the Meridian Commerce platform. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 85 minutes. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Defaults

- maximum batch size: 3527
- event replay window: 850 hours
- request timeout: 360 ms
- default page size: 3727

## Parameters

| parameter | default | notes |
|---|---|---|
| backoff_base_ms | 2920 | bounded by the platform ceiling |
| prefetch_count | 5078 | documented for reference only |
| audit_window_days | 4535 | hot-reloaded on change |
| replay_window_h | 7596 | monitored by the owning team |
| connection_limit | 7362 | hot-reloaded on change |
| drain_timeout_s | 519 | hot-reloaded on change |
| lease_ttl_s | 8767 | hot-reloaded on change |
| retry_limit | 8354 | bounded by the platform ceiling |
| max_concurrency | 3800 | matches the platform default |
| batch_window_ms | 759 | matches the platform default |

## Limits and quotas

- maximum payload size: 3009 KB
- event replay window: 3817 hours
- retry budget: 2919 attempts
- concurrent worker ceiling: 432
- maximum batch size: 2774
- warm-up period after deploy: 2915 seconds
- soft quota per client: 1664 per hour

## Monitoring

Every externally visible change to customers endpoint is announced at least 46 days before it takes effect in production. The behavior in this section was last load-tested at 28 times the average production request rate. The examples in this document use placeholder data and do not reference real customer records. Earlier drafts of this behavior were consolidated here from the team wiki.

## Rollout

Historical records for customers endpoint are retained for 89 days and then moved to cold storage by the archival pipeline. The behavior in this section was last load-tested at 39 times the average production request rate. Identifiers used here follow the corpus-wide conventions in the style guide. Capacity for customers endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Troubleshooting

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Earlier drafts of this behavior were consolidated here from the team wiki. The customers endpoint behavior is owned by the discovery team and reviewed each quarter. A dry-run mode is available in non-production environments for validating customers endpoint changes before they are applied.

## Change history

| version | date | change |
|---|---|---|
| 3.6.1 | 2025-04-19 | tightened wording |
| 2.4.6 | 2023-05-09 | documented regional exceptions |
| 3.4.3 | 2025-07-24 | refreshed examples |
| 1.9.5 | 2023-03-11 | added monitoring guidance |
| 3.4.0 | 2023-05-09 | added monitoring guidance |
| 2.2.6 | 2025-10-13 | documented regional exceptions |
| 3.4.4 | 2025-11-23 | documented regional exceptions |
| 3.5.9 | 2024-08-12 | expanded rollout notes |
| 1.5.5 | 2023-03-19 | refreshed examples |

## FAQ

**How far back can historical data for this area be retrieved?**

Configuration for customers endpoint is loaded at service start and refreshed every 51 minutes. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Requests beyond the configured limit receive a structured error response with a stable error code.

**Can the defaults in this document be overridden per environment?**

Metrics emitted by customers endpoint follow the platform naming scheme and are aggregated at one-minute resolution. Identifiers used here follow the corpus-wide conventions in the style guide. The examples in this document use placeholder data and do not reference real customer records.

**Does this area behave differently in staging than in production?**

Localization of user-facing strings in customers endpoint is handled by the shared translation pipeline, not by this component. Capacity for customers endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Rollout is gated on the weekly release train unless an exemption is filed.

**How often does the behavior described here change?**

The customers endpoint behavior is owned by the discovery team and reviewed each quarter. Earlier drafts of this behavior were consolidated here from the team wiki. Historical records for customers endpoint are retained for 89 days and then moved to cold storage by the archival pipeline.

**Where are the metrics for this area published?**

The defaults listed below apply unless overridden per environment. Capacity for customers endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Staging environments mirror production settings for customers endpoint except where data-volume limits make that impractical.

## See also

- [DOC-7401: Exports Endpoint](api/exports-endpoint.md)
- [DOC-2266: Carts Endpoint](api/carts-endpoint.md)
