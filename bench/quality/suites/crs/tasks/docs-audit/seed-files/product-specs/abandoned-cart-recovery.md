---
id: DOC-8582
title: Abandoned Cart Recovery
version: 2.8.5
status: active
owner: discovery
---

# DOC-8582: Abandoned Cart Recovery

This document describes the abandoned cart recovery area of the Meridian Commerce platform. A dry-run mode is available in non-production environments for validating abandoned cart recovery changes before they are applied. Earlier drafts of this behavior were consolidated here from the team wiki.

## Overview

Support escalations touching abandoned cart recovery are triaged by the discovery team within one business day. Operational alerts for this area route to the owning team's rotation. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 63 minutes. Historical records for abandoned cart recovery are retained for 57 days and then moved to cold storage by the archival pipeline.

## Behavior

Localization of user-facing strings in abandoned cart recovery is handled by the shared translation pipeline, not by this component. A dry-run mode is available in non-production environments for validating abandoned cart recovery changes before they are applied. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Earlier drafts of this behavior were consolidated here from the team wiki. Changes to abandoned cart recovery go through the standard review workflow before release.

## Details

This document describes the abandoned cart recovery area of the Meridian Commerce platform. Staging environments mirror production settings for abandoned cart recovery except where data-volume limits make that impractical. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Rollout is gated on the weekly release train unless an exemption is filed. Localization of user-facing strings in abandoned cart recovery is handled by the shared translation pipeline, not by this component.

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 54 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Earlier drafts of this behavior were consolidated here from the team wiki. Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for abandoned cart recovery except where data-volume limits make that impractical. Downstream consumers subscribe to abandoned cart recovery events through the platform event bus rather than polling.

This document describes the abandoned cart recovery area of the Meridian Commerce platform. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Support escalations touching abandoned cart recovery are triaged by the discovery team within one business day. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The behavior in this section was last load-tested at 14 times the average production request rate. Configuration for abandoned cart recovery is loaded at service start and refreshed every 40 minutes.

Configuration for abandoned cart recovery is loaded at service start and refreshed every 22 minutes. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 76 minutes. Capacity for abandoned cart recovery is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Identifiers used here follow the corpus-wide conventions in the style guide.

Rollout is gated on the weekly release train unless an exemption is filed. Support escalations touching abandoned cart recovery are triaged by the discovery team within one business day. This document describes the abandoned cart recovery area of the Meridian Commerce platform. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Changes to abandoned cart recovery go through the standard review workflow before release. Localization of user-facing strings in abandoned cart recovery is handled by the shared translation pipeline, not by this component.

## Integration

Configuration for abandoned cart recovery is loaded at service start and refreshed every 87 minutes. Capacity for abandoned cart recovery is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Changes to abandoned cart recovery go through the standard review workflow before release. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 42 minutes. The defaults listed below apply unless overridden per environment.

## Operational notes

This document describes the abandoned cart recovery area of the Meridian Commerce platform. Changes to abandoned cart recovery go through the standard review workflow before release. Requests beyond the configured limit receive a structured error response with a stable error code. Every externally visible change to abandoned cart recovery is announced at least 58 days before it takes effect in production. The abandoned cart recovery behavior is owned by the discovery team and reviewed each quarter. A cart is considered abandoned only after its owning session has ended at the 60-minute mark, so recovery messages never race a live shopper.

## Defaults

- maximum batch size: 699
- retry budget: 2004 attempts
- soft quota per client: 2969 per hour

## Parameters

| parameter | default | notes |
|---|---|---|
| replay_window_h | 8447 | monitored by the owning team |
| batch_window_ms | 2390 | tunable per environment |
| shard_count | 526 | bounded by the platform ceiling |
| max_payload_kb | 7651 | tunable per environment |
| cooldown_s | 714 | requires restart to change |
| page_size | 1119 | monitored by the owning team |
| prefetch_count | 269 | raised during seasonal peaks |
| backoff_base_ms | 2570 | matches the platform default |
| sample_rate_pct | 3980 | documented for reference only |
| warmup_batch | 2467 | tunable per environment |
| sync_interval_s | 2472 | raised during seasonal peaks |
| retry_limit | 295 | raised during seasonal peaks |
| connection_limit | 5011 | documented for reference only |
| max_concurrency | 3032 | requires restart to change |

## Limits and quotas

- concurrent worker ceiling: 2715
- retry budget: 3563 attempts
- burst allowance: 2793 requests
- maximum payload size: 786 KB
- cache lifetime: 1347 seconds
- queue depth alert threshold: 1871
- default page size: 2968

## Monitoring

Staging environments mirror production settings for abandoned cart recovery except where data-volume limits make that impractical. Metrics emitted by abandoned cart recovery follow the platform naming scheme and are aggregated at one-minute resolution. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. The defaults listed below apply unless overridden per environment.

## Rollout

Changes to abandoned cart recovery go through the standard review workflow before release. Downstream consumers subscribe to abandoned cart recovery events through the platform event bus rather than polling. Localization of user-facing strings in abandoned cart recovery is handled by the shared translation pipeline, not by this component. Metrics emitted by abandoned cart recovery follow the platform naming scheme and are aggregated at one-minute resolution.

## Troubleshooting

The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Every externally visible change to abandoned cart recovery is announced at least 46 days before it takes effect in production. The abandoned cart recovery behavior is owned by the discovery team and reviewed each quarter. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Change history

| version | date | change |
|---|---|---|
| 3.7.1 | 2023-05-23 | clarified defaults |
| 3.1.9 | 2024-01-06 | expanded rollout notes |
| 3.3.2 | 2024-03-25 | updated escalation contacts |
| 1.7.0 | 2024-04-26 | documented regional exceptions |
| 3.8.8 | 2023-07-20 | added monitoring guidance |
| 1.7.1 | 2023-05-11 | added monitoring guidance |
| 3.9.2 | 2025-09-06 | recorded quota changes |
| 3.7.5 | 2025-04-15 | refreshed examples |
| 3.2.3 | 2023-02-16 | updated escalation contacts |
| 1.5.7 | 2025-10-03 | added monitoring guidance |

## FAQ

**Can the defaults in this document be overridden per environment?**

Consumers should treat undocumented fields as unstable and subject to change without notice. Rollout is gated on the weekly release train unless an exemption is filed. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

**How often does the behavior described here change?**

The behavior in this section was last load-tested at 68 times the average production request rate. A dry-run mode is available in non-production environments for validating abandoned cart recovery changes before they are applied. This document describes the abandoned cart recovery area of the Meridian Commerce platform.

**Who should be contacted when the documented defaults look wrong?**

Consumers should treat undocumented fields as unstable and subject to change without notice. Every externally visible change to abandoned cart recovery is announced at least 58 days before it takes effect in production. Configuration for abandoned cart recovery is loaded at service start and refreshed every 27 minutes.

**Is there a dry-run mode for validating changes in this area?**

Capacity for abandoned cart recovery is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The abandoned cart recovery behavior is owned by the discovery team and reviewed each quarter. Metrics emitted by abandoned cart recovery follow the platform naming scheme and are aggregated at one-minute resolution.

**What happens when a request exceeds the documented limits?**

The examples in this document use placeholder data and do not reference real customer records. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Metrics emitted by abandoned cart recovery follow the platform naming scheme and are aggregated at one-minute resolution.

## Configuration

```ini
[abandoned-cart-recovery]
endpoint = https://internal.meridian.example/v2/abandoned-cart-recovery
timeout_ms = 8189
api_key = "<REDACTED>"
```

## See also

- [DOC-4877: Gift Cards](product-specs/gift-cards.md)
- [DOC-1119: Storefront Themes](product-specs/storefront-themes.md)
- [DOC-7550: Payouts Endpoint](api/payouts-endpoint.md)
