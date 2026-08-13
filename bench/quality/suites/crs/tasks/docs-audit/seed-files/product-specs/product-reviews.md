---
id: DOC-7915
title: Product Reviews
version: 1.7.6
status: active
owner: traffic-eng
---

# DOC-7915: Product Reviews

Every externally visible change to product reviews is announced at least 78 days before it takes effect in production. A dry-run mode is available in non-production environments for validating product reviews changes before they are applied. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly.

## Overview

Support escalations touching product reviews are triaged by the traffic-eng team within one business day. Requests beyond the configured limit receive a structured error response with a stable error code. Metrics emitted by product reviews follow the platform naming scheme and are aggregated at one-minute resolution. Configuration for product reviews is loaded at service start and refreshed every 7 minutes.

## Behavior

Staging environments mirror production settings for product reviews except where data-volume limits make that impractical. Data written by product reviews is idempotent at the record level, so replayed events cannot create duplicates. Identifiers used here follow the corpus-wide conventions in the style guide. This document describes the product reviews area of the Meridian Commerce platform. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Details

Every externally visible change to product reviews is announced at least 44 days before it takes effect in production. Downstream consumers subscribe to product reviews events through the platform event bus rather than polling. Batch processing for product reviews runs on a fixed schedule and drains its queue completely before the next cycle begins. Earlier drafts of this behavior were consolidated here from the team wiki. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Configuration for product reviews is loaded at service start and refreshed every 12 minutes.

The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 29 minutes. Every externally visible change to product reviews is announced at least 17 days before it takes effect in production. Consumers should treat undocumented fields as unstable and subject to change without notice. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Staging environments mirror production settings for product reviews except where data-volume limits make that impractical.

Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. This document describes the product reviews area of the Meridian Commerce platform. The behavior in this section was last load-tested at 71 times the average production request rate. Support escalations touching product reviews are triaged by the traffic-eng team within one business day. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Metrics emitted by product reviews follow the platform naming scheme and are aggregated at one-minute resolution.

The examples in this document use placeholder data and do not reference real customer records. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 32 minutes. Downstream consumers subscribe to product reviews events through the platform event bus rather than polling. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Operational alerts for this area route to the owning team's rotation.

Operational alerts for this area route to the owning team's rotation. The defaults listed below apply unless overridden per environment. Historical records for product reviews are retained for 46 days and then moved to cold storage by the archival pipeline. Every externally visible change to product reviews is announced at least 61 days before it takes effect in production. A dry-run mode is available in non-production environments for validating product reviews changes before they are applied. Data written by product reviews is idempotent at the record level, so replayed events cannot create duplicates.

## Integration

The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 49 minutes. The defaults listed below apply unless overridden per environment. Batch processing for product reviews runs on a fixed schedule and drains its queue completely before the next cycle begins. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Operational notes

Staging environments mirror production settings for product reviews except where data-volume limits make that impractical. A dry-run mode is available in non-production environments for validating product reviews changes before they are applied. Operational alerts for this area route to the owning team's rotation. The defaults listed below apply unless overridden per environment. Metrics emitted by product reviews follow the platform naming scheme and are aggregated at one-minute resolution.

## Defaults

- maximum batch size: 2922
- queue depth alert threshold: 1356
- soft quota per client: 1979 per hour
- default page size: 1698

## Parameters

| parameter | default | notes |
|---|---|---|
| connection_limit | 45 | tunable per environment |
| drain_timeout_s | 3226 | tunable per environment |
| lease_ttl_s | 7110 | requires restart to change |
| max_payload_kb | 2647 | documented for reference only |
| page_size | 521 | hot-reloaded on change |
| warmup_batch | 8302 | hot-reloaded on change |
| shard_count | 6841 | hot-reloaded on change |
| sample_rate_pct | 6960 | matches the platform default |
| prefetch_count | 6673 | hot-reloaded on change |
| cache_ttl_s | 8651 | raised during seasonal peaks |

## Limits and quotas

- maximum payload size: 1678 KB
- maximum batch size: 2552
- request timeout: 1395 ms
- cache lifetime: 2419 seconds
- default page size: 2513
- retry budget: 2734 attempts
- concurrent worker ceiling: 90

## Monitoring

Earlier drafts of this behavior were consolidated here from the team wiki. Metrics emitted by product reviews follow the platform naming scheme and are aggregated at one-minute resolution. Support escalations touching product reviews are triaged by the traffic-eng team within one business day. Identifiers used here follow the corpus-wide conventions in the style guide.

## Rollout

Capacity for product reviews is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Changes to product reviews go through the standard review workflow before release. The product reviews behavior is owned by the traffic-eng team and reviewed each quarter. Configuration for product reviews is loaded at service start and refreshed every 88 minutes.

## Troubleshooting

This document describes the product reviews area of the Meridian Commerce platform. The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. A dry-run mode is available in non-production environments for validating product reviews changes before they are applied. Metrics emitted by product reviews follow the platform naming scheme and are aggregated at one-minute resolution.

## Change history

| version | date | change |
|---|---|---|
| 2.5.1 | 2023-02-14 | documented regional exceptions |
| 1.6.5 | 2025-05-19 | aligned terminology with the style guide |
| 3.5.6 | 2024-10-14 | documented error codes |
| 1.2.7 | 2024-01-09 | tightened wording |
| 1.9.5 | 2024-01-10 | tightened wording |
| 3.1.7 | 2024-08-02 | aligned terminology with the style guide |
| 3.1.6 | 2024-10-27 | expanded rollout notes |
| 2.0.0 | 2023-08-15 | updated escalation contacts |
| 1.8.0 | 2024-12-09 | documented regional exceptions |
| 2.4.0 | 2024-04-23 | documented error codes |

## FAQ

**How often does the behavior described here change?**

Operational alerts for this area route to the owning team's rotation. The defaults listed below apply unless overridden per environment. Consumers should treat undocumented fields as unstable and subject to change without notice.

**Does this area behave differently in staging than in production?**

Localization of user-facing strings in product reviews is handled by the shared translation pipeline, not by this component. Downstream consumers subscribe to product reviews events through the platform event bus rather than polling. Historical records for product reviews are retained for 89 days and then moved to cold storage by the archival pipeline.

**Is there a dry-run mode for validating changes in this area?**

Localization of user-facing strings in product reviews is handled by the shared translation pipeline, not by this component. Identifiers used here follow the corpus-wide conventions in the style guide. The product reviews behavior is owned by the traffic-eng team and reviewed each quarter.

**Where are the metrics for this area published?**

Changes to product reviews go through the standard review workflow before release. Identifiers used here follow the corpus-wide conventions in the style guide. The examples in this document use placeholder data and do not reference real customer records.

**Can the defaults in this document be overridden per environment?**

The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Batch processing for product reviews runs on a fixed schedule and drains its queue completely before the next cycle begins.

**What happens when a request exceeds the documented limits?**

This document describes the product reviews area of the Meridian Commerce platform. The defaults listed below apply unless overridden per environment. Changes to product reviews go through the standard review workflow before release.

## See also

- [DOC-8356: Search Endpoint](api/search-endpoint.md)
- [DOC-6916: Traffic Ramp](sops/traffic-ramp.md)
