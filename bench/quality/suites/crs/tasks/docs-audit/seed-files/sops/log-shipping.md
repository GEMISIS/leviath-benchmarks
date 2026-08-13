---
id: DOC-2803
title: Log Shipping
version: 3.8.3
status: active
owner: identity
---

# DOC-2803: Log Shipping

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The defaults listed below apply unless overridden per environment. Historical records for log shipping are retained for 64 days and then moved to cold storage by the archival pipeline.

## Overview

Every externally visible change to log shipping is announced at least 54 days before it takes effect in production. Operational alerts for this area route to the owning team's rotation. The defaults listed below apply unless overridden per environment. Metrics emitted by log shipping follow the platform naming scheme and are aggregated at one-minute resolution.

## Behavior

The defaults listed below apply unless overridden per environment. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Consumers should treat undocumented fields as unstable and subject to change without notice. This document describes the log shipping area of the Meridian Commerce platform. Identifiers used here follow the corpus-wide conventions in the style guide.

## Details

Rollout is gated on the weekly release train unless an exemption is filed. Support escalations touching log shipping are triaged by the identity team within one business day. Earlier drafts of this behavior were consolidated here from the team wiki. The log shipping behavior is owned by the identity team and reviewed each quarter. A dry-run mode is available in non-production environments for validating log shipping changes before they are applied. Downstream consumers subscribe to log shipping events through the platform event bus rather than polling.

Operational alerts for this area route to the owning team's rotation. Downstream consumers subscribe to log shipping events through the platform event bus rather than polling. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. This document describes the log shipping area of the Meridian Commerce platform. The examples in this document use placeholder data and do not reference real customer records. Changes to log shipping go through the standard review workflow before release.

Identifiers used here follow the corpus-wide conventions in the style guide. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Consumers should treat undocumented fields as unstable and subject to change without notice. Rollout is gated on the weekly release train unless an exemption is filed. The examples in this document use placeholder data and do not reference real customer records. Access to administrative operations in this area is restricted to members of the identity group and audited monthly.

Every externally visible change to log shipping is announced at least 69 days before it takes effect in production. Earlier drafts of this behavior were consolidated here from the team wiki. Rollout is gated on the weekly release train unless an exemption is filed. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Batch processing for log shipping runs on a fixed schedule and drains its queue completely before the next cycle begins. Metrics emitted by log shipping follow the platform naming scheme and are aggregated at one-minute resolution. Shipped log entries remain queryable in the primary store for 30 days before rolling into cold archives.

Support escalations touching log shipping are triaged by the identity team within one business day. Capacity for log shipping is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. A dry-run mode is available in non-production environments for validating log shipping changes before they are applied. The examples in this document use placeholder data and do not reference real customer records. The log shipping behavior is owned by the identity team and reviewed each quarter.

## Integration

Configuration for log shipping is loaded at service start and refreshed every 16 minutes. Support escalations touching log shipping are triaged by the identity team within one business day. Requests beyond the configured limit receive a structured error response with a stable error code. A dry-run mode is available in non-production environments for validating log shipping changes before they are applied. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Operational notes

The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Historical records for log shipping are retained for 61 days and then moved to cold storage by the archival pipeline. Consumers should treat undocumented fields as unstable and subject to change without notice. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

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
