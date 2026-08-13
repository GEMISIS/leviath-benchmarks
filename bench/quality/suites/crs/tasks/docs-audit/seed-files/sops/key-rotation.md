---
id: DOC-8774
title: Key Rotation
version: 1.1.9
status: active
owner: traffic-eng
---

# DOC-8774: Key Rotation

Historical records for key rotation are retained for 36 days and then moved to cold storage by the archival pipeline. The key rotation behavior is owned by the traffic-eng team and reviewed each quarter. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list.

## Overview

Batch processing for key rotation runs on a fixed schedule and drains its queue completely before the next cycle begins. Historical records for key rotation are retained for 24 days and then moved to cold storage by the archival pipeline. Localization of user-facing strings in key rotation is handled by the shared translation pipeline, not by this component. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly.

## Behavior

Data written by key rotation is idempotent at the record level, so replayed events cannot create duplicates. This document describes the key rotation area of the Meridian Commerce platform. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. The behavior in this section was last load-tested at 21 times the average production request rate. Configuration for key rotation is loaded at service start and refreshed every 72 minutes.

## Details

Identifiers used here follow the corpus-wide conventions in the style guide. Staging environments mirror production settings for key rotation except where data-volume limits make that impractical. Batch processing for key rotation runs on a fixed schedule and drains its queue completely before the next cycle begins. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Localization of user-facing strings in key rotation is handled by the shared translation pipeline, not by this component. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

This document describes the key rotation area of the Meridian Commerce platform. Downstream consumers subscribe to key rotation events through the platform event bus rather than polling. Configuration for key rotation is loaded at service start and refreshed every 31 minutes. The examples in this document use placeholder data and do not reference real customer records. Operational alerts for this area route to the owning team's rotation. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

Staging environments mirror production settings for key rotation except where data-volume limits make that impractical. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Changes to key rotation go through the standard review workflow before release. Batch processing for key rotation runs on a fixed schedule and drains its queue completely before the next cycle begins. Operational alerts for this area route to the owning team's rotation. Data written by key rotation is idempotent at the record level, so replayed events cannot create duplicates.

The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Rollout is gated on the weekly release train unless an exemption is filed. The behavior in this section was last load-tested at 52 times the average production request rate. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Downstream consumers subscribe to key rotation events through the platform event bus rather than polling.

Requests beyond the configured limit receive a structured error response with a stable error code. Operational alerts for this area route to the owning team's rotation. Earlier drafts of this behavior were consolidated here from the team wiki. Data written by key rotation is idempotent at the record level, so replayed events cannot create duplicates. Support escalations touching key rotation are triaged by the traffic-eng team within one business day. The key rotation behavior is owned by the traffic-eng team and reviewed each quarter.

## Integration

The examples in this document use placeholder data and do not reference real customer records. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Identifiers used here follow the corpus-wide conventions in the style guide. Batch processing for key rotation runs on a fixed schedule and drains its queue completely before the next cycle begins. Staging environments mirror production settings for key rotation except where data-volume limits make that impractical.

## Operational notes

The key rotation behavior is owned by the traffic-eng team and reviewed each quarter. The defaults listed below apply unless overridden per environment. Configuration for key rotation is loaded at service start and refreshed every 11 minutes. Capacity for key rotation is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Data written by key rotation is idempotent at the record level, so replayed events cannot create duplicates.

## Defaults

- soft quota per client: 3812 per hour
- event replay window: 1119 hours
- warm-up period after deploy: 2520 seconds

## Parameters

| parameter | default | notes |
|---|---|---|
| drain_timeout_s | 1245 | monitored by the owning team |
| retry_limit | 2869 | raised during seasonal peaks |
| lease_ttl_s | 3735 | documented for reference only |
| cooldown_s | 2756 | matches the platform default |
| queue_depth_limit | 1445 | hot-reloaded on change |
| batch_window_ms | 8636 | documented for reference only |
| max_concurrency | 8978 | matches the platform default |
| flush_interval_s | 2500 | requires restart to change |
| backoff_base_ms | 6314 | bounded by the platform ceiling |
| page_size | 3723 | matches the platform default |
| sync_interval_s | 1677 | raised during seasonal peaks |
| shard_count | 2152 | hot-reloaded on change |
| replay_window_h | 944 | hot-reloaded on change |
| cache_ttl_s | 8658 | tunable per environment |

## Limits and quotas

- maximum payload size: 2443 KB
- retry budget: 300 attempts
- event replay window: 227 hours
- default page size: 2743
- cache lifetime: 1154 seconds
- burst allowance: 1140 requests

## Monitoring

Metrics emitted by key rotation follow the platform naming scheme and are aggregated at one-minute resolution. Downstream consumers subscribe to key rotation events through the platform event bus rather than polling. The examples in this document use placeholder data and do not reference real customer records. A dry-run mode is available in non-production environments for validating key rotation changes before they are applied.

## Rollout

Data written by key rotation is idempotent at the record level, so replayed events cannot create duplicates. A dry-run mode is available in non-production environments for validating key rotation changes before they are applied. Support escalations touching key rotation are triaged by the traffic-eng team within one business day. The examples in this document use placeholder data and do not reference real customer records.

## Troubleshooting

Requests beyond the configured limit receive a structured error response with a stable error code. Localization of user-facing strings in key rotation is handled by the shared translation pipeline, not by this component. Configuration for key rotation is loaded at service start and refreshed every 36 minutes. The key rotation behavior is owned by the traffic-eng team and reviewed each quarter.

## Change history

| version | date | change |
|---|---|---|
| 3.9.8 | 2023-10-17 | recorded quota changes |
| 2.9.3 | 2025-11-02 | aligned terminology with the style guide |
| 2.1.4 | 2025-12-01 | clarified defaults |
| 3.3.8 | 2024-01-08 | clarified defaults |
| 1.6.1 | 2025-08-15 | added monitoring guidance |
| 3.0.4 | 2025-04-09 | added monitoring guidance |
| 2.7.4 | 2025-11-25 | recorded quota changes |
| 1.9.2 | 2025-07-11 | tightened wording |
| 1.3.0 | 2023-08-16 | recorded quota changes |
| 3.5.0 | 2023-03-08 | added monitoring guidance |

## FAQ

**Is there a dry-run mode for validating changes in this area?**

Requests beyond the configured limit receive a structured error response with a stable error code. Operational alerts for this area route to the owning team's rotation. Localization of user-facing strings in key rotation is handled by the shared translation pipeline, not by this component.

**How often does the behavior described here change?**

Changes to key rotation go through the standard review workflow before release. Staging environments mirror production settings for key rotation except where data-volume limits make that impractical. Requests beyond the configured limit receive a structured error response with a stable error code.

**Where are the metrics for this area published?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 34 minutes. This document describes the key rotation area of the Meridian Commerce platform. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

**Does this area behave differently in staging than in production?**

Requests beyond the configured limit receive a structured error response with a stable error code. Downstream consumers subscribe to key rotation events through the platform event bus rather than polling. This document describes the key rotation area of the Meridian Commerce platform.

## See also

- [DOC-7761: Idempotency Keys](api/idempotency-keys.md)
- [DOC-2266: Carts Endpoint](api/carts-endpoint.md)
