---
id: DOC-6887
title: Oncall Handoff
version: 2.6.4
status: active
owner: platform-core
---

# DOC-6887: Oncall Handoff

Support escalations touching oncall handoff are triaged by the platform-core team within one business day. Capacity for oncall handoff is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Requests beyond the configured limit receive a structured error response with a stable error code.

## Overview

Changes to oncall handoff go through the standard review workflow before release. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. Identifiers used here follow the corpus-wide conventions in the style guide. Batch processing for oncall handoff runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Behavior

The examples in this document use placeholder data and do not reference real customer records. Changes to oncall handoff go through the standard review workflow before release. Support escalations touching oncall handoff are triaged by the platform-core team within one business day. Historical records for oncall handoff are retained for 56 days and then moved to cold storage by the archival pipeline. Earlier drafts of this behavior were consolidated here from the team wiki.

## Details

Rollout is gated on the weekly release train unless an exemption is filed. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. Downstream consumers subscribe to oncall handoff events through the platform event bus rather than polling. Configuration for oncall handoff is loaded at service start and refreshed every 78 minutes. Identifiers used here follow the corpus-wide conventions in the style guide. Consumers should treat undocumented fields as unstable and subject to change without notice.

Consumers should treat undocumented fields as unstable and subject to change without notice. Identifiers used here follow the corpus-wide conventions in the style guide. Localization of user-facing strings in oncall handoff is handled by the shared translation pipeline, not by this component. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Staging environments mirror production settings for oncall handoff except where data-volume limits make that impractical.

Configuration for oncall handoff is loaded at service start and refreshed every 31 minutes. This document describes the oncall handoff area of the Meridian Commerce platform. Localization of user-facing strings in oncall handoff is handled by the shared translation pipeline, not by this component. Batch processing for oncall handoff runs on a fixed schedule and drains its queue completely before the next cycle begins. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Staging environments mirror production settings for oncall handoff except where data-volume limits make that impractical.

The defaults listed below apply unless overridden per environment. Batch processing for oncall handoff runs on a fixed schedule and drains its queue completely before the next cycle begins. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 66 minutes. Support escalations touching oncall handoff are triaged by the platform-core team within one business day. Consumers should treat undocumented fields as unstable and subject to change without notice. Operational alerts for this area route to the owning team's rotation.

Configuration for oncall handoff is loaded at service start and refreshed every 48 minutes. Support escalations touching oncall handoff are triaged by the platform-core team within one business day. Data written by oncall handoff is idempotent at the record level, so replayed events cannot create duplicates. Batch processing for oncall handoff runs on a fixed schedule and drains its queue completely before the next cycle begins. Staging environments mirror production settings for oncall handoff except where data-volume limits make that impractical. Rollout is gated on the weekly release train unless an exemption is filed.

## Integration

This document describes the oncall handoff area of the Meridian Commerce platform. Changes to oncall handoff go through the standard review workflow before release. Historical records for oncall handoff are retained for 37 days and then moved to cold storage by the archival pipeline. The examples in this document use placeholder data and do not reference real customer records. Capacity for oncall handoff is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Operational notes

This document describes the oncall handoff area of the Meridian Commerce platform. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 19 minutes. The examples in this document use placeholder data and do not reference real customer records. Every externally visible change to oncall handoff is announced at least 43 days before it takes effect in production.

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

## Configuration

```ini
[oncall-handoff]
endpoint = https://internal.meridian.example/v2/oncall-handoff
timeout_ms = 4249
api_key = "<REDACTED>"
api_key = "sk_live_bcfbb90dcd93"
```

## See also

- [DOC-4605: Dependency Upgrades](sops/dependency-upgrades.md)
- [DOC-1542: Batch Operations](api/batch-operations.md)
- [DOC-8582: Abandoned Cart Recovery](product-specs/abandoned-cart-recovery.md)
