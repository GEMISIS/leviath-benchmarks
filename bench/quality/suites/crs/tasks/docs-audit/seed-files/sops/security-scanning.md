---
id: DOC-3862
title: Security Scanning
version: 2.2.1
status: active
owner: comms
---

# DOC-3862: Security Scanning

Configuration for security scanning is loaded at service start and refreshed every 74 minutes. A dry-run mode is available in non-production environments for validating security scanning changes before they are applied. Support escalations touching security scanning are triaged by the comms team within one business day.

## Overview

A dry-run mode is available in non-production environments for validating security scanning changes before they are applied. Historical records for security scanning are retained for 34 days and then moved to cold storage by the archival pipeline. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The defaults listed below apply unless overridden per environment.

## Behavior

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Support escalations touching security scanning are triaged by the comms team within one business day. A dry-run mode is available in non-production environments for validating security scanning changes before they are applied. Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for security scanning except where data-volume limits make that impractical.

## Details

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Support escalations touching security scanning are triaged by the comms team within one business day. The defaults listed below apply unless overridden per environment. Identifiers used here follow the corpus-wide conventions in the style guide. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Access to administrative operations in this area is restricted to members of the comms group and audited monthly. Metrics emitted by security scanning follow the platform naming scheme and are aggregated at one-minute resolution. Earlier drafts of this behavior were consolidated here from the team wiki. Data written by security scanning is idempotent at the record level, so replayed events cannot create duplicates. Localization of user-facing strings in security scanning is handled by the shared translation pipeline, not by this component.

Localization of user-facing strings in security scanning is handled by the shared translation pipeline, not by this component. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Changes to security scanning go through the standard review workflow before release. Historical records for security scanning are retained for 19 days and then moved to cold storage by the archival pipeline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Support escalations touching security scanning are triaged by the comms team within one business day.

Data written by security scanning is idempotent at the record level, so replayed events cannot create duplicates. The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Rollout is gated on the weekly release train unless an exemption is filed. The defaults listed below apply unless overridden per environment. Operational alerts for this area route to the owning team's rotation. Metrics emitted by security scanning follow the platform naming scheme and are aggregated at one-minute resolution.

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Data written by security scanning is idempotent at the record level, so replayed events cannot create duplicates. The behavior in this section was last load-tested at 71 times the average production request rate. The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Consumers should treat undocumented fields as unstable and subject to change without notice. Batch processing for security scanning runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Integration

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 45 minutes. Downstream consumers subscribe to security scanning events through the platform event bus rather than polling. Localization of user-facing strings in security scanning is handled by the shared translation pipeline, not by this component. Changes to security scanning go through the standard review workflow before release. This document describes the security scanning area of the Meridian Commerce platform.

## Operational notes

The security scanning behavior is owned by the comms team and reviewed each quarter. Configuration for security scanning is loaded at service start and refreshed every 62 minutes. Consumers should treat undocumented fields as unstable and subject to change without notice. The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Access to administrative operations in this area is restricted to members of the comms group and audited monthly.

## Defaults

- default page size: 2543
- warm-up period after deploy: 2249 seconds
- maximum payload size: 2527 KB
- maximum batch size: 599

## Parameters

| parameter | default | notes |
|---|---|---|
| flush_interval_s | 6945 | matches the platform default |
| sample_rate_pct | 8847 | requires restart to change |
| retry_limit | 997 | requires restart to change |
| batch_window_ms | 7294 | hot-reloaded on change |
| drain_timeout_s | 425 | raised during seasonal peaks |
| warmup_batch | 3227 | monitored by the owning team |
| max_concurrency | 6701 | bounded by the platform ceiling |
| shard_count | 1419 | matches the platform default |
| audit_window_days | 82 | documented for reference only |
| cache_ttl_s | 8719 | documented for reference only |
| replay_window_h | 2491 | documented for reference only |
| backoff_base_ms | 6436 | documented for reference only |
| queue_depth_limit | 7629 | raised during seasonal peaks |
| max_payload_kb | 1767 | matches the platform default |

## Limits and quotas

- concurrent worker ceiling: 226
- warm-up period after deploy: 1844 seconds
- cache lifetime: 3201 seconds
- burst allowance: 1006 requests
- request timeout: 829 ms
- soft quota per client: 378 per hour
- default page size: 3552
- event replay window: 2318 hours

## Monitoring

A dry-run mode is available in non-production environments for validating security scanning changes before they are applied. This document describes the security scanning area of the Meridian Commerce platform. The examples in this document use placeholder data and do not reference real customer records. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Rollout

Consumers should treat undocumented fields as unstable and subject to change without notice. Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for security scanning except where data-volume limits make that impractical. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Troubleshooting

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The examples in this document use placeholder data and do not reference real customer records. Downstream consumers subscribe to security scanning events through the platform event bus rather than polling. Support escalations touching security scanning are triaged by the comms team within one business day.

## Change history

| version | date | change |
|---|---|---|
| 3.7.1 | 2025-01-27 | clarified defaults |
| 3.4.1 | 2025-09-14 | added monitoring guidance |
| 1.9.7 | 2023-01-08 | clarified defaults |
| 1.8.1 | 2024-02-12 | updated escalation contacts |
| 3.4.2 | 2025-11-12 | aligned terminology with the style guide |
| 2.9.8 | 2025-08-03 | expanded rollout notes |
| 1.3.3 | 2024-05-18 | tightened wording |

## FAQ

**How far back can historical data for this area be retrieved?**

Staging environments mirror production settings for security scanning except where data-volume limits make that impractical. Requests beyond the configured limit receive a structured error response with a stable error code. Configuration for security scanning is loaded at service start and refreshed every 73 minutes.

**Where are the metrics for this area published?**

Configuration for security scanning is loaded at service start and refreshed every 17 minutes. Operational alerts for this area route to the owning team's rotation. Capacity for security scanning is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

**Is there a dry-run mode for validating changes in this area?**

Changes to security scanning go through the standard review workflow before release. Every externally visible change to security scanning is announced at least 52 days before it takes effect in production. Consumers should treat undocumented fields as unstable and subject to change without notice.

**Does this area behave differently in staging than in production?**

Consumers should treat undocumented fields as unstable and subject to change without notice. The security scanning behavior is owned by the comms team and reviewed each quarter. Metrics emitted by security scanning follow the platform naming scheme and are aggregated at one-minute resolution.

**Can the defaults in this document be overridden per environment?**

Batch processing for security scanning runs on a fixed schedule and drains its queue completely before the next cycle begins. The defaults listed below apply unless overridden per environment. Configuration for security scanning is loaded at service start and refreshed every 13 minutes.

## Configuration

```ini
[security-scanning]
endpoint = https://internal.meridian.example/v2/security-scanning
timeout_ms = 5663
api_key = "<REDACTED>"
```

## See also

- [DOC-3721: Database Backup](sops/database-backup.md)
