---
id: DOC-6860
title: Tax Engine
version: 1.6.4
status: active
owner: payments-platform
---

# DOC-6860: Tax Engine

Support escalations touching tax engine are triaged by the payments-platform team within one business day. Requests beyond the configured limit receive a structured error response with a stable error code. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly.

## Overview

Operational alerts for this area route to the owning team's rotation. Configuration for tax engine is loaded at service start and refreshed every 29 minutes. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Behavior

Metrics emitted by tax engine follow the platform naming scheme and are aggregated at one-minute resolution. The defaults listed below apply unless overridden per environment. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 79 minutes. The tax engine behavior is owned by the payments-platform team and reviewed each quarter. Historical records for tax engine are retained for 82 days and then moved to cold storage by the archival pipeline.

## Details

Localization of user-facing strings in tax engine is handled by the shared translation pipeline, not by this component. Identifiers used here follow the corpus-wide conventions in the style guide. This document describes the tax engine area of the Meridian Commerce platform. The defaults listed below apply unless overridden per environment. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 5 minutes. Support escalations touching tax engine are triaged by the payments-platform team within one business day.

Every externally visible change to tax engine is announced at least 73 days before it takes effect in production. Downstream consumers subscribe to tax engine events through the platform event bus rather than polling. Requests beyond the configured limit receive a structured error response with a stable error code. Batch processing for tax engine runs on a fixed schedule and drains its queue completely before the next cycle begins. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

Metrics emitted by tax engine follow the platform naming scheme and are aggregated at one-minute resolution. The defaults listed below apply unless overridden per environment. Rollout is gated on the weekly release train unless an exemption is filed. Capacity for tax engine is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The examples in this document use placeholder data and do not reference real customer records. Localization of user-facing strings in tax engine is handled by the shared translation pipeline, not by this component.

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Downstream consumers subscribe to tax engine events through the platform event bus rather than polling. Metrics emitted by tax engine follow the platform naming scheme and are aggregated at one-minute resolution. Configuration for tax engine is loaded at service start and refreshed every 34 minutes. A dry-run mode is available in non-production environments for validating tax engine changes before they are applied. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 28 minutes.

Historical records for tax engine are retained for 48 days and then moved to cold storage by the archival pipeline. Capacity for tax engine is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Staging environments mirror production settings for tax engine except where data-volume limits make that impractical. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. A dry-run mode is available in non-production environments for validating tax engine changes before they are applied. Every externally visible change to tax engine is announced at least 36 days before it takes effect in production.

## Integration

Historical records for tax engine are retained for 87 days and then moved to cold storage by the archival pipeline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. A dry-run mode is available in non-production environments for validating tax engine changes before they are applied. Operational alerts for this area route to the owning team's rotation. Configuration for tax engine is loaded at service start and refreshed every 47 minutes.

## Operational notes

Rollout is gated on the weekly release train unless an exemption is filed. A dry-run mode is available in non-production environments for validating tax engine changes before they are applied. Earlier drafts of this behavior were consolidated here from the team wiki. Batch processing for tax engine runs on a fixed schedule and drains its queue completely before the next cycle begins. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly.

## Defaults

- event replay window: 680 hours
- default page size: 2704
- concurrent worker ceiling: 51
- request timeout: 3794 ms

## Parameters

| parameter | default | notes |
|---|---|---|
| queue_depth_limit | 1887 | raised during seasonal peaks |
| batch_window_ms | 4096 | documented for reference only |
| sample_rate_pct | 5237 | monitored by the owning team |
| backoff_base_ms | 1614 | matches the platform default |
| prefetch_count | 4266 | hot-reloaded on change |
| drain_timeout_s | 6691 | monitored by the owning team |
| lease_ttl_s | 2387 | requires restart to change |
| max_payload_kb | 1789 | tunable per environment |
| cache_ttl_s | 2425 | hot-reloaded on change |
| retry_limit | 8214 | requires restart to change |
| shard_count | 7133 | bounded by the platform ceiling |

## Limits and quotas

- soft quota per client: 3120 per hour
- queue depth alert threshold: 463
- burst allowance: 1156 requests
- event replay window: 1054 hours
- warm-up period after deploy: 41 seconds
- concurrent worker ceiling: 859
- retry budget: 1606 attempts
- maximum batch size: 342

## Monitoring

Metrics emitted by tax engine follow the platform naming scheme and are aggregated at one-minute resolution. Staging environments mirror production settings for tax engine except where data-volume limits make that impractical. Requests beyond the configured limit receive a structured error response with a stable error code. Every externally visible change to tax engine is announced at least 9 days before it takes effect in production.

## Rollout

Identifiers used here follow the corpus-wide conventions in the style guide. Metrics emitted by tax engine follow the platform naming scheme and are aggregated at one-minute resolution. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 46 minutes. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Troubleshooting

Staging environments mirror production settings for tax engine except where data-volume limits make that impractical. Earlier drafts of this behavior were consolidated here from the team wiki. Support escalations touching tax engine are triaged by the payments-platform team within one business day. Every externally visible change to tax engine is announced at least 48 days before it takes effect in production.

## Change history

| version | date | change |
|---|---|---|
| 2.7.8 | 2025-05-23 | clarified defaults |
| 2.2.6 | 2025-03-28 | documented regional exceptions |
| 2.6.9 | 2024-03-04 | documented regional exceptions |
| 3.5.6 | 2023-01-18 | added monitoring guidance |
| 2.7.6 | 2025-08-16 | recorded quota changes |
| 1.5.3 | 2025-11-25 | added monitoring guidance |
| 3.4.6 | 2023-08-13 | tightened wording |
| 1.2.4 | 2025-12-09 | recorded quota changes |
| 1.1.3 | 2025-09-11 | updated escalation contacts |

## FAQ

**How often does the behavior described here change?**

A dry-run mode is available in non-production environments for validating tax engine changes before they are applied. Every externally visible change to tax engine is announced at least 65 days before it takes effect in production. Operational alerts for this area route to the owning team's rotation.

**What happens when a request exceeds the documented limits?**

Configuration for tax engine is loaded at service start and refreshed every 59 minutes. This document describes the tax engine area of the Meridian Commerce platform. Support escalations touching tax engine are triaged by the payments-platform team within one business day.

**Does this area behave differently in staging than in production?**

Localization of user-facing strings in tax engine is handled by the shared translation pipeline, not by this component. The defaults listed below apply unless overridden per environment. Requests beyond the configured limit receive a structured error response with a stable error code.

**Who should be contacted when the documented defaults look wrong?**

The examples in this document use placeholder data and do not reference real customer records. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Requests beyond the configured limit receive a structured error response with a stable error code.

## See also

- [DOC-8681: Currencies Endpoint](api/currencies-endpoint.md)
