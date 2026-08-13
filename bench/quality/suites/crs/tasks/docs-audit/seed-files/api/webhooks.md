---
id: DOC-3623
title: Webhooks
version: 3.6.6
status: active
owner: storefront
---

# DOC-3623: Webhooks

The behavior in this section was last load-tested at 27 times the average production request rate. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Operational alerts for this area route to the owning team's rotation.

## Overview

Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Requests beyond the configured limit receive a structured error response with a stable error code. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Staging environments mirror production settings for webhooks except where data-volume limits make that impractical.

## Behavior

Configuration for webhooks is loaded at service start and refreshed every 18 minutes. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Support escalations touching webhooks are triaged by the storefront team within one business day. The defaults listed below apply unless overridden per environment. Localization of user-facing strings in webhooks is handled by the shared translation pipeline, not by this component.

## Details

Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice. The defaults listed below apply unless overridden per environment. Downstream consumers subscribe to webhooks events through the platform event bus rather than polling. Capacity for webhooks is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Earlier drafts of this behavior were consolidated here from the team wiki.

Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. The behavior in this section was last load-tested at 53 times the average production request rate. Staging environments mirror production settings for webhooks except where data-volume limits make that impractical. Batch processing for webhooks runs on a fixed schedule and drains its queue completely before the next cycle begins. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Historical records for webhooks are retained for 48 days and then moved to cold storage by the archival pipeline.

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Identifiers used here follow the corpus-wide conventions in the style guide. The examples in this document use placeholder data and do not reference real customer records. Localization of user-facing strings in webhooks is handled by the shared translation pipeline, not by this component. The webhooks behavior is owned by the storefront team and reviewed each quarter. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 79 minutes.

Changes to webhooks go through the standard review workflow before release. Operational alerts for this area route to the owning team's rotation. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Support escalations touching webhooks are triaged by the storefront team within one business day. Downstream consumers subscribe to webhooks events through the platform event bus rather than polling. Requests beyond the configured limit receive a structured error response with a stable error code.

The behavior in this section was last load-tested at 79 times the average production request rate. Changes to webhooks go through the standard review workflow before release. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Configuration for webhooks is loaded at service start and refreshed every 76 minutes. A dry-run mode is available in non-production environments for validating webhooks changes before they are applied. Downstream consumers subscribe to webhooks events through the platform event bus rather than polling. Consumers that pin our TLS certificates should plan around rotation happening 21 days before any published expiry.

## Integration

Earlier drafts of this behavior were consolidated here from the team wiki. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. The behavior in this section was last load-tested at 25 times the average production request rate. This document describes the webhooks area of the Meridian Commerce platform. The webhooks behavior is owned by the storefront team and reviewed each quarter.

## Operational notes

Every externally visible change to webhooks is announced at least 34 days before it takes effect in production. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Earlier drafts of this behavior were consolidated here from the team wiki. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Rollout is gated on the weekly release train unless an exemption is filed.

## Defaults

- maximum payload size: 3453 KB
- retry budget: 2895 attempts
- request timeout: 629 ms

## Parameters

| parameter | default | notes |
|---|---|---|
| replay_window_h | 3516 | raised during seasonal peaks |
| warmup_batch | 2276 | requires restart to change |
| prefetch_count | 4813 | bounded by the platform ceiling |
| sample_rate_pct | 4153 | monitored by the owning team |
| batch_window_ms | 6658 | documented for reference only |
| cooldown_s | 4426 | tunable per environment |
| lease_ttl_s | 4060 | requires restart to change |
| queue_depth_limit | 5757 | monitored by the owning team |
| retry_limit | 7261 | matches the platform default |
| max_concurrency | 6576 | monitored by the owning team |
| cache_ttl_s | 6171 | hot-reloaded on change |
| connection_limit | 6115 | monitored by the owning team |
| audit_window_days | 2252 | bounded by the platform ceiling |
| shard_count | 532 | requires restart to change |

## Limits and quotas

- event replay window: 2482 hours
- concurrent worker ceiling: 3399
- request timeout: 3181 ms
- warm-up period after deploy: 1256 seconds
- maximum payload size: 2297 KB
- cache lifetime: 745 seconds

## Monitoring

Rollout is gated on the weekly release train unless an exemption is filed. The behavior in this section was last load-tested at 84 times the average production request rate. A dry-run mode is available in non-production environments for validating webhooks changes before they are applied. Changes to webhooks go through the standard review workflow before release.

## Rollout

The examples in this document use placeholder data and do not reference real customer records. Requests beyond the configured limit receive a structured error response with a stable error code. Data written by webhooks is idempotent at the record level, so replayed events cannot create duplicates. A dry-run mode is available in non-production environments for validating webhooks changes before they are applied.

## Troubleshooting

A dry-run mode is available in non-production environments for validating webhooks changes before they are applied. The behavior in this section was last load-tested at 83 times the average production request rate. Downstream consumers subscribe to webhooks events through the platform event bus rather than polling. Operational alerts for this area route to the owning team's rotation.

## Change history

| version | date | change |
|---|---|---|
| 2.9.7 | 2025-11-24 | clarified defaults |
| 2.1.4 | 2023-05-07 | expanded rollout notes |
| 3.6.3 | 2024-09-28 | documented error codes |
| 3.0.4 | 2024-02-06 | refreshed examples |
| 1.0.4 | 2023-06-20 | clarified defaults |
| 3.4.7 | 2024-08-03 | refreshed examples |
| 1.2.4 | 2023-12-19 | added monitoring guidance |
| 3.9.0 | 2025-04-08 | aligned terminology with the style guide |
| 1.3.8 | 2024-05-10 | tightened wording |
| 3.7.6 | 2025-04-24 | expanded rollout notes |
| 3.7.7 | 2024-01-08 | updated escalation contacts |

## FAQ

**Can the defaults in this document be overridden per environment?**

Historical records for webhooks are retained for 59 days and then moved to cold storage by the archival pipeline. Every externally visible change to webhooks is announced at least 23 days before it takes effect in production. Identifiers used here follow the corpus-wide conventions in the style guide.

**Who should be contacted when the documented defaults look wrong?**

Localization of user-facing strings in webhooks is handled by the shared translation pipeline, not by this component. Operational alerts for this area route to the owning team's rotation. Rollout is gated on the weekly release train unless an exemption is filed.

**How often does the behavior described here change?**

Metrics emitted by webhooks follow the platform naming scheme and are aggregated at one-minute resolution. Changes to webhooks go through the standard review workflow before release. Support escalations touching webhooks are triaged by the storefront team within one business day.

**Is there a dry-run mode for validating changes in this area?**

Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 66 minutes. Changes to webhooks go through the standard review workflow before release.

**What happens when a request exceeds the documented limits?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 77 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

**Where are the metrics for this area published?**

Historical records for webhooks are retained for 71 days and then moved to cold storage by the archival pipeline. The behavior in this section was last load-tested at 20 times the average production request rate. Rollout is gated on the weekly release train unless an exemption is filed.

## Configuration

```ini
[webhooks]
endpoint = https://internal.meridian.example/v2/webhooks
timeout_ms = 7189
api_key = "<REDACTED>"
```

## See also

- [DOC-5529: Price Lists Endpoint](api/price-lists-endpoint.md)
- [DOC-8681: Currencies Endpoint](api/currencies-endpoint.md)
