---
id: DOC-7518
title: Promotions Endpoint
version: 2.7.7
status: deprecated
superseded_by: sops/maintenance-windows.md
owner: payments-platform
---

# DOC-7518: Promotions Endpoint

Requests beyond the configured limit receive a structured error response with a stable error code. Metrics emitted by promotions endpoint follow the platform naming scheme and are aggregated at one-minute resolution. Historical records for promotions endpoint are retained for 43 days and then moved to cold storage by the archival pipeline.

## Overview

Configuration for promotions endpoint is loaded at service start and refreshed every 71 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Operational alerts for this area route to the owning team's rotation. Historical records for promotions endpoint are retained for 83 days and then moved to cold storage by the archival pipeline.

## Behavior

The promotions endpoint behavior is owned by the payments-platform team and reviewed each quarter. Rollout is gated on the weekly release train unless an exemption is filed. The examples in this document use placeholder data and do not reference real customer records. Staging environments mirror production settings for promotions endpoint except where data-volume limits make that impractical. Requests beyond the configured limit receive a structured error response with a stable error code.

## Details

The defaults listed below apply unless overridden per environment. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Consumers should treat undocumented fields as unstable and subject to change without notice. The behavior in this section was last load-tested at 89 times the average production request rate. Requests beyond the configured limit receive a structured error response with a stable error code. Configuration for promotions endpoint is loaded at service start and refreshed every 75 minutes.

Support escalations touching promotions endpoint are triaged by the payments-platform team within one business day. Consumers should treat undocumented fields as unstable and subject to change without notice. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 55 minutes. The behavior in this section was last load-tested at 13 times the average production request rate. Requests beyond the configured limit receive a structured error response with a stable error code. Capacity for promotions endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Requests beyond the configured limit receive a structured error response with a stable error code. The behavior in this section was last load-tested at 8 times the average production request rate. Rollout is gated on the weekly release train unless an exemption is filed. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

Staging environments mirror production settings for promotions endpoint except where data-volume limits make that impractical. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Configuration for promotions endpoint is loaded at service start and refreshed every 54 minutes. Historical records for promotions endpoint are retained for 83 days and then moved to cold storage by the archival pipeline. A dry-run mode is available in non-production environments for validating promotions endpoint changes before they are applied. Earlier drafts of this behavior were consolidated here from the team wiki.

Consumers should treat undocumented fields as unstable and subject to change without notice. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 22 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Data written by promotions endpoint is idempotent at the record level, so replayed events cannot create duplicates. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Downstream consumers subscribe to promotions endpoint events through the platform event bus rather than polling.

## Integration

Batch processing for promotions endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. The promotions endpoint behavior is owned by the payments-platform team and reviewed each quarter. Downstream consumers subscribe to promotions endpoint events through the platform event bus rather than polling. Every externally visible change to promotions endpoint is announced at least 51 days before it takes effect in production. Rollout is gated on the weekly release train unless an exemption is filed.

## Operational notes

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 42 minutes. The behavior in this section was last load-tested at 89 times the average production request rate. Every externally visible change to promotions endpoint is announced at least 11 days before it takes effect in production. Consumers should treat undocumented fields as unstable and subject to change without notice. Earlier drafts of this behavior were consolidated here from the team wiki.

## Defaults

- default page size: 1584
- maximum payload size: 1480 KB
- maximum batch size: 820

## Parameters

| parameter | default | notes |
|---|---|---|
| backoff_base_ms | 4266 | tunable per environment |
| audit_window_days | 7448 | documented for reference only |
| warmup_batch | 339 | requires restart to change |
| max_payload_kb | 5058 | raised during seasonal peaks |
| connection_limit | 3383 | raised during seasonal peaks |
| replay_window_h | 5385 | hot-reloaded on change |
| flush_interval_s | 1203 | documented for reference only |
| queue_depth_limit | 5163 | documented for reference only |
| shard_count | 5879 | documented for reference only |
| sample_rate_pct | 5948 | raised during seasonal peaks |
| retry_limit | 8656 | bounded by the platform ceiling |
| page_size | 1143 | monitored by the owning team |
| sync_interval_s | 35 | bounded by the platform ceiling |

## Limits and quotas

- retry budget: 617 attempts
- cache lifetime: 2179 seconds
- maximum batch size: 2888
- request timeout: 2776 ms
- maximum payload size: 2463 KB
- concurrent worker ceiling: 1472
- soft quota per client: 2247 per hour
- burst allowance: 2852 requests

## Monitoring

The behavior in this section was last load-tested at 38 times the average production request rate. Every externally visible change to promotions endpoint is announced at least 11 days before it takes effect in production. This document describes the promotions endpoint area of the Meridian Commerce platform. Localization of user-facing strings in promotions endpoint is handled by the shared translation pipeline, not by this component.

## Rollout

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Requests beyond the configured limit receive a structured error response with a stable error code. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Capacity for promotions endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Troubleshooting

Localization of user-facing strings in promotions endpoint is handled by the shared translation pipeline, not by this component. The promotions endpoint behavior is owned by the payments-platform team and reviewed each quarter. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Metrics emitted by promotions endpoint follow the platform naming scheme and are aggregated at one-minute resolution.

## Change history

| version | date | change |
|---|---|---|
| 1.3.9 | 2023-02-06 | aligned terminology with the style guide |
| 1.1.1 | 2024-04-13 | added monitoring guidance |
| 1.0.2 | 2024-05-22 | updated escalation contacts |
| 2.5.8 | 2024-02-21 | documented regional exceptions |
| 2.3.5 | 2025-05-12 | added monitoring guidance |
| 1.4.7 | 2025-12-09 | refreshed examples |
| 1.5.8 | 2023-01-28 | added monitoring guidance |
| 2.4.0 | 2023-11-15 | documented error codes |
| 2.6.0 | 2024-11-09 | expanded rollout notes |
| 1.9.2 | 2024-05-14 | clarified defaults |

## FAQ

**How far back can historical data for this area be retrieved?**

Batch processing for promotions endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. The behavior in this section was last load-tested at 53 times the average production request rate. Localization of user-facing strings in promotions endpoint is handled by the shared translation pipeline, not by this component.

**Can the defaults in this document be overridden per environment?**

The examples in this document use placeholder data and do not reference real customer records. Data written by promotions endpoint is idempotent at the record level, so replayed events cannot create duplicates. The defaults listed below apply unless overridden per environment.

**Where are the metrics for this area published?**

Support escalations touching promotions endpoint are triaged by the payments-platform team within one business day. Requests beyond the configured limit receive a structured error response with a stable error code. Configuration for promotions endpoint is loaded at service start and refreshed every 27 minutes.

**Is there a dry-run mode for validating changes in this area?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 17 minutes. Downstream consumers subscribe to promotions endpoint events through the platform event bus rather than polling. Earlier drafts of this behavior were consolidated here from the team wiki.

**How often does the behavior described here change?**

Operational alerts for this area route to the owning team's rotation. The defaults listed below apply unless overridden per environment. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list.

## See also

- [DOC-3554: Feature Flag Hygiene](sops/feature-flag-hygiene.md)
- [DOC-7657: Customer Segments](product-specs/customer-segments.md)
