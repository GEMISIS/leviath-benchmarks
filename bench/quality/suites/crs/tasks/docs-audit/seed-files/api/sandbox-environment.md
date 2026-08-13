---
id: DOC-3997
title: Sandbox Environment
version: 2.1
status: deprecated
superseded_by: api/sandbox-environment-next.md
owner: storefront
---

# DOC-3998: Sandbox Environment

Earlier drafts of this behavior were consolidated here from the team wiki. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 67 minutes. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Overview

Earlier drafts of this behavior were consolidated here from the team wiki. The sandbox environment behavior is owned by the storefront team and reviewed each quarter. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list.

## Behavior

The behavior in this section was last load-tested at 25 times the average production request rate. Rollout is gated on the weekly release train unless an exemption is filed. Configuration for sandbox environment is loaded at service start and refreshed every 38 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Every externally visible change to sandbox environment is announced at least 44 days before it takes effect in production.

## Details

Configuration for sandbox environment is loaded at service start and refreshed every 41 minutes. Batch processing for sandbox environment runs on a fixed schedule and drains its queue completely before the next cycle begins. Localization of user-facing strings in sandbox environment is handled by the shared translation pipeline, not by this component. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Downstream consumers subscribe to sandbox environment events through the platform event bus rather than polling. Identifiers used here follow the corpus-wide conventions in the style guide.

A dry-run mode is available in non-production environments for validating sandbox environment changes before they are applied. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Downstream consumers subscribe to sandbox environment events through the platform event bus rather than polling. The defaults listed below apply unless overridden per environment. Changes to sandbox environment go through the standard review workflow before release. Support escalations touching sandbox environment are triaged by the storefront team within one business day.

Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Changes to sandbox environment go through the standard review workflow before release. Batch processing for sandbox environment runs on a fixed schedule and drains its queue completely before the next cycle begins. Requests beyond the configured limit receive a structured error response with a stable error code. The behavior in this section was last load-tested at 68 times the average production request rate. This document describes the sandbox environment area of the Meridian Commerce platform.

Downstream consumers subscribe to sandbox environment events through the platform event bus rather than polling. Consumers should treat undocumented fields as unstable and subject to change without notice. Identifiers used here follow the corpus-wide conventions in the style guide. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for sandbox environment except where data-volume limits make that impractical.

Configuration for sandbox environment is loaded at service start and refreshed every 46 minutes. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Metrics emitted by sandbox environment follow the platform naming scheme and are aggregated at one-minute resolution. Batch processing for sandbox environment runs on a fixed schedule and drains its queue completely before the next cycle begins. Capacity for sandbox environment is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Every externally visible change to sandbox environment is announced at least 31 days before it takes effect in production.

## Integration

Historical records for sandbox environment are retained for 7 days and then moved to cold storage by the archival pipeline. Staging environments mirror production settings for sandbox environment except where data-volume limits make that impractical. The sandbox environment behavior is owned by the storefront team and reviewed each quarter. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Operational notes

Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to sandbox environment go through the standard review workflow before release. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. A dry-run mode is available in non-production environments for validating sandbox environment changes before they are applied. This document describes the sandbox environment area of the Meridian Commerce platform.

## Defaults

- burst allowance: 1212 requests
- soft quota per client: 2393 per hour
- event replay window: 1434 hours
- request timeout: 1609 ms

## Parameters

| parameter | default | notes |
|---|---|---|
| shard_count | 4647 | matches the platform default |
| audit_window_days | 8255 | requires restart to change |
| page_size | 5622 | requires restart to change |
| sample_rate_pct | 1786 | matches the platform default |
| retry_limit | 2730 | matches the platform default |
| lease_ttl_s | 7155 | documented for reference only |
| queue_depth_limit | 8955 | hot-reloaded on change |
| max_concurrency | 756 | documented for reference only |
| sync_interval_s | 2843 | monitored by the owning team |
| prefetch_count | 3686 | hot-reloaded on change |
| replay_window_h | 8855 | bounded by the platform ceiling |
| batch_window_ms | 6441 | bounded by the platform ceiling |

## Limits and quotas

- burst allowance: 2622 requests
- warm-up period after deploy: 2991 seconds
- soft quota per client: 582 per hour
- cache lifetime: 3338 seconds
- event replay window: 1780 hours
- concurrent worker ceiling: 3478
- queue depth alert threshold: 3264

## Monitoring

Data written by sandbox environment is idempotent at the record level, so replayed events cannot create duplicates. Capacity for sandbox environment is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Configuration for sandbox environment is loaded at service start and refreshed every 72 minutes. Requests beyond the configured limit receive a structured error response with a stable error code.

## Rollout

This document describes the sandbox environment area of the Meridian Commerce platform. Localization of user-facing strings in sandbox environment is handled by the shared translation pipeline, not by this component. Historical records for sandbox environment are retained for 48 days and then moved to cold storage by the archival pipeline. The defaults listed below apply unless overridden per environment.

## Troubleshooting

The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Downstream consumers subscribe to sandbox environment events through the platform event bus rather than polling. Data written by sandbox environment is idempotent at the record level, so replayed events cannot create duplicates. Capacity for sandbox environment is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Change history

| version | date | change |
|---|---|---|
| 1.3.1 | 2025-01-25 | added monitoring guidance |
| 3.7.9 | 2024-05-28 | documented regional exceptions |
| 2.2.4 | 2024-12-08 | refreshed examples |
| 2.2.9 | 2025-02-08 | updated escalation contacts |
| 1.9.4 | 2023-10-18 | aligned terminology with the style guide |
| 3.6.5 | 2023-08-21 | expanded rollout notes |
| 3.7.9 | 2023-02-14 | tightened wording |
| 2.3.6 | 2024-05-04 | updated escalation contacts |

## FAQ

**What happens when a request exceeds the documented limits?**

This document describes the sandbox environment area of the Meridian Commerce platform. The examples in this document use placeholder data and do not reference real customer records. A dry-run mode is available in non-production environments for validating sandbox environment changes before they are applied.

**Can the defaults in this document be overridden per environment?**

Localization of user-facing strings in sandbox environment is handled by the shared translation pipeline, not by this component. Support escalations touching sandbox environment are triaged by the storefront team within one business day. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list.

**Who should be contacted when the documented defaults look wrong?**

Historical records for sandbox environment are retained for 59 days and then moved to cold storage by the archival pipeline. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Localization of user-facing strings in sandbox environment is handled by the shared translation pipeline, not by this component.

**Is there a dry-run mode for validating changes in this area?**

Downstream consumers subscribe to sandbox environment events through the platform event bus rather than polling. The examples in this document use placeholder data and do not reference real customer records. Identifiers used here follow the corpus-wide conventions in the style guide.

**Where are the metrics for this area published?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Every externally visible change to sandbox environment is announced at least 81 days before it takes effect in production. Downstream consumers subscribe to sandbox environment events through the platform event bus rather than polling.

**Does this area behave differently in staging than in production?**

Historical records for sandbox environment are retained for 37 days and then moved to cold storage by the archival pipeline. The behavior in this section was last load-tested at 52 times the average production request rate. Requests beyond the configured limit receive a structured error response with a stable error code.

## See also

- [DOC-9169: International Pricing](product-specs/international-pricing.md)
- [Background notes](product-specs/subscription-billing-v2.md)
- [Background notes](sops/fleet-patching-v2.md)
