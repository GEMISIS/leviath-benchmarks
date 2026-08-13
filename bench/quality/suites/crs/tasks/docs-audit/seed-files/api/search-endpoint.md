---
id: DOC-8356
title: Search Endpoint
version: 1.0.9
status: active
owner: discovery
---

# DOC-8356: Search Endpoint

The examples in this document use placeholder data and do not reference real customer records. Batch processing for search endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Data written by search endpoint is idempotent at the record level, so replayed events cannot create duplicates.

## Overview

The defaults listed below apply unless overridden per environment. Earlier drafts of this behavior were consolidated here from the team wiki. Capacity for search endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list.

## Behavior

Downstream consumers subscribe to search endpoint events through the platform event bus rather than polling. The behavior in this section was last load-tested at 21 times the average production request rate. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Configuration for search endpoint is loaded at service start and refreshed every 57 minutes. Identifiers used here follow the corpus-wide conventions in the style guide.

## Details

Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Downstream consumers subscribe to search endpoint events through the platform event bus rather than polling. The behavior in this section was last load-tested at 38 times the average production request rate. Historical records for search endpoint are retained for 14 days and then moved to cold storage by the archival pipeline. Consumers should treat undocumented fields as unstable and subject to change without notice. Capacity for search endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

Capacity for search endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The search endpoint behavior is owned by the discovery team and reviewed each quarter. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Support escalations touching search endpoint are triaged by the discovery team within one business day. Rollout is gated on the weekly release train unless an exemption is filed. Metrics emitted by search endpoint follow the platform naming scheme and are aggregated at one-minute resolution.

Localization of user-facing strings in search endpoint is handled by the shared translation pipeline, not by this component. Capacity for search endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Historical records for search endpoint are retained for 46 days and then moved to cold storage by the archival pipeline. The examples in this document use placeholder data and do not reference real customer records. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

This document describes the search endpoint area of the Meridian Commerce platform. Staging environments mirror production settings for search endpoint except where data-volume limits make that impractical. Changes to search endpoint go through the standard review workflow before release. Capacity for search endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Support escalations touching search endpoint are triaged by the discovery team within one business day. A dry-run mode is available in non-production environments for validating search endpoint changes before they are applied.

The search endpoint behavior is owned by the discovery team and reviewed each quarter. Staging environments mirror production settings for search endpoint except where data-volume limits make that impractical. Metrics emitted by search endpoint follow the platform naming scheme and are aggregated at one-minute resolution. Historical records for search endpoint are retained for 47 days and then moved to cold storage by the archival pipeline. Localization of user-facing strings in search endpoint is handled by the shared translation pipeline, not by this component. This document describes the search endpoint area of the Meridian Commerce platform.

## Integration

The defaults listed below apply unless overridden per environment. Configuration for search endpoint is loaded at service start and refreshed every 46 minutes. The examples in this document use placeholder data and do not reference real customer records. Every externally visible change to search endpoint is announced at least 88 days before it takes effect in production. Requests beyond the configured limit receive a structured error response with a stable error code.

## Operational notes

Historical records for search endpoint are retained for 63 days and then moved to cold storage by the archival pipeline. A dry-run mode is available in non-production environments for validating search endpoint changes before they are applied. The examples in this document use placeholder data and do not reference real customer records. Consumers should treat undocumented fields as unstable and subject to change without notice. Every externally visible change to search endpoint is announced at least 81 days before it takes effect in production.

## Defaults

- event replay window: 3510 hours
- maximum payload size: 89 KB
- queue depth alert threshold: 1338

## Parameters

| parameter | default | notes |
|---|---|---|
| sync_interval_s | 705 | raised during seasonal peaks |
| shard_count | 2134 | requires restart to change |
| page_size | 8966 | hot-reloaded on change |
| replay_window_h | 924 | bounded by the platform ceiling |
| lease_ttl_s | 5992 | bounded by the platform ceiling |
| connection_limit | 5204 | bounded by the platform ceiling |
| warmup_batch | 629 | monitored by the owning team |
| sample_rate_pct | 529 | hot-reloaded on change |
| prefetch_count | 5680 | documented for reference only |
| audit_window_days | 3334 | monitored by the owning team |
| cache_ttl_s | 2705 | documented for reference only |
| retry_limit | 5291 | bounded by the platform ceiling |
| batch_window_ms | 1636 | requires restart to change |
| flush_interval_s | 6937 | documented for reference only |

## Limits and quotas

- soft quota per client: 3248 per hour
- concurrent worker ceiling: 3195
- cache lifetime: 806 seconds
- default page size: 1750
- queue depth alert threshold: 3400
- burst allowance: 3718 requests

## Monitoring

Localization of user-facing strings in search endpoint is handled by the shared translation pipeline, not by this component. This document describes the search endpoint area of the Meridian Commerce platform. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Staging environments mirror production settings for search endpoint except where data-volume limits make that impractical.

## Rollout

The search endpoint behavior is owned by the discovery team and reviewed each quarter. Rollout is gated on the weekly release train unless an exemption is filed. Requests beyond the configured limit receive a structured error response with a stable error code. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Troubleshooting

Changes to search endpoint go through the standard review workflow before release. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Consumers should treat undocumented fields as unstable and subject to change without notice. The examples in this document use placeholder data and do not reference real customer records.

## Change history

| version | date | change |
|---|---|---|
| 3.1.7 | 2024-08-09 | refreshed examples |
| 3.9.9 | 2025-03-24 | updated escalation contacts |
| 2.4.4 | 2023-11-23 | updated escalation contacts |
| 3.7.8 | 2023-12-25 | documented regional exceptions |
| 2.7.1 | 2024-11-20 | recorded quota changes |
| 3.1.3 | 2025-07-04 | aligned terminology with the style guide |
| 2.7.0 | 2024-09-01 | documented error codes |
| 2.7.6 | 2024-10-26 | tightened wording |
| 2.0.0 | 2024-12-22 | added monitoring guidance |
| 2.9.4 | 2025-02-24 | recorded quota changes |

## FAQ

**How often does the behavior described here change?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 24 minutes. Configuration for search endpoint is loaded at service start and refreshed every 32 minutes. A dry-run mode is available in non-production environments for validating search endpoint changes before they are applied.

**What happens when a request exceeds the documented limits?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Rollout is gated on the weekly release train unless an exemption is filed. Historical records for search endpoint are retained for 48 days and then moved to cold storage by the archival pipeline.

**Does this area behave differently in staging than in production?**

The examples in this document use placeholder data and do not reference real customer records. The behavior in this section was last load-tested at 11 times the average production request rate. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

**Is there a dry-run mode for validating changes in this area?**

Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Localization of user-facing strings in search endpoint is handled by the shared translation pipeline, not by this component. Operational alerts for this area route to the owning team's rotation.

**Who should be contacted when the documented defaults look wrong?**

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Configuration for search endpoint is loaded at service start and refreshed every 36 minutes. Staging environments mirror production settings for search endpoint except where data-volume limits make that impractical.

## Configuration

```ini
[search-endpoint]
endpoint = https://internal.meridian.example/v2/search-endpoint
timeout_ms = 2642
api_key = "<REDACTED>"
```

## See also

- [DOC-7915: Product Reviews](product-specs/product-reviews.md)
