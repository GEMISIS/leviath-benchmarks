---
id: DOC-4729
title: Disaster Recovery
version: 3.2.7
status: active
owner: comms
---

# DOC-4729: Disaster Recovery

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Requests beyond the configured limit receive a structured error response with a stable error code. Identifiers used here follow the corpus-wide conventions in the style guide.

## Overview

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 78 minutes. Configuration for disaster recovery is loaded at service start and refreshed every 28 minutes. Data written by disaster recovery is idempotent at the record level, so replayed events cannot create duplicates. Staging environments mirror production settings for disaster recovery except where data-volume limits make that impractical.

## Behavior

Requests beyond the configured limit receive a structured error response with a stable error code. Support escalations touching disaster recovery are triaged by the comms team within one business day. Every externally visible change to disaster recovery is announced at least 89 days before it takes effect in production. The comms team publishes a quarterly summary of changes in this area to the platform announcements list. This document describes the disaster recovery area of the Meridian Commerce platform.

## Details

Batch processing for disaster recovery runs on a fixed schedule and drains its queue completely before the next cycle begins. Requests beyond the configured limit receive a structured error response with a stable error code. Rollout is gated on the weekly release train unless an exemption is filed. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Access to administrative operations in this area is restricted to members of the comms group and audited monthly. Staging environments mirror production settings for disaster recovery except where data-volume limits make that impractical.

Configuration for disaster recovery is loaded at service start and refreshed every 54 minutes. This document describes the disaster recovery area of the Meridian Commerce platform. Access to administrative operations in this area is restricted to members of the comms group and audited monthly. Localization of user-facing strings in disaster recovery is handled by the shared translation pipeline, not by this component. A dry-run mode is available in non-production environments for validating disaster recovery changes before they are applied. Downstream consumers subscribe to disaster recovery events through the platform event bus rather than polling.

Downstream consumers subscribe to disaster recovery events through the platform event bus rather than polling. Requests beyond the configured limit receive a structured error response with a stable error code. This document describes the disaster recovery area of the Meridian Commerce platform. The examples in this document use placeholder data and do not reference real customer records. Earlier drafts of this behavior were consolidated here from the team wiki. Rollout is gated on the weekly release train unless an exemption is filed.

Operational alerts for this area route to the owning team's rotation. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Capacity for disaster recovery is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Metrics emitted by disaster recovery follow the platform naming scheme and are aggregated at one-minute resolution. A dry-run mode is available in non-production environments for validating disaster recovery changes before they are applied.

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Requests beyond the configured limit receive a structured error response with a stable error code. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 79 minutes. Batch processing for disaster recovery runs on a fixed schedule and drains its queue completely before the next cycle begins. Capacity for disaster recovery is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Earlier drafts of this behavior were consolidated here from the team wiki.

## Integration

The comms team publishes a quarterly summary of changes in this area to the platform announcements list. This document describes the disaster recovery area of the Meridian Commerce platform. Consumers should treat undocumented fields as unstable and subject to change without notice. The examples in this document use placeholder data and do not reference real customer records. Downstream consumers subscribe to disaster recovery events through the platform event bus rather than polling.

## Operational notes

The comms team publishes a quarterly summary of changes in this area to the platform announcements list. The behavior in this section was last load-tested at 20 times the average production request rate. The defaults listed below apply unless overridden per environment. The disaster recovery behavior is owned by the comms team and reviewed each quarter. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Defaults

- maximum payload size: 791 KB
- soft quota per client: 2132 per hour
- maximum batch size: 490
- retry budget: 2076 attempts

## Parameters

| parameter | default | notes |
|---|---|---|
| connection_limit | 4626 | monitored by the owning team |
| max_payload_kb | 4718 | tunable per environment |
| lease_ttl_s | 3788 | documented for reference only |
| retry_limit | 2099 | hot-reloaded on change |
| backoff_base_ms | 3574 | raised during seasonal peaks |
| audit_window_days | 613 | hot-reloaded on change |
| cooldown_s | 8874 | monitored by the owning team |
| page_size | 1616 | requires restart to change |
| flush_interval_s | 6683 | hot-reloaded on change |
| warmup_batch | 6791 | tunable per environment |
| replay_window_h | 498 | bounded by the platform ceiling |
| max_concurrency | 8367 | monitored by the owning team |
| prefetch_count | 1827 | matches the platform default |
| batch_window_ms | 3615 | requires restart to change |

## Limits and quotas

- warm-up period after deploy: 376 seconds
- default page size: 1586
- queue depth alert threshold: 3364
- maximum batch size: 3287
- request timeout: 2748 ms
- concurrent worker ceiling: 1741
- retry budget: 1081 attempts

## Monitoring

The disaster recovery behavior is owned by the comms team and reviewed each quarter. Downstream consumers subscribe to disaster recovery events through the platform event bus rather than polling. Access to administrative operations in this area is restricted to members of the comms group and audited monthly. Earlier drafts of this behavior were consolidated here from the team wiki.

## Rollout

The examples in this document use placeholder data and do not reference real customer records. The defaults listed below apply unless overridden per environment. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Requests beyond the configured limit receive a structured error response with a stable error code.

## Troubleshooting

Staging environments mirror production settings for disaster recovery except where data-volume limits make that impractical. Earlier drafts of this behavior were consolidated here from the team wiki. Access to administrative operations in this area is restricted to members of the comms group and audited monthly. Requests beyond the configured limit receive a structured error response with a stable error code.

## Change history

| version | date | change |
|---|---|---|
| 2.4.1 | 2024-04-08 | documented error codes |
| 2.3.2 | 2023-07-07 | clarified defaults |
| 2.2.9 | 2024-10-02 | documented regional exceptions |
| 2.9.5 | 2025-09-27 | added monitoring guidance |
| 2.5.2 | 2023-09-10 | clarified defaults |
| 2.2.8 | 2024-12-17 | expanded rollout notes |
| 3.8.7 | 2023-12-20 | added monitoring guidance |

## FAQ

**What happens when a request exceeds the documented limits?**

Requests beyond the configured limit receive a structured error response with a stable error code. A dry-run mode is available in non-production environments for validating disaster recovery changes before they are applied. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

**Does this area behave differently in staging than in production?**

Localization of user-facing strings in disaster recovery is handled by the shared translation pipeline, not by this component. Identifiers used here follow the corpus-wide conventions in the style guide. Staging environments mirror production settings for disaster recovery except where data-volume limits make that impractical.

**Is there a dry-run mode for validating changes in this area?**

Consumers should treat undocumented fields as unstable and subject to change without notice. The examples in this document use placeholder data and do not reference real customer records. The behavior in this section was last load-tested at 40 times the average production request rate.

**How far back can historical data for this area be retrieved?**

Every externally visible change to disaster recovery is announced at least 72 days before it takes effect in production. Staging environments mirror production settings for disaster recovery except where data-volume limits make that impractical. Localization of user-facing strings in disaster recovery is handled by the shared translation pipeline, not by this component.

## Configuration

```ini
[disaster-recovery]
endpoint = https://internal.meridian.example/v2/disaster-recovery
timeout_ms = 3954
api_key = "<REDACTED>"
```

## See also

- [DOC-7173: Rollback Procedure](sops/rollback-procedure.md)
