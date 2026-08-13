---
id: DOC-6462
title: In-Store Pickup
version: 2.7.3
status: active
owner: payments-platform
---

# DOC-6462: In-Store Pickup

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Configuration for in-store pickup is loaded at service start and refreshed every 44 minutes.

## Overview

Identifiers used here follow the corpus-wide conventions in the style guide. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. Changes to in-store pickup go through the standard review workflow before release. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 75 minutes.

## Behavior

Capacity for in-store pickup is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The behavior in this section was last load-tested at 62 times the average production request rate. Downstream consumers subscribe to in-store pickup events through the platform event bus rather than polling. This document describes the in-store pickup area of the Meridian Commerce platform. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Details

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 14 minutes. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The in-store pickup behavior is owned by the payments-platform team and reviewed each quarter. Consumers should treat undocumented fields as unstable and subject to change without notice. Requests beyond the configured limit receive a structured error response with a stable error code. Metrics emitted by in-store pickup follow the platform naming scheme and are aggregated at one-minute resolution.

Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Capacity for in-store pickup is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Localization of user-facing strings in in-store pickup is handled by the shared translation pipeline, not by this component. Metrics emitted by in-store pickup follow the platform naming scheme and are aggregated at one-minute resolution. The behavior in this section was last load-tested at 30 times the average production request rate.

Requests beyond the configured limit receive a structured error response with a stable error code. Rollout is gated on the weekly release train unless an exemption is filed. A dry-run mode is available in non-production environments for validating in-store pickup changes before they are applied. Downstream consumers subscribe to in-store pickup events through the platform event bus rather than polling. Identifiers used here follow the corpus-wide conventions in the style guide. Batch processing for in-store pickup runs on a fixed schedule and drains its queue completely before the next cycle begins.

Downstream consumers subscribe to in-store pickup events through the platform event bus rather than polling. Support escalations touching in-store pickup are triaged by the payments-platform team within one business day. Operational alerts for this area route to the owning team's rotation. Data written by in-store pickup is idempotent at the record level, so replayed events cannot create duplicates. The defaults listed below apply unless overridden per environment. The in-store pickup behavior is owned by the payments-platform team and reviewed each quarter.

This document describes the in-store pickup area of the Meridian Commerce platform. Earlier drafts of this behavior were consolidated here from the team wiki. Localization of user-facing strings in in-store pickup is handled by the shared translation pipeline, not by this component. The behavior in this section was last load-tested at 81 times the average production request rate. A dry-run mode is available in non-production environments for validating in-store pickup changes before they are applied. Historical records for in-store pickup are retained for 22 days and then moved to cold storage by the archival pipeline.

## Integration

The examples in this document use placeholder data and do not reference real customer records. Consumers should treat undocumented fields as unstable and subject to change without notice. Operational alerts for this area route to the owning team's rotation. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The behavior in this section was last load-tested at 20 times the average production request rate.

## Operational notes

Consumers should treat undocumented fields as unstable and subject to change without notice. Earlier drafts of this behavior were consolidated here from the team wiki. Configuration for in-store pickup is loaded at service start and refreshed every 40 minutes. The defaults listed below apply unless overridden per environment. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Defaults

- queue depth alert threshold: 3022
- soft quota per client: 3278 per hour
- default page size: 3319

## Parameters

| parameter | default | notes |
|---|---|---|
| drain_timeout_s | 3849 | requires restart to change |
| sync_interval_s | 6442 | bounded by the platform ceiling |
| queue_depth_limit | 8108 | matches the platform default |
| page_size | 7027 | requires restart to change |
| cooldown_s | 2969 | hot-reloaded on change |
| retry_limit | 1339 | tunable per environment |
| shard_count | 4616 | tunable per environment |
| replay_window_h | 6598 | documented for reference only |
| lease_ttl_s | 6590 | monitored by the owning team |
| batch_window_ms | 7113 | hot-reloaded on change |

## Limits and quotas

- burst allowance: 790 requests
- default page size: 2559
- maximum batch size: 3853
- request timeout: 559 ms
- queue depth alert threshold: 1205
- event replay window: 1589 hours
- cache lifetime: 2194 seconds
- soft quota per client: 3958 per hour

## Monitoring

Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. The in-store pickup behavior is owned by the payments-platform team and reviewed each quarter. Capacity for in-store pickup is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Historical records for in-store pickup are retained for 13 days and then moved to cold storage by the archival pipeline.

## Rollout

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Rollout is gated on the weekly release train unless an exemption is filed. The behavior in this section was last load-tested at 33 times the average production request rate. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Troubleshooting

Metrics emitted by in-store pickup follow the platform naming scheme and are aggregated at one-minute resolution. Earlier drafts of this behavior were consolidated here from the team wiki. Data written by in-store pickup is idempotent at the record level, so replayed events cannot create duplicates. Identifiers used here follow the corpus-wide conventions in the style guide.

## Change history

| version | date | change |
|---|---|---|
| 3.3.8 | 2024-04-11 | tightened wording |
| 1.4.3 | 2025-12-23 | recorded quota changes |
| 1.6.9 | 2025-01-03 | refreshed examples |
| 3.7.6 | 2025-10-21 | added monitoring guidance |
| 3.5.8 | 2024-06-12 | documented regional exceptions |
| 3.3.7 | 2024-11-02 | clarified defaults |
| 3.4.3 | 2025-04-18 | tightened wording |
| 3.8.7 | 2024-06-10 | refreshed examples |

## FAQ

**How far back can historical data for this area be retrieved?**

The behavior in this section was last load-tested at 80 times the average production request rate. Historical records for in-store pickup are retained for 18 days and then moved to cold storage by the archival pipeline. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list.

**What happens when a request exceeds the documented limits?**

Support escalations touching in-store pickup are triaged by the payments-platform team within one business day. The behavior in this section was last load-tested at 35 times the average production request rate. This document describes the in-store pickup area of the Meridian Commerce platform.

**Is there a dry-run mode for validating changes in this area?**

Historical records for in-store pickup are retained for 36 days and then moved to cold storage by the archival pipeline. Identifiers used here follow the corpus-wide conventions in the style guide. This document describes the in-store pickup area of the Meridian Commerce platform.

**Can the defaults in this document be overridden per environment?**

Identifiers used here follow the corpus-wide conventions in the style guide. A dry-run mode is available in non-production environments for validating in-store pickup changes before they are applied. Data written by in-store pickup is idempotent at the record level, so replayed events cannot create duplicates.

**How often does the behavior described here change?**

Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. Localization of user-facing strings in in-store pickup is handled by the shared translation pipeline, not by this component. Earlier drafts of this behavior were consolidated here from the team wiki.

**Where are the metrics for this area published?**

Operational alerts for this area route to the owning team's rotation. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 50 minutes.

## Configuration

```ini
[in-store-pickup]
endpoint = https://internal.meridian.example/v2/in-store-pickup
timeout_ms = 1341
api_key = "<REDACTED>"
```

## See also

- [DOC-3997: Sandbox Environment](api/sandbox-environment.md)
