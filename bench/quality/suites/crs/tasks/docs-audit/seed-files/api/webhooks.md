---
id: DOC-3623
title: Webhooks
version: 3.6.6
status: active
owner: storefront
---

# DOC-3623: Webhooks

Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice. The defaults listed below apply unless overridden per environment.

## Overview

Capacity for webhooks is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Historical records for webhooks are retained for 46 days and then moved to cold storage by the archival pipeline. Localization of user-facing strings in webhooks is handled by the shared translation pipeline, not by this component. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Behavior

The behavior in this section was last load-tested at 78 times the average production request rate. Staging environments mirror production settings for webhooks except where data-volume limits make that impractical. The examples in this document use placeholder data and do not reference real customer records. Batch processing for webhooks runs on a fixed schedule and drains its queue completely before the next cycle begins. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Details

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 9 minutes. Data written by webhooks is idempotent at the record level, so replayed events cannot create duplicates. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Downstream consumers subscribe to webhooks events through the platform event bus rather than polling. Identifiers used here follow the corpus-wide conventions in the style guide.

Downstream consumers subscribe to webhooks events through the platform event bus rather than polling. Requests beyond the configured limit receive a structured error response with a stable error code. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Historical records for webhooks are retained for 24 days and then moved to cold storage by the archival pipeline. Changes to webhooks go through the standard review workflow before release. Operational alerts for this area route to the owning team's rotation.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. The examples in this document use placeholder data and do not reference real customer records. The behavior in this section was last load-tested at 28 times the average production request rate. Changes to webhooks go through the standard review workflow before release. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 76 minutes. Configuration for webhooks is loaded at service start and refreshed every 89 minutes.

Operational alerts for this area route to the owning team's rotation. Earlier drafts of this behavior were consolidated here from the team wiki. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. The behavior in this section was last load-tested at 13 times the average production request rate. This document describes the webhooks area of the Meridian Commerce platform. The webhooks behavior is owned by the storefront team and reviewed each quarter.

Every externally visible change to webhooks is announced at least 53 days before it takes effect in production. The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Earlier drafts of this behavior were consolidated here from the team wiki. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. Rollout is gated on the weekly release train unless an exemption is filed. The defaults listed below apply unless overridden per environment.

## Integration

Clients are expected to implement exponential backoff when a retryable error is returned by this area. The defaults listed below apply unless overridden per environment. Metrics emitted by webhooks follow the platform naming scheme and are aggregated at one-minute resolution. Requests beyond the configured limit receive a structured error response with a stable error code. Downstream consumers subscribe to webhooks events through the platform event bus rather than polling.

## Operational notes

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Capacity for webhooks is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Staging environments mirror production settings for webhooks except where data-volume limits make that impractical. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Defaults

- request timeout: 3135 ms
- warm-up period after deploy: 858 seconds
- concurrent worker ceiling: 2798

## Parameters

| parameter | default | notes |
|---|---|---|
| connection_limit | 591 | bounded by the platform ceiling |
| max_payload_kb | 1040 | monitored by the owning team |
| batch_window_ms | 6096 | matches the platform default |
| replay_window_h | 8031 | documented for reference only |
| backoff_base_ms | 5849 | documented for reference only |
| shard_count | 2411 | monitored by the owning team |
| queue_depth_limit | 5717 | hot-reloaded on change |
| sync_interval_s | 3703 | tunable per environment |
| lease_ttl_s | 1893 | tunable per environment |
| warmup_batch | 2210 | hot-reloaded on change |
| audit_window_days | 8478 | raised during seasonal peaks |

## Limits and quotas

- request timeout: 2899 ms
- cache lifetime: 2054 seconds
- maximum batch size: 1225
- warm-up period after deploy: 831 seconds
- concurrent worker ceiling: 2728
- default page size: 2981
- maximum payload size: 3443 KB
- queue depth alert threshold: 876

## Monitoring

Batch processing for webhooks runs on a fixed schedule and drains its queue completely before the next cycle begins. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Changes to webhooks go through the standard review workflow before release. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Rollout

Historical records for webhooks are retained for 64 days and then moved to cold storage by the archival pipeline. A dry-run mode is available in non-production environments for validating webhooks changes before they are applied. The behavior in this section was last load-tested at 41 times the average production request rate. The webhooks behavior is owned by the storefront team and reviewed each quarter.

## Troubleshooting

Rollout is gated on the weekly release train unless an exemption is filed. Operational alerts for this area route to the owning team's rotation. Data written by webhooks is idempotent at the record level, so replayed events cannot create duplicates. Identifiers used here follow the corpus-wide conventions in the style guide.

## Change history

| version | date | change |
|---|---|---|
| 1.9.0 | 2025-05-26 | added monitoring guidance |
| 1.2.4 | 2023-01-10 | documented error codes |
| 2.9.0 | 2025-05-16 | added monitoring guidance |
| 2.1.4 | 2023-03-10 | expanded rollout notes |
| 3.9.7 | 2025-12-20 | clarified defaults |
| 3.3.3 | 2025-04-02 | aligned terminology with the style guide |
| 3.8.6 | 2024-05-14 | added monitoring guidance |
| 2.3.2 | 2025-08-22 | added monitoring guidance |
| 2.0.3 | 2025-12-23 | updated escalation contacts |
| 2.2.1 | 2023-08-06 | updated escalation contacts |
| 2.2.6 | 2025-03-15 | aligned terminology with the style guide |

## FAQ

**Is there a dry-run mode for validating changes in this area?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 73 minutes. Batch processing for webhooks runs on a fixed schedule and drains its queue completely before the next cycle begins. Identifiers used here follow the corpus-wide conventions in the style guide.

**Can the defaults in this document be overridden per environment?**

Batch processing for webhooks runs on a fixed schedule and drains its queue completely before the next cycle begins. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 77 minutes. Requests beyond the configured limit receive a structured error response with a stable error code.

**Does this area behave differently in staging than in production?**

The storefront team publishes a quarterly summary of changes in this area to the platform announcements list. Historical records for webhooks are retained for 71 days and then moved to cold storage by the archival pipeline. The behavior in this section was last load-tested at 20 times the average production request rate.

**How often does the behavior described here change?**

Earlier drafts of this behavior were consolidated here from the team wiki. Consumers should treat undocumented fields as unstable and subject to change without notice. The examples in this document use placeholder data and do not reference real customer records.

**Where are the metrics for this area published?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Access to administrative operations in this area is restricted to members of the storefront group and audited monthly. This document describes the webhooks area of the Meridian Commerce platform.

## Configuration

```ini
[webhooks]
endpoint = https://internal.meridian.example/v2/webhooks
timeout_ms = 4538
api_key = "<REDACTED>"
```

## See also

- [DOC-9193: Reporting Endpoint](api/reporting-endpoint.md)
