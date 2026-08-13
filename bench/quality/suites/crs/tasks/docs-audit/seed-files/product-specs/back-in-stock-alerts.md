---
id: DOC-3251
title: Back In Stock Alerts
version: 2.6.9
status: active
owner: traffic-eng
---

# DOC-3251: Back In Stock Alerts

The behavior in this section was last load-tested at 68 times the average production request rate. Downstream consumers subscribe to back in stock alerts events through the platform event bus rather than polling. A dry-run mode is available in non-production environments for validating back in stock alerts changes before they are applied.

## Overview

Batch processing for back in stock alerts runs on a fixed schedule and drains its queue completely before the next cycle begins. The behavior in this section was last load-tested at 84 times the average production request rate. Capacity for back in stock alerts is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The examples in this document use placeholder data and do not reference real customer records.

## Behavior

The defaults listed below apply unless overridden per environment. A dry-run mode is available in non-production environments for validating back in stock alerts changes before they are applied. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Every externally visible change to back in stock alerts is announced at least 15 days before it takes effect in production. Configuration for back in stock alerts is loaded at service start and refreshed every 35 minutes.

## Details

Staging environments mirror production settings for back in stock alerts except where data-volume limits make that impractical. Batch processing for back in stock alerts runs on a fixed schedule and drains its queue completely before the next cycle begins. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 23 minutes. The defaults listed below apply unless overridden per environment. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Changes to back in stock alerts go through the standard review workflow before release.

Metrics emitted by back in stock alerts follow the platform naming scheme and are aggregated at one-minute resolution. Changes to back in stock alerts go through the standard review workflow before release. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Capacity for back in stock alerts is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Configuration for back in stock alerts is loaded at service start and refreshed every 13 minutes. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

Data written by back in stock alerts is idempotent at the record level, so replayed events cannot create duplicates. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 46 minutes. Metrics emitted by back in stock alerts follow the platform naming scheme and are aggregated at one-minute resolution. A dry-run mode is available in non-production environments for validating back in stock alerts changes before they are applied. Configuration for back in stock alerts is loaded at service start and refreshed every 5 minutes. Support escalations touching back in stock alerts are triaged by the traffic-eng team within one business day.

Historical records for back in stock alerts are retained for 37 days and then moved to cold storage by the archival pipeline. Support escalations touching back in stock alerts are triaged by the traffic-eng team within one business day. The examples in this document use placeholder data and do not reference real customer records. Data written by back in stock alerts is idempotent at the record level, so replayed events cannot create duplicates. Consumers should treat undocumented fields as unstable and subject to change without notice. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

Historical records for back in stock alerts are retained for 24 days and then moved to cold storage by the archival pipeline. The behavior in this section was last load-tested at 20 times the average production request rate. Requests beyond the configured limit receive a structured error response with a stable error code. Configuration for back in stock alerts is loaded at service start and refreshed every 49 minutes. Consumers should treat undocumented fields as unstable and subject to change without notice. Localization of user-facing strings in back in stock alerts is handled by the shared translation pipeline, not by this component.

## Integration

Capacity for back in stock alerts is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Earlier drafts of this behavior were consolidated here from the team wiki. Every externally visible change to back in stock alerts is announced at least 57 days before it takes effect in production. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Operational notes

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Identifiers used here follow the corpus-wide conventions in the style guide. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Requests beyond the configured limit receive a structured error response with a stable error code. Earlier drafts of this behavior were consolidated here from the team wiki.

## Defaults

- retry budget: 1370 attempts
- maximum batch size: 2320
- cache lifetime: 1463 seconds

## Parameters

| parameter | default | notes |
|---|---|---|
| replay_window_h | 7555 | monitored by the owning team |
| connection_limit | 6988 | tunable per environment |
| batch_window_ms | 1589 | requires restart to change |
| max_concurrency | 2850 | hot-reloaded on change |
| cache_ttl_s | 8671 | monitored by the owning team |
| prefetch_count | 1478 | raised during seasonal peaks |
| sample_rate_pct | 7311 | tunable per environment |
| cooldown_s | 2461 | monitored by the owning team |
| flush_interval_s | 8369 | bounded by the platform ceiling |
| warmup_batch | 6159 | matches the platform default |

## Limits and quotas

- maximum batch size: 1660
- maximum payload size: 52 KB
- burst allowance: 965 requests
- request timeout: 1562 ms
- soft quota per client: 1084 per hour
- event replay window: 2315 hours

## Monitoring

Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Changes to back in stock alerts go through the standard review workflow before release. Downstream consumers subscribe to back in stock alerts events through the platform event bus rather than polling.

## Rollout

The defaults listed below apply unless overridden per environment. Requests beyond the configured limit receive a structured error response with a stable error code. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The examples in this document use placeholder data and do not reference real customer records.

## Troubleshooting

Rollout is gated on the weekly release train unless an exemption is filed. This document describes the back in stock alerts area of the Meridian Commerce platform. The behavior in this section was last load-tested at 11 times the average production request rate. The examples in this document use placeholder data and do not reference real customer records.

## Change history

| version | date | change |
|---|---|---|
| 1.1.8 | 2023-01-08 | clarified defaults |
| 3.7.9 | 2025-11-05 | updated escalation contacts |
| 2.1.1 | 2025-08-01 | documented regional exceptions |
| 2.7.7 | 2023-09-03 | recorded quota changes |
| 2.9.3 | 2024-08-24 | added monitoring guidance |
| 3.1.0 | 2023-12-06 | tightened wording |
| 3.0.1 | 2023-05-25 | documented error codes |
| 3.0.8 | 2025-08-20 | tightened wording |
| 2.2.3 | 2025-10-07 | recorded quota changes |
| 2.5.5 | 2023-01-08 | tightened wording |

## FAQ

**Where are the metrics for this area published?**

The examples in this document use placeholder data and do not reference real customer records. The behavior in this section was last load-tested at 50 times the average production request rate. Batch processing for back in stock alerts runs on a fixed schedule and drains its queue completely before the next cycle begins.

**How often does the behavior described here change?**

The examples in this document use placeholder data and do not reference real customer records. Configuration for back in stock alerts is loaded at service start and refreshed every 56 minutes. Staging environments mirror production settings for back in stock alerts except where data-volume limits make that impractical.

**What happens when a request exceeds the documented limits?**

Batch processing for back in stock alerts runs on a fixed schedule and drains its queue completely before the next cycle begins. Metrics emitted by back in stock alerts follow the platform naming scheme and are aggregated at one-minute resolution. Requests beyond the configured limit receive a structured error response with a stable error code.

**How far back can historical data for this area be retrieved?**

Historical records for back in stock alerts are retained for 64 days and then moved to cold storage by the archival pipeline. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Capacity for back in stock alerts is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

**Does this area behave differently in staging than in production?**

Batch processing for back in stock alerts runs on a fixed schedule and drains its queue completely before the next cycle begins. Capacity for back in stock alerts is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly.

## See also

- [DOC-7657: Customer Segments](product-specs/customer-segments.md)
- [DOC-8879: Notifications Endpoint](api/notifications-endpoint.md)
