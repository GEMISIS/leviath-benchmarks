---
id: DOC-7915
title: Product Reviews
version: 1.7.6
status: active
owner: traffic-eng
---

# DOC-7915: Product Reviews

Batch processing for product reviews runs on a fixed schedule and drains its queue completely before the next cycle begins. The examples in this document use placeholder data and do not reference real customer records. Downstream consumers subscribe to product reviews events through the platform event bus rather than polling.

## Overview

The examples in this document use placeholder data and do not reference real customer records. Configuration for product reviews is loaded at service start and refreshed every 54 minutes. Downstream consumers subscribe to product reviews events through the platform event bus rather than polling. A dry-run mode is available in non-production environments for validating product reviews changes before they are applied.

## Behavior

Changes to product reviews go through the standard review workflow before release. The defaults listed below apply unless overridden per environment. The behavior in this section was last load-tested at 5 times the average production request rate. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Data written by product reviews is idempotent at the record level, so replayed events cannot create duplicates.

## Details

A dry-run mode is available in non-production environments for validating product reviews changes before they are applied. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Historical records for product reviews are retained for 17 days and then moved to cold storage by the archival pipeline. Requests beyond the configured limit receive a structured error response with a stable error code. Support escalations touching product reviews are triaged by the traffic-eng team within one business day. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

This document describes the product reviews area of the Meridian Commerce platform. Staging environments mirror production settings for product reviews except where data-volume limits make that impractical. Data written by product reviews is idempotent at the record level, so replayed events cannot create duplicates. Identifiers used here follow the corpus-wide conventions in the style guide. The examples in this document use placeholder data and do not reference real customer records. Consumers should treat undocumented fields as unstable and subject to change without notice.

Downstream consumers subscribe to product reviews events through the platform event bus rather than polling. Batch processing for product reviews runs on a fixed schedule and drains its queue completely before the next cycle begins. Earlier drafts of this behavior were consolidated here from the team wiki. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Configuration for product reviews is loaded at service start and refreshed every 12 minutes. Rollout is gated on the weekly release train unless an exemption is filed.

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 29 minutes. Every externally visible change to product reviews is announced at least 29 days before it takes effect in production. Consumers should treat undocumented fields as unstable and subject to change without notice. Downstream consumers subscribe to product reviews events through the platform event bus rather than polling. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Staging environments mirror production settings for product reviews except where data-volume limits make that impractical.

Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. This document describes the product reviews area of the Meridian Commerce platform. The behavior in this section was last load-tested at 71 times the average production request rate. Support escalations touching product reviews are triaged by the traffic-eng team within one business day. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Metrics emitted by product reviews follow the platform naming scheme and are aggregated at one-minute resolution.

## Integration

The examples in this document use placeholder data and do not reference real customer records. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Downstream consumers subscribe to product reviews events through the platform event bus rather than polling. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Operational alerts for this area route to the owning team's rotation.

## Operational notes

Requests beyond the configured limit receive a structured error response with a stable error code. Operational alerts for this area route to the owning team's rotation. The defaults listed below apply unless overridden per environment. Historical records for product reviews are retained for 83 days and then moved to cold storage by the archival pipeline. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 46 minutes.

## Defaults

- warm-up period after deploy: 1975 seconds
- queue depth alert threshold: 3854
- burst allowance: 1343 requests
- retry budget: 2084 attempts

## Parameters

| parameter | default | notes |
|---|---|---|
| cache_ttl_s | 5159 | raised during seasonal peaks |
| sample_rate_pct | 1268 | matches the platform default |
| audit_window_days | 5677 | tunable per environment |
| prefetch_count | 5387 | matches the platform default |
| sync_interval_s | 6755 | tunable per environment |
| batch_window_ms | 5098 | documented for reference only |
| warmup_batch | 2353 | tunable per environment |
| flush_interval_s | 4493 | hot-reloaded on change |
| max_payload_kb | 45 | tunable per environment |
| max_concurrency | 3226 | tunable per environment |
| page_size | 7110 | requires restart to change |
| lease_ttl_s | 2647 | documented for reference only |

## Limits and quotas

- request timeout: 3205 ms
- warm-up period after deploy: 3670 seconds
- event replay window: 1855 hours
- burst allowance: 2632 requests
- maximum payload size: 1678 KB
- retry budget: 597 attempts

## Monitoring

Staging environments mirror production settings for product reviews except where data-volume limits make that impractical. Support escalations touching product reviews are triaged by the traffic-eng team within one business day. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 79 minutes. Downstream consumers subscribe to product reviews events through the platform event bus rather than polling.

## Rollout

Identifiers used here follow the corpus-wide conventions in the style guide. The examples in this document use placeholder data and do not reference real customer records. Rollout is gated on the weekly release train unless an exemption is filed. This document describes the product reviews area of the Meridian Commerce platform.

## Troubleshooting

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Historical records for product reviews are retained for 51 days and then moved to cold storage by the archival pipeline. Clients are expected to implement exponential backoff when a retryable error is returned by this area. A dry-run mode is available in non-production environments for validating product reviews changes before they are applied.

## Change history

| version | date | change |
|---|---|---|
| 3.4.2 | 2023-01-04 | clarified defaults |
| 3.7.0 | 2024-11-21 | recorded quota changes |
| 3.1.3 | 2024-06-12 | documented error codes |
| 1.1.6 | 2025-02-28 | tightened wording |
| 2.8.4 | 2025-04-23 | recorded quota changes |
| 2.5.9 | 2024-12-28 | documented error codes |
| 1.2.7 | 2024-01-09 | tightened wording |
| 1.9.5 | 2024-01-10 | tightened wording |

## FAQ

**Who should be contacted when the documented defaults look wrong?**

Support escalations touching product reviews are triaged by the traffic-eng team within one business day. Changes to product reviews go through the standard review workflow before release. Downstream consumers subscribe to product reviews events through the platform event bus rather than polling.

**What happens when a request exceeds the documented limits?**

Downstream consumers subscribe to product reviews events through the platform event bus rather than polling. The behavior in this section was last load-tested at 41 times the average production request rate. Support escalations touching product reviews are triaged by the traffic-eng team within one business day.

**How far back can historical data for this area be retrieved?**

The product reviews behavior is owned by the traffic-eng team and reviewed each quarter. The defaults listed below apply unless overridden per environment. Batch processing for product reviews runs on a fixed schedule and drains its queue completely before the next cycle begins.

**Can the defaults in this document be overridden per environment?**

Staging environments mirror production settings for product reviews except where data-volume limits make that impractical. The product reviews behavior is owned by the traffic-eng team and reviewed each quarter. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list.

**How often does the behavior described here change?**

Rollout is gated on the weekly release train unless an exemption is filed. This document describes the product reviews area of the Meridian Commerce platform. Capacity for product reviews is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

**Where are the metrics for this area published?**

Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. The examples in this document use placeholder data and do not reference real customer records. The product reviews behavior is owned by the traffic-eng team and reviewed each quarter.

## Configuration

```ini
[product-reviews]
endpoint = https://internal.meridian.example/v2/product-reviews
timeout_ms = 1079
api_key = "<REDACTED>"
```

## See also

- [DOC-9070: Split Payments](product-specs/split-payments.md)
- [DOC-9579: Database Failover](sops/database-failover.md)
- [DOC-9195: Price Rules](product-specs/price-rules.md)
