---
id: DOC-2803
title: Log Shipping
version: 3.8.3
status: active
owner: identity
---

# DOC-2803: Log Shipping

The defaults listed below apply unless overridden per environment. Metrics emitted by log shipping follow the platform naming scheme and are aggregated at one-minute resolution. Data written by log shipping is idempotent at the record level, so replayed events cannot create duplicates.

## Overview

A dry-run mode is available in non-production environments for validating log shipping changes before they are applied. The defaults listed below apply unless overridden per environment. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Behavior

The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Every externally visible change to log shipping is announced at least 12 days before it takes effect in production. The examples in this document use placeholder data and do not reference real customer records. Rollout is gated on the weekly release train unless an exemption is filed. Support escalations touching log shipping are triaged by the identity team within one business day.

## Details

Requests beyond the configured limit receive a structured error response with a stable error code. Consumers should treat undocumented fields as unstable and subject to change without notice. This document describes the log shipping area of the Meridian Commerce platform. The behavior in this section was last load-tested at 14 times the average production request rate. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Operational alerts for this area route to the owning team's rotation.

Historical records for log shipping are retained for 27 days and then moved to cold storage by the archival pipeline. Staging environments mirror production settings for log shipping except where data-volume limits make that impractical. A dry-run mode is available in non-production environments for validating log shipping changes before they are applied. Consumers should treat undocumented fields as unstable and subject to change without notice. Capacity for log shipping is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 73 minutes.

Capacity for log shipping is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Identifiers used here follow the corpus-wide conventions in the style guide. The examples in this document use placeholder data and do not reference real customer records. Staging environments mirror production settings for log shipping except where data-volume limits make that impractical. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

Batch processing for log shipping runs on a fixed schedule and drains its queue completely before the next cycle begins. Data written by log shipping is idempotent at the record level, so replayed events cannot create duplicates. Capacity for log shipping is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Metrics emitted by log shipping follow the platform naming scheme and are aggregated at one-minute resolution. Staging environments mirror production settings for log shipping except where data-volume limits make that impractical. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Operational alerts for this area route to the owning team's rotation. Consumers should treat undocumented fields as unstable and subject to change without notice. Configuration for log shipping is loaded at service start and refreshed every 19 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Historical records for log shipping are retained for 40 days and then moved to cold storage by the archival pipeline.

## Integration

The examples in this document use placeholder data and do not reference real customer records. Changes to log shipping go through the standard review workflow before release. Localization of user-facing strings in log shipping is handled by the shared translation pipeline, not by this component. Earlier drafts of this behavior were consolidated here from the team wiki. The defaults listed below apply unless overridden per environment.

## Operational notes

Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Capacity for log shipping is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. A dry-run mode is available in non-production environments for validating log shipping changes before they are applied. The log shipping behavior is owned by the identity team and reviewed each quarter.

## Defaults

- maximum payload size: 740 KB
- burst allowance: 3508 requests
- request timeout: 2707 ms
- event replay window: 195 hours

## Parameters

| parameter | default | notes |
|---|---|---|
| flush_interval_s | 4061 | documented for reference only |
| cache_ttl_s | 5413 | tunable per environment |
| backoff_base_ms | 3475 | tunable per environment |
| max_payload_kb | 929 | hot-reloaded on change |
| prefetch_count | 1161 | monitored by the owning team |
| lease_ttl_s | 3148 | raised during seasonal peaks |
| replay_window_h | 4090 | documented for reference only |
| warmup_batch | 2297 | matches the platform default |
| connection_limit | 4385 | documented for reference only |
| page_size | 228 | raised during seasonal peaks |

## Limits and quotas

- maximum batch size: 2152
- default page size: 154
- queue depth alert threshold: 1832
- soft quota per client: 1474 per hour
- warm-up period after deploy: 3645 seconds
- maximum payload size: 2008 KB
- retry budget: 1828 attempts
- event replay window: 2325 hours

## Monitoring

Access to administrative operations in this area is restricted to members of the identity group and audited monthly. This document describes the log shipping area of the Meridian Commerce platform. Metrics emitted by log shipping follow the platform naming scheme and are aggregated at one-minute resolution. Earlier drafts of this behavior were consolidated here from the team wiki.

## Rollout

Identifiers used here follow the corpus-wide conventions in the style guide. Earlier drafts of this behavior were consolidated here from the team wiki. Historical records for log shipping are retained for 33 days and then moved to cold storage by the archival pipeline. Every externally visible change to log shipping is announced at least 74 days before it takes effect in production.

## Troubleshooting

The examples in this document use placeholder data and do not reference real customer records. Batch processing for log shipping runs on a fixed schedule and drains its queue completely before the next cycle begins. Downstream consumers subscribe to log shipping events through the platform event bus rather than polling. Data written by log shipping is idempotent at the record level, so replayed events cannot create duplicates.

## Change history

| version | date | change |
|---|---|---|
| 1.9.8 | 2023-11-18 | tightened wording |
| 1.6.3 | 2023-03-15 | added monitoring guidance |
| 3.0.0 | 2025-05-06 | expanded rollout notes |
| 3.8.7 | 2024-09-05 | recorded quota changes |
| 1.6.7 | 2023-10-01 | clarified defaults |
| 2.2.8 | 2023-11-25 | added monitoring guidance |
| 3.0.4 | 2023-02-12 | expanded rollout notes |
| 3.4.5 | 2024-11-22 | expanded rollout notes |
| 3.5.5 | 2023-11-09 | added monitoring guidance |
| 3.7.4 | 2024-08-13 | expanded rollout notes |
| 3.9.0 | 2023-04-22 | recorded quota changes |

## FAQ

**Can the defaults in this document be overridden per environment?**

A dry-run mode is available in non-production environments for validating log shipping changes before they are applied. Changes to log shipping go through the standard review workflow before release. The defaults listed below apply unless overridden per environment.

**Where are the metrics for this area published?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Staging environments mirror production settings for log shipping except where data-volume limits make that impractical. Downstream consumers subscribe to log shipping events through the platform event bus rather than polling.

**Who should be contacted when the documented defaults look wrong?**

Changes to log shipping go through the standard review workflow before release. Operational alerts for this area route to the owning team's rotation. Consumers should treat undocumented fields as unstable and subject to change without notice.

**Does this area behave differently in staging than in production?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Changes to log shipping go through the standard review workflow before release. The behavior in this section was last load-tested at 11 times the average production request rate.

**Is there a dry-run mode for validating changes in this area?**

Localization of user-facing strings in log shipping is handled by the shared translation pipeline, not by this component. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Identifiers used here follow the corpus-wide conventions in the style guide.

## See also

- [DOC-1417: Multi Currency](product-specs/multi-currency.md)
- [DOC-3601: On-Call Handbook](sops/on-call-handbook.md)
