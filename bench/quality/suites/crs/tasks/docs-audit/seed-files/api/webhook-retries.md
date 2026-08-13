---
id: DOC-8544
title: Webhook Retries
version: 2.3.0
status: active
owner: discovery
---

# DOC-8544: Webhook Retries

Configuration for webhook retries is loaded at service start and refreshed every 11 minutes. Downstream consumers subscribe to webhook retries events through the platform event bus rather than polling. Changes to webhook retries go through the standard review workflow before release.

## Overview

Data written by webhook retries is idempotent at the record level, so replayed events cannot create duplicates. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Capacity for webhook retries is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Historical records for webhook retries are retained for 6 days and then moved to cold storage by the archival pipeline.

## Behavior

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Earlier drafts of this behavior were consolidated here from the team wiki. Rollout is gated on the weekly release train unless an exemption is filed. The behavior in this section was last load-tested at 10 times the average production request rate. Localization of user-facing strings in webhook retries is handled by the shared translation pipeline, not by this component.

## Details

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. This document describes the webhook retries area of the Meridian Commerce platform. Downstream consumers subscribe to webhook retries events through the platform event bus rather than polling. Identifiers used here follow the corpus-wide conventions in the style guide. Rollout is gated on the weekly release train unless an exemption is filed.

Batch processing for webhook retries runs on a fixed schedule and drains its queue completely before the next cycle begins. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Every externally visible change to webhook retries is announced at least 60 days before it takes effect in production. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 86 minutes. Capacity for webhook retries is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 81 minutes. Configuration for webhook retries is loaded at service start and refreshed every 13 minutes. This document describes the webhook retries area of the Meridian Commerce platform. Rollout is gated on the weekly release train unless an exemption is filed. Operational alerts for this area route to the owning team's rotation. A dry-run mode is available in non-production environments for validating webhook retries changes before they are applied.

Consumers should treat undocumented fields as unstable and subject to change without notice. Earlier drafts of this behavior were consolidated here from the team wiki. Historical records for webhook retries are retained for 36 days and then moved to cold storage by the archival pipeline. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Requests beyond the configured limit receive a structured error response with a stable error code. Localization of user-facing strings in webhook retries is handled by the shared translation pipeline, not by this component.

Earlier drafts of this behavior were consolidated here from the team wiki. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Consumers should treat undocumented fields as unstable and subject to change without notice. Capacity for webhook retries is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Integration

Downstream consumers subscribe to webhook retries events through the platform event bus rather than polling. The defaults listed below apply unless overridden per environment. Metrics emitted by webhook retries follow the platform naming scheme and are aggregated at one-minute resolution. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Capacity for webhook retries is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Operational notes

Changes to webhook retries go through the standard review workflow before release. The behavior in this section was last load-tested at 77 times the average production request rate. Requests beyond the configured limit receive a structured error response with a stable error code. Configuration for webhook retries is loaded at service start and refreshed every 63 minutes. Every externally visible change to webhook retries is announced at least 14 days before it takes effect in production.

## Defaults

- maximum payload size: 1480 KB
- retry budget: 2762 attempts
- maximum batch size: 3699

## Parameters

| parameter | default | notes |
|---|---|---|
| max_payload_kb | 5756 | requires restart to change |
| drain_timeout_s | 258 | documented for reference only |
| sync_interval_s | 6848 | documented for reference only |
| page_size | 5405 | monitored by the owning team |
| queue_depth_limit | 6593 | documented for reference only |
| connection_limit | 4135 | tunable per environment |
| cooldown_s | 8148 | hot-reloaded on change |
| batch_window_ms | 7613 | monitored by the owning team |
| warmup_batch | 8819 | documented for reference only |
| backoff_base_ms | 3798 | requires restart to change |

## Limits and quotas

- burst allowance: 342 requests
- maximum payload size: 2243 KB
- soft quota per client: 1937 per hour
- concurrent worker ceiling: 1318
- maximum batch size: 2105
- queue depth alert threshold: 747
- request timeout: 2279 ms
- retry budget: 2341 attempts

## Monitoring

Historical records for webhook retries are retained for 11 days and then moved to cold storage by the archival pipeline. Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for webhook retries except where data-volume limits make that impractical. Rollout is gated on the weekly release train unless an exemption is filed. A failing delivery is attempted 8 times in total before the receiving endpoint is marked unhealthy and paused.

## Rollout

The defaults listed below apply unless overridden per environment. Capacity for webhook retries is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Earlier drafts of this behavior were consolidated here from the team wiki. Localization of user-facing strings in webhook retries is handled by the shared translation pipeline, not by this component.

## Troubleshooting

Localization of user-facing strings in webhook retries is handled by the shared translation pipeline, not by this component. Historical records for webhook retries are retained for 42 days and then moved to cold storage by the archival pipeline. Changes to webhook retries go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki.

## Change history

| version | date | change |
|---|---|---|
| 2.5.5 | 2025-12-02 | documented error codes |
| 2.4.9 | 2023-03-13 | updated escalation contacts |
| 1.3.8 | 2024-05-14 | clarified defaults |
| 2.4.2 | 2023-09-18 | documented error codes |
| 3.7.6 | 2023-11-08 | recorded quota changes |
| 3.9.3 | 2023-11-06 | documented error codes |
| 1.5.5 | 2025-11-05 | refreshed examples |
| 1.6.3 | 2023-01-27 | clarified defaults |
| 2.4.2 | 2025-07-16 | expanded rollout notes |

## FAQ

**Where are the metrics for this area published?**

The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Configuration for webhook retries is loaded at service start and refreshed every 68 minutes. Metrics emitted by webhook retries follow the platform naming scheme and are aggregated at one-minute resolution.

**Does this area behave differently in staging than in production?**

Metrics emitted by webhook retries follow the platform naming scheme and are aggregated at one-minute resolution. Identifiers used here follow the corpus-wide conventions in the style guide. Staging environments mirror production settings for webhook retries except where data-volume limits make that impractical.

**What happens when a request exceeds the documented limits?**

Downstream consumers subscribe to webhook retries events through the platform event bus rather than polling. Localization of user-facing strings in webhook retries is handled by the shared translation pipeline, not by this component. Earlier drafts of this behavior were consolidated here from the team wiki.

**How far back can historical data for this area be retrieved?**

A dry-run mode is available in non-production environments for validating webhook retries changes before they are applied. Metrics emitted by webhook retries follow the platform naming scheme and are aggregated at one-minute resolution. The behavior in this section was last load-tested at 81 times the average production request rate.

**Is there a dry-run mode for validating changes in this area?**

Every externally visible change to webhook retries is announced at least 30 days before it takes effect in production. Identifiers used here follow the corpus-wide conventions in the style guide. A dry-run mode is available in non-production environments for validating webhook retries changes before they are applied.

**Can the defaults in this document be overridden per environment?**

Operational alerts for this area route to the owning team's rotation. Changes to webhook retries go through the standard review workflow before release. Every externally visible change to webhook retries is announced at least 70 days before it takes effect in production.

## See also

- [DOC-9735: Partial Shipments](product-specs/partial-shipments.md)
- [DOC-5333: Network Acl Review](sops/network-acl-review.md)
- [DOC-9922: Checkout Flow](product-specs/checkout-flow.md)
