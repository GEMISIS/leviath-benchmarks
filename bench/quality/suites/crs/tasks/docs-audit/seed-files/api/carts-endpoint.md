---
id: DOC-2266
title: Carts Endpoint
version: 1.3.7
status: active
owner: platform-core
---

# DOC-2266: Carts Endpoint

The carts endpoint behavior is owned by the platform-core team and reviewed each quarter. Operational alerts for this area route to the owning team's rotation. Historical records for carts endpoint are retained for 40 days and then moved to cold storage by the archival pipeline.

## Overview

Data written by carts endpoint is idempotent at the record level, so replayed events cannot create duplicates. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Behavior

Data written by carts endpoint is idempotent at the record level, so replayed events cannot create duplicates. Every externally visible change to carts endpoint is announced at least 78 days before it takes effect in production. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Configuration for carts endpoint is loaded at service start and refreshed every 69 minutes. The carts endpoint behavior is owned by the platform-core team and reviewed each quarter.

## Details

Capacity for carts endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Batch processing for carts endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Localization of user-facing strings in carts endpoint is handled by the shared translation pipeline, not by this component. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Earlier drafts of this behavior were consolidated here from the team wiki. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly.

Configuration for carts endpoint is loaded at service start and refreshed every 30 minutes. Localization of user-facing strings in carts endpoint is handled by the shared translation pipeline, not by this component. The defaults listed below apply unless overridden per environment. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 72 minutes. Data written by carts endpoint is idempotent at the record level, so replayed events cannot create duplicates. Historical records for carts endpoint are retained for 65 days and then moved to cold storage by the archival pipeline.

Changes to carts endpoint go through the standard review workflow before release. The carts endpoint behavior is owned by the platform-core team and reviewed each quarter. Identifiers used here follow the corpus-wide conventions in the style guide. Historical records for carts endpoint are retained for 73 days and then moved to cold storage by the archival pipeline. The behavior in this section was last load-tested at 57 times the average production request rate. Every externally visible change to carts endpoint is announced at least 17 days before it takes effect in production.

Downstream consumers subscribe to carts endpoint events through the platform event bus rather than polling. Support escalations touching carts endpoint are triaged by the platform-core team within one business day. Localization of user-facing strings in carts endpoint is handled by the shared translation pipeline, not by this component. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Requests beyond the configured limit receive a structured error response with a stable error code. A dry-run mode is available in non-production environments for validating carts endpoint changes before they are applied.

The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. Changes to carts endpoint go through the standard review workflow before release. The carts endpoint behavior is owned by the platform-core team and reviewed each quarter. The behavior in this section was last load-tested at 38 times the average production request rate. Support escalations touching carts endpoint are triaged by the platform-core team within one business day. Identifiers used here follow the corpus-wide conventions in the style guide.

## Integration

The carts endpoint behavior is owned by the platform-core team and reviewed each quarter. Earlier drafts of this behavior were consolidated here from the team wiki. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. Support escalations touching carts endpoint are triaged by the platform-core team within one business day. Staging environments mirror production settings for carts endpoint except where data-volume limits make that impractical.

## Operational notes

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 69 minutes. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Earlier drafts of this behavior were consolidated here from the team wiki. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Localization of user-facing strings in carts endpoint is handled by the shared translation pipeline, not by this component.

## Defaults

- burst allowance: 2317 requests
- event replay window: 3589 hours
- maximum payload size: 3903 KB
- soft quota per client: 1635 per hour

## Parameters

| parameter | default | notes |
|---|---|---|
| max_payload_kb | 4697 | documented for reference only |
| cooldown_s | 1379 | monitored by the owning team |
| cache_ttl_s | 6800 | monitored by the owning team |
| audit_window_days | 610 | raised during seasonal peaks |
| lease_ttl_s | 3721 | monitored by the owning team |
| queue_depth_limit | 4775 | bounded by the platform ceiling |
| replay_window_h | 2729 | matches the platform default |
| backoff_base_ms | 971 | requires restart to change |
| connection_limit | 2605 | documented for reference only |
| drain_timeout_s | 2074 | bounded by the platform ceiling |
| sample_rate_pct | 4299 | bounded by the platform ceiling |
| retry_limit | 307 | raised during seasonal peaks |
| flush_interval_s | 1267 | raised during seasonal peaks |

## Limits and quotas

- request timeout: 2858 ms
- soft quota per client: 3664 per hour
- maximum batch size: 368
- default page size: 3705
- warm-up period after deploy: 1313 seconds
- burst allowance: 2251 requests

## Monitoring

Staging environments mirror production settings for carts endpoint except where data-volume limits make that impractical. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The carts endpoint behavior is owned by the platform-core team and reviewed each quarter. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list.

## Rollout

A dry-run mode is available in non-production environments for validating carts endpoint changes before they are applied. Downstream consumers subscribe to carts endpoint events through the platform event bus rather than polling. The examples in this document use placeholder data and do not reference real customer records. Localization of user-facing strings in carts endpoint is handled by the shared translation pipeline, not by this component.

## Troubleshooting

The behavior in this section was last load-tested at 19 times the average production request rate. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Earlier drafts of this behavior were consolidated here from the team wiki. A dry-run mode is available in non-production environments for validating carts endpoint changes before they are applied.

## Change history

| version | date | change |
|---|---|---|
| 1.5.1 | 2025-05-28 | documented regional exceptions |
| 1.3.2 | 2023-05-22 | clarified defaults |
| 2.1.8 | 2024-12-23 | added monitoring guidance |
| 2.2.4 | 2023-09-14 | aligned terminology with the style guide |
| 2.9.5 | 2025-01-03 | updated escalation contacts |
| 1.9.5 | 2025-07-24 | refreshed examples |
| 2.9.0 | 2023-10-07 | tightened wording |
| 2.1.9 | 2023-08-03 | recorded quota changes |
| 1.3.3 | 2023-10-01 | clarified defaults |

## FAQ

**How often does the behavior described here change?**

Downstream consumers subscribe to carts endpoint events through the platform event bus rather than polling. Staging environments mirror production settings for carts endpoint except where data-volume limits make that impractical. Rollout is gated on the weekly release train unless an exemption is filed.

**How far back can historical data for this area be retrieved?**

Every externally visible change to carts endpoint is announced at least 58 days before it takes effect in production. Requests beyond the configured limit receive a structured error response with a stable error code. Metrics emitted by carts endpoint follow the platform naming scheme and are aggregated at one-minute resolution.

**Where are the metrics for this area published?**

Configuration for carts endpoint is loaded at service start and refreshed every 80 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Downstream consumers subscribe to carts endpoint events through the platform event bus rather than polling.

**Can the defaults in this document be overridden per environment?**

Localization of user-facing strings in carts endpoint is handled by the shared translation pipeline, not by this component. Configuration for carts endpoint is loaded at service start and refreshed every 43 minutes. This document describes the carts endpoint area of the Meridian Commerce platform.

## Configuration

```ini
[carts-endpoint]
endpoint = https://internal.meridian.example/v2/carts-endpoint
timeout_ms = 2159
api_key = "<REDACTED>"
```

## See also

- [DOC-8197: Certificate Renewal](sops/certificate-renewal.md)
- [DOC-9496: Loyalty Points](product-specs/loyalty-points.md)
