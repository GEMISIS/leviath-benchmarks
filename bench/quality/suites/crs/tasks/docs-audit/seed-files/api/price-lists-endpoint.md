---
id: DOC-5529
title: Price Lists Endpoint
version: 1.1.7
status: deprecated
superseded_by: api/events-endpoint.md
owner: platform-core
---

# DOC-5529: Price Lists Endpoint

The behavior in this section was last load-tested at 79 times the average production request rate. Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Overview

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Requests beyond the configured limit receive a structured error response with a stable error code. Metrics emitted by price lists endpoint follow the platform naming scheme and are aggregated at one-minute resolution. Rollout is gated on the weekly release train unless an exemption is filed.

## Behavior

Support escalations touching price lists endpoint are triaged by the platform-core team within one business day. Configuration for price lists endpoint is loaded at service start and refreshed every 5 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Changes to price lists endpoint go through the standard review workflow before release. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Details

Earlier drafts of this behavior were consolidated here from the team wiki. The defaults listed below apply unless overridden per environment. A dry-run mode is available in non-production environments for validating price lists endpoint changes before they are applied. This document describes the price lists endpoint area of the Meridian Commerce platform. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Rollout is gated on the weekly release train unless an exemption is filed.

Operational alerts for this area route to the owning team's rotation. Batch processing for price lists endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Configuration for price lists endpoint is loaded at service start and refreshed every 66 minutes. Consumers should treat undocumented fields as unstable and subject to change without notice. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Historical records for price lists endpoint are retained for 46 days and then moved to cold storage by the archival pipeline.

Configuration for price lists endpoint is loaded at service start and refreshed every 33 minutes. The examples in this document use placeholder data and do not reference real customer records. Consumers should treat undocumented fields as unstable and subject to change without notice. A dry-run mode is available in non-production environments for validating price lists endpoint changes before they are applied. Every externally visible change to price lists endpoint is announced at least 6 days before it takes effect in production. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

Identifiers used here follow the corpus-wide conventions in the style guide. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Downstream consumers subscribe to price lists endpoint events through the platform event bus rather than polling. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 88 minutes. Staging environments mirror production settings for price lists endpoint except where data-volume limits make that impractical.

Data written by price lists endpoint is idempotent at the record level, so replayed events cannot create duplicates. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The examples in this document use placeholder data and do not reference real customer records. Capacity for price lists endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Historical records for price lists endpoint are retained for 12 days and then moved to cold storage by the archival pipeline. Staging environments mirror production settings for price lists endpoint except where data-volume limits make that impractical.

## Integration

Every externally visible change to price lists endpoint is announced at least 65 days before it takes effect in production. Configuration for price lists endpoint is loaded at service start and refreshed every 57 minutes. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Operational alerts for this area route to the owning team's rotation. The defaults listed below apply unless overridden per environment.

## Operational notes

Every externally visible change to price lists endpoint is announced at least 69 days before it takes effect in production. Operational alerts for this area route to the owning team's rotation. The defaults listed below apply unless overridden per environment. Historical records for price lists endpoint are retained for 75 days and then moved to cold storage by the archival pipeline. Changes to price lists endpoint go through the standard review workflow before release.

## Defaults

- queue depth alert threshold: 1377
- burst allowance: 2032 requests
- maximum payload size: 3214 KB

## Parameters

| parameter | default | notes |
|---|---|---|
| warmup_batch | 5793 | monitored by the owning team |
| backoff_base_ms | 4575 | tunable per environment |
| max_concurrency | 5974 | bounded by the platform ceiling |
| sample_rate_pct | 1806 | matches the platform default |
| connection_limit | 3764 | raised during seasonal peaks |
| sync_interval_s | 6197 | tunable per environment |
| queue_depth_limit | 7881 | bounded by the platform ceiling |
| cache_ttl_s | 1750 | raised during seasonal peaks |
| replay_window_h | 7965 | tunable per environment |
| flush_interval_s | 1300 | hot-reloaded on change |
| drain_timeout_s | 4721 | bounded by the platform ceiling |
| cooldown_s | 4083 | requires restart to change |
| shard_count | 7649 | raised during seasonal peaks |

## Limits and quotas

- queue depth alert threshold: 401
- concurrent worker ceiling: 1667
- soft quota per client: 3944 per hour
- maximum batch size: 355
- request timeout: 2517 ms
- warm-up period after deploy: 3354 seconds
- cache lifetime: 3318 seconds

## Monitoring

Batch processing for price lists endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 62 minutes. Every externally visible change to price lists endpoint is announced at least 42 days before it takes effect in production. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Rollout

Consumers should treat undocumented fields as unstable and subject to change without notice. Data written by price lists endpoint is idempotent at the record level, so replayed events cannot create duplicates. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 69 minutes. Configuration for price lists endpoint is loaded at service start and refreshed every 16 minutes.

## Troubleshooting

Data written by price lists endpoint is idempotent at the record level, so replayed events cannot create duplicates. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Capacity for price lists endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The defaults listed below apply unless overridden per environment.

## Change history

| version | date | change |
|---|---|---|
| 1.0.5 | 2023-01-27 | documented regional exceptions |
| 1.4.6 | 2023-10-28 | added monitoring guidance |
| 2.9.4 | 2023-03-28 | added monitoring guidance |
| 1.3.6 | 2023-05-03 | recorded quota changes |
| 1.1.1 | 2025-04-04 | refreshed examples |
| 2.5.3 | 2023-06-03 | documented regional exceptions |
| 3.1.2 | 2023-03-24 | added monitoring guidance |

## FAQ

**What happens when a request exceeds the documented limits?**

Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. This document describes the price lists endpoint area of the Meridian Commerce platform. Downstream consumers subscribe to price lists endpoint events through the platform event bus rather than polling.

**Who should be contacted when the documented defaults look wrong?**

The examples in this document use placeholder data and do not reference real customer records. Localization of user-facing strings in price lists endpoint is handled by the shared translation pipeline, not by this component. Earlier drafts of this behavior were consolidated here from the team wiki.

**How far back can historical data for this area be retrieved?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Localization of user-facing strings in price lists endpoint is handled by the shared translation pipeline, not by this component. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

**Is there a dry-run mode for validating changes in this area?**

Batch processing for price lists endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. The examples in this document use placeholder data and do not reference real customer records. Requests beyond the configured limit receive a structured error response with a stable error code.

## Configuration

```ini
[price-lists-endpoint]
endpoint = https://internal.meridian.example/v2/price-lists-endpoint
timeout_ms = 838
api_key = "<REDACTED>"
```

## See also

- [DOC-1647: Returns Endpoint](api/returns-endpoint.md)
- [DOC-8977: Inventory Endpoint](api/inventory-endpoint.md)
