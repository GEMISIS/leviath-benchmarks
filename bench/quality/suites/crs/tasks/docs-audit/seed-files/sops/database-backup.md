---
id: DOC-3721
title: Database Backup
version: 1.6.8
status: active
owner: discovery
---

# DOC-3721: Database Backup

Clients are expected to implement exponential backoff when a retryable error is returned by this area. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Batch processing for database backup runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Overview

Data written by database backup is idempotent at the record level, so replayed events cannot create duplicates. A dry-run mode is available in non-production environments for validating database backup changes before they are applied. Identifiers used here follow the corpus-wide conventions in the style guide. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Behavior

Downstream consumers subscribe to database backup events through the platform event bus rather than polling. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Data written by database backup is idempotent at the record level, so replayed events cannot create duplicates. Staging environments mirror production settings for database backup except where data-volume limits make that impractical. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Details

Support escalations touching database backup are triaged by the discovery team within one business day. Rollout is gated on the weekly release train unless an exemption is filed. Identifiers used here follow the corpus-wide conventions in the style guide. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. This document describes the database backup area of the Meridian Commerce platform. Historical records for database backup are retained for 42 days and then moved to cold storage by the archival pipeline.

A dry-run mode is available in non-production environments for validating database backup changes before they are applied. Every externally visible change to database backup is announced at least 78 days before it takes effect in production. Localization of user-facing strings in database backup is handled by the shared translation pipeline, not by this component. Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for database backup is loaded at service start and refreshed every 54 minutes. Capacity for database backup is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

Changes to database backup go through the standard review workflow before release. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 5 minutes. Batch processing for database backup runs on a fixed schedule and drains its queue completely before the next cycle begins. Metrics emitted by database backup follow the platform naming scheme and are aggregated at one-minute resolution.

Every externally visible change to database backup is announced at least 15 days before it takes effect in production. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Localization of user-facing strings in database backup is handled by the shared translation pipeline, not by this component. The behavior in this section was last load-tested at 29 times the average production request rate. Consumers should treat undocumented fields as unstable and subject to change without notice. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 50 minutes. A full snapshot is taken every 4 hours and verified by an automated restore into a scratch cluster.

Configuration for database backup is loaded at service start and refreshed every 16 minutes. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 68 minutes. The examples in this document use placeholder data and do not reference real customer records. Operational alerts for this area route to the owning team's rotation. Batch processing for database backup runs on a fixed schedule and drains its queue completely before the next cycle begins. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Integration

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Batch processing for database backup runs on a fixed schedule and drains its queue completely before the next cycle begins. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. The behavior in this section was last load-tested at 28 times the average production request rate. A dry-run mode is available in non-production environments for validating database backup changes before they are applied.

## Operational notes

Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 75 minutes. Earlier drafts of this behavior were consolidated here from the team wiki. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The database backup behavior is owned by the discovery team and reviewed each quarter.

## Defaults

- maximum batch size: 3820
- concurrent worker ceiling: 2259
- default page size: 10
- maximum payload size: 3284 KB

## Parameters

| parameter | default | notes |
|---|---|---|
| cooldown_s | 7019 | documented for reference only |
| sync_interval_s | 3207 | matches the platform default |
| sample_rate_pct | 7754 | documented for reference only |
| page_size | 5051 | documented for reference only |
| backoff_base_ms | 1053 | tunable per environment |
| max_concurrency | 8353 | tunable per environment |
| drain_timeout_s | 8035 | monitored by the owning team |
| max_payload_kb | 5537 | hot-reloaded on change |
| cache_ttl_s | 6806 | hot-reloaded on change |
| prefetch_count | 2073 | hot-reloaded on change |
| retry_limit | 2762 | hot-reloaded on change |

## Limits and quotas

- queue depth alert threshold: 3836
- concurrent worker ceiling: 2176
- soft quota per client: 2148 per hour
- cache lifetime: 2129 seconds
- default page size: 475
- request timeout: 2914 ms
- maximum payload size: 441 KB
- warm-up period after deploy: 3113 seconds

## Monitoring

Historical records for database backup are retained for 26 days and then moved to cold storage by the archival pipeline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Configuration for database backup is loaded at service start and refreshed every 6 minutes. Downstream consumers subscribe to database backup events through the platform event bus rather than polling.

## Rollout

Support escalations touching database backup are triaged by the discovery team within one business day. Localization of user-facing strings in database backup is handled by the shared translation pipeline, not by this component. Downstream consumers subscribe to database backup events through the platform event bus rather than polling. A dry-run mode is available in non-production environments for validating database backup changes before they are applied.

## Troubleshooting

A dry-run mode is available in non-production environments for validating database backup changes before they are applied. Consumers should treat undocumented fields as unstable and subject to change without notice. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 47 minutes.

## Change history

| version | date | change |
|---|---|---|
| 1.8.3 | 2025-06-01 | clarified defaults |
| 2.2.5 | 2023-11-02 | aligned terminology with the style guide |
| 1.2.1 | 2024-01-10 | refreshed examples |
| 2.0.4 | 2025-09-22 | aligned terminology with the style guide |
| 2.1.3 | 2024-03-11 | aligned terminology with the style guide |
| 3.7.2 | 2023-05-28 | documented regional exceptions |
| 2.2.2 | 2023-08-14 | aligned terminology with the style guide |
| 3.1.5 | 2024-07-14 | documented error codes |
| 3.7.6 | 2024-03-03 | tightened wording |
| 1.5.4 | 2023-02-02 | updated escalation contacts |
| 3.7.0 | 2024-12-21 | recorded quota changes |

## FAQ

**Is there a dry-run mode for validating changes in this area?**

Metrics emitted by database backup follow the platform naming scheme and are aggregated at one-minute resolution. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 24 minutes.

**How far back can historical data for this area be retrieved?**

Changes to database backup go through the standard review workflow before release. Identifiers used here follow the corpus-wide conventions in the style guide. Staging environments mirror production settings for database backup except where data-volume limits make that impractical.

**Where are the metrics for this area published?**

Identifiers used here follow the corpus-wide conventions in the style guide. Batch processing for database backup runs on a fixed schedule and drains its queue completely before the next cycle begins. The behavior in this section was last load-tested at 43 times the average production request rate.

**What happens when a request exceeds the documented limits?**

Data written by database backup is idempotent at the record level, so replayed events cannot create duplicates. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Changes to database backup go through the standard review workflow before release.

**How often does the behavior described here change?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 84 minutes. Staging environments mirror production settings for database backup except where data-volume limits make that impractical. Batch processing for database backup runs on a fixed schedule and drains its queue completely before the next cycle begins.

## See also

- [DOC-8794: Capacity Planning](sops/capacity-planning.md)
- [DOC-4056: Preorder Management](product-specs/preorder-management.md)
