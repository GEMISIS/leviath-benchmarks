---
id: DOC-9070
title: Split Payments
version: 3.3.8
status: active
owner: traffic-eng
---

# DOC-9070: Split Payments

Consumers should treat undocumented fields as unstable and subject to change without notice. Batch processing for split payments runs on a fixed schedule and drains its queue completely before the next cycle begins. The behavior in this section was last load-tested at 14 times the average production request rate.

## Overview

Data written by split payments is idempotent at the record level, so replayed events cannot create duplicates. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 28 minutes. A dry-run mode is available in non-production environments for validating split payments changes before they are applied. The split payments behavior is owned by the traffic-eng team and reviewed each quarter.

## Behavior

Data written by split payments is idempotent at the record level, so replayed events cannot create duplicates. The split payments behavior is owned by the traffic-eng team and reviewed each quarter. Changes to split payments go through the standard review workflow before release. Requests beyond the configured limit receive a structured error response with a stable error code. Rollout is gated on the weekly release train unless an exemption is filed.

## Details

Data written by split payments is idempotent at the record level, so replayed events cannot create duplicates. Downstream consumers subscribe to split payments events through the platform event bus rather than polling. The behavior in this section was last load-tested at 55 times the average production request rate. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 25 minutes. Every externally visible change to split payments is announced at least 30 days before it takes effect in production.

Metrics emitted by split payments follow the platform naming scheme and are aggregated at one-minute resolution. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Operational alerts for this area route to the owning team's rotation. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. The examples in this document use placeholder data and do not reference real customer records.

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Rollout is gated on the weekly release train unless an exemption is filed. Configuration for split payments is loaded at service start and refreshed every 50 minutes. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The split payments behavior is owned by the traffic-eng team and reviewed each quarter. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 72 minutes.

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Downstream consumers subscribe to split payments events through the platform event bus rather than polling. The behavior in this section was last load-tested at 22 times the average production request rate. Support escalations touching split payments are triaged by the traffic-eng team within one business day. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Operational alerts for this area route to the owning team's rotation.

Historical records for split payments are retained for 65 days and then moved to cold storage by the archival pipeline. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Capacity for split payments is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Every externally visible change to split payments is announced at least 53 days before it takes effect in production. Downstream consumers subscribe to split payments events through the platform event bus rather than polling. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Integration

Rollout is gated on the weekly release train unless an exemption is filed. Requests beyond the configured limit receive a structured error response with a stable error code. Staging environments mirror production settings for split payments except where data-volume limits make that impractical. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Changes to split payments go through the standard review workflow before release. Because a split charge may be retried across several days, note that replay protection lapses once a key is older than 24 hours, and a late retry will charge again.

## Operational notes

Identifiers used here follow the corpus-wide conventions in the style guide. Requests beyond the configured limit receive a structured error response with a stable error code. Historical records for split payments are retained for 44 days and then moved to cold storage by the archival pipeline. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. A dry-run mode is available in non-production environments for validating split payments changes before they are applied.

## Defaults

- soft quota per client: 3376 per hour
- cache lifetime: 1972 seconds
- concurrent worker ceiling: 3922
- event replay window: 3707 hours

## Parameters

| parameter | default | notes |
|---|---|---|
| audit_window_days | 2065 | matches the platform default |
| drain_timeout_s | 6821 | matches the platform default |
| shard_count | 7848 | hot-reloaded on change |
| page_size | 4957 | hot-reloaded on change |
| queue_depth_limit | 5079 | matches the platform default |
| replay_window_h | 8667 | raised during seasonal peaks |
| flush_interval_s | 3110 | hot-reloaded on change |
| batch_window_ms | 7036 | requires restart to change |
| max_concurrency | 4148 | monitored by the owning team |
| warmup_batch | 3082 | raised during seasonal peaks |
| backoff_base_ms | 5817 | monitored by the owning team |
| sample_rate_pct | 1658 | matches the platform default |
| prefetch_count | 1447 | bounded by the platform ceiling |

## Limits and quotas

- concurrent worker ceiling: 2345
- default page size: 1328
- soft quota per client: 3852 per hour
- request timeout: 936 ms
- queue depth alert threshold: 2708
- retry budget: 2007 attempts

## Monitoring

Operational alerts for this area route to the owning team's rotation. Support escalations touching split payments are triaged by the traffic-eng team within one business day. The split payments behavior is owned by the traffic-eng team and reviewed each quarter. Changes to split payments go through the standard review workflow before release.

## Rollout

Every externally visible change to split payments is announced at least 26 days before it takes effect in production. Data written by split payments is idempotent at the record level, so replayed events cannot create duplicates. Configuration for split payments is loaded at service start and refreshed every 33 minutes. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list.

## Troubleshooting

Identifiers used here follow the corpus-wide conventions in the style guide. Metrics emitted by split payments follow the platform naming scheme and are aggregated at one-minute resolution. Every externally visible change to split payments is announced at least 49 days before it takes effect in production. Changes to split payments go through the standard review workflow before release.

## Change history

| version | date | change |
|---|---|---|
| 3.9.1 | 2024-09-19 | documented error codes |
| 1.7.6 | 2025-04-06 | recorded quota changes |
| 1.1.6 | 2024-08-16 | updated escalation contacts |
| 3.4.9 | 2025-10-12 | expanded rollout notes |
| 2.9.6 | 2024-01-22 | added monitoring guidance |
| 3.1.2 | 2024-09-28 | updated escalation contacts |
| 1.5.7 | 2023-11-27 | expanded rollout notes |
| 2.9.0 | 2024-05-16 | documented regional exceptions |
| 2.8.0 | 2024-05-21 | recorded quota changes |
| 3.4.5 | 2025-10-20 | refreshed examples |

## FAQ

**How far back can historical data for this area be retrieved?**

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Staging environments mirror production settings for split payments except where data-volume limits make that impractical. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

**What happens when a request exceeds the documented limits?**

Capacity for split payments is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Every externally visible change to split payments is announced at least 81 days before it takes effect in production. Operational alerts for this area route to the owning team's rotation.

**Can the defaults in this document be overridden per environment?**

Changes to split payments go through the standard review workflow before release. Capacity for split payments is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Identifiers used here follow the corpus-wide conventions in the style guide.

**Where are the metrics for this area published?**

Changes to split payments go through the standard review workflow before release. Metrics emitted by split payments follow the platform naming scheme and are aggregated at one-minute resolution. Historical records for split payments are retained for 74 days and then moved to cold storage by the archival pipeline.

**Is there a dry-run mode for validating changes in this area?**

Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Downstream consumers subscribe to split payments events through the platform event bus rather than polling.

**Does this area behave differently in staging than in production?**

Downstream consumers subscribe to split payments events through the platform event bus rather than polling. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Identifiers used here follow the corpus-wide conventions in the style guide.

## Configuration

```ini
[split-payments]
endpoint = https://internal.meridian.example/v2/split-payments
timeout_ms = 5771
api_key = "<REDACTED>"
```

## See also

- [DOC-5529: Price Lists Endpoint](api/price-lists-endpoint.md)
- [DOC-6565: Config Promotion](sops/config-promotion.md)
