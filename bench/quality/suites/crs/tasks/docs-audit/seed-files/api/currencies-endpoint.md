---
id: DOC-8681
title: Currencies Endpoint
version: 3.5.0
status: active
owner: platform-core
---

# DOC-8681: Currencies Endpoint

This document describes the currencies endpoint area of the Meridian Commerce platform. Data written by currencies endpoint is idempotent at the record level, so replayed events cannot create duplicates. The behavior in this section was last load-tested at 80 times the average production request rate.

## Overview

The behavior in this section was last load-tested at 46 times the average production request rate. Batch processing for currencies endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Historical records for currencies endpoint are retained for 54 days and then moved to cold storage by the archival pipeline. Identifiers used here follow the corpus-wide conventions in the style guide.

## Behavior

Consumers should treat undocumented fields as unstable and subject to change without notice. The behavior in this section was last load-tested at 22 times the average production request rate. The examples in this document use placeholder data and do not reference real customer records. Batch processing for currencies endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. A dry-run mode is available in non-production environments for validating currencies endpoint changes before they are applied.

## Details

Downstream consumers subscribe to currencies endpoint events through the platform event bus rather than polling. The behavior in this section was last load-tested at 78 times the average production request rate. A dry-run mode is available in non-production environments for validating currencies endpoint changes before they are applied. Every externally visible change to currencies endpoint is announced at least 58 days before it takes effect in production. Localization of user-facing strings in currencies endpoint is handled by the shared translation pipeline, not by this component. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list.

The behavior in this section was last load-tested at 89 times the average production request rate. The defaults listed below apply unless overridden per environment. Changes to currencies endpoint go through the standard review workflow before release. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Consumers should treat undocumented fields as unstable and subject to change without notice.

Operational alerts for this area route to the owning team's rotation. The currencies endpoint behavior is owned by the platform-core team and reviewed each quarter. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 83 minutes. The behavior in this section was last load-tested at 13 times the average production request rate. Every externally visible change to currencies endpoint is announced at least 12 days before it takes effect in production. The defaults listed below apply unless overridden per environment.

Rollout is gated on the weekly release train unless an exemption is filed. Requests beyond the configured limit receive a structured error response with a stable error code. Operational alerts for this area route to the owning team's rotation. Support escalations touching currencies endpoint are triaged by the platform-core team within one business day. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

Consumers should treat undocumented fields as unstable and subject to change without notice. The defaults listed below apply unless overridden per environment. Staging environments mirror production settings for currencies endpoint except where data-volume limits make that impractical. Support escalations touching currencies endpoint are triaged by the platform-core team within one business day. Downstream consumers subscribe to currencies endpoint events through the platform event bus rather than polling. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list.

## Integration

Support escalations touching currencies endpoint are triaged by the platform-core team within one business day. This document describes the currencies endpoint area of the Meridian Commerce platform. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. Capacity for currencies endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Localization of user-facing strings in currencies endpoint is handled by the shared translation pipeline, not by this component.

## Operational notes

Operational alerts for this area route to the owning team's rotation. Earlier drafts of this behavior were consolidated here from the team wiki. The defaults listed below apply unless overridden per environment. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. This document describes the currencies endpoint area of the Meridian Commerce platform.

## Defaults

- default page size: 680
- cache lifetime: 1390 seconds
- concurrent worker ceiling: 3849
- maximum batch size: 1999

## Parameters

| parameter | default | notes |
|---|---|---|
| drain_timeout_s | 1074 | monitored by the owning team |
| lease_ttl_s | 970 | documented for reference only |
| warmup_batch | 6058 | hot-reloaded on change |
| cache_ttl_s | 8868 | requires restart to change |
| sync_interval_s | 3861 | matches the platform default |
| batch_window_ms | 8146 | bounded by the platform ceiling |
| sample_rate_pct | 1034 | bounded by the platform ceiling |
| shard_count | 533 | tunable per environment |
| backoff_base_ms | 4220 | documented for reference only |
| replay_window_h | 554 | bounded by the platform ceiling |
| queue_depth_limit | 7558 | monitored by the owning team |
| retry_limit | 7774 | raised during seasonal peaks |

## Limits and quotas

- warm-up period after deploy: 3376 seconds
- retry budget: 3411 attempts
- soft quota per client: 3457 per hour
- burst allowance: 2711 requests
- default page size: 283
- event replay window: 3661 hours

## Monitoring

Identifiers used here follow the corpus-wide conventions in the style guide. Batch processing for currencies endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Earlier drafts of this behavior were consolidated here from the team wiki. Operational alerts for this area route to the owning team's rotation.

## Rollout

Configuration for currencies endpoint is loaded at service start and refreshed every 77 minutes. Support escalations touching currencies endpoint are triaged by the platform-core team within one business day. Localization of user-facing strings in currencies endpoint is handled by the shared translation pipeline, not by this component. Operational alerts for this area route to the owning team's rotation.

## Troubleshooting

Earlier drafts of this behavior were consolidated here from the team wiki. Configuration for currencies endpoint is loaded at service start and refreshed every 23 minutes. Every externally visible change to currencies endpoint is announced at least 36 days before it takes effect in production. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Change history

| version | date | change |
|---|---|---|
| 3.2.7 | 2025-07-12 | added monitoring guidance |
| 1.6.0 | 2023-05-24 | clarified defaults |
| 1.2.2 | 2025-07-10 | documented regional exceptions |
| 1.8.2 | 2025-01-10 | added monitoring guidance |
| 2.9.5 | 2025-03-04 | tightened wording |
| 1.4.9 | 2025-07-17 | clarified defaults |
| 3.7.0 | 2023-11-24 | documented regional exceptions |
| 2.2.8 | 2023-05-03 | documented error codes |
| 3.7.7 | 2024-08-08 | added monitoring guidance |
| 2.3.7 | 2023-12-23 | clarified defaults |
| 2.3.7 | 2025-12-10 | added monitoring guidance |

## FAQ

**How often does the behavior described here change?**

A dry-run mode is available in non-production environments for validating currencies endpoint changes before they are applied. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 68 minutes. Support escalations touching currencies endpoint are triaged by the platform-core team within one business day.

**Where are the metrics for this area published?**

The behavior in this section was last load-tested at 59 times the average production request rate. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The examples in this document use placeholder data and do not reference real customer records.

**Who should be contacted when the documented defaults look wrong?**

A dry-run mode is available in non-production environments for validating currencies endpoint changes before they are applied. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

**How far back can historical data for this area be retrieved?**

Data written by currencies endpoint is idempotent at the record level, so replayed events cannot create duplicates. Staging environments mirror production settings for currencies endpoint except where data-volume limits make that impractical. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly.

**Is there a dry-run mode for validating changes in this area?**

Metrics emitted by currencies endpoint follow the platform naming scheme and are aggregated at one-minute resolution. The defaults listed below apply unless overridden per environment. A dry-run mode is available in non-production environments for validating currencies endpoint changes before they are applied.

**What happens when a request exceeds the documented limits?**

The defaults listed below apply unless overridden per environment. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Staging environments mirror production settings for currencies endpoint except where data-volume limits make that impractical.

## Configuration

```ini
[currencies-endpoint]
endpoint = https://internal.meridian.example/v2/currencies-endpoint
timeout_ms = 2639
api_key = "<REDACTED>"
api_key = "sk_live_6dd5f5881f19"
```

## See also

- [DOC-4877: Gift Cards](product-specs/gift-cards.md)
- [DOC-9072: Auth Tokens](api/auth-tokens.md)
- [DOC-9807: Region Evacuation](sops/region-evacuation.md)
