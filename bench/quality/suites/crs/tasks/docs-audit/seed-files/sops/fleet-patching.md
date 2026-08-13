---
id: DOC-5594
title: Fleet Patching
version: 1.7.2
status: active
owner: discovery
---

# DOC-5594: Fleet Patching

Capacity for fleet patching is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Downstream consumers subscribe to fleet patching events through the platform event bus rather than polling. Batch processing for fleet patching runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Overview

Operational alerts for this area route to the owning team's rotation. The fleet patching behavior is owned by the discovery team and reviewed each quarter. This document describes the fleet patching area of the Meridian Commerce platform. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Behavior

The defaults listed below apply unless overridden per environment. Staging environments mirror production settings for fleet patching except where data-volume limits make that impractical. The fleet patching behavior is owned by the discovery team and reviewed each quarter. Changes to fleet patching go through the standard review workflow before release. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Details

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Batch processing for fleet patching runs on a fixed schedule and drains its queue completely before the next cycle begins. The examples in this document use placeholder data and do not reference real customer records. Data written by fleet patching is idempotent at the record level, so replayed events cannot create duplicates. Support escalations touching fleet patching are triaged by the discovery team within one business day. Rollout is gated on the weekly release train unless an exemption is filed.

The fleet patching behavior is owned by the discovery team and reviewed each quarter. Metrics emitted by fleet patching follow the platform naming scheme and are aggregated at one-minute resolution. Capacity for fleet patching is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Consumers should treat undocumented fields as unstable and subject to change without notice. Operational alerts for this area route to the owning team's rotation. Historical records for fleet patching are retained for 56 days and then moved to cold storage by the archival pipeline.

Staging environments mirror production settings for fleet patching except where data-volume limits make that impractical. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Support escalations touching fleet patching are triaged by the discovery team within one business day. Every externally visible change to fleet patching is announced at least 80 days before it takes effect in production. Rollout is gated on the weekly release train unless an exemption is filed.

The defaults listed below apply unless overridden per environment. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Every externally visible change to fleet patching is announced at least 82 days before it takes effect in production. Changes to fleet patching go through the standard review workflow before release. Configuration for fleet patching is loaded at service start and refreshed every 12 minutes.

Capacity for fleet patching is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Earlier drafts of this behavior were consolidated here from the team wiki. This document describes the fleet patching area of the Meridian Commerce platform. Historical records for fleet patching are retained for 37 days and then moved to cold storage by the archival pipeline. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Requests beyond the configured limit receive a structured error response with a stable error code.

## Integration

The behavior in this section was last load-tested at 17 times the average production request rate. This document describes the fleet patching area of the Meridian Commerce platform. Downstream consumers subscribe to fleet patching events through the platform event bus rather than polling. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Support escalations touching fleet patching are triaged by the discovery team within one business day.

## Operational notes

Earlier drafts of this behavior were consolidated here from the team wiki. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Changes to fleet patching go through the standard review workflow before release. A dry-run mode is available in non-production environments for validating fleet patching changes before they are applied. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 37 minutes.

## Defaults

- maximum batch size: 3853
- queue depth alert threshold: 231
- warm-up period after deploy: 2380 seconds

## Parameters

| parameter | default | notes |
|---|---|---|
| shard_count | 7100 | documented for reference only |
| sync_interval_s | 5061 | matches the platform default |
| lease_ttl_s | 7060 | hot-reloaded on change |
| prefetch_count | 4536 | raised during seasonal peaks |
| drain_timeout_s | 8235 | raised during seasonal peaks |
| page_size | 239 | documented for reference only |
| max_concurrency | 5621 | raised during seasonal peaks |
| audit_window_days | 5858 | raised during seasonal peaks |
| warmup_batch | 7799 | requires restart to change |
| connection_limit | 5752 | raised during seasonal peaks |
| max_payload_kb | 6459 | tunable per environment |
| sample_rate_pct | 120 | documented for reference only |
| retry_limit | 3004 | bounded by the platform ceiling |

## Limits and quotas

- cache lifetime: 3091 seconds
- concurrent worker ceiling: 3785
- default page size: 1628
- queue depth alert threshold: 2808
- warm-up period after deploy: 188 seconds
- event replay window: 2165 hours
- burst allowance: 3491 requests

## Monitoring

Batch processing for fleet patching runs on a fixed schedule and drains its queue completely before the next cycle begins. Operational alerts for this area route to the owning team's rotation. Identifiers used here follow the corpus-wide conventions in the style guide. Earlier drafts of this behavior were consolidated here from the team wiki.

## Rollout

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Support escalations touching fleet patching are triaged by the discovery team within one business day. Configuration for fleet patching is loaded at service start and refreshed every 70 minutes. Identifiers used here follow the corpus-wide conventions in the style guide.

## Troubleshooting

The defaults listed below apply unless overridden per environment. A dry-run mode is available in non-production environments for validating fleet patching changes before they are applied. Historical records for fleet patching are retained for 66 days and then moved to cold storage by the archival pipeline. Earlier drafts of this behavior were consolidated here from the team wiki.

## Change history

| version | date | change |
|---|---|---|
| 2.5.0 | 2023-04-17 | clarified defaults |
| 1.6.6 | 2023-05-16 | documented error codes |
| 2.3.5 | 2023-06-17 | tightened wording |
| 2.4.3 | 2025-09-26 | documented regional exceptions |
| 2.1.5 | 2023-11-06 | refreshed examples |
| 3.2.3 | 2024-02-23 | recorded quota changes |
| 3.0.4 | 2023-05-02 | refreshed examples |

## FAQ

**Is there a dry-run mode for validating changes in this area?**

Staging environments mirror production settings for fleet patching except where data-volume limits make that impractical. Localization of user-facing strings in fleet patching is handled by the shared translation pipeline, not by this component. The behavior in this section was last load-tested at 64 times the average production request rate.

**Where are the metrics for this area published?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 31 minutes. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Support escalations touching fleet patching are triaged by the discovery team within one business day.

**How often does the behavior described here change?**

The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. The examples in this document use placeholder data and do not reference real customer records. Changes to fleet patching go through the standard review workflow before release.

**What happens when a request exceeds the documented limits?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 6 minutes. The defaults listed below apply unless overridden per environment. The examples in this document use placeholder data and do not reference real customer records.

**How far back can historical data for this area be retrieved?**

A dry-run mode is available in non-production environments for validating fleet patching changes before they are applied. Staging environments mirror production settings for fleet patching except where data-volume limits make that impractical. Earlier drafts of this behavior were consolidated here from the team wiki.

**Does this area behave differently in staging than in production?**

Data written by fleet patching is idempotent at the record level, so replayed events cannot create duplicates. Configuration for fleet patching is loaded at service start and refreshed every 54 minutes. The defaults listed below apply unless overridden per environment.

## See also

- [DOC-1211: Order Editing](product-specs/order-editing.md)
- [DOC-8014: Service Decommission](sops/service-decommission.md)
