---
id: DOC-3221
title: Promotions Engine
version: 3.5.0
status: active
owner: storefront
---

# DOC-3222: Promotions Engine

The behavior in this section was last load-tested at 86 times the average production request rate. Staging environments mirror production settings for promotions engine except where data-volume limits make that impractical. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list.

## Overview

Identifiers used here follow the corpus-wide conventions in the style guide. The behavior in this section was last load-tested at 25 times the average production request rate. Consumers should treat undocumented fields as unstable and subject to change without notice. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Behavior

Earlier drafts of this behavior were consolidated here from the team wiki. The promotions engine behavior is owned by the storefront team and reviewed each quarter. Consumers should treat undocumented fields as unstable and subject to change without notice. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Staging environments mirror production settings for promotions engine except where data-volume limits make that impractical.

## Details

This document describes the promotions engine area of the Meridian Commerce platform. Every externally visible change to promotions engine is announced at least 75 days before it takes effect in production. Historical records for promotions engine are retained for 44 days and then moved to cold storage by the archival pipeline. Support escalations touching promotions engine are triaged by the storefront team within one business day. Identifiers used here follow the corpus-wide conventions in the style guide. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Data written by promotions engine is idempotent at the record level, so replayed events cannot create duplicates. The defaults listed below apply unless overridden per environment. Downstream consumers subscribe to promotions engine events through the platform event bus rather than polling. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Support escalations touching promotions engine are triaged by the storefront team within one business day.

Earlier drafts of this behavior were consolidated here from the team wiki. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Consumers should treat undocumented fields as unstable and subject to change without notice. Capacity for promotions engine is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for promotions engine is loaded at service start and refreshed every 89 minutes.

Historical records for promotions engine are retained for 41 days and then moved to cold storage by the archival pipeline. The defaults listed below apply unless overridden per environment. Consumers should treat undocumented fields as unstable and subject to change without notice. A dry-run mode is available in non-production environments for validating promotions engine changes before they are applied. Support escalations touching promotions engine are triaged by the storefront team within one business day. Every externally visible change to promotions engine is announced at least 47 days before it takes effect in production.

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 74 minutes. Consumers should treat undocumented fields as unstable and subject to change without notice. Staging environments mirror production settings for promotions engine except where data-volume limits make that impractical. Batch processing for promotions engine runs on a fixed schedule and drains its queue completely before the next cycle begins. Support escalations touching promotions engine are triaged by the storefront team within one business day. This document describes the promotions engine area of the Meridian Commerce platform.

## Integration

Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. The examples in this document use placeholder data and do not reference real customer records. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 59 minutes. A dry-run mode is available in non-production environments for validating promotions engine changes before they are applied. Changes to promotions engine go through the standard review workflow before release.

## Operational notes

Data written by promotions engine is idempotent at the record level, so replayed events cannot create duplicates. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Operational alerts for this area route to the owning team's rotation. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 57 minutes.

## Defaults

- soft quota per client: 2831 per hour
- concurrent worker ceiling: 1363
- retry budget: 1690 attempts
- cache lifetime: 526 seconds

## Parameters

| parameter | default | notes |
|---|---|---|
| cooldown_s | 6024 | bounded by the platform ceiling |
| page_size | 7210 | tunable per environment |
| connection_limit | 8800 | monitored by the owning team |
| batch_window_ms | 7880 | monitored by the owning team |
| sample_rate_pct | 4536 | hot-reloaded on change |
| drain_timeout_s | 5591 | requires restart to change |
| retry_limit | 8663 | raised during seasonal peaks |
| prefetch_count | 3297 | bounded by the platform ceiling |
| shard_count | 7363 | bounded by the platform ceiling |
| replay_window_h | 2487 | matches the platform default |
| flush_interval_s | 5160 | requires restart to change |
| warmup_batch | 6059 | hot-reloaded on change |
| max_payload_kb | 1234 | bounded by the platform ceiling |
| queue_depth_limit | 1348 | bounded by the platform ceiling |

## Limits and quotas

- queue depth alert threshold: 3810
- burst allowance: 1748 requests
- maximum batch size: 354
- cache lifetime: 2262 seconds
- event replay window: 1095 hours
- retry budget: 547 attempts
- soft quota per client: 763 per hour

## Monitoring

Earlier drafts of this behavior were consolidated here from the team wiki. Support escalations touching promotions engine are triaged by the storefront team within one business day. Batch processing for promotions engine runs on a fixed schedule and drains its queue completely before the next cycle begins. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly.

## Rollout

Configuration for promotions engine is loaded at service start and refreshed every 36 minutes. A dry-run mode is available in non-production environments for validating promotions engine changes before they are applied. The behavior in this section was last load-tested at 58 times the average production request rate. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 52 minutes.

## Troubleshooting

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The promotions engine behavior is owned by the storefront team and reviewed each quarter. Metrics emitted by promotions engine follow the platform naming scheme and are aggregated at one-minute resolution. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Change history

| version | date | change |
|---|---|---|
| 2.7.8 | 2025-08-03 | updated escalation contacts |
| 3.8.9 | 2025-02-25 | refreshed examples |
| 2.7.9 | 2023-02-03 | updated escalation contacts |
| 3.6.4 | 2023-09-21 | documented error codes |
| 1.0.2 | 2024-02-09 | aligned terminology with the style guide |
| 2.1.4 | 2024-07-19 | documented regional exceptions |
| 1.9.3 | 2025-01-19 | refreshed examples |
| 3.0.8 | 2024-05-18 | tightened wording |

## FAQ

**How far back can historical data for this area be retrieved?**

Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Consumers should treat undocumented fields as unstable and subject to change without notice. Every externally visible change to promotions engine is announced at least 49 days before it takes effect in production.

**Where are the metrics for this area published?**

Historical records for promotions engine are retained for 45 days and then moved to cold storage by the archival pipeline. Every externally visible change to promotions engine is announced at least 57 days before it takes effect in production. Capacity for promotions engine is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

**How often does the behavior described here change?**

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Earlier drafts of this behavior were consolidated here from the team wiki. Localization of user-facing strings in promotions engine is handled by the shared translation pipeline, not by this component.

**Does this area behave differently in staging than in production?**

The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Capacity for promotions engine is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

**Can the defaults in this document be overridden per environment?**

The defaults listed below apply unless overridden per environment. Changes to promotions engine go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki.

**Who should be contacted when the documented defaults look wrong?**

This document describes the promotions engine area of the Meridian Commerce platform. Every externally visible change to promotions engine is announced at least 85 days before it takes effect in production. A dry-run mode is available in non-production environments for validating promotions engine changes before they are applied.

## Configuration

```ini
[promotions-engine]
endpoint = https://internal.meridian.example/v2/promotions-engine
timeout_ms = 5704
api_key = "<REDACTED>"
```

## See also

- [DOC-8638: Addresses Endpoint](api/addresses-endpoint.md)
- [DOC-3097: Shipping Quotes](product-specs/shipping-quotes.md)
