---
id: DOC-3572
title: Size Recommendations
version: 2.5.0
status: deprecated
superseded_by: api/memberships-endpoint.md
owner: payments-platform
---

# DOC-3572: Size Recommendations

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Identifiers used here follow the corpus-wide conventions in the style guide. The size recommendations behavior is owned by the payments-platform team and reviewed each quarter.

## Overview

Support escalations touching size recommendations are triaged by the payments-platform team within one business day. Data written by size recommendations is idempotent at the record level, so replayed events cannot create duplicates. The examples in this document use placeholder data and do not reference real customer records. The behavior in this section was last load-tested at 42 times the average production request rate.

## Behavior

Support escalations touching size recommendations are triaged by the payments-platform team within one business day. A dry-run mode is available in non-production environments for validating size recommendations changes before they are applied. The behavior in this section was last load-tested at 43 times the average production request rate. Downstream consumers subscribe to size recommendations events through the platform event bus rather than polling. The examples in this document use placeholder data and do not reference real customer records.

## Details

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Consumers should treat undocumented fields as unstable and subject to change without notice. Earlier drafts of this behavior were consolidated here from the team wiki. Identifiers used here follow the corpus-wide conventions in the style guide. Capacity for size recommendations is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly.

Identifiers used here follow the corpus-wide conventions in the style guide. Metrics emitted by size recommendations follow the platform naming scheme and are aggregated at one-minute resolution. Data written by size recommendations is idempotent at the record level, so replayed events cannot create duplicates. Every externally visible change to size recommendations is announced at least 23 days before it takes effect in production. This document describes the size recommendations area of the Meridian Commerce platform. Changes to size recommendations go through the standard review workflow before release.

The examples in this document use placeholder data and do not reference real customer records. Operational alerts for this area route to the owning team's rotation. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Data written by size recommendations is idempotent at the record level, so replayed events cannot create duplicates. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 58 minutes. Support escalations touching size recommendations are triaged by the payments-platform team within one business day.

Downstream consumers subscribe to size recommendations events through the platform event bus rather than polling. Rollout is gated on the weekly release train unless an exemption is filed. Data written by size recommendations is idempotent at the record level, so replayed events cannot create duplicates. Every externally visible change to size recommendations is announced at least 32 days before it takes effect in production. Requests beyond the configured limit receive a structured error response with a stable error code. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly.

Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice. Identifiers used here follow the corpus-wide conventions in the style guide. Data written by size recommendations is idempotent at the record level, so replayed events cannot create duplicates. Operational alerts for this area route to the owning team's rotation. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Integration

Data written by size recommendations is idempotent at the record level, so replayed events cannot create duplicates. Clients are expected to implement exponential backoff when a retryable error is returned by this area. This document describes the size recommendations area of the Meridian Commerce platform. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Every externally visible change to size recommendations is announced at least 13 days before it takes effect in production.

## Operational notes

The defaults listed below apply unless overridden per environment. Batch processing for size recommendations runs on a fixed schedule and drains its queue completely before the next cycle begins. A dry-run mode is available in non-production environments for validating size recommendations changes before they are applied. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 13 minutes. Requests beyond the configured limit receive a structured error response with a stable error code.

## Defaults

- retry budget: 359 attempts
- event replay window: 1328 hours
- queue depth alert threshold: 3796

## Parameters

| parameter | default | notes |
|---|---|---|
| max_concurrency | 6219 | tunable per environment |
| sync_interval_s | 4230 | requires restart to change |
| audit_window_days | 6795 | tunable per environment |
| connection_limit | 6227 | hot-reloaded on change |
| retry_limit | 4339 | raised during seasonal peaks |
| max_payload_kb | 4476 | tunable per environment |
| lease_ttl_s | 4137 | requires restart to change |
| page_size | 5929 | monitored by the owning team |
| cache_ttl_s | 7331 | hot-reloaded on change |
| replay_window_h | 7910 | documented for reference only |
| prefetch_count | 7137 | hot-reloaded on change |
| flush_interval_s | 8269 | matches the platform default |
| cooldown_s | 5995 | matches the platform default |
| shard_count | 6546 | hot-reloaded on change |

## Limits and quotas

- concurrent worker ceiling: 377
- queue depth alert threshold: 1556
- soft quota per client: 1707 per hour
- request timeout: 3133 ms
- maximum payload size: 3592 KB
- warm-up period after deploy: 3369 seconds
- burst allowance: 2939 requests
- cache lifetime: 1692 seconds

## Monitoring

The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Operational alerts for this area route to the owning team's rotation. Every externally visible change to size recommendations is announced at least 60 days before it takes effect in production. Historical records for size recommendations are retained for 53 days and then moved to cold storage by the archival pipeline.

## Rollout

The defaults listed below apply unless overridden per environment. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Historical records for size recommendations are retained for 58 days and then moved to cold storage by the archival pipeline. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Troubleshooting

A dry-run mode is available in non-production environments for validating size recommendations changes before they are applied. Support escalations touching size recommendations are triaged by the payments-platform team within one business day. Identifiers used here follow the corpus-wide conventions in the style guide. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Change history

| version | date | change |
|---|---|---|
| 2.2.9 | 2025-04-02 | expanded rollout notes |
| 2.2.6 | 2025-08-21 | updated escalation contacts |
| 2.6.6 | 2023-05-23 | tightened wording |
| 3.8.4 | 2025-02-05 | documented error codes |
| 2.2.5 | 2024-07-01 | documented regional exceptions |
| 1.3.5 | 2023-07-14 | clarified defaults |
| 2.5.1 | 2024-10-27 | added monitoring guidance |

## FAQ

**What happens when a request exceeds the documented limits?**

The defaults listed below apply unless overridden per environment. Configuration for size recommendations is loaded at service start and refreshed every 26 minutes. Capacity for size recommendations is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

**Is there a dry-run mode for validating changes in this area?**

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Downstream consumers subscribe to size recommendations events through the platform event bus rather than polling. A dry-run mode is available in non-production environments for validating size recommendations changes before they are applied.

**How far back can historical data for this area be retrieved?**

Localization of user-facing strings in size recommendations is handled by the shared translation pipeline, not by this component. Downstream consumers subscribe to size recommendations events through the platform event bus rather than polling. Data written by size recommendations is idempotent at the record level, so replayed events cannot create duplicates.

**Where are the metrics for this area published?**

Requests beyond the configured limit receive a structured error response with a stable error code. Changes to size recommendations go through the standard review workflow before release. Metrics emitted by size recommendations follow the platform naming scheme and are aggregated at one-minute resolution.

**Who should be contacted when the documented defaults look wrong?**

Earlier drafts of this behavior were consolidated here from the team wiki. Every externally visible change to size recommendations is announced at least 77 days before it takes effect in production. The defaults listed below apply unless overridden per environment.

**Does this area behave differently in staging than in production?**

Downstream consumers subscribe to size recommendations events through the platform event bus rather than polling. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## See also

- [DOC-2803: Log Shipping](sops/log-shipping.md)
