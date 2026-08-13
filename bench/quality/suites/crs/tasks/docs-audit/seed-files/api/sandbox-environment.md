---
id: DOC-3997
title: Sandbox Environment
version: 2.4.4
status: active
owner: storefront
---

# DOC-3997: Sandbox Environment

Metrics emitted by sandbox environment follow the platform naming scheme and are aggregated at one-minute resolution. Localization of user-facing strings in sandbox environment is handled by the shared translation pipeline, not by this component. Operational alerts for this area route to the owning team's rotation.

## Overview

Requests beyond the configured limit receive a structured error response with a stable error code. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Identifiers used here follow the corpus-wide conventions in the style guide. This document describes the sandbox environment area of the Meridian Commerce platform.

## Behavior

Every externally visible change to sandbox environment is announced at least 51 days before it takes effect in production. Operational alerts for this area route to the owning team's rotation. This document describes the sandbox environment area of the Meridian Commerce platform. Data written by sandbox environment is idempotent at the record level, so replayed events cannot create duplicates. Localization of user-facing strings in sandbox environment is handled by the shared translation pipeline, not by this component.

## Details

Staging environments mirror production settings for sandbox environment except where data-volume limits make that impractical. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The defaults listed below apply unless overridden per environment. Earlier drafts of this behavior were consolidated here from the team wiki. Downstream consumers subscribe to sandbox environment events through the platform event bus rather than polling. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. This document describes the sandbox environment area of the Meridian Commerce platform. Localization of user-facing strings in sandbox environment is handled by the shared translation pipeline, not by this component. The behavior in this section was last load-tested at 17 times the average production request rate. A dry-run mode is available in non-production environments for validating sandbox environment changes before they are applied. Metrics emitted by sandbox environment follow the platform naming scheme and are aggregated at one-minute resolution.

Identifiers used here follow the corpus-wide conventions in the style guide. The defaults listed below apply unless overridden per environment. Capacity for sandbox environment is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Consumers should treat undocumented fields as unstable and subject to change without notice. The behavior in this section was last load-tested at 58 times the average production request rate. Every externally visible change to sandbox environment is announced at least 26 days before it takes effect in production.

Rollout is gated on the weekly release train unless an exemption is filed. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Consumers should treat undocumented fields as unstable and subject to change without notice. A dry-run mode is available in non-production environments for validating sandbox environment changes before they are applied. Every externally visible change to sandbox environment is announced at least 15 days before it takes effect in production. This document describes the sandbox environment area of the Meridian Commerce platform.

The sandbox environment behavior is owned by the storefront team and reviewed each quarter. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Earlier drafts of this behavior were consolidated here from the team wiki. Requests beyond the configured limit receive a structured error response with a stable error code. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Changes to sandbox environment go through the standard review workflow before release.

## Integration

Operational alerts for this area route to the owning team's rotation. Batch processing for sandbox environment runs on a fixed schedule and drains its queue completely before the next cycle begins. Earlier drafts of this behavior were consolidated here from the team wiki. Downstream consumers subscribe to sandbox environment events through the platform event bus rather than polling. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Operational notes

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Staging environments mirror production settings for sandbox environment except where data-volume limits make that impractical. Configuration for sandbox environment is loaded at service start and refreshed every 87 minutes. Data written by sandbox environment is idempotent at the record level, so replayed events cannot create duplicates.

## Defaults

- soft quota per client: 3285 per hour
- cache lifetime: 1934 seconds
- maximum batch size: 847
- burst allowance: 2341 requests

## Parameters

| parameter | default | notes |
|---|---|---|
| retry_limit | 151 | monitored by the owning team |
| max_concurrency | 616 | matches the platform default |
| warmup_batch | 204 | raised during seasonal peaks |
| page_size | 6302 | monitored by the owning team |
| cache_ttl_s | 7041 | hot-reloaded on change |
| audit_window_days | 4810 | monitored by the owning team |
| shard_count | 6400 | monitored by the owning team |
| sample_rate_pct | 7516 | tunable per environment |
| sync_interval_s | 4184 | tunable per environment |
| connection_limit | 5895 | monitored by the owning team |
| max_payload_kb | 6723 | monitored by the owning team |
| replay_window_h | 3367 | raised during seasonal peaks |
| flush_interval_s | 8891 | matches the platform default |
| queue_depth_limit | 8255 | requires restart to change |

## Limits and quotas

- maximum batch size: 1551
- event replay window: 2248 hours
- queue depth alert threshold: 745
- request timeout: 198 ms
- maximum payload size: 2982 KB
- soft quota per client: 1780 per hour
- retry budget: 720 attempts

## Monitoring

Historical records for sandbox environment are retained for 22 days and then moved to cold storage by the archival pipeline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Data written by sandbox environment is idempotent at the record level, so replayed events cannot create duplicates. The defaults listed below apply unless overridden per environment. The sandbox is wiped and reseeded on a fixed 14-day calendar cycle.

## Rollout

Support escalations touching sandbox environment are triaged by the storefront team within one business day. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Operational alerts for this area route to the owning team's rotation.

## Troubleshooting

Rollout is gated on the weekly release train unless an exemption is filed. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Historical records for sandbox environment are retained for 17 days and then moved to cold storage by the archival pipeline.

## Change history

| version | date | change |
|---|---|---|
| 2.0.8 | 2024-01-25 | updated escalation contacts |
| 1.3.3 | 2024-03-13 | documented error codes |
| 2.1.3 | 2023-02-26 | aligned terminology with the style guide |
| 1.0.7 | 2025-08-20 | tightened wording |
| 2.8.7 | 2023-12-10 | tightened wording |
| 3.3.4 | 2024-03-19 | documented error codes |
| 1.9.0 | 2025-11-09 | documented error codes |
| 3.8.3 | 2025-12-14 | recorded quota changes |

## FAQ

**Is there a dry-run mode for validating changes in this area?**

Metrics emitted by sandbox environment follow the platform naming scheme and are aggregated at one-minute resolution. The examples in this document use placeholder data and do not reference real customer records. Every externally visible change to sandbox environment is announced at least 17 days before it takes effect in production.

**Can the defaults in this document be overridden per environment?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Localization of user-facing strings in sandbox environment is handled by the shared translation pipeline, not by this component. Data written by sandbox environment is idempotent at the record level, so replayed events cannot create duplicates.

**Who should be contacted when the documented defaults look wrong?**

Localization of user-facing strings in sandbox environment is handled by the shared translation pipeline, not by this component. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 37 minutes. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list.

**Where are the metrics for this area published?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. The defaults listed below apply unless overridden per environment.

## See also

- [DOC-4102: Staging Refresh](sops/staging-refresh.md)
