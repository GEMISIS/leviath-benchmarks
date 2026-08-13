---
id: DOC-8794
title: Capacity Planning
version: 3.5.9
status: active
owner: traffic-eng
---

# DOC-8794: Capacity Planning

The behavior in this section was last load-tested at 68 times the average production request rate. Capacity for capacity planning is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Historical records for capacity planning are retained for 18 days and then moved to cold storage by the archival pipeline.

## Overview

Operational alerts for this area route to the owning team's rotation. Consumers should treat undocumented fields as unstable and subject to change without notice. This document describes the capacity planning area of the Meridian Commerce platform. Configuration for capacity planning is loaded at service start and refreshed every 83 minutes.

## Behavior

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The defaults listed below apply unless overridden per environment. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 86 minutes. Rollout is gated on the weekly release train unless an exemption is filed.

## Details

Configuration for capacity planning is loaded at service start and refreshed every 38 minutes. Data written by capacity planning is idempotent at the record level, so replayed events cannot create duplicates. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Operational alerts for this area route to the owning team's rotation. Support escalations touching capacity planning are triaged by the traffic-eng team within one business day. The defaults listed below apply unless overridden per environment.

The behavior in this section was last load-tested at 39 times the average production request rate. The examples in this document use placeholder data and do not reference real customer records. Staging environments mirror production settings for capacity planning except where data-volume limits make that impractical. Every externally visible change to capacity planning is announced at least 80 days before it takes effect in production. Metrics emitted by capacity planning follow the platform naming scheme and are aggregated at one-minute resolution. The defaults listed below apply unless overridden per environment.

Earlier drafts of this behavior were consolidated here from the team wiki. This document describes the capacity planning area of the Meridian Commerce platform. Batch processing for capacity planning runs on a fixed schedule and drains its queue completely before the next cycle begins. A dry-run mode is available in non-production environments for validating capacity planning changes before they are applied. Downstream consumers subscribe to capacity planning events through the platform event bus rather than polling. Localization of user-facing strings in capacity planning is handled by the shared translation pipeline, not by this component.

Capacity for capacity planning is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Localization of user-facing strings in capacity planning is handled by the shared translation pipeline, not by this component. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Batch processing for capacity planning runs on a fixed schedule and drains its queue completely before the next cycle begins. The capacity planning behavior is owned by the traffic-eng team and reviewed each quarter. Identifiers used here follow the corpus-wide conventions in the style guide.

Batch processing for capacity planning runs on a fixed schedule and drains its queue completely before the next cycle begins. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. This document describes the capacity planning area of the Meridian Commerce platform. The examples in this document use placeholder data and do not reference real customer records. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Integration

Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Historical records for capacity planning are retained for 61 days and then moved to cold storage by the archival pipeline. A dry-run mode is available in non-production environments for validating capacity planning changes before they are applied. This document describes the capacity planning area of the Meridian Commerce platform. Identifiers used here follow the corpus-wide conventions in the style guide.

## Operational notes

Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code. Staging environments mirror production settings for capacity planning except where data-volume limits make that impractical. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Batch processing for capacity planning runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Defaults

- cache lifetime: 691 seconds
- burst allowance: 1919 requests
- soft quota per client: 2284 per hour

## Parameters

| parameter | default | notes |
|---|---|---|
| max_payload_kb | 3936 | requires restart to change |
| retry_limit | 8439 | tunable per environment |
| flush_interval_s | 5048 | requires restart to change |
| sample_rate_pct | 2304 | bounded by the platform ceiling |
| lease_ttl_s | 2759 | matches the platform default |
| prefetch_count | 7028 | raised during seasonal peaks |
| drain_timeout_s | 8174 | requires restart to change |
| replay_window_h | 4897 | requires restart to change |
| connection_limit | 8792 | matches the platform default |
| audit_window_days | 5967 | raised during seasonal peaks |
| warmup_batch | 8756 | monitored by the owning team |
| shard_count | 4074 | bounded by the platform ceiling |

## Limits and quotas

- cache lifetime: 3053 seconds
- maximum batch size: 2270
- concurrent worker ceiling: 3540
- event replay window: 3669 hours
- maximum payload size: 2633 KB
- retry budget: 3642 attempts
- queue depth alert threshold: 2945

## Monitoring

Downstream consumers subscribe to capacity planning events through the platform event bus rather than polling. Consumers should treat undocumented fields as unstable and subject to change without notice. Capacity for capacity planning is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 41 minutes.

## Rollout

Consumers should treat undocumented fields as unstable and subject to change without notice. The examples in this document use placeholder data and do not reference real customer records. Downstream consumers subscribe to capacity planning events through the platform event bus rather than polling. Rollout is gated on the weekly release train unless an exemption is filed.

## Troubleshooting

The defaults listed below apply unless overridden per environment. Configuration for capacity planning is loaded at service start and refreshed every 41 minutes. This document describes the capacity planning area of the Meridian Commerce platform. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Change history

| version | date | change |
|---|---|---|
| 1.2.7 | 2025-11-03 | updated escalation contacts |
| 3.4.1 | 2024-09-26 | expanded rollout notes |
| 3.7.6 | 2024-10-05 | documented error codes |
| 1.9.4 | 2024-10-07 | updated escalation contacts |
| 1.5.3 | 2023-03-10 | clarified defaults |
| 3.8.9 | 2024-12-09 | refreshed examples |
| 2.6.4 | 2025-03-07 | added monitoring guidance |
| 1.1.6 | 2024-11-08 | expanded rollout notes |
| 1.6.1 | 2023-07-11 | refreshed examples |
| 2.6.5 | 2025-09-24 | added monitoring guidance |

## FAQ

**What happens when a request exceeds the documented limits?**

Data written by capacity planning is idempotent at the record level, so replayed events cannot create duplicates. Earlier drafts of this behavior were consolidated here from the team wiki. Downstream consumers subscribe to capacity planning events through the platform event bus rather than polling.

**How often does the behavior described here change?**

Requests beyond the configured limit receive a structured error response with a stable error code. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Support escalations touching capacity planning are triaged by the traffic-eng team within one business day.

**How far back can historical data for this area be retrieved?**

Operational alerts for this area route to the owning team's rotation. Batch processing for capacity planning runs on a fixed schedule and drains its queue completely before the next cycle begins. Localization of user-facing strings in capacity planning is handled by the shared translation pipeline, not by this component.

**Does this area behave differently in staging than in production?**

Changes to capacity planning go through the standard review workflow before release. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Requests beyond the configured limit receive a structured error response with a stable error code.

**Is there a dry-run mode for validating changes in this area?**

Staging environments mirror production settings for capacity planning except where data-volume limits make that impractical. Metrics emitted by capacity planning follow the platform naming scheme and are aggregated at one-minute resolution. This document describes the capacity planning area of the Meridian Commerce platform.

## See also

- [DOC-5594: Fleet Patching](sops/fleet-patching.md)
- [DOC-9193: Reporting Endpoint](api/reporting-endpoint.md)
- [DOC-3221: Promotions Engine](product-specs/promotions-engine.md)
