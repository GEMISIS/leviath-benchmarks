---
id: DOC-2269
title: Schema Migration
version: 3.5.7
status: active
owner: identity
---

# DOC-2269: Schema Migration

A dry-run mode is available in non-production environments for validating schema migration changes before they are applied. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Localization of user-facing strings in schema migration is handled by the shared translation pipeline, not by this component.

## Overview

A dry-run mode is available in non-production environments for validating schema migration changes before they are applied. Downstream consumers subscribe to schema migration events through the platform event bus rather than polling. The defaults listed below apply unless overridden per environment. Batch processing for schema migration runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Behavior

The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Metrics emitted by schema migration follow the platform naming scheme and are aggregated at one-minute resolution. Support escalations touching schema migration are triaged by the identity team within one business day. Requests beyond the configured limit receive a structured error response with a stable error code. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Details

This document describes the schema migration area of the Meridian Commerce platform. Capacity for schema migration is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The schema migration behavior is owned by the identity team and reviewed each quarter. Every externally visible change to schema migration is announced at least 74 days before it takes effect in production. Localization of user-facing strings in schema migration is handled by the shared translation pipeline, not by this component. Staging environments mirror production settings for schema migration except where data-volume limits make that impractical.

This document describes the schema migration area of the Meridian Commerce platform. The examples in this document use placeholder data and do not reference real customer records. Capacity for schema migration is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The schema migration behavior is owned by the identity team and reviewed each quarter. Consumers should treat undocumented fields as unstable and subject to change without notice.

Consumers should treat undocumented fields as unstable and subject to change without notice. Capacity for schema migration is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Configuration for schema migration is loaded at service start and refreshed every 75 minutes. A dry-run mode is available in non-production environments for validating schema migration changes before they are applied. The behavior in this section was last load-tested at 43 times the average production request rate. Access to administrative operations in this area is restricted to members of the identity group and audited monthly.

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Support escalations touching schema migration are triaged by the identity team within one business day. Every externally visible change to schema migration is announced at least 57 days before it takes effect in production. This document describes the schema migration area of the Meridian Commerce platform. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

Identifiers used here follow the corpus-wide conventions in the style guide. Operational alerts for this area route to the owning team's rotation. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. The schema migration behavior is owned by the identity team and reviewed each quarter. The behavior in this section was last load-tested at 82 times the average production request rate. Localization of user-facing strings in schema migration is handled by the shared translation pipeline, not by this component.

## Integration

Data written by schema migration is idempotent at the record level, so replayed events cannot create duplicates. Consumers should treat undocumented fields as unstable and subject to change without notice. Staging environments mirror production settings for schema migration except where data-volume limits make that impractical. Support escalations touching schema migration are triaged by the identity team within one business day. Identifiers used here follow the corpus-wide conventions in the style guide.

## Operational notes

Support escalations touching schema migration are triaged by the identity team within one business day. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. The schema migration behavior is owned by the identity team and reviewed each quarter. Rollout is gated on the weekly release train unless an exemption is filed. Requests beyond the configured limit receive a structured error response with a stable error code.

## Defaults

- burst allowance: 1543 requests
- retry budget: 1097 attempts
- default page size: 3670

## Parameters

| parameter | default | notes |
|---|---|---|
| connection_limit | 4104 | raised during seasonal peaks |
| shard_count | 6767 | tunable per environment |
| sample_rate_pct | 3967 | hot-reloaded on change |
| queue_depth_limit | 6620 | hot-reloaded on change |
| prefetch_count | 2206 | matches the platform default |
| max_payload_kb | 2040 | matches the platform default |
| cache_ttl_s | 5463 | bounded by the platform ceiling |
| flush_interval_s | 4025 | documented for reference only |
| drain_timeout_s | 4481 | monitored by the owning team |
| sync_interval_s | 5455 | requires restart to change |

## Limits and quotas

- request timeout: 1242 ms
- cache lifetime: 2351 seconds
- default page size: 2314
- queue depth alert threshold: 3425
- burst allowance: 3393 requests
- soft quota per client: 2430 per hour
- maximum batch size: 1825

## Monitoring

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Historical records for schema migration are retained for 51 days and then moved to cold storage by the archival pipeline. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Earlier drafts of this behavior were consolidated here from the team wiki.

## Rollout

Requests beyond the configured limit receive a structured error response with a stable error code. Downstream consumers subscribe to schema migration events through the platform event bus rather than polling. Batch processing for schema migration runs on a fixed schedule and drains its queue completely before the next cycle begins. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Troubleshooting

Metrics emitted by schema migration follow the platform naming scheme and are aggregated at one-minute resolution. The behavior in this section was last load-tested at 53 times the average production request rate. Historical records for schema migration are retained for 19 days and then moved to cold storage by the archival pipeline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Change history

| version | date | change |
|---|---|---|
| 2.2.8 | 2024-06-06 | added monitoring guidance |
| 2.5.9 | 2025-03-23 | recorded quota changes |
| 1.6.4 | 2025-04-17 | recorded quota changes |
| 2.2.1 | 2024-06-25 | expanded rollout notes |
| 1.6.1 | 2024-10-05 | tightened wording |
| 1.9.1 | 2024-02-08 | documented error codes |
| 1.4.2 | 2025-07-08 | updated escalation contacts |
| 1.5.2 | 2023-01-26 | updated escalation contacts |
| 1.2.3 | 2025-12-06 | added monitoring guidance |
| 3.9.6 | 2024-11-09 | tightened wording |

## FAQ

**What happens when a request exceeds the documented limits?**

Changes to schema migration go through the standard review workflow before release. Data written by schema migration is idempotent at the record level, so replayed events cannot create duplicates. Metrics emitted by schema migration follow the platform naming scheme and are aggregated at one-minute resolution.

**Who should be contacted when the documented defaults look wrong?**

The schema migration behavior is owned by the identity team and reviewed each quarter. Identifiers used here follow the corpus-wide conventions in the style guide. The behavior in this section was last load-tested at 76 times the average production request rate.

**Does this area behave differently in staging than in production?**

Earlier drafts of this behavior were consolidated here from the team wiki. Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for schema migration is loaded at service start and refreshed every 70 minutes.

**Where are the metrics for this area published?**

Support escalations touching schema migration are triaged by the identity team within one business day. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 37 minutes. Configuration for schema migration is loaded at service start and refreshed every 27 minutes.

**How far back can historical data for this area be retrieved?**

Every externally visible change to schema migration is announced at least 24 days before it takes effect in production. Rollout is gated on the weekly release train unless an exemption is filed. A dry-run mode is available in non-production environments for validating schema migration changes before they are applied.

**Is there a dry-run mode for validating changes in this area?**

The schema migration behavior is owned by the identity team and reviewed each quarter. Downstream consumers subscribe to schema migration events through the platform event bus rather than polling. Historical records for schema migration are retained for 17 days and then moved to cold storage by the archival pipeline.

## See also

- [DOC-2195: Catalog Endpoint](api/catalog-endpoint.md)
- [DOC-7401: Exports Endpoint](api/exports-endpoint.md)
- [DOC-6349: Coupons Endpoint](api/coupons-endpoint.md)
