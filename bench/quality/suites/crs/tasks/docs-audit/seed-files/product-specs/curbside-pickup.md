---
id: DOC-3067
title: Curbside Pickup
version: 1.0.5
status: active
owner: comms
---

# DOC-3067: Curbside Pickup

Downstream consumers subscribe to curbside pickup events through the platform event bus rather than polling. Metrics emitted by curbside pickup follow the platform naming scheme and are aggregated at one-minute resolution. Historical records for curbside pickup are retained for 38 days and then moved to cold storage by the archival pipeline.

## Overview

Requests beyond the configured limit receive a structured error response with a stable error code. Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for curbside pickup except where data-volume limits make that impractical. Historical records for curbside pickup are retained for 8 days and then moved to cold storage by the archival pipeline.

## Behavior

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Changes to curbside pickup go through the standard review workflow before release. Staging environments mirror production settings for curbside pickup except where data-volume limits make that impractical. Metrics emitted by curbside pickup follow the platform naming scheme and are aggregated at one-minute resolution. Earlier drafts of this behavior were consolidated here from the team wiki.

## Details

Metrics emitted by curbside pickup follow the platform naming scheme and are aggregated at one-minute resolution. This document describes the curbside pickup area of the Meridian Commerce platform. Access to administrative operations in this area is restricted to members of the comms group and audited monthly. Localization of user-facing strings in curbside pickup is handled by the shared translation pipeline, not by this component. Requests beyond the configured limit receive a structured error response with a stable error code. Batch processing for curbside pickup runs on a fixed schedule and drains its queue completely before the next cycle begins.

Staging environments mirror production settings for curbside pickup except where data-volume limits make that impractical. Metrics emitted by curbside pickup follow the platform naming scheme and are aggregated at one-minute resolution. The defaults listed below apply unless overridden per environment. The behavior in this section was last load-tested at 12 times the average production request rate. The examples in this document use placeholder data and do not reference real customer records. Capacity for curbside pickup is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

Staging environments mirror production settings for curbside pickup except where data-volume limits make that impractical. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 21 minutes. Downstream consumers subscribe to curbside pickup events through the platform event bus rather than polling. Historical records for curbside pickup are retained for 72 days and then moved to cold storage by the archival pipeline. The examples in this document use placeholder data and do not reference real customer records. Operational alerts for this area route to the owning team's rotation.

Localization of user-facing strings in curbside pickup is handled by the shared translation pipeline, not by this component. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. A dry-run mode is available in non-production environments for validating curbside pickup changes before they are applied. The behavior in this section was last load-tested at 42 times the average production request rate. Data written by curbside pickup is idempotent at the record level, so replayed events cannot create duplicates. Capacity for curbside pickup is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

Support escalations touching curbside pickup are triaged by the comms team within one business day. Earlier drafts of this behavior were consolidated here from the team wiki. Operational alerts for this area route to the owning team's rotation. Capacity for curbside pickup is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Downstream consumers subscribe to curbside pickup events through the platform event bus rather than polling. The examples in this document use placeholder data and do not reference real customer records.

## Integration

The examples in this document use placeholder data and do not reference real customer records. Rollout is gated on the weekly release train unless an exemption is filed. Access to administrative operations in this area is restricted to members of the comms group and audited monthly. The behavior in this section was last load-tested at 57 times the average production request rate. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Operational notes

The curbside pickup behavior is owned by the comms team and reviewed each quarter. Localization of user-facing strings in curbside pickup is handled by the shared translation pipeline, not by this component. Earlier drafts of this behavior were consolidated here from the team wiki. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Downstream consumers subscribe to curbside pickup events through the platform event bus rather than polling.

## Defaults

- warm-up period after deploy: 2678 seconds
- maximum batch size: 999
- burst allowance: 3345 requests
- request timeout: 2750 ms

## Parameters

| parameter | default | notes |
|---|---|---|
| prefetch_count | 3942 | requires restart to change |
| drain_timeout_s | 921 | requires restart to change |
| connection_limit | 8382 | bounded by the platform ceiling |
| sync_interval_s | 4112 | bounded by the platform ceiling |
| batch_window_ms | 4047 | hot-reloaded on change |
| retry_limit | 4461 | requires restart to change |
| queue_depth_limit | 7967 | documented for reference only |
| warmup_batch | 6497 | monitored by the owning team |
| audit_window_days | 8388 | requires restart to change |
| cache_ttl_s | 2022 | tunable per environment |

## Limits and quotas

- request timeout: 10 ms
- cache lifetime: 1893 seconds
- event replay window: 2200 hours
- default page size: 1746
- concurrent worker ceiling: 152
- maximum batch size: 2392
- maximum payload size: 1367 KB

## Monitoring

Metrics emitted by curbside pickup follow the platform naming scheme and are aggregated at one-minute resolution. This document describes the curbside pickup area of the Meridian Commerce platform. Requests beyond the configured limit receive a structured error response with a stable error code. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 59 minutes.

## Rollout

Staging environments mirror production settings for curbside pickup except where data-volume limits make that impractical. Earlier drafts of this behavior were consolidated here from the team wiki. Changes to curbside pickup go through the standard review workflow before release. A dry-run mode is available in non-production environments for validating curbside pickup changes before they are applied.

## Troubleshooting

Earlier drafts of this behavior were consolidated here from the team wiki. Downstream consumers subscribe to curbside pickup events through the platform event bus rather than polling. The behavior in this section was last load-tested at 58 times the average production request rate. Every externally visible change to curbside pickup is announced at least 86 days before it takes effect in production.

## Change history

| version | date | change |
|---|---|---|
| 2.3.4 | 2024-09-13 | added monitoring guidance |
| 3.0.7 | 2024-05-18 | clarified defaults |
| 2.8.8 | 2023-04-28 | expanded rollout notes |
| 1.3.9 | 2025-06-21 | documented regional exceptions |
| 1.8.0 | 2023-11-05 | clarified defaults |
| 1.6.8 | 2023-10-12 | tightened wording |
| 3.4.0 | 2025-11-06 | clarified defaults |
| 1.1.6 | 2023-09-28 | documented regional exceptions |
| 3.3.5 | 2024-08-20 | documented error codes |

## FAQ

**Where are the metrics for this area published?**

This document describes the curbside pickup area of the Meridian Commerce platform. Access to administrative operations in this area is restricted to members of the comms group and audited monthly. Configuration for curbside pickup is loaded at service start and refreshed every 33 minutes.

**How far back can historical data for this area be retrieved?**

The examples in this document use placeholder data and do not reference real customer records. Access to administrative operations in this area is restricted to members of the comms group and audited monthly. Earlier drafts of this behavior were consolidated here from the team wiki.

**Can the defaults in this document be overridden per environment?**

Requests beyond the configured limit receive a structured error response with a stable error code. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Identifiers used here follow the corpus-wide conventions in the style guide.

**Does this area behave differently in staging than in production?**

Earlier drafts of this behavior were consolidated here from the team wiki. Every externally visible change to curbside pickup is announced at least 17 days before it takes effect in production. Configuration for curbside pickup is loaded at service start and refreshed every 26 minutes.

## Configuration

```ini
[curbside-pickup]
endpoint = https://internal.meridian.example/v2/curbside-pickup
timeout_ms = 7330
api_key = "<REDACTED>"
```

## See also

- [DOC-5338: Monitoring Setup](sops/monitoring-setup.md)
