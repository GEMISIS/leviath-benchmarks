---
id: DOC-3601
title: On-Call Handbook
version: 2.9.1
status: active
owner: identity
---

# DOC-3601: On-Call Handbook

Consumers should treat undocumented fields as unstable and subject to change without notice. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. The defaults listed below apply unless overridden per environment.

## Overview

Every externally visible change to on-call handbook is announced at least 50 days before it takes effect in production. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Batch processing for on-call handbook runs on a fixed schedule and drains its queue completely before the next cycle begins. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Behavior

Metrics emitted by on-call handbook follow the platform naming scheme and are aggregated at one-minute resolution. Changes to on-call handbook go through the standard review workflow before release. Operational alerts for this area route to the owning team's rotation. Rollout is gated on the weekly release train unless an exemption is filed. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Details

Configuration for on-call handbook is loaded at service start and refreshed every 42 minutes. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Changes to on-call handbook go through the standard review workflow before release. Metrics emitted by on-call handbook follow the platform naming scheme and are aggregated at one-minute resolution. Downstream consumers subscribe to on-call handbook events through the platform event bus rather than polling. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

Data written by on-call handbook is idempotent at the record level, so replayed events cannot create duplicates. Operational alerts for this area route to the owning team's rotation. Metrics emitted by on-call handbook follow the platform naming scheme and are aggregated at one-minute resolution. Configuration for on-call handbook is loaded at service start and refreshed every 8 minutes. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Changes to on-call handbook go through the standard review workflow before release.

Metrics emitted by on-call handbook follow the platform naming scheme and are aggregated at one-minute resolution. Localization of user-facing strings in on-call handbook is handled by the shared translation pipeline, not by this component. Rollout is gated on the weekly release train unless an exemption is filed. A dry-run mode is available in non-production environments for validating on-call handbook changes before they are applied. The examples in this document use placeholder data and do not reference real customer records. The defaults listed below apply unless overridden per environment.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Historical records for on-call handbook are retained for 21 days and then moved to cold storage by the archival pipeline. The defaults listed below apply unless overridden per environment. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Rollout is gated on the weekly release train unless an exemption is filed. Capacity for on-call handbook is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

Batch processing for on-call handbook runs on a fixed schedule and drains its queue completely before the next cycle begins. The on-call handbook behavior is owned by the identity team and reviewed each quarter. Rollout is gated on the weekly release train unless an exemption is filed. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 77 minutes. Staging environments mirror production settings for on-call handbook except where data-volume limits make that impractical. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Integration

Rollout is gated on the weekly release train unless an exemption is filed. Metrics emitted by on-call handbook follow the platform naming scheme and are aggregated at one-minute resolution. The on-call handbook behavior is owned by the identity team and reviewed each quarter. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Operational notes

Data written by on-call handbook is idempotent at the record level, so replayed events cannot create duplicates. Every externally visible change to on-call handbook is announced at least 82 days before it takes effect in production. Identifiers used here follow the corpus-wide conventions in the style guide. The examples in this document use placeholder data and do not reference real customer records. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Defaults

- concurrent worker ceiling: 686
- burst allowance: 2699 requests
- default page size: 1548
- queue depth alert threshold: 2162

## Parameters

| parameter | default | notes |
|---|---|---|
| max_concurrency | 5603 | tunable per environment |
| queue_depth_limit | 2641 | raised during seasonal peaks |
| connection_limit | 8222 | raised during seasonal peaks |
| prefetch_count | 2558 | raised during seasonal peaks |
| shard_count | 5217 | hot-reloaded on change |
| audit_window_days | 5075 | hot-reloaded on change |
| cooldown_s | 363 | monitored by the owning team |
| sync_interval_s | 891 | requires restart to change |
| retry_limit | 2379 | raised during seasonal peaks |
| batch_window_ms | 3490 | raised during seasonal peaks |

## Limits and quotas

- maximum batch size: 2048
- maximum payload size: 3285 KB
- default page size: 440
- concurrent worker ceiling: 1572
- queue depth alert threshold: 1632
- request timeout: 2114 ms
- cache lifetime: 1630 seconds
- event replay window: 2269 hours

## Monitoring

The examples in this document use placeholder data and do not reference real customer records. Data written by on-call handbook is idempotent at the record level, so replayed events cannot create duplicates. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Localization of user-facing strings in on-call handbook is handled by the shared translation pipeline, not by this component.

## Rollout

Data written by on-call handbook is idempotent at the record level, so replayed events cannot create duplicates. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Batch processing for on-call handbook runs on a fixed schedule and drains its queue completely before the next cycle begins. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Troubleshooting

Identifiers used here follow the corpus-wide conventions in the style guide. Data written by on-call handbook is idempotent at the record level, so replayed events cannot create duplicates. Earlier drafts of this behavior were consolidated here from the team wiki. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Change history

| version | date | change |
|---|---|---|
| 2.0.2 | 2023-12-06 | aligned terminology with the style guide |
| 1.5.3 | 2024-06-04 | documented error codes |
| 2.8.6 | 2025-11-24 | recorded quota changes |
| 3.1.1 | 2023-05-05 | aligned terminology with the style guide |
| 2.1.5 | 2025-12-17 | clarified defaults |
| 1.9.9 | 2025-07-14 | documented regional exceptions |
| 1.6.8 | 2025-04-01 | clarified defaults |

## FAQ

**How far back can historical data for this area be retrieved?**

Identifiers used here follow the corpus-wide conventions in the style guide. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Consumers should treat undocumented fields as unstable and subject to change without notice.

**What happens when a request exceeds the documented limits?**

Downstream consumers subscribe to on-call handbook events through the platform event bus rather than polling. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Data written by on-call handbook is idempotent at the record level, so replayed events cannot create duplicates.

**Is there a dry-run mode for validating changes in this area?**

This document describes the on-call handbook area of the Meridian Commerce platform. Metrics emitted by on-call handbook follow the platform naming scheme and are aggregated at one-minute resolution. Data written by on-call handbook is idempotent at the record level, so replayed events cannot create duplicates.

**Does this area behave differently in staging than in production?**

Identifiers used here follow the corpus-wide conventions in the style guide. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. This document describes the on-call handbook area of the Meridian Commerce platform.

**Can the defaults in this document be overridden per environment?**

Localization of user-facing strings in on-call handbook is handled by the shared translation pipeline, not by this component. Identifiers used here follow the corpus-wide conventions in the style guide. Changes to on-call handbook go through the standard review workflow before release.

**Where are the metrics for this area published?**

Localization of user-facing strings in on-call handbook is handled by the shared translation pipeline, not by this component. Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for on-call handbook is loaded at service start and refreshed every 67 minutes.

## Configuration

```ini
[on-call-handbook]
endpoint = https://internal.meridian.example/v2/on-call-handbook
timeout_ms = 3326
api_key = "<REDACTED>"
```

## See also

- [DOC-9195: Price Rules](product-specs/price-rules.md)
- [DOC-6349: Coupons Endpoint](api/coupons-endpoint.md)
