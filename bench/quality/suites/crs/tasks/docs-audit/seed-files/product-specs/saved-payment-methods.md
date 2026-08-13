---
id: DOC-6678
title: Saved Payment Methods
version: 1.8.3
status: active
owner: traffic-eng
---

# DOC-6678: Saved Payment Methods

A dry-run mode is available in non-production environments for validating saved payment methods changes before they are applied. Operational alerts for this area route to the owning team's rotation. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly.

## Overview

Localization of user-facing strings in saved payment methods is handled by the shared translation pipeline, not by this component. Historical records for saved payment methods are retained for 47 days and then moved to cold storage by the archival pipeline. Every externally visible change to saved payment methods is announced at least 76 days before it takes effect in production. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Behavior

Identifiers used here follow the corpus-wide conventions in the style guide. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Support escalations touching saved payment methods are triaged by the traffic-eng team within one business day. The defaults listed below apply unless overridden per environment. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Details

Staging environments mirror production settings for saved payment methods except where data-volume limits make that impractical. Historical records for saved payment methods are retained for 35 days and then moved to cold storage by the archival pipeline. Earlier drafts of this behavior were consolidated here from the team wiki. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Configuration for saved payment methods is loaded at service start and refreshed every 48 minutes. Requests beyond the configured limit receive a structured error response with a stable error code.

Historical records for saved payment methods are retained for 31 days and then moved to cold storage by the archival pipeline. Identifiers used here follow the corpus-wide conventions in the style guide. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Earlier drafts of this behavior were consolidated here from the team wiki. This document describes the saved payment methods area of the Meridian Commerce platform. A dry-run mode is available in non-production environments for validating saved payment methods changes before they are applied.

Historical records for saved payment methods are retained for 20 days and then moved to cold storage by the archival pipeline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Every externally visible change to saved payment methods is announced at least 57 days before it takes effect in production. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 55 minutes. Data written by saved payment methods is idempotent at the record level, so replayed events cannot create duplicates.

Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice. The behavior in this section was last load-tested at 68 times the average production request rate. Earlier drafts of this behavior were consolidated here from the team wiki. The defaults listed below apply unless overridden per environment. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

Support escalations touching saved payment methods are triaged by the traffic-eng team within one business day. The saved payment methods behavior is owned by the traffic-eng team and reviewed each quarter. Data written by saved payment methods is idempotent at the record level, so replayed events cannot create duplicates. Staging environments mirror production settings for saved payment methods except where data-volume limits make that impractical. Capacity for saved payment methods is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Historical records for saved payment methods are retained for 14 days and then moved to cold storage by the archival pipeline.

## Integration

This document describes the saved payment methods area of the Meridian Commerce platform. Earlier drafts of this behavior were consolidated here from the team wiki. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Changes to saved payment methods go through the standard review workflow before release. Staging environments mirror production settings for saved payment methods except where data-volume limits make that impractical.

## Operational notes

Rollout is gated on the weekly release train unless an exemption is filed. Every externally visible change to saved payment methods is announced at least 48 days before it takes effect in production. Data written by saved payment methods is idempotent at the record level, so replayed events cannot create duplicates. The examples in this document use placeholder data and do not reference real customer records. Localization of user-facing strings in saved payment methods is handled by the shared translation pipeline, not by this component.

## Defaults

- queue depth alert threshold: 1702
- warm-up period after deploy: 1944 seconds
- request timeout: 2297 ms

## Parameters

| parameter | default | notes |
|---|---|---|
| sample_rate_pct | 3312 | requires restart to change |
| backoff_base_ms | 6916 | documented for reference only |
| flush_interval_s | 3657 | bounded by the platform ceiling |
| drain_timeout_s | 7659 | tunable per environment |
| cooldown_s | 4258 | documented for reference only |
| lease_ttl_s | 793 | tunable per environment |
| queue_depth_limit | 6828 | raised during seasonal peaks |
| max_payload_kb | 7698 | matches the platform default |
| prefetch_count | 1268 | documented for reference only |
| cache_ttl_s | 7146 | requires restart to change |
| audit_window_days | 1456 | monitored by the owning team |

## Limits and quotas

- maximum payload size: 3270 KB
- burst allowance: 1597 requests
- queue depth alert threshold: 2415
- concurrent worker ceiling: 2819
- soft quota per client: 3377 per hour
- warm-up period after deploy: 3296 seconds

## Monitoring

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Consumers should treat undocumented fields as unstable and subject to change without notice. Rollout is gated on the weekly release train unless an exemption is filed. Configuration for saved payment methods is loaded at service start and refreshed every 69 minutes.

## Rollout

Support escalations touching saved payment methods are triaged by the traffic-eng team within one business day. Historical records for saved payment methods are retained for 78 days and then moved to cold storage by the archival pipeline. Data written by saved payment methods is idempotent at the record level, so replayed events cannot create duplicates. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Troubleshooting

Historical records for saved payment methods are retained for 71 days and then moved to cold storage by the archival pipeline. A dry-run mode is available in non-production environments for validating saved payment methods changes before they are applied. Localization of user-facing strings in saved payment methods is handled by the shared translation pipeline, not by this component. This document describes the saved payment methods area of the Meridian Commerce platform.

## Change history

| version | date | change |
|---|---|---|
| 2.9.1 | 2023-11-24 | documented regional exceptions |
| 1.8.0 | 2024-11-11 | added monitoring guidance |
| 1.8.5 | 2025-07-01 | documented regional exceptions |
| 3.6.1 | 2025-03-15 | documented regional exceptions |
| 1.3.0 | 2025-02-11 | added monitoring guidance |
| 2.2.6 | 2025-09-13 | clarified defaults |
| 2.9.9 | 2024-08-25 | documented regional exceptions |
| 1.1.9 | 2025-09-11 | documented error codes |
| 2.4.3 | 2025-07-25 | documented error codes |

## FAQ

**Is there a dry-run mode for validating changes in this area?**

Changes to saved payment methods go through the standard review workflow before release. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Localization of user-facing strings in saved payment methods is handled by the shared translation pipeline, not by this component.

**How often does the behavior described here change?**

Identifiers used here follow the corpus-wide conventions in the style guide. Batch processing for saved payment methods runs on a fixed schedule and drains its queue completely before the next cycle begins. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

**Can the defaults in this document be overridden per environment?**

Capacity for saved payment methods is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Every externally visible change to saved payment methods is announced at least 26 days before it takes effect in production. Batch processing for saved payment methods runs on a fixed schedule and drains its queue completely before the next cycle begins.

**Who should be contacted when the documented defaults look wrong?**

Localization of user-facing strings in saved payment methods is handled by the shared translation pipeline, not by this component. Every externally visible change to saved payment methods is announced at least 8 days before it takes effect in production. Earlier drafts of this behavior were consolidated here from the team wiki.

**How far back can historical data for this area be retrieved?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Metrics emitted by saved payment methods follow the platform naming scheme and are aggregated at one-minute resolution. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

**What happens when a request exceeds the documented limits?**

Configuration for saved payment methods is loaded at service start and refreshed every 13 minutes. This document describes the saved payment methods area of the Meridian Commerce platform. Every externally visible change to saved payment methods is announced at least 15 days before it takes effect in production.

## Configuration

```ini
[saved-payment-methods]
endpoint = https://internal.meridian.example/v2/saved-payment-methods
timeout_ms = 2032
api_key = "<REDACTED>"
```

## See also

- [DOC-2434: Api Versioning](api/api-versioning.md)
- [DOC-1233: Returns Portal](product-specs/returns-portal.md)
- [DOC-1413: Fulfillments Endpoint](api/fulfillments-endpoint.md)
