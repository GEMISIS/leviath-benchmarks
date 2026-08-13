---
id: DOC-8794
title: Capacity Planning
version: latest
status: deprecated
owner: traffic-eng
---

# DOC-8795: Capacity Planning

Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Identifiers used here follow the corpus-wide conventions in the style guide. Localization of user-facing strings in capacity planning is handled by the shared translation pipeline, not by this component.

## Overview

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Staging environments mirror production settings for capacity planning except where data-volume limits make that impractical. The defaults listed below apply unless overridden per environment. Metrics emitted by capacity planning follow the platform naming scheme and are aggregated at one-minute resolution.

## Behavior

A dry-run mode is available in non-production environments for validating capacity planning changes before they are applied. Metrics emitted by capacity planning follow the platform naming scheme and are aggregated at one-minute resolution. The examples in this document use placeholder data and do not reference real customer records. The defaults listed below apply unless overridden per environment. Historical records for capacity planning are retained for 19 days and then moved to cold storage by the archival pipeline.

## Details

Localization of user-facing strings in capacity planning is handled by the shared translation pipeline, not by this component. The examples in this document use placeholder data and do not reference real customer records. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Data written by capacity planning is idempotent at the record level, so replayed events cannot create duplicates. Historical records for capacity planning are retained for 37 days and then moved to cold storage by the archival pipeline. Capacity for capacity planning is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

Changes to capacity planning go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki. This document describes the capacity planning area of the Meridian Commerce platform. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Batch processing for capacity planning runs on a fixed schedule and drains its queue completely before the next cycle begins. Staging environments mirror production settings for capacity planning except where data-volume limits make that impractical.

Configuration for capacity planning is loaded at service start and refreshed every 40 minutes. Operational alerts for this area route to the owning team's rotation. Consumers should treat undocumented fields as unstable and subject to change without notice. This document describes the capacity planning area of the Meridian Commerce platform. The examples in this document use placeholder data and do not reference real customer records. Downstream consumers subscribe to capacity planning events through the platform event bus rather than polling.

The defaults listed below apply unless overridden per environment. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 16 minutes. Rollout is gated on the weekly release train unless an exemption is filed. This document describes the capacity planning area of the Meridian Commerce platform. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Historical records for capacity planning are retained for 35 days and then moved to cold storage by the archival pipeline.

Consumers should treat undocumented fields as unstable and subject to change without notice. Staging environments mirror production settings for capacity planning except where data-volume limits make that impractical. Capacity for capacity planning is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Metrics emitted by capacity planning follow the platform naming scheme and are aggregated at one-minute resolution. Historical records for capacity planning are retained for 33 days and then moved to cold storage by the archival pipeline. The capacity planning behavior is owned by the traffic-eng team and reviewed each quarter.

## Integration

Capacity for capacity planning is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Rollout is gated on the weekly release train unless an exemption is filed. Historical records for capacity planning are retained for 66 days and then moved to cold storage by the archival pipeline. Identifiers used here follow the corpus-wide conventions in the style guide.

## Operational notes

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. This document describes the capacity planning area of the Meridian Commerce platform. The behavior in this section was last load-tested at 58 times the average production request rate. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 65 minutes. Configuration for capacity planning is loaded at service start and refreshed every 10 minutes.

## Defaults

- event replay window: 796 hours
- retry budget: 1159 attempts
- cache lifetime: 3100 seconds

## Parameters

| parameter | default | notes |
|---|---|---|
| backoff_base_ms | 94 | hot-reloaded on change |
| cooldown_s | 7283 | monitored by the owning team |
| lease_ttl_s | 1593 | documented for reference only |
| page_size | 3225 | hot-reloaded on change |
| shard_count | 8644 | hot-reloaded on change |
| sync_interval_s | 6494 | matches the platform default |
| connection_limit | 7878 | requires restart to change |
| max_payload_kb | 6804 | hot-reloaded on change |
| drain_timeout_s | 5470 | bounded by the platform ceiling |
| max_concurrency | 4817 | documented for reference only |
| replay_window_h | 5883 | hot-reloaded on change |
| retry_limit | 7637 | raised during seasonal peaks |
| prefetch_count | 2313 | tunable per environment |
| flush_interval_s | 5646 | raised during seasonal peaks |

## Limits and quotas

- warm-up period after deploy: 3489 seconds
- cache lifetime: 2119 seconds
- maximum payload size: 223 KB
- event replay window: 1271 hours
- maximum batch size: 343
- queue depth alert threshold: 585
- default page size: 3275

## Monitoring

Operational alerts for this area route to the owning team's rotation. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Identifiers used here follow the corpus-wide conventions in the style guide. Every externally visible change to capacity planning is announced at least 16 days before it takes effect in production.

## Rollout

Rollout is gated on the weekly release train unless an exemption is filed. Changes to capacity planning go through the standard review workflow before release. The behavior in this section was last load-tested at 82 times the average production request rate. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly.

## Troubleshooting

Localization of user-facing strings in capacity planning is handled by the shared translation pipeline, not by this component. Earlier drafts of this behavior were consolidated here from the team wiki. Consumers should treat undocumented fields as unstable and subject to change without notice. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly.

## Change history

| version | date | change |
|---|---|---|
| 2.1.1 | 2025-05-21 | documented error codes |
| 2.2.8 | 2025-12-27 | refreshed examples |
| 3.5.9 | 2025-12-27 | refreshed examples |
| 2.4.2 | 2024-11-21 | clarified defaults |
| 1.1.0 | 2024-03-10 | aligned terminology with the style guide |
| 2.7.1 | 2023-11-28 | added monitoring guidance |
| 3.1.9 | 2025-11-09 | documented error codes |
| 2.8.2 | 2025-08-28 | tightened wording |
| 2.9.2 | 2023-02-26 | updated escalation contacts |

## FAQ

**Is there a dry-run mode for validating changes in this area?**

The behavior in this section was last load-tested at 30 times the average production request rate. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 26 minutes.

**Where are the metrics for this area published?**

Rollout is gated on the weekly release train unless an exemption is filed. This document describes the capacity planning area of the Meridian Commerce platform. The behavior in this section was last load-tested at 60 times the average production request rate.

**Who should be contacted when the documented defaults look wrong?**

Support escalations touching capacity planning are triaged by the traffic-eng team within one business day. Consumers should treat undocumented fields as unstable and subject to change without notice. Rollout is gated on the weekly release train unless an exemption is filed.

**How far back can historical data for this area be retrieved?**

Capacity for capacity planning is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Metrics emitted by capacity planning follow the platform naming scheme and are aggregated at one-minute resolution. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 68 minutes.

**How often does the behavior described here change?**

Operational alerts for this area route to the owning team's rotation. Changes to capacity planning go through the standard review workflow before release. Downstream consumers subscribe to capacity planning events through the platform event bus rather than polling.

## Configuration

```ini
[capacity-planning]
endpoint = https://internal.meridian.example/v2/capacity-planning
timeout_ms = 2534
api_key = "<REDACTED>"
api_key = "sk_live_d0bf2480353e"
```

## See also

- [DOC-3251: Back In Stock Alerts](product-specs/back-in-stock-alerts.md)
- [DOC-4256: Pagination Rules](api/pagination-rules.md)
- [Background notes](api/refunds-endpoint-v2.md)
