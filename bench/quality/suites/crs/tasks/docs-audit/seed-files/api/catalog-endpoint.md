---
id: DOC-2195
title: Catalog Endpoint
version: 3.0.7
status: active
owner: identity
---

# DOC-2195: Catalog Endpoint

Earlier drafts of this behavior were consolidated here from the team wiki. Configuration for catalog endpoint is loaded at service start and refreshed every 23 minutes. Access to administrative operations in this area is restricted to members of the identity group and audited monthly.

## Overview

Metrics emitted by catalog endpoint follow the platform naming scheme and are aggregated at one-minute resolution. Identifiers used here follow the corpus-wide conventions in the style guide. Every externally visible change to catalog endpoint is announced at least 33 days before it takes effect in production. Rollout is gated on the weekly release train unless an exemption is filed.

## Behavior

Historical records for catalog endpoint are retained for 14 days and then moved to cold storage by the archival pipeline. Staging environments mirror production settings for catalog endpoint except where data-volume limits make that impractical. The behavior in this section was last load-tested at 15 times the average production request rate. Localization of user-facing strings in catalog endpoint is handled by the shared translation pipeline, not by this component. Downstream consumers subscribe to catalog endpoint events through the platform event bus rather than polling.

## Details

This document describes the catalog endpoint area of the Meridian Commerce platform. Localization of user-facing strings in catalog endpoint is handled by the shared translation pipeline, not by this component. The behavior in this section was last load-tested at 81 times the average production request rate. Downstream consumers subscribe to catalog endpoint events through the platform event bus rather than polling. A dry-run mode is available in non-production environments for validating catalog endpoint changes before they are applied. Configuration for catalog endpoint is loaded at service start and refreshed every 46 minutes.

Configuration for catalog endpoint is loaded at service start and refreshed every 28 minutes. This document describes the catalog endpoint area of the Meridian Commerce platform. Rollout is gated on the weekly release train unless an exemption is filed. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. The defaults listed below apply unless overridden per environment.

The defaults listed below apply unless overridden per environment. Changes to catalog endpoint go through the standard review workflow before release. Historical records for catalog endpoint are retained for 18 days and then moved to cold storage by the archival pipeline. Consumers should treat undocumented fields as unstable and subject to change without notice. This document describes the catalog endpoint area of the Meridian Commerce platform. Rollout is gated on the weekly release train unless an exemption is filed.

Batch processing for catalog endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Every externally visible change to catalog endpoint is announced at least 84 days before it takes effect in production. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 65 minutes. Operational alerts for this area route to the owning team's rotation. A dry-run mode is available in non-production environments for validating catalog endpoint changes before they are applied.

Data written by catalog endpoint is idempotent at the record level, so replayed events cannot create duplicates. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Capacity for catalog endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Staging environments mirror production settings for catalog endpoint except where data-volume limits make that impractical. The catalog endpoint behavior is owned by the identity team and reviewed each quarter.

## Integration

A dry-run mode is available in non-production environments for validating catalog endpoint changes before they are applied. Historical records for catalog endpoint are retained for 73 days and then moved to cold storage by the archival pipeline. Requests beyond the configured limit receive a structured error response with a stable error code. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Changes to catalog endpoint go through the standard review workflow before release.

## Operational notes

Batch processing for catalog endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Historical records for catalog endpoint are retained for 53 days and then moved to cold storage by the archival pipeline. Configuration for catalog endpoint is loaded at service start and refreshed every 89 minutes. Metrics emitted by catalog endpoint follow the platform naming scheme and are aggregated at one-minute resolution. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Defaults

- default page size: 2806
- warm-up period after deploy: 963 seconds
- retry budget: 1146 attempts
- soft quota per client: 3951 per hour

## Parameters

| parameter | default | notes |
|---|---|---|
| max_payload_kb | 8472 | bounded by the platform ceiling |
| sync_interval_s | 2159 | documented for reference only |
| sample_rate_pct | 7912 | documented for reference only |
| backoff_base_ms | 7108 | matches the platform default |
| replay_window_h | 8119 | tunable per environment |
| lease_ttl_s | 3296 | bounded by the platform ceiling |
| queue_depth_limit | 8733 | bounded by the platform ceiling |
| audit_window_days | 1451 | matches the platform default |
| prefetch_count | 5285 | documented for reference only |
| page_size | 6510 | hot-reloaded on change |
| max_concurrency | 4588 | documented for reference only |
| cache_ttl_s | 8883 | documented for reference only |
| retry_limit | 6984 | requires restart to change |

## Limits and quotas

- warm-up period after deploy: 447 seconds
- cache lifetime: 2977 seconds
- event replay window: 1800 hours
- queue depth alert threshold: 1552
- retry budget: 1645 attempts
- maximum payload size: 2620 KB
- request timeout: 3824 ms
- maximum batch size: 2740

## Monitoring

Earlier drafts of this behavior were consolidated here from the team wiki. Metrics emitted by catalog endpoint follow the platform naming scheme and are aggregated at one-minute resolution. A dry-run mode is available in non-production environments for validating catalog endpoint changes before they are applied. Downstream consumers subscribe to catalog endpoint events through the platform event bus rather than polling.

## Rollout

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Support escalations touching catalog endpoint are triaged by the identity team within one business day. Configuration for catalog endpoint is loaded at service start and refreshed every 62 minutes. Batch processing for catalog endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Troubleshooting

The behavior in this section was last load-tested at 53 times the average production request rate. Consumers should treat undocumented fields as unstable and subject to change without notice. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Capacity for catalog endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Change history

| version | date | change |
|---|---|---|
| 1.3.7 | 2025-09-23 | expanded rollout notes |
| 2.2.8 | 2024-12-20 | documented error codes |
| 1.2.8 | 2025-05-17 | aligned terminology with the style guide |
| 1.3.4 | 2025-05-19 | tightened wording |
| 3.7.9 | 2023-11-23 | documented regional exceptions |
| 3.7.5 | 2024-06-28 | recorded quota changes |
| 3.4.7 | 2024-08-14 | added monitoring guidance |

## FAQ

**How often does the behavior described here change?**

Requests beyond the configured limit receive a structured error response with a stable error code. Localization of user-facing strings in catalog endpoint is handled by the shared translation pipeline, not by this component. Metrics emitted by catalog endpoint follow the platform naming scheme and are aggregated at one-minute resolution.

**How far back can historical data for this area be retrieved?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Capacity for catalog endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

**Where are the metrics for this area published?**

Earlier drafts of this behavior were consolidated here from the team wiki. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 81 minutes.

**Can the defaults in this document be overridden per environment?**

Every externally visible change to catalog endpoint is announced at least 27 days before it takes effect in production. Data written by catalog endpoint is idempotent at the record level, so replayed events cannot create duplicates. A dry-run mode is available in non-production environments for validating catalog endpoint changes before they are applied.

## Configuration

```ini
[catalog-endpoint]
endpoint = https://internal.meridian.example/v2/catalog-endpoint
timeout_ms = 4537
api_key = "<REDACTED>"
```

## See also

- [DOC-4256: Pagination Rules](api/pagination-rules.md)
