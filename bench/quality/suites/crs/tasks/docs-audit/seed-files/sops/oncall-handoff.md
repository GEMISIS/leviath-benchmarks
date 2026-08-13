---
id: DOC-6887
title: Oncall Handoff
version: 2.6.4
status: active
owner: platform-core
---

# DOC-6887: Oncall Handoff

Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Rollout is gated on the weekly release train unless an exemption is filed. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list.

## Overview

Batch processing for oncall handoff runs on a fixed schedule and drains its queue completely before the next cycle begins. Consumers should treat undocumented fields as unstable and subject to change without notice. The examples in this document use placeholder data and do not reference real customer records. Metrics emitted by oncall handoff follow the platform naming scheme and are aggregated at one-minute resolution.

## Behavior

Earlier drafts of this behavior were consolidated here from the team wiki. A dry-run mode is available in non-production environments for validating oncall handoff changes before they are applied. Rollout is gated on the weekly release train unless an exemption is filed. Identifiers used here follow the corpus-wide conventions in the style guide. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list.

## Details

Consumers should treat undocumented fields as unstable and subject to change without notice. Batch processing for oncall handoff runs on a fixed schedule and drains its queue completely before the next cycle begins. Identifiers used here follow the corpus-wide conventions in the style guide. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 28 minutes. A dry-run mode is available in non-production environments for validating oncall handoff changes before they are applied. Historical records for oncall handoff are retained for 75 days and then moved to cold storage by the archival pipeline.

The examples in this document use placeholder data and do not reference real customer records. Staging environments mirror production settings for oncall handoff except where data-volume limits make that impractical. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Consumers should treat undocumented fields as unstable and subject to change without notice. Localization of user-facing strings in oncall handoff is handled by the shared translation pipeline, not by this component. Metrics emitted by oncall handoff follow the platform naming scheme and are aggregated at one-minute resolution.

Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Staging environments mirror production settings for oncall handoff except where data-volume limits make that impractical. Data written by oncall handoff is idempotent at the record level, so replayed events cannot create duplicates. Operational alerts for this area route to the owning team's rotation. Historical records for oncall handoff are retained for 34 days and then moved to cold storage by the archival pipeline. Localization of user-facing strings in oncall handoff is handled by the shared translation pipeline, not by this component.

Batch processing for oncall handoff runs on a fixed schedule and drains its queue completely before the next cycle begins. Support escalations touching oncall handoff are triaged by the platform-core team within one business day. Consumers should treat undocumented fields as unstable and subject to change without notice. Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

Staging environments mirror production settings for oncall handoff except where data-volume limits make that impractical. Rollout is gated on the weekly release train unless an exemption is filed. Localization of user-facing strings in oncall handoff is handled by the shared translation pipeline, not by this component. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. A dry-run mode is available in non-production environments for validating oncall handoff changes before they are applied. Identifiers used here follow the corpus-wide conventions in the style guide.

## Integration

Historical records for oncall handoff are retained for 68 days and then moved to cold storage by the archival pipeline. The examples in this document use placeholder data and do not reference real customer records. Capacity for oncall handoff is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Downstream consumers subscribe to oncall handoff events through the platform event bus rather than polling. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Operational notes

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 37 minutes. This document describes the oncall handoff area of the Meridian Commerce platform. The examples in this document use placeholder data and do not reference real customer records. Every externally visible change to oncall handoff is announced at least 43 days before it takes effect in production.

## Defaults

- cache lifetime: 78 seconds
- queue depth alert threshold: 3982
- event replay window: 3647 hours

## Parameters

| parameter | default | notes |
|---|---|---|
| sample_rate_pct | 1103 | raised during seasonal peaks |
| sync_interval_s | 5507 | requires restart to change |
| replay_window_h | 7656 | matches the platform default |
| shard_count | 835 | monitored by the owning team |
| prefetch_count | 8169 | hot-reloaded on change |
| cooldown_s | 6834 | tunable per environment |
| page_size | 4434 | raised during seasonal peaks |
| backoff_base_ms | 3635 | hot-reloaded on change |
| retry_limit | 6099 | raised during seasonal peaks |
| drain_timeout_s | 4361 | monitored by the owning team |

## Limits and quotas

- default page size: 19
- retry budget: 1174 attempts
- burst allowance: 2754 requests
- request timeout: 3990 ms
- cache lifetime: 554 seconds
- queue depth alert threshold: 2425

## Monitoring

This document describes the oncall handoff area of the Meridian Commerce platform. Requests beyond the configured limit receive a structured error response with a stable error code. Capacity for oncall handoff is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Metrics emitted by oncall handoff follow the platform naming scheme and are aggregated at one-minute resolution.

## Rollout

Localization of user-facing strings in oncall handoff is handled by the shared translation pipeline, not by this component. Batch processing for oncall handoff runs on a fixed schedule and drains its queue completely before the next cycle begins. The examples in this document use placeholder data and do not reference real customer records. A dry-run mode is available in non-production environments for validating oncall handoff changes before they are applied.

## Troubleshooting

Configuration for oncall handoff is loaded at service start and refreshed every 86 minutes. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The oncall handoff behavior is owned by the platform-core team and reviewed each quarter. Requests beyond the configured limit receive a structured error response with a stable error code.

## Change history

| version | date | change |
|---|---|---|
| 3.4.8 | 2025-03-15 | recorded quota changes |
| 2.2.9 | 2024-05-05 | expanded rollout notes |
| 2.4.1 | 2025-07-03 | aligned terminology with the style guide |
| 3.3.0 | 2023-04-27 | expanded rollout notes |
| 2.0.4 | 2024-07-11 | updated escalation contacts |
| 1.9.5 | 2024-07-07 | added monitoring guidance |
| 2.0.9 | 2025-07-03 | documented regional exceptions |
| 1.1.4 | 2023-04-26 | expanded rollout notes |
| 3.5.2 | 2025-12-19 | documented regional exceptions |
| 1.3.3 | 2025-06-17 | updated escalation contacts |
| 1.4.1 | 2024-12-25 | expanded rollout notes |

## FAQ

**Does this area behave differently in staging than in production?**

Earlier drafts of this behavior were consolidated here from the team wiki. Every externally visible change to oncall handoff is announced at least 44 days before it takes effect in production. Requests beyond the configured limit receive a structured error response with a stable error code.

**Where are the metrics for this area published?**

Every externally visible change to oncall handoff is announced at least 40 days before it takes effect in production. Identifiers used here follow the corpus-wide conventions in the style guide. Metrics emitted by oncall handoff follow the platform naming scheme and are aggregated at one-minute resolution.

**Is there a dry-run mode for validating changes in this area?**

Rollout is gated on the weekly release train unless an exemption is filed. Requests beyond the configured limit receive a structured error response with a stable error code. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list.

**How often does the behavior described here change?**

This document describes the oncall handoff area of the Meridian Commerce platform. The examples in this document use placeholder data and do not reference real customer records. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 32 minutes.

**What happens when a request exceeds the documented limits?**

Changes to oncall handoff go through the standard review workflow before release. A dry-run mode is available in non-production environments for validating oncall handoff changes before they are applied. The defaults listed below apply unless overridden per environment.

**Who should be contacted when the documented defaults look wrong?**

The behavior in this section was last load-tested at 25 times the average production request rate. Rollout is gated on the weekly release train unless an exemption is filed. Changes to oncall handoff go through the standard review workflow before release.

## See also

- [DOC-4803: Batch Job Recovery](sops/batch-job-recovery.md)
