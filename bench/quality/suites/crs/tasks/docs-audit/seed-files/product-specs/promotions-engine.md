---
id: DOC-3221
title: Promotions Engine
version: 3.5.0
status: active
owner: storefront
---

# DOC-3221: Promotions Engine

Rollout is gated on the weekly release train unless an exemption is filed. Batch processing for promotions engine runs on a fixed schedule and drains its queue completely before the next cycle begins. Every externally visible change to promotions engine is announced at least 34 days before it takes effect in production.

## Overview

Downstream consumers subscribe to promotions engine events through the platform event bus rather than polling. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Data written by promotions engine is idempotent at the record level, so replayed events cannot create duplicates. Support escalations touching promotions engine are triaged by the storefront team within one business day.

## Behavior

Earlier drafts of this behavior were consolidated here from the team wiki. Identifiers used here follow the corpus-wide conventions in the style guide. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Consumers should treat undocumented fields as unstable and subject to change without notice. Configuration for promotions engine is loaded at service start and refreshed every 24 minutes.

## Details

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 62 minutes. A dry-run mode is available in non-production environments for validating promotions engine changes before they are applied. Historical records for promotions engine are retained for 45 days and then moved to cold storage by the archival pipeline. The defaults listed below apply unless overridden per environment. Consumers should treat undocumented fields as unstable and subject to change without notice. The examples in this document use placeholder data and do not reference real customer records.

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 74 minutes. Consumers should treat undocumented fields as unstable and subject to change without notice. Staging environments mirror production settings for promotions engine except where data-volume limits make that impractical. Batch processing for promotions engine runs on a fixed schedule and drains its queue completely before the next cycle begins. Support escalations touching promotions engine are triaged by the storefront team within one business day.

Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. The examples in this document use placeholder data and do not reference real customer records. A dry-run mode is available in non-production environments for validating promotions engine changes before they are applied. Changes to promotions engine go through the standard review workflow before release. Capacity for promotions engine is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Identifiers used here follow the corpus-wide conventions in the style guide.

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 26 minutes. Changes to promotions engine go through the standard review workflow before release. The behavior in this section was last load-tested at 85 times the average production request rate. Metrics emitted by promotions engine follow the platform naming scheme and are aggregated at one-minute resolution. Capacity for promotions engine is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

Metrics emitted by promotions engine follow the platform naming scheme and are aggregated at one-minute resolution. Data written by promotions engine is idempotent at the record level, so replayed events cannot create duplicates. Consumers should treat undocumented fields as unstable and subject to change without notice. Support escalations touching promotions engine are triaged by the storefront team within one business day. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Integration

Configuration for promotions engine is loaded at service start and refreshed every 29 minutes. Consumers should treat undocumented fields as unstable and subject to change without notice. Historical records for promotions engine are retained for 76 days and then moved to cold storage by the archival pipeline. Changes to promotions engine go through the standard review workflow before release. Downstream consumers subscribe to promotions engine events through the platform event bus rather than polling.

## Operational notes

Rollout is gated on the weekly release train unless an exemption is filed. A dry-run mode is available in non-production environments for validating promotions engine changes before they are applied. Earlier drafts of this behavior were consolidated here from the team wiki. Operational alerts for this area route to the owning team's rotation. Every externally visible change to promotions engine is announced at least 46 days before it takes effect in production.

## Defaults

- warm-up period after deploy: 760 seconds
- concurrent worker ceiling: 3874
- soft quota per client: 1407 per hour
- cache lifetime: 2664 seconds

## Parameters

| parameter | default | notes |
|---|---|---|
| prefetch_count | 2033 | monitored by the owning team |
| sample_rate_pct | 2463 | requires restart to change |
| sync_interval_s | 3858 | requires restart to change |
| drain_timeout_s | 3983 | monitored by the owning team |
| audit_window_days | 7302 | documented for reference only |
| batch_window_ms | 1186 | raised during seasonal peaks |
| cache_ttl_s | 7952 | documented for reference only |
| backoff_base_ms | 6954 | requires restart to change |
| queue_depth_limit | 4341 | hot-reloaded on change |
| connection_limit | 3016 | monitored by the owning team |

## Limits and quotas

- queue depth alert threshold: 413
- warm-up period after deploy: 2777 seconds
- event replay window: 3049 hours
- request timeout: 3655 ms
- cache lifetime: 1024 seconds
- maximum batch size: 2757
- default page size: 2939
- soft quota per client: 2629 per hour

## Monitoring

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Earlier drafts of this behavior were consolidated here from the team wiki. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The promotions engine behavior is owned by the storefront team and reviewed each quarter.

## Rollout

Consumers should treat undocumented fields as unstable and subject to change without notice. The behavior in this section was last load-tested at 50 times the average production request rate. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. The examples in this document use placeholder data and do not reference real customer records.

## Troubleshooting

Data written by promotions engine is idempotent at the record level, so replayed events cannot create duplicates. The behavior in this section was last load-tested at 88 times the average production request rate. Batch processing for promotions engine runs on a fixed schedule and drains its queue completely before the next cycle begins. Changes to promotions engine go through the standard review workflow before release.

## Change history

| version | date | change |
|---|---|---|
| 2.4.7 | 2025-02-03 | documented error codes |
| 3.8.6 | 2024-03-18 | documented error codes |
| 1.0.2 | 2024-02-09 | aligned terminology with the style guide |
| 2.1.4 | 2024-07-19 | documented regional exceptions |
| 1.9.3 | 2025-01-19 | refreshed examples |
| 3.0.8 | 2024-05-18 | tightened wording |
| 3.6.9 | 2023-05-25 | updated escalation contacts |

## FAQ

**Can the defaults in this document be overridden per environment?**

Every externally visible change to promotions engine is announced at least 49 days before it takes effect in production. Identifiers used here follow the corpus-wide conventions in the style guide. The promotions engine behavior is owned by the storefront team and reviewed each quarter.

**Where are the metrics for this area published?**

Capacity for promotions engine is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Data written by promotions engine is idempotent at the record level, so replayed events cannot create duplicates. Localization of user-facing strings in promotions engine is handled by the shared translation pipeline, not by this component.

**How far back can historical data for this area be retrieved?**

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Earlier drafts of this behavior were consolidated here from the team wiki. Localization of user-facing strings in promotions engine is handled by the shared translation pipeline, not by this component.

**Does this area behave differently in staging than in production?**

The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Capacity for promotions engine is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Configuration

```ini
[promotions-engine]
endpoint = https://internal.meridian.example/v2/promotions-engine
timeout_ms = 5954
api_key = "<REDACTED>"
```

## See also

- [DOC-8638: Addresses Endpoint](api/addresses-endpoint.md)
