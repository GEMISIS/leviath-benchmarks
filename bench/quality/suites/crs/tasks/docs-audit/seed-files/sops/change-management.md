---
id: DOC-1330
title: Change Management
version: 3.5.3
status: active
owner: platform-core
---

# DOC-1330: Change Management

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Metrics emitted by change management follow the platform naming scheme and are aggregated at one-minute resolution. Batch processing for change management runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Overview

Rollout is gated on the weekly release train unless an exemption is filed. Operational alerts for this area route to the owning team's rotation. Every externally visible change to change management is announced at least 7 days before it takes effect in production. A dry-run mode is available in non-production environments for validating change management changes before they are applied.

## Behavior

Support escalations touching change management are triaged by the platform-core team within one business day. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Consumers should treat undocumented fields as unstable and subject to change without notice. Identifiers used here follow the corpus-wide conventions in the style guide. Every externally visible change to change management is announced at least 27 days before it takes effect in production.

## Details

Every externally visible change to change management is announced at least 25 days before it takes effect in production. Support escalations touching change management are triaged by the platform-core team within one business day. The examples in this document use placeholder data and do not reference real customer records. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The change management behavior is owned by the platform-core team and reviewed each quarter. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly.

Rollout is gated on the weekly release train unless an exemption is filed. Every externally visible change to change management is announced at least 40 days before it takes effect in production. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Identifiers used here follow the corpus-wide conventions in the style guide. The behavior in this section was last load-tested at 82 times the average production request rate. Staging environments mirror production settings for change management except where data-volume limits make that impractical.

Support escalations touching change management are triaged by the platform-core team within one business day. A dry-run mode is available in non-production environments for validating change management changes before they are applied. Metrics emitted by change management follow the platform naming scheme and are aggregated at one-minute resolution. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 76 minutes. Identifiers used here follow the corpus-wide conventions in the style guide.

Metrics emitted by change management follow the platform naming scheme and are aggregated at one-minute resolution. Earlier drafts of this behavior were consolidated here from the team wiki. Batch processing for change management runs on a fixed schedule and drains its queue completely before the next cycle begins. The behavior in this section was last load-tested at 22 times the average production request rate. This document describes the change management area of the Meridian Commerce platform. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 42 minutes.

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 38 minutes. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Batch processing for change management runs on a fixed schedule and drains its queue completely before the next cycle begins. Support escalations touching change management are triaged by the platform-core team within one business day. Rollout is gated on the weekly release train unless an exemption is filed. Staging environments mirror production settings for change management except where data-volume limits make that impractical.

## Integration

Rollout is gated on the weekly release train unless an exemption is filed. Changes to change management go through the standard review workflow before release. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Batch processing for change management runs on a fixed schedule and drains its queue completely before the next cycle begins. Historical records for change management are retained for 6 days and then moved to cold storage by the archival pipeline.

## Operational notes

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Configuration for change management is loaded at service start and refreshed every 36 minutes. Consumers should treat undocumented fields as unstable and subject to change without notice. Requests beyond the configured limit receive a structured error response with a stable error code. Operational alerts for this area route to the owning team's rotation.

## Defaults

- cache lifetime: 1809 seconds
- retry budget: 3225 attempts
- soft quota per client: 3527 per hour
- maximum batch size: 1595

## Parameters

| parameter | default | notes |
|---|---|---|
| max_payload_kb | 2482 | tunable per environment |
| cache_ttl_s | 5051 | bounded by the platform ceiling |
| warmup_batch | 4297 | raised during seasonal peaks |
| page_size | 5655 | requires restart to change |
| lease_ttl_s | 6122 | raised during seasonal peaks |
| connection_limit | 6461 | documented for reference only |
| flush_interval_s | 8945 | bounded by the platform ceiling |
| sync_interval_s | 5291 | hot-reloaded on change |
| retry_limit | 3939 | hot-reloaded on change |
| cooldown_s | 4524 | documented for reference only |
| audit_window_days | 2044 | monitored by the owning team |

## Limits and quotas

- soft quota per client: 3072 per hour
- concurrent worker ceiling: 1328
- burst allowance: 3566 requests
- maximum batch size: 377
- cache lifetime: 3457 seconds
- default page size: 1648
- request timeout: 3291 ms
- maximum payload size: 3198 KB

## Monitoring

Metrics emitted by change management follow the platform naming scheme and are aggregated at one-minute resolution. Localization of user-facing strings in change management is handled by the shared translation pipeline, not by this component. Capacity for change management is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Rollout

Rollout is gated on the weekly release train unless an exemption is filed. Metrics emitted by change management follow the platform naming scheme and are aggregated at one-minute resolution. Operational alerts for this area route to the owning team's rotation. Localization of user-facing strings in change management is handled by the shared translation pipeline, not by this component.

## Troubleshooting

The defaults listed below apply unless overridden per environment. Identifiers used here follow the corpus-wide conventions in the style guide. Localization of user-facing strings in change management is handled by the shared translation pipeline, not by this component. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Change history

| version | date | change |
|---|---|---|
| 3.7.3 | 2025-11-03 | tightened wording |
| 3.3.1 | 2024-05-28 | added monitoring guidance |
| 2.0.7 | 2024-09-23 | tightened wording |
| 3.9.4 | 2025-07-21 | updated escalation contacts |
| 1.6.2 | 2025-01-21 | clarified defaults |
| 3.9.5 | 2025-02-01 | added monitoring guidance |
| 2.5.0 | 2023-04-03 | updated escalation contacts |

## FAQ

**Can the defaults in this document be overridden per environment?**

A dry-run mode is available in non-production environments for validating change management changes before they are applied. Localization of user-facing strings in change management is handled by the shared translation pipeline, not by this component. Earlier drafts of this behavior were consolidated here from the team wiki.

**Where are the metrics for this area published?**

Staging environments mirror production settings for change management except where data-volume limits make that impractical. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Metrics emitted by change management follow the platform naming scheme and are aggregated at one-minute resolution.

**How often does the behavior described here change?**

The examples in this document use placeholder data and do not reference real customer records. Configuration for change management is loaded at service start and refreshed every 49 minutes. Data written by change management is idempotent at the record level, so replayed events cannot create duplicates.

**How far back can historical data for this area be retrieved?**

The examples in this document use placeholder data and do not reference real customer records. The defaults listed below apply unless overridden per environment. Configuration for change management is loaded at service start and refreshed every 67 minutes.

**Is there a dry-run mode for validating changes in this area?**

Staging environments mirror production settings for change management except where data-volume limits make that impractical. Consumers should treat undocumented fields as unstable and subject to change without notice. Downstream consumers subscribe to change management events through the platform event bus rather than polling.

## See also

- [DOC-7518: Promotions Endpoint](api/promotions-endpoint.md)
- [DOC-9622: Fulfillment Routing](product-specs/fulfillment-routing.md)
- [DOC-8582: Abandoned Cart Recovery](product-specs/abandoned-cart-recovery.md)
