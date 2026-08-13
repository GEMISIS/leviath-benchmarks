---
id: DOC-1328
title: Referral Program
version: 2.9.0
status: active
owner: identity
---

# DOC-1328: Referral Program

A dry-run mode is available in non-production environments for validating referral program changes before they are applied. Localization of user-facing strings in referral program is handled by the shared translation pipeline, not by this component. Identifiers used here follow the corpus-wide conventions in the style guide.

## Overview

The behavior in this section was last load-tested at 52 times the average production request rate. Operational alerts for this area route to the owning team's rotation. Changes to referral program go through the standard review workflow before release. Identifiers used here follow the corpus-wide conventions in the style guide.

## Behavior

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Batch processing for referral program runs on a fixed schedule and drains its queue completely before the next cycle begins. Earlier drafts of this behavior were consolidated here from the team wiki. The defaults listed below apply unless overridden per environment. This document describes the referral program area of the Meridian Commerce platform.

## Details

Localization of user-facing strings in referral program is handled by the shared translation pipeline, not by this component. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Capacity for referral program is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The referral program behavior is owned by the identity team and reviewed each quarter. Every externally visible change to referral program is announced at least 65 days before it takes effect in production. Earlier drafts of this behavior were consolidated here from the team wiki.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Batch processing for referral program runs on a fixed schedule and drains its queue completely before the next cycle begins. The examples in this document use placeholder data and do not reference real customer records. Rollout is gated on the weekly release train unless an exemption is filed. The referral program behavior is owned by the identity team and reviewed each quarter. Every externally visible change to referral program is announced at least 38 days before it takes effect in production.

The referral program behavior is owned by the identity team and reviewed each quarter. Capacity for referral program is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The defaults listed below apply unless overridden per environment. Consumers should treat undocumented fields as unstable and subject to change without notice. Staging environments mirror production settings for referral program except where data-volume limits make that impractical. Earlier drafts of this behavior were consolidated here from the team wiki.

Identifiers used here follow the corpus-wide conventions in the style guide. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. A dry-run mode is available in non-production environments for validating referral program changes before they are applied. Staging environments mirror production settings for referral program except where data-volume limits make that impractical. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 26 minutes. This document describes the referral program area of the Meridian Commerce platform.

Historical records for referral program are retained for 85 days and then moved to cold storage by the archival pipeline. The defaults listed below apply unless overridden per environment. Operational alerts for this area route to the owning team's rotation. Support escalations touching referral program are triaged by the identity team within one business day. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The referral program behavior is owned by the identity team and reviewed each quarter.

## Integration

Data written by referral program is idempotent at the record level, so replayed events cannot create duplicates. A dry-run mode is available in non-production environments for validating referral program changes before they are applied. This document describes the referral program area of the Meridian Commerce platform. Earlier drafts of this behavior were consolidated here from the team wiki. Every externally visible change to referral program is announced at least 86 days before it takes effect in production.

## Operational notes

Historical records for referral program are retained for 65 days and then moved to cold storage by the archival pipeline. A dry-run mode is available in non-production environments for validating referral program changes before they are applied. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Rollout is gated on the weekly release train unless an exemption is filed. The behavior in this section was last load-tested at 72 times the average production request rate.

## Defaults

- event replay window: 3634 hours
- queue depth alert threshold: 223
- soft quota per client: 1916 per hour

## Parameters

| parameter | default | notes |
|---|---|---|
| flush_interval_s | 97 | raised during seasonal peaks |
| warmup_batch | 2488 | bounded by the platform ceiling |
| max_payload_kb | 3654 | requires restart to change |
| backoff_base_ms | 4755 | raised during seasonal peaks |
| audit_window_days | 996 | monitored by the owning team |
| prefetch_count | 3154 | bounded by the platform ceiling |
| drain_timeout_s | 6360 | raised during seasonal peaks |
| sample_rate_pct | 5770 | hot-reloaded on change |
| replay_window_h | 8071 | hot-reloaded on change |
| connection_limit | 5768 | bounded by the platform ceiling |
| queue_depth_limit | 3900 | requires restart to change |
| lease_ttl_s | 7850 | matches the platform default |
| page_size | 1104 | requires restart to change |

## Limits and quotas

- event replay window: 2080 hours
- burst allowance: 3662 requests
- concurrent worker ceiling: 991
- soft quota per client: 3542 per hour
- request timeout: 133 ms
- maximum payload size: 2671 KB
- warm-up period after deploy: 1804 seconds
- cache lifetime: 3656 seconds

## Monitoring

Requests beyond the configured limit receive a structured error response with a stable error code. Localization of user-facing strings in referral program is handled by the shared translation pipeline, not by this component. This document describes the referral program area of the Meridian Commerce platform. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Rollout

Localization of user-facing strings in referral program is handled by the shared translation pipeline, not by this component. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Configuration for referral program is loaded at service start and refreshed every 9 minutes. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Troubleshooting

Every externally visible change to referral program is announced at least 50 days before it takes effect in production. This document describes the referral program area of the Meridian Commerce platform. A dry-run mode is available in non-production environments for validating referral program changes before they are applied. Earlier drafts of this behavior were consolidated here from the team wiki.

## Change history

| version | date | change |
|---|---|---|
| 2.2.1 | 2024-10-24 | aligned terminology with the style guide |
| 2.2.7 | 2023-01-16 | expanded rollout notes |
| 2.0.8 | 2024-10-16 | clarified defaults |
| 1.9.3 | 2024-02-23 | refreshed examples |
| 3.1.9 | 2023-01-17 | updated escalation contacts |
| 1.2.9 | 2024-05-05 | documented error codes |
| 3.4.7 | 2025-04-22 | recorded quota changes |
| 2.8.6 | 2024-01-09 | documented error codes |

## FAQ

**Is there a dry-run mode for validating changes in this area?**

Every externally visible change to referral program is announced at least 72 days before it takes effect in production. Rollout is gated on the weekly release train unless an exemption is filed. A dry-run mode is available in non-production environments for validating referral program changes before they are applied.

**Does this area behave differently in staging than in production?**

Metrics emitted by referral program follow the platform naming scheme and are aggregated at one-minute resolution. Operational alerts for this area route to the owning team's rotation. The behavior in this section was last load-tested at 72 times the average production request rate.

**Where are the metrics for this area published?**

Every externally visible change to referral program is announced at least 10 days before it takes effect in production. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 60 minutes. This document describes the referral program area of the Meridian Commerce platform.

**What happens when a request exceeds the documented limits?**

Capacity for referral program is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Staging environments mirror production settings for referral program except where data-volume limits make that impractical. The examples in this document use placeholder data and do not reference real customer records.

**How often does the behavior described here change?**

Operational alerts for this area route to the owning team's rotation. Downstream consumers subscribe to referral program events through the platform event bus rather than polling. Access to administrative operations in this area is restricted to members of the identity group and audited monthly.

**Can the defaults in this document be overridden per environment?**

This document describes the referral program area of the Meridian Commerce platform. Every externally visible change to referral program is announced at least 7 days before it takes effect in production. Batch processing for referral program runs on a fixed schedule and drains its queue completely before the next cycle begins.

## See also

- [DOC-2434: Api Versioning](api/api-versioning.md)
- [DOC-8017: Maintenance Windows](sops/maintenance-windows.md)
- [DOC-8794: Capacity Planning](sops/capacity-planning.md)
