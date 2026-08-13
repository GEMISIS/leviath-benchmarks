---
id: DOC-7761
title: Idempotency Keys
version: 3.3.8
status: active
owner: payments-platform
---

# DOC-7761: Idempotency Keys

Configuration for idempotency keys is loaded at service start and refreshed every 33 minutes. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Earlier drafts of this behavior were consolidated here from the team wiki.

## Overview

Rollout is gated on the weekly release train unless an exemption is filed. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The idempotency keys behavior is owned by the payments-platform team and reviewed each quarter. Downstream consumers subscribe to idempotency keys events through the platform event bus rather than polling.

## Behavior

The idempotency keys behavior is owned by the payments-platform team and reviewed each quarter. This document describes the idempotency keys area of the Meridian Commerce platform. Operational alerts for this area route to the owning team's rotation. Data written by idempotency keys is idempotent at the record level, so replayed events cannot create duplicates. Localization of user-facing strings in idempotency keys is handled by the shared translation pipeline, not by this component.

## Details

The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Changes to idempotency keys go through the standard review workflow before release. Every externally visible change to idempotency keys is announced at least 82 days before it takes effect in production. Consumers should treat undocumented fields as unstable and subject to change without notice. Staging environments mirror production settings for idempotency keys except where data-volume limits make that impractical. Localization of user-facing strings in idempotency keys is handled by the shared translation pipeline, not by this component.

Downstream consumers subscribe to idempotency keys events through the platform event bus rather than polling. Rollout is gated on the weekly release train unless an exemption is filed. Localization of user-facing strings in idempotency keys is handled by the shared translation pipeline, not by this component. The examples in this document use placeholder data and do not reference real customer records. Support escalations touching idempotency keys are triaged by the payments-platform team within one business day. Consumers should treat undocumented fields as unstable and subject to change without notice.

Capacity for idempotency keys is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Operational alerts for this area route to the owning team's rotation. Metrics emitted by idempotency keys follow the platform naming scheme and are aggregated at one-minute resolution. Consumers should treat undocumented fields as unstable and subject to change without notice. Historical records for idempotency keys are retained for 27 days and then moved to cold storage by the archival pipeline. Requests beyond the configured limit receive a structured error response with a stable error code.

Support escalations touching idempotency keys are triaged by the payments-platform team within one business day. Data written by idempotency keys is idempotent at the record level, so replayed events cannot create duplicates. Rollout is gated on the weekly release train unless an exemption is filed. Historical records for idempotency keys are retained for 50 days and then moved to cold storage by the archival pipeline. Configuration for idempotency keys is loaded at service start and refreshed every 39 minutes. Changes to idempotency keys go through the standard review workflow before release.

Localization of user-facing strings in idempotency keys is handled by the shared translation pipeline, not by this component. Support escalations touching idempotency keys are triaged by the payments-platform team within one business day. Rollout is gated on the weekly release train unless an exemption is filed. Staging environments mirror production settings for idempotency keys except where data-volume limits make that impractical. Downstream consumers subscribe to idempotency keys events through the platform event bus rather than polling. Metrics emitted by idempotency keys follow the platform naming scheme and are aggregated at one-minute resolution.

## Integration

A dry-run mode is available in non-production environments for validating idempotency keys changes before they are applied. Downstream consumers subscribe to idempotency keys events through the platform event bus rather than polling. The defaults listed below apply unless overridden per environment. Changes to idempotency keys go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki. An idempotency key is honored for 72 hours from first use; the same key presented later starts a fresh operation.

## Operational notes

Configuration for idempotency keys is loaded at service start and refreshed every 78 minutes. Historical records for idempotency keys are retained for 8 days and then moved to cold storage by the archival pipeline. Rollout is gated on the weekly release train unless an exemption is filed. A dry-run mode is available in non-production environments for validating idempotency keys changes before they are applied. Earlier drafts of this behavior were consolidated here from the team wiki.

## Defaults

- queue depth alert threshold: 418
- burst allowance: 2026 requests
- cache lifetime: 2221 seconds
- concurrent worker ceiling: 162

## Parameters

| parameter | default | notes |
|---|---|---|
| cooldown_s | 858 | documented for reference only |
| sync_interval_s | 493 | requires restart to change |
| drain_timeout_s | 5698 | hot-reloaded on change |
| prefetch_count | 4872 | documented for reference only |
| replay_window_h | 6646 | tunable per environment |
| backoff_base_ms | 2575 | raised during seasonal peaks |
| max_payload_kb | 7635 | bounded by the platform ceiling |
| max_concurrency | 7384 | bounded by the platform ceiling |
| sample_rate_pct | 2800 | raised during seasonal peaks |
| retry_limit | 8394 | matches the platform default |
| shard_count | 4130 | hot-reloaded on change |

## Limits and quotas

- cache lifetime: 296 seconds
- retry budget: 3028 attempts
- request timeout: 1407 ms
- concurrent worker ceiling: 2808
- warm-up period after deploy: 2350 seconds
- maximum payload size: 2489 KB

## Monitoring

The examples in this document use placeholder data and do not reference real customer records. Localization of user-facing strings in idempotency keys is handled by the shared translation pipeline, not by this component. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Rollout

Metrics emitted by idempotency keys follow the platform naming scheme and are aggregated at one-minute resolution. The behavior in this section was last load-tested at 48 times the average production request rate. Identifiers used here follow the corpus-wide conventions in the style guide. Operational alerts for this area route to the owning team's rotation.

## Troubleshooting

Changes to idempotency keys go through the standard review workflow before release. Localization of user-facing strings in idempotency keys is handled by the shared translation pipeline, not by this component. The idempotency keys behavior is owned by the payments-platform team and reviewed each quarter. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Change history

| version | date | change |
|---|---|---|
| 3.9.6 | 2024-11-06 | documented regional exceptions |
| 2.2.1 | 2023-07-14 | added monitoring guidance |
| 2.3.1 | 2025-03-23 | tightened wording |
| 2.9.9 | 2023-04-28 | aligned terminology with the style guide |
| 1.7.9 | 2025-02-27 | aligned terminology with the style guide |
| 1.1.0 | 2024-10-23 | aligned terminology with the style guide |
| 1.0.2 | 2024-03-01 | clarified defaults |

## FAQ

**Where are the metrics for this area published?**

Changes to idempotency keys go through the standard review workflow before release. The examples in this document use placeholder data and do not reference real customer records. Downstream consumers subscribe to idempotency keys events through the platform event bus rather than polling.

**Who should be contacted when the documented defaults look wrong?**

Configuration for idempotency keys is loaded at service start and refreshed every 53 minutes. Capacity for idempotency keys is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Rollout is gated on the weekly release train unless an exemption is filed.

**How often does the behavior described here change?**

The behavior in this section was last load-tested at 27 times the average production request rate. A dry-run mode is available in non-production environments for validating idempotency keys changes before they are applied. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

**What happens when a request exceeds the documented limits?**

Support escalations touching idempotency keys are triaged by the payments-platform team within one business day. Configuration for idempotency keys is loaded at service start and refreshed every 33 minutes. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly.

**Is there a dry-run mode for validating changes in this area?**

Historical records for idempotency keys are retained for 25 days and then moved to cold storage by the archival pipeline. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. Requests beyond the configured limit receive a structured error response with a stable error code.

**Does this area behave differently in staging than in production?**

Operational alerts for this area route to the owning team's rotation. Localization of user-facing strings in idempotency keys is handled by the shared translation pipeline, not by this component. Earlier drafts of this behavior were consolidated here from the team wiki.

## Configuration

```ini
[idempotency-keys]
endpoint = https://internal.meridian.example/v2/idempotency-keys
timeout_ms = 2707
api_key = "<REDACTED>"
```

## See also

- [DOC-4877: Gift Cards](product-specs/gift-cards.md)
