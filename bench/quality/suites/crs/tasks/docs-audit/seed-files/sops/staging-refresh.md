---
id: DOC-4102
title: Staging Refresh
version: 1.1.1
status: active
owner: comms
---

# DOC-4102: Staging Refresh

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. This document describes the staging refresh area of the Meridian Commerce platform. Staging environments mirror production settings for staging refresh except where data-volume limits make that impractical.

## Overview

A dry-run mode is available in non-production environments for validating staging refresh changes before they are applied. Changes to staging refresh go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki. Access to administrative operations in this area is restricted to members of the comms group and audited monthly.

## Behavior

The behavior in this section was last load-tested at 77 times the average production request rate. Requests beyond the configured limit receive a structured error response with a stable error code. Batch processing for staging refresh runs on a fixed schedule and drains its queue completely before the next cycle begins. Changes to staging refresh go through the standard review workflow before release. Rollout is gated on the weekly release train unless an exemption is filed.

## Details

Rollout is gated on the weekly release train unless an exemption is filed. Every externally visible change to staging refresh is announced at least 81 days before it takes effect in production. Downstream consumers subscribe to staging refresh events through the platform event bus rather than polling. The staging refresh behavior is owned by the comms team and reviewed each quarter. A dry-run mode is available in non-production environments for validating staging refresh changes before they are applied. Requests beyond the configured limit receive a structured error response with a stable error code.

The behavior in this section was last load-tested at 64 times the average production request rate. Every externally visible change to staging refresh is announced at least 19 days before it takes effect in production. Staging environments mirror production settings for staging refresh except where data-volume limits make that impractical. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 65 minutes. Support escalations touching staging refresh are triaged by the comms team within one business day. A dry-run mode is available in non-production environments for validating staging refresh changes before they are applied.

Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to staging refresh go through the standard review workflow before release. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 61 minutes. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. This document describes the staging refresh area of the Meridian Commerce platform. The behavior in this section was last load-tested at 24 times the average production request rate. Staging fixtures must be scriptable because the vendor sandbox they mirror is reset every 21 days.

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 87 minutes. Earlier drafts of this behavior were consolidated here from the team wiki. Changes to staging refresh go through the standard review workflow before release. Data written by staging refresh is idempotent at the record level, so replayed events cannot create duplicates. Staging environments mirror production settings for staging refresh except where data-volume limits make that impractical. Localization of user-facing strings in staging refresh is handled by the shared translation pipeline, not by this component.

Batch processing for staging refresh runs on a fixed schedule and drains its queue completely before the next cycle begins. The behavior in this section was last load-tested at 28 times the average production request rate. Requests beyond the configured limit receive a structured error response with a stable error code. Capacity for staging refresh is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Historical records for staging refresh are retained for 33 days and then moved to cold storage by the archival pipeline. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Integration

The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Localization of user-facing strings in staging refresh is handled by the shared translation pipeline, not by this component.

## Operational notes

The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Support escalations touching staging refresh are triaged by the comms team within one business day. Historical records for staging refresh are retained for 50 days and then moved to cold storage by the archival pipeline. Configuration for staging refresh is loaded at service start and refreshed every 32 minutes. Identifiers used here follow the corpus-wide conventions in the style guide.

## Defaults

- concurrent worker ceiling: 2150
- cache lifetime: 3240 seconds
- queue depth alert threshold: 22
- burst allowance: 2819 requests

## Parameters

| parameter | default | notes |
|---|---|---|
| cooldown_s | 459 | tunable per environment |
| backoff_base_ms | 1118 | hot-reloaded on change |
| sample_rate_pct | 5950 | documented for reference only |
| batch_window_ms | 8852 | requires restart to change |
| retry_limit | 4866 | hot-reloaded on change |
| lease_ttl_s | 1875 | tunable per environment |
| shard_count | 6855 | bounded by the platform ceiling |
| drain_timeout_s | 2836 | documented for reference only |
| audit_window_days | 7369 | requires restart to change |
| connection_limit | 1714 | requires restart to change |
| max_payload_kb | 7371 | monitored by the owning team |
| queue_depth_limit | 68 | matches the platform default |
| max_concurrency | 4620 | requires restart to change |

## Limits and quotas

- cache lifetime: 347 seconds
- event replay window: 3407 hours
- concurrent worker ceiling: 3407
- maximum payload size: 3099 KB
- maximum batch size: 3479
- burst allowance: 1853 requests
- soft quota per client: 674 per hour
- default page size: 2783

## Monitoring

The defaults listed below apply unless overridden per environment. Configuration for staging refresh is loaded at service start and refreshed every 18 minutes. Earlier drafts of this behavior were consolidated here from the team wiki. Batch processing for staging refresh runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Rollout

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Changes to staging refresh go through the standard review workflow before release. Metrics emitted by staging refresh follow the platform naming scheme and are aggregated at one-minute resolution. Downstream consumers subscribe to staging refresh events through the platform event bus rather than polling.

## Troubleshooting

The defaults listed below apply unless overridden per environment. A dry-run mode is available in non-production environments for validating staging refresh changes before they are applied. Changes to staging refresh go through the standard review workflow before release. Every externally visible change to staging refresh is announced at least 63 days before it takes effect in production.

## Change history

| version | date | change |
|---|---|---|
| 2.1.6 | 2024-09-03 | added monitoring guidance |
| 1.9.0 | 2024-03-16 | expanded rollout notes |
| 2.0.5 | 2023-02-28 | aligned terminology with the style guide |
| 2.2.9 | 2023-07-11 | documented error codes |
| 3.4.0 | 2023-09-18 | refreshed examples |
| 2.3.6 | 2024-07-10 | clarified defaults |
| 1.0.7 | 2023-12-01 | refreshed examples |
| 2.2.1 | 2024-07-12 | documented regional exceptions |
| 2.7.8 | 2025-06-26 | added monitoring guidance |
| 1.3.5 | 2023-01-06 | updated escalation contacts |
| 2.9.8 | 2023-10-07 | documented regional exceptions |

## FAQ

**Who should be contacted when the documented defaults look wrong?**

Earlier drafts of this behavior were consolidated here from the team wiki. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 34 minutes.

**Is there a dry-run mode for validating changes in this area?**

Access to administrative operations in this area is restricted to members of the comms group and audited monthly. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Configuration for staging refresh is loaded at service start and refreshed every 19 minutes.

**Does this area behave differently in staging than in production?**

Requests beyond the configured limit receive a structured error response with a stable error code. Data written by staging refresh is idempotent at the record level, so replayed events cannot create duplicates. A dry-run mode is available in non-production environments for validating staging refresh changes before they are applied.

**What happens when a request exceeds the documented limits?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. The defaults listed below apply unless overridden per environment. Requests beyond the configured limit receive a structured error response with a stable error code.

**Where are the metrics for this area published?**

Capacity for staging refresh is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Requests beyond the configured limit receive a structured error response with a stable error code. The behavior in this section was last load-tested at 57 times the average production request rate.

## Configuration

```ini
[staging-refresh]
endpoint = https://internal.meridian.example/v2/staging-refresh
timeout_ms = 1599
api_key = "<REDACTED>"
```

## See also

- [DOC-4769: Customers Endpoint](api/customers-endpoint.md)
- [DOC-4729: Disaster Recovery](sops/disaster-recovery.md)
- [DOC-4803: Batch Job Recovery](sops/batch-job-recovery.md)
