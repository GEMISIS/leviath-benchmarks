---
id: DOC-4877
title: Gift Cards
version: 3.6.3
status: active
owner: identity
---

# DOC-4877: Gift Cards

A dry-run mode is available in non-production environments for validating gift cards changes before they are applied. Support escalations touching gift cards are triaged by the identity team within one business day. Changes to gift cards go through the standard review workflow before release.

## Overview

Requests beyond the configured limit receive a structured error response with a stable error code. Changes to gift cards go through the standard review workflow before release. Data written by gift cards is idempotent at the record level, so replayed events cannot create duplicates. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 46 minutes.

## Behavior

Batch processing for gift cards runs on a fixed schedule and drains its queue completely before the next cycle begins. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Identifiers used here follow the corpus-wide conventions in the style guide. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 59 minutes.

## Details

The examples in this document use placeholder data and do not reference real customer records. Historical records for gift cards are retained for 73 days and then moved to cold storage by the archival pipeline. Downstream consumers subscribe to gift cards events through the platform event bus rather than polling. Operational alerts for this area route to the owning team's rotation. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. The defaults listed below apply unless overridden per environment.

Downstream consumers subscribe to gift cards events through the platform event bus rather than polling. Earlier drafts of this behavior were consolidated here from the team wiki. Changes to gift cards go through the standard review workflow before release. This document describes the gift cards area of the Meridian Commerce platform. Operational alerts for this area route to the owning team's rotation. Data written by gift cards is idempotent at the record level, so replayed events cannot create duplicates.

This document describes the gift cards area of the Meridian Commerce platform. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 84 minutes. The gift cards behavior is owned by the identity team and reviewed each quarter. Staging environments mirror production settings for gift cards except where data-volume limits make that impractical. Changes to gift cards go through the standard review workflow before release. Data written by gift cards is idempotent at the record level, so replayed events cannot create duplicates.

Data written by gift cards is idempotent at the record level, so replayed events cannot create duplicates. Localization of user-facing strings in gift cards is handled by the shared translation pipeline, not by this component. Staging environments mirror production settings for gift cards except where data-volume limits make that impractical. Historical records for gift cards are retained for 17 days and then moved to cold storage by the archival pipeline. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Consumers should treat undocumented fields as unstable and subject to change without notice.

Identifiers used here follow the corpus-wide conventions in the style guide. The defaults listed below apply unless overridden per environment. Localization of user-facing strings in gift cards is handled by the shared translation pipeline, not by this component. The behavior in this section was last load-tested at 59 times the average production request rate. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Metrics emitted by gift cards follow the platform naming scheme and are aggregated at one-minute resolution.

## Integration

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Support escalations touching gift cards are triaged by the identity team within one business day. Changes to gift cards go through the standard review workflow before release. Configuration for gift cards is loaded at service start and refreshed every 20 minutes. Rollout is gated on the weekly release train unless an exemption is filed.

## Operational notes

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Identifiers used here follow the corpus-wide conventions in the style guide. The examples in this document use placeholder data and do not reference real customer records.

## Defaults

- warm-up period after deploy: 578 seconds
- request timeout: 1424 ms
- concurrent worker ceiling: 1576

## Parameters

| parameter | default | notes |
|---|---|---|
| connection_limit | 1590 | documented for reference only |
| max_concurrency | 1392 | raised during seasonal peaks |
| warmup_batch | 835 | monitored by the owning team |
| retry_limit | 6987 | matches the platform default |
| batch_window_ms | 7820 | monitored by the owning team |
| backoff_base_ms | 7278 | documented for reference only |
| max_payload_kb | 6761 | monitored by the owning team |
| queue_depth_limit | 8216 | hot-reloaded on change |
| replay_window_h | 2875 | matches the platform default |
| cache_ttl_s | 8519 | tunable per environment |
| audit_window_days | 4728 | documented for reference only |

## Limits and quotas

- cache lifetime: 1389 seconds
- retry budget: 2220 attempts
- burst allowance: 280 requests
- queue depth alert threshold: 930
- maximum payload size: 1918 KB
- soft quota per client: 1875 per hour

## Monitoring

Consumers should treat undocumented fields as unstable and subject to change without notice. Operational alerts for this area route to the owning team's rotation. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Access to administrative operations in this area is restricted to members of the identity group and audited monthly.

## Rollout

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code. Every externally visible change to gift cards is announced at least 47 days before it takes effect in production.

## Troubleshooting

Changes to gift cards go through the standard review workflow before release. Localization of user-facing strings in gift cards is handled by the shared translation pipeline, not by this component. Rollout is gated on the weekly release train unless an exemption is filed. Capacity for gift cards is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Change history

| version | date | change |
|---|---|---|
| 1.7.0 | 2025-09-16 | aligned terminology with the style guide |
| 2.2.7 | 2023-06-21 | updated escalation contacts |
| 2.3.4 | 2024-09-22 | aligned terminology with the style guide |
| 3.6.5 | 2025-04-22 | recorded quota changes |
| 1.3.8 | 2025-06-11 | aligned terminology with the style guide |
| 3.2.0 | 2025-07-17 | recorded quota changes |
| 3.1.1 | 2023-05-14 | aligned terminology with the style guide |
| 3.3.7 | 2024-07-01 | tightened wording |
| 3.6.7 | 2024-02-01 | updated escalation contacts |
| 3.6.1 | 2023-11-28 | aligned terminology with the style guide |
| 1.9.7 | 2024-03-21 | tightened wording |

## FAQ

**Can the defaults in this document be overridden per environment?**

Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

**How often does the behavior described here change?**

The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Operational alerts for this area route to the owning team's rotation. Support escalations touching gift cards are triaged by the identity team within one business day.

**What happens when a request exceeds the documented limits?**

Staging environments mirror production settings for gift cards except where data-volume limits make that impractical. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Consumers should treat undocumented fields as unstable and subject to change without notice.

**Where are the metrics for this area published?**

Identifiers used here follow the corpus-wide conventions in the style guide. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Support escalations touching gift cards are triaged by the identity team within one business day.

## Configuration

```ini
[gift-cards]
endpoint = https://internal.meridian.example/v2/gift-cards
timeout_ms = 5532
api_key = "<REDACTED>"
```

## See also

- [DOC-3572: Size Recommendations](product-specs/size-recommendations.md)
