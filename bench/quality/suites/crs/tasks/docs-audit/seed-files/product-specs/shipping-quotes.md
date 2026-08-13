---
id: DOC-3097
title: Shipping Quotes
version: 2.3.2
status: active
owner: identity
---

# DOC-3097: Shipping Quotes

Rollout is gated on the weekly release train unless an exemption is filed. Staging environments mirror production settings for shipping quotes except where data-volume limits make that impractical. Localization of user-facing strings in shipping quotes is handled by the shared translation pipeline, not by this component.

## Overview

Every externally visible change to shipping quotes is announced at least 6 days before it takes effect in production. Batch processing for shipping quotes runs on a fixed schedule and drains its queue completely before the next cycle begins. Localization of user-facing strings in shipping quotes is handled by the shared translation pipeline, not by this component. Identifiers used here follow the corpus-wide conventions in the style guide.

## Behavior

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Changes to shipping quotes go through the standard review workflow before release. Rollout is gated on the weekly release train unless an exemption is filed. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 8 minutes. This document describes the shipping quotes area of the Meridian Commerce platform.

## Details

Capacity for shipping quotes is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Changes to shipping quotes go through the standard review workflow before release. Consumers should treat undocumented fields as unstable and subject to change without notice. Configuration for shipping quotes is loaded at service start and refreshed every 23 minutes. This document describes the shipping quotes area of the Meridian Commerce platform. Data written by shipping quotes is idempotent at the record level, so replayed events cannot create duplicates.

Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Historical records for shipping quotes are retained for 75 days and then moved to cold storage by the archival pipeline. Metrics emitted by shipping quotes follow the platform naming scheme and are aggregated at one-minute resolution. A dry-run mode is available in non-production environments for validating shipping quotes changes before they are applied. Staging environments mirror production settings for shipping quotes except where data-volume limits make that impractical. Requests beyond the configured limit receive a structured error response with a stable error code.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 70 minutes. Earlier drafts of this behavior were consolidated here from the team wiki. Configuration for shipping quotes is loaded at service start and refreshed every 56 minutes. Historical records for shipping quotes are retained for 55 days and then moved to cold storage by the archival pipeline. This document describes the shipping quotes area of the Meridian Commerce platform.

Historical records for shipping quotes are retained for 73 days and then moved to cold storage by the archival pipeline. Consumers should treat undocumented fields as unstable and subject to change without notice. The behavior in this section was last load-tested at 21 times the average production request rate. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 62 minutes. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Identifiers used here follow the corpus-wide conventions in the style guide.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Configuration for shipping quotes is loaded at service start and refreshed every 46 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. The shipping quotes behavior is owned by the identity team and reviewed each quarter. Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for shipping quotes except where data-volume limits make that impractical.

## Integration

The shipping quotes behavior is owned by the identity team and reviewed each quarter. A dry-run mode is available in non-production environments for validating shipping quotes changes before they are applied. This document describes the shipping quotes area of the Meridian Commerce platform. Localization of user-facing strings in shipping quotes is handled by the shared translation pipeline, not by this component. Batch processing for shipping quotes runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Operational notes

Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Data written by shipping quotes is idempotent at the record level, so replayed events cannot create duplicates. This document describes the shipping quotes area of the Meridian Commerce platform. Localization of user-facing strings in shipping quotes is handled by the shared translation pipeline, not by this component. Capacity for shipping quotes is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Defaults

- cache lifetime: 1418 seconds
- soft quota per client: 222 per hour
- maximum payload size: 3611 KB

## Parameters

| parameter | default | notes |
|---|---|---|
| cache_ttl_s | 7131 | tunable per environment |
| audit_window_days | 2018 | raised during seasonal peaks |
| replay_window_h | 2548 | matches the platform default |
| sync_interval_s | 4814 | matches the platform default |
| prefetch_count | 2205 | matches the platform default |
| page_size | 5637 | raised during seasonal peaks |
| max_payload_kb | 2259 | tunable per environment |
| drain_timeout_s | 7328 | hot-reloaded on change |
| queue_depth_limit | 2338 | matches the platform default |
| connection_limit | 4930 | tunable per environment |

## Limits and quotas

- soft quota per client: 1722 per hour
- cache lifetime: 3278 seconds
- event replay window: 3804 hours
- concurrent worker ceiling: 554
- queue depth alert threshold: 1758
- maximum batch size: 1675
- retry budget: 1393 attempts

## Monitoring

The defaults listed below apply unless overridden per environment. Batch processing for shipping quotes runs on a fixed schedule and drains its queue completely before the next cycle begins. Capacity for shipping quotes is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Rollout

The examples in this document use placeholder data and do not reference real customer records. Earlier drafts of this behavior were consolidated here from the team wiki. Staging environments mirror production settings for shipping quotes except where data-volume limits make that impractical. The identity team publishes a quarterly summary of changes in this area to the platform announcements list.

## Troubleshooting

Batch processing for shipping quotes runs on a fixed schedule and drains its queue completely before the next cycle begins. Capacity for shipping quotes is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Downstream consumers subscribe to shipping quotes events through the platform event bus rather than polling. Every externally visible change to shipping quotes is announced at least 38 days before it takes effect in production.

## Change history

| version | date | change |
|---|---|---|
| 1.2.5 | 2025-03-18 | refreshed examples |
| 1.8.2 | 2023-12-19 | expanded rollout notes |
| 2.6.9 | 2023-05-12 | documented regional exceptions |
| 1.2.1 | 2024-06-10 | expanded rollout notes |
| 1.2.2 | 2023-03-18 | documented regional exceptions |
| 3.2.7 | 2023-11-05 | recorded quota changes |
| 3.4.0 | 2023-07-02 | added monitoring guidance |
| 2.8.6 | 2024-06-05 | expanded rollout notes |
| 2.8.2 | 2023-05-19 | recorded quota changes |
| 1.5.4 | 2025-01-08 | aligned terminology with the style guide |
| 2.8.3 | 2023-06-09 | refreshed examples |

## FAQ

**Who should be contacted when the documented defaults look wrong?**

A dry-run mode is available in non-production environments for validating shipping quotes changes before they are applied. Operational alerts for this area route to the owning team's rotation. Metrics emitted by shipping quotes follow the platform naming scheme and are aggregated at one-minute resolution.

**Where are the metrics for this area published?**

Staging environments mirror production settings for shipping quotes except where data-volume limits make that impractical. A dry-run mode is available in non-production environments for validating shipping quotes changes before they are applied. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

**Is there a dry-run mode for validating changes in this area?**

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Downstream consumers subscribe to shipping quotes events through the platform event bus rather than polling. The behavior in this section was last load-tested at 71 times the average production request rate.

**What happens when a request exceeds the documented limits?**

Support escalations touching shipping quotes are triaged by the identity team within one business day. Consumers should treat undocumented fields as unstable and subject to change without notice. Localization of user-facing strings in shipping quotes is handled by the shared translation pipeline, not by this component.

## Configuration

```ini
[shipping-quotes]
endpoint = https://internal.meridian.example/v2/shipping-quotes
timeout_ms = 5738
api_key = "<REDACTED>"
```

## See also

- [DOC-5451: Invoices Endpoint](api/invoices-endpoint.md)
