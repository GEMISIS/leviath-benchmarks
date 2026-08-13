---
id: DOC-4867
title: Fraud Screening
version: 2.1
status: deprecated
superseded_by: product-specs/fraud-screening-next.md
owner: traffic-eng
---

# DOC-4868: Fraud Screening

The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Metrics emitted by fraud screening follow the platform naming scheme and are aggregated at one-minute resolution. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Overview

Requests beyond the configured limit receive a structured error response with a stable error code. The defaults listed below apply unless overridden per environment. Rollout is gated on the weekly release train unless an exemption is filed. Staging environments mirror production settings for fraud screening except where data-volume limits make that impractical.

## Behavior

Staging environments mirror production settings for fraud screening except where data-volume limits make that impractical. Metrics emitted by fraud screening follow the platform naming scheme and are aggregated at one-minute resolution. Every externally visible change to fraud screening is announced at least 44 days before it takes effect in production. The fraud screening behavior is owned by the traffic-eng team and reviewed each quarter. The behavior in this section was last load-tested at 36 times the average production request rate.

## Details

Capacity for fraud screening is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Data written by fraud screening is idempotent at the record level, so replayed events cannot create duplicates. Support escalations touching fraud screening are triaged by the traffic-eng team within one business day. Earlier drafts of this behavior were consolidated here from the team wiki. Staging environments mirror production settings for fraud screening except where data-volume limits make that impractical. Downstream consumers subscribe to fraud screening events through the platform event bus rather than polling.

The fraud screening behavior is owned by the traffic-eng team and reviewed each quarter. Changes to fraud screening go through the standard review workflow before release. The behavior in this section was last load-tested at 51 times the average production request rate. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Batch processing for fraud screening runs on a fixed schedule and drains its queue completely before the next cycle begins. Earlier drafts of this behavior were consolidated here from the team wiki.

Batch processing for fraud screening runs on a fixed schedule and drains its queue completely before the next cycle begins. Capacity for fraud screening is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The behavior in this section was last load-tested at 18 times the average production request rate. Configuration for fraud screening is loaded at service start and refreshed every 9 minutes. Metrics emitted by fraud screening follow the platform naming scheme and are aggregated at one-minute resolution. Localization of user-facing strings in fraud screening is handled by the shared translation pipeline, not by this component.

Staging environments mirror production settings for fraud screening except where data-volume limits make that impractical. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Downstream consumers subscribe to fraud screening events through the platform event bus rather than polling. Requests beyond the configured limit receive a structured error response with a stable error code. Earlier drafts of this behavior were consolidated here from the team wiki. Batch processing for fraud screening runs on a fixed schedule and drains its queue completely before the next cycle begins.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Requests beyond the configured limit receive a structured error response with a stable error code. Rollout is gated on the weekly release train unless an exemption is filed. Capacity for fraud screening is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The behavior in this section was last load-tested at 41 times the average production request rate.

## Integration

The fraud screening behavior is owned by the traffic-eng team and reviewed each quarter. Requests beyond the configured limit receive a structured error response with a stable error code. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Localization of user-facing strings in fraud screening is handled by the shared translation pipeline, not by this component. The defaults listed below apply unless overridden per environment.

## Operational notes

Rollout is gated on the weekly release train unless an exemption is filed. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. The fraud screening behavior is owned by the traffic-eng team and reviewed each quarter. Staging environments mirror production settings for fraud screening except where data-volume limits make that impractical. Operational alerts for this area route to the owning team's rotation.

## Defaults

- burst allowance: 3066 requests
- maximum batch size: 1175
- retry budget: 786 attempts

## Parameters

| parameter | default | notes |
|---|---|---|
| page_size | 3640 | hot-reloaded on change |
| drain_timeout_s | 7580 | raised during seasonal peaks |
| warmup_batch | 3582 | bounded by the platform ceiling |
| retry_limit | 7526 | matches the platform default |
| sync_interval_s | 1877 | documented for reference only |
| backoff_base_ms | 4930 | raised during seasonal peaks |
| shard_count | 3791 | matches the platform default |
| sample_rate_pct | 3109 | monitored by the owning team |
| max_concurrency | 2347 | requires restart to change |
| replay_window_h | 2892 | documented for reference only |

## Limits and quotas

- soft quota per client: 3663 per hour
- request timeout: 2119 ms
- maximum payload size: 2570 KB
- concurrent worker ceiling: 129
- queue depth alert threshold: 1212
- cache lifetime: 86 seconds
- retry budget: 1035 attempts
- default page size: 2276

## Monitoring

Identifiers used here follow the corpus-wide conventions in the style guide. Batch processing for fraud screening runs on a fixed schedule and drains its queue completely before the next cycle begins. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Downstream consumers subscribe to fraud screening events through the platform event bus rather than polling.

## Rollout

The examples in this document use placeholder data and do not reference real customer records. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 24 minutes. The defaults listed below apply unless overridden per environment.

## Troubleshooting

Batch processing for fraud screening runs on a fixed schedule and drains its queue completely before the next cycle begins. A dry-run mode is available in non-production environments for validating fraud screening changes before they are applied. Support escalations touching fraud screening are triaged by the traffic-eng team within one business day. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Change history

| version | date | change |
|---|---|---|
| 3.0.7 | 2023-11-10 | refreshed examples |
| 2.6.9 | 2024-02-13 | recorded quota changes |
| 3.7.6 | 2025-06-18 | documented regional exceptions |
| 2.7.8 | 2024-06-03 | recorded quota changes |
| 2.7.1 | 2025-12-21 | aligned terminology with the style guide |
| 3.5.1 | 2023-06-24 | updated escalation contacts |
| 1.5.2 | 2025-08-24 | documented regional exceptions |
| 2.9.4 | 2025-12-24 | recorded quota changes |

## FAQ

**Who should be contacted when the documented defaults look wrong?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Earlier drafts of this behavior were consolidated here from the team wiki. This document describes the fraud screening area of the Meridian Commerce platform.

**What happens when a request exceeds the documented limits?**

Downstream consumers subscribe to fraud screening events through the platform event bus rather than polling. Configuration for fraud screening is loaded at service start and refreshed every 89 minutes. Data written by fraud screening is idempotent at the record level, so replayed events cannot create duplicates.

**How far back can historical data for this area be retrieved?**

Capacity for fraud screening is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Support escalations touching fraud screening are triaged by the traffic-eng team within one business day.

**How often does the behavior described here change?**

Earlier drafts of this behavior were consolidated here from the team wiki. Metrics emitted by fraud screening follow the platform naming scheme and are aggregated at one-minute resolution. The defaults listed below apply unless overridden per environment.

## Configuration

```ini
[fraud-screening]
endpoint = https://internal.meridian.example/v2/fraud-screening
timeout_ms = 3578
api_key = "<REDACTED>"
```

## See also

- [DOC-1233: Returns Portal](product-specs/returns-portal.md)
- [DOC-3171: Data Archival](sops/data-archival.md)
- [DOC-4315: Wishlist Sharing](product-specs/wishlist-sharing.md)
- [Background notes](api/pagination-rules-v2.md)
- [Background notes](sops/maintenance-windows-v2.md)
