---
id: DOC-9622
title: Fulfillment Routing
version: 1.1.7
status: active
owner: payments-platform
---

# DOC-9622: Fulfillment Routing

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Downstream consumers subscribe to fulfillment routing events through the platform event bus rather than polling. A dry-run mode is available in non-production environments for validating fulfillment routing changes before they are applied.

## Overview

Historical records for fulfillment routing are retained for 58 days and then moved to cold storage by the archival pipeline. The fulfillment routing behavior is owned by the payments-platform team and reviewed each quarter. The behavior in this section was last load-tested at 85 times the average production request rate. The defaults listed below apply unless overridden per environment.

## Behavior

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 67 minutes. Downstream consumers subscribe to fulfillment routing events through the platform event bus rather than polling. Operational alerts for this area route to the owning team's rotation. Batch processing for fulfillment routing runs on a fixed schedule and drains its queue completely before the next cycle begins. Data written by fulfillment routing is idempotent at the record level, so replayed events cannot create duplicates.

## Details

The behavior in this section was last load-tested at 80 times the average production request rate. Rollout is gated on the weekly release train unless an exemption is filed. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Downstream consumers subscribe to fulfillment routing events through the platform event bus rather than polling. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

This document describes the fulfillment routing area of the Meridian Commerce platform. Earlier drafts of this behavior were consolidated here from the team wiki. Batch processing for fulfillment routing runs on a fixed schedule and drains its queue completely before the next cycle begins. Every externally visible change to fulfillment routing is announced at least 44 days before it takes effect in production. A dry-run mode is available in non-production environments for validating fulfillment routing changes before they are applied. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

Staging environments mirror production settings for fulfillment routing except where data-volume limits make that impractical. The examples in this document use placeholder data and do not reference real customer records. A dry-run mode is available in non-production environments for validating fulfillment routing changes before they are applied. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The behavior in this section was last load-tested at 13 times the average production request rate. Rollout is gated on the weekly release train unless an exemption is filed.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Batch processing for fulfillment routing runs on a fixed schedule and drains its queue completely before the next cycle begins. The examples in this document use placeholder data and do not reference real customer records. Configuration for fulfillment routing is loaded at service start and refreshed every 58 minutes. This document describes the fulfillment routing area of the Meridian Commerce platform. Downstream consumers subscribe to fulfillment routing events through the platform event bus rather than polling.

Localization of user-facing strings in fulfillment routing is handled by the shared translation pipeline, not by this component. Configuration for fulfillment routing is loaded at service start and refreshed every 9 minutes. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 64 minutes. The fulfillment routing behavior is owned by the payments-platform team and reviewed each quarter. Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Integration

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Batch processing for fulfillment routing runs on a fixed schedule and drains its queue completely before the next cycle begins. Changes to fulfillment routing go through the standard review workflow before release. Metrics emitted by fulfillment routing follow the platform naming scheme and are aggregated at one-minute resolution.

## Operational notes

Metrics emitted by fulfillment routing follow the platform naming scheme and are aggregated at one-minute resolution. Rollout is gated on the weekly release train unless an exemption is filed. Localization of user-facing strings in fulfillment routing is handled by the shared translation pipeline, not by this component. Batch processing for fulfillment routing runs on a fixed schedule and drains its queue completely before the next cycle begins. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Defaults

- maximum batch size: 2063
- burst allowance: 2132 requests
- cache lifetime: 510 seconds

## Parameters

| parameter | default | notes |
|---|---|---|
| max_concurrency | 8881 | tunable per environment |
| page_size | 3097 | hot-reloaded on change |
| max_payload_kb | 4171 | monitored by the owning team |
| warmup_batch | 6043 | matches the platform default |
| shard_count | 4629 | requires restart to change |
| sync_interval_s | 2325 | tunable per environment |
| sample_rate_pct | 1843 | hot-reloaded on change |
| prefetch_count | 5798 | raised during seasonal peaks |
| connection_limit | 2082 | monitored by the owning team |
| queue_depth_limit | 6342 | bounded by the platform ceiling |
| flush_interval_s | 3249 | tunable per environment |
| retry_limit | 6270 | hot-reloaded on change |

## Limits and quotas

- maximum payload size: 3320 KB
- default page size: 1695
- burst allowance: 422 requests
- maximum batch size: 1668
- concurrent worker ceiling: 3217
- event replay window: 2797 hours
- warm-up period after deploy: 2154 seconds
- request timeout: 500 ms

## Monitoring

Downstream consumers subscribe to fulfillment routing events through the platform event bus rather than polling. Operational alerts for this area route to the owning team's rotation. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Capacity for fulfillment routing is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Rollout

Metrics emitted by fulfillment routing follow the platform naming scheme and are aggregated at one-minute resolution. Localization of user-facing strings in fulfillment routing is handled by the shared translation pipeline, not by this component. Data written by fulfillment routing is idempotent at the record level, so replayed events cannot create duplicates. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 13 minutes.

## Troubleshooting

Rollout is gated on the weekly release train unless an exemption is filed. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Data written by fulfillment routing is idempotent at the record level, so replayed events cannot create duplicates. Staging environments mirror production settings for fulfillment routing except where data-volume limits make that impractical.

## Change history

| version | date | change |
|---|---|---|
| 2.5.8 | 2024-01-09 | documented regional exceptions |
| 3.7.9 | 2023-04-01 | added monitoring guidance |
| 2.6.3 | 2025-06-07 | documented error codes |
| 1.4.1 | 2024-11-09 | recorded quota changes |
| 1.5.5 | 2024-06-23 | recorded quota changes |
| 1.0.7 | 2023-04-28 | recorded quota changes |
| 2.9.3 | 2025-09-07 | tightened wording |
| 1.2.9 | 2023-07-07 | clarified defaults |

## FAQ

**How far back can historical data for this area be retrieved?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 39 minutes. Configuration for fulfillment routing is loaded at service start and refreshed every 82 minutes. Identifiers used here follow the corpus-wide conventions in the style guide.

**Does this area behave differently in staging than in production?**

The defaults listed below apply unless overridden per environment. Configuration for fulfillment routing is loaded at service start and refreshed every 27 minutes. Earlier drafts of this behavior were consolidated here from the team wiki.

**What happens when a request exceeds the documented limits?**

Downstream consumers subscribe to fulfillment routing events through the platform event bus rather than polling. Metrics emitted by fulfillment routing follow the platform naming scheme and are aggregated at one-minute resolution. Staging environments mirror production settings for fulfillment routing except where data-volume limits make that impractical.

**How often does the behavior described here change?**

Support escalations touching fulfillment routing are triaged by the payments-platform team within one business day. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Rollout is gated on the weekly release train unless an exemption is filed.

**Who should be contacted when the documented defaults look wrong?**

Operational alerts for this area route to the owning team's rotation. The defaults listed below apply unless overridden per environment. Identifiers used here follow the corpus-wide conventions in the style guide.

**Where are the metrics for this area published?**

The examples in this document use placeholder data and do not reference real customer records. Downstream consumers subscribe to fulfillment routing events through the platform event bus rather than polling. Batch processing for fulfillment routing runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Configuration

```ini
[fulfillment-routing]
endpoint = https://internal.meridian.example/v2/fulfillment-routing
timeout_ms = 4344
api_key = "<REDACTED>"
```

## See also

- [DOC-5594: Fleet Patching](sops/fleet-patching.md)
- [DOC-5284: Address Book](product-specs/address-book.md)
