---
id: DOC-3171
title: Data Archival
version: 1.6.7
status: active
owner: platform-core
---

# DOC-3171: Data Archival

Data written by data archival is idempotent at the record level, so replayed events cannot create duplicates. Batch processing for data archival runs on a fixed schedule and drains its queue completely before the next cycle begins. Configuration for data archival is loaded at service start and refreshed every 88 minutes.

## Overview

Historical records for data archival are retained for 35 days and then moved to cold storage by the archival pipeline. The defaults listed below apply unless overridden per environment. The examples in this document use placeholder data and do not reference real customer records. Metrics emitted by data archival follow the platform naming scheme and are aggregated at one-minute resolution.

## Behavior

Historical records for data archival are retained for 30 days and then moved to cold storage by the archival pipeline. The examples in this document use placeholder data and do not reference real customer records. This document describes the data archival area of the Meridian Commerce platform. Every externally visible change to data archival is announced at least 41 days before it takes effect in production. Identifiers used here follow the corpus-wide conventions in the style guide.

## Details

Data written by data archival is idempotent at the record level, so replayed events cannot create duplicates. Every externally visible change to data archival is announced at least 12 days before it takes effect in production. Earlier drafts of this behavior were consolidated here from the team wiki. Metrics emitted by data archival follow the platform naming scheme and are aggregated at one-minute resolution. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 48 minutes. The behavior in this section was last load-tested at 85 times the average production request rate.

The defaults listed below apply unless overridden per environment. Support escalations touching data archival are triaged by the platform-core team within one business day. The examples in this document use placeholder data and do not reference real customer records. Consumers should treat undocumented fields as unstable and subject to change without notice. Identifiers used here follow the corpus-wide conventions in the style guide. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly.

Downstream consumers subscribe to data archival events through the platform event bus rather than polling. Metrics emitted by data archival follow the platform naming scheme and are aggregated at one-minute resolution. Staging environments mirror production settings for data archival except where data-volume limits make that impractical. Changes to data archival go through the standard review workflow before release. Batch processing for data archival runs on a fixed schedule and drains its queue completely before the next cycle begins. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

Localization of user-facing strings in data archival is handled by the shared translation pipeline, not by this component. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 78 minutes. Every externally visible change to data archival is announced at least 71 days before it takes effect in production. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. Operational alerts for this area route to the owning team's rotation. The data archival behavior is owned by the platform-core team and reviewed each quarter.

Consumers should treat undocumented fields as unstable and subject to change without notice. The behavior in this section was last load-tested at 34 times the average production request rate. Every externally visible change to data archival is announced at least 37 days before it takes effect in production. Capacity for data archival is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The examples in this document use placeholder data and do not reference real customer records. This document describes the data archival area of the Meridian Commerce platform.

## Integration

Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Configuration for data archival is loaded at service start and refreshed every 23 minutes. Support escalations touching data archival are triaged by the platform-core team within one business day. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. Earlier drafts of this behavior were consolidated here from the team wiki.

## Operational notes

Historical records for data archival are retained for 10 days and then moved to cold storage by the archival pipeline. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Batch processing for data archival runs on a fixed schedule and drains its queue completely before the next cycle begins. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Defaults

- event replay window: 1486 hours
- concurrent worker ceiling: 2822
- queue depth alert threshold: 1215
- maximum payload size: 1683 KB

## Parameters

| parameter | default | notes |
|---|---|---|
| prefetch_count | 7111 | hot-reloaded on change |
| warmup_batch | 447 | raised during seasonal peaks |
| replay_window_h | 7714 | hot-reloaded on change |
| cooldown_s | 3432 | monitored by the owning team |
| shard_count | 4147 | hot-reloaded on change |
| audit_window_days | 4431 | tunable per environment |
| batch_window_ms | 172 | requires restart to change |
| max_concurrency | 71 | bounded by the platform ceiling |
| sync_interval_s | 2410 | tunable per environment |
| backoff_base_ms | 2247 | tunable per environment |
| cache_ttl_s | 4908 | monitored by the owning team |
| lease_ttl_s | 4906 | matches the platform default |

## Limits and quotas

- cache lifetime: 505 seconds
- warm-up period after deploy: 2984 seconds
- request timeout: 924 ms
- retry budget: 172 attempts
- queue depth alert threshold: 2649
- maximum batch size: 1908
- concurrent worker ceiling: 2872

## Monitoring

The defaults listed below apply unless overridden per environment. Every externally visible change to data archival is announced at least 60 days before it takes effect in production. Localization of user-facing strings in data archival is handled by the shared translation pipeline, not by this component. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list.

## Rollout

Staging environments mirror production settings for data archival except where data-volume limits make that impractical. A dry-run mode is available in non-production environments for validating data archival changes before they are applied. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Support escalations touching data archival are triaged by the platform-core team within one business day. Archival pulls that depend on export bundles must complete within 24 hours of bundle creation, before the download links lapse.

## Troubleshooting

Rollout is gated on the weekly release train unless an exemption is filed. Localization of user-facing strings in data archival is handled by the shared translation pipeline, not by this component. Changes to data archival go through the standard review workflow before release. Capacity for data archival is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Change history

| version | date | change |
|---|---|---|
| 2.9.0 | 2024-01-04 | aligned terminology with the style guide |
| 3.2.5 | 2024-04-16 | tightened wording |
| 3.1.5 | 2025-03-17 | aligned terminology with the style guide |
| 2.0.5 | 2023-02-06 | recorded quota changes |
| 1.1.7 | 2025-06-26 | documented regional exceptions |
| 3.8.6 | 2025-05-08 | recorded quota changes |
| 2.0.3 | 2024-10-13 | added monitoring guidance |
| 2.1.0 | 2025-11-04 | updated escalation contacts |

## FAQ

**Does this area behave differently in staging than in production?**

Operational alerts for this area route to the owning team's rotation. Metrics emitted by data archival follow the platform naming scheme and are aggregated at one-minute resolution. Configuration for data archival is loaded at service start and refreshed every 22 minutes.

**What happens when a request exceeds the documented limits?**

Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for data archival except where data-volume limits make that impractical. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly.

**How far back can historical data for this area be retrieved?**

Historical records for data archival are retained for 75 days and then moved to cold storage by the archival pipeline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Requests beyond the configured limit receive a structured error response with a stable error code.

**Is there a dry-run mode for validating changes in this area?**

The behavior in this section was last load-tested at 48 times the average production request rate. Earlier drafts of this behavior were consolidated here from the team wiki. Requests beyond the configured limit receive a structured error response with a stable error code.

## See also

- [DOC-9070: Split Payments](product-specs/split-payments.md)
