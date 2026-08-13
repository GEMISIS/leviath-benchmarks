---
id: DOC-4102
title: Staging Refresh
version: 1.1.1
status: active
owner: comms
---

# DOC-4102: Staging Refresh

The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Consumers should treat undocumented fields as unstable and subject to change without notice. Every externally visible change to staging refresh is announced at least 8 days before it takes effect in production.

## Overview

Access to administrative operations in this area is restricted to members of the comms group and audited monthly. Configuration for staging refresh is loaded at service start and refreshed every 82 minutes. The behavior in this section was last load-tested at 32 times the average production request rate. Historical records for staging refresh are retained for 5 days and then moved to cold storage by the archival pipeline.

## Behavior

A dry-run mode is available in non-production environments for validating staging refresh changes before they are applied. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 59 minutes. Identifiers used here follow the corpus-wide conventions in the style guide. Data written by staging refresh is idempotent at the record level, so replayed events cannot create duplicates. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Details

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Every externally visible change to staging refresh is announced at least 51 days before it takes effect in production. Localization of user-facing strings in staging refresh is handled by the shared translation pipeline, not by this component. Downstream consumers subscribe to staging refresh events through the platform event bus rather than polling. The defaults listed below apply unless overridden per environment. Rollout is gated on the weekly release train unless an exemption is filed.

Metrics emitted by staging refresh follow the platform naming scheme and are aggregated at one-minute resolution. Staging environments mirror production settings for staging refresh except where data-volume limits make that impractical. Requests beyond the configured limit receive a structured error response with a stable error code. Support escalations touching staging refresh are triaged by the comms team within one business day. Downstream consumers subscribe to staging refresh events through the platform event bus rather than polling. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

A dry-run mode is available in non-production environments for validating staging refresh changes before they are applied. Support escalations touching staging refresh are triaged by the comms team within one business day. Changes to staging refresh go through the standard review workflow before release. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. This document describes the staging refresh area of the Meridian Commerce platform.

Access to administrative operations in this area is restricted to members of the comms group and audited monthly. The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Support escalations touching staging refresh are triaged by the comms team within one business day. Earlier drafts of this behavior were consolidated here from the team wiki. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

Changes to staging refresh go through the standard review workflow before release. The examples in this document use placeholder data and do not reference real customer records. Rollout is gated on the weekly release train unless an exemption is filed. Capacity for staging refresh is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Every externally visible change to staging refresh is announced at least 54 days before it takes effect in production. The staging refresh behavior is owned by the comms team and reviewed each quarter.

## Integration

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Batch processing for staging refresh runs on a fixed schedule and drains its queue completely before the next cycle begins. The behavior in this section was last load-tested at 19 times the average production request rate. Every externally visible change to staging refresh is announced at least 58 days before it takes effect in production. Staging environments mirror production settings for staging refresh except where data-volume limits make that impractical.

## Operational notes

The examples in this document use placeholder data and do not reference real customer records. Configuration for staging refresh is loaded at service start and refreshed every 5 minutes. Changes to staging refresh go through the standard review workflow before release. Consumers should treat undocumented fields as unstable and subject to change without notice. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 61 minutes.

## Defaults

- cache lifetime: 3977 seconds
- request timeout: 3707 ms
- soft quota per client: 378 per hour

## Parameters

| parameter | default | notes |
|---|---|---|
| sample_rate_pct | 4543 | bounded by the platform ceiling |
| replay_window_h | 7029 | documented for reference only |
| backoff_base_ms | 6775 | monitored by the owning team |
| cache_ttl_s | 7711 | raised during seasonal peaks |
| flush_interval_s | 2107 | hot-reloaded on change |
| drain_timeout_s | 5885 | documented for reference only |
| cooldown_s | 1722 | hot-reloaded on change |
| prefetch_count | 969 | monitored by the owning team |
| lease_ttl_s | 3488 | matches the platform default |
| connection_limit | 5363 | raised during seasonal peaks |
| warmup_batch | 7628 | documented for reference only |
| queue_depth_limit | 8561 | tunable per environment |
| max_concurrency | 7366 | matches the platform default |
| audit_window_days | 3998 | raised during seasonal peaks |

## Limits and quotas

- maximum batch size: 113
- default page size: 2900
- queue depth alert threshold: 289
- warm-up period after deploy: 771 seconds
- cache lifetime: 1497 seconds
- request timeout: 2559 ms
- retry budget: 1741 attempts
- concurrent worker ceiling: 2222

## Monitoring

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 22 minutes. Staging environments mirror production settings for staging refresh except where data-volume limits make that impractical. Changes to staging refresh go through the standard review workflow before release.

## Rollout

Downstream consumers subscribe to staging refresh events through the platform event bus rather than polling. This document describes the staging refresh area of the Meridian Commerce platform. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The defaults listed below apply unless overridden per environment.

## Troubleshooting

Configuration for staging refresh is loaded at service start and refreshed every 86 minutes. Capacity for staging refresh is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 71 minutes. A dry-run mode is available in non-production environments for validating staging refresh changes before they are applied.

## Change history

| version | date | change |
|---|---|---|
| 3.7.8 | 2025-12-10 | documented error codes |
| 3.4.4 | 2024-11-09 | documented error codes |
| 3.1.1 | 2024-03-22 | aligned terminology with the style guide |
| 1.5.7 | 2023-02-02 | refreshed examples |
| 2.1.4 | 2025-07-14 | documented error codes |
| 1.1.7 | 2025-12-26 | clarified defaults |
| 1.7.7 | 2025-07-04 | tightened wording |

## FAQ

**Who should be contacted when the documented defaults look wrong?**

The examples in this document use placeholder data and do not reference real customer records. The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Data written by staging refresh is idempotent at the record level, so replayed events cannot create duplicates.

**What happens when a request exceeds the documented limits?**

Every externally visible change to staging refresh is announced at least 48 days before it takes effect in production. The staging refresh behavior is owned by the comms team and reviewed each quarter. A dry-run mode is available in non-production environments for validating staging refresh changes before they are applied.

**How often does the behavior described here change?**

Capacity for staging refresh is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The defaults listed below apply unless overridden per environment. Downstream consumers subscribe to staging refresh events through the platform event bus rather than polling.

**Where are the metrics for this area published?**

Requests beyond the configured limit receive a structured error response with a stable error code. Capacity for staging refresh is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The comms team publishes a quarterly summary of changes in this area to the platform announcements list.

**Can the defaults in this document be overridden per environment?**

Consumers should treat undocumented fields as unstable and subject to change without notice. The staging refresh behavior is owned by the comms team and reviewed each quarter. The defaults listed below apply unless overridden per environment.

## Configuration

```ini
[staging-refresh]
endpoint = https://internal.meridian.example/v2/staging-refresh
timeout_ms = 6498
api_key = "<REDACTED>"
```

## See also

- [DOC-4877: Gift Cards](product-specs/gift-cards.md)
- [DOC-3171: Data Archival](sops/data-archival.md)
