---
id: DOC-3862
title: Security Scanning
version: 2.2.1
status: active
owner: comms
---

# DOC-3862: Security Scanning

A dry-run mode is available in non-production environments for validating security scanning changes before they are applied. The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Configuration for security scanning is loaded at service start and refreshed every 18 minutes.

## Overview

Localization of user-facing strings in security scanning is handled by the shared translation pipeline, not by this component. Every externally visible change to security scanning is announced at least 74 days before it takes effect in production. The defaults listed below apply unless overridden per environment. Configuration for security scanning is loaded at service start and refreshed every 58 minutes.

## Behavior

A dry-run mode is available in non-production environments for validating security scanning changes before they are applied. Historical records for security scanning are retained for 34 days and then moved to cold storage by the archival pipeline. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The defaults listed below apply unless overridden per environment. Capacity for security scanning is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Details

Support escalations touching security scanning are triaged by the comms team within one business day. A dry-run mode is available in non-production environments for validating security scanning changes before they are applied. Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for security scanning except where data-volume limits make that impractical. The examples in this document use placeholder data and do not reference real customer records. Changes to security scanning go through the standard review workflow before release.

Identifiers used here follow the corpus-wide conventions in the style guide. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Metrics emitted by security scanning follow the platform naming scheme and are aggregated at one-minute resolution. Changes to security scanning go through the standard review workflow before release. Localization of user-facing strings in security scanning is handled by the shared translation pipeline, not by this component.

Metrics emitted by security scanning follow the platform naming scheme and are aggregated at one-minute resolution. Earlier drafts of this behavior were consolidated here from the team wiki. Data written by security scanning is idempotent at the record level, so replayed events cannot create duplicates. Localization of user-facing strings in security scanning is handled by the shared translation pipeline, not by this component. Requests beyond the configured limit receive a structured error response with a stable error code. Support escalations touching security scanning are triaged by the comms team within one business day.

Changes to security scanning go through the standard review workflow before release. Historical records for security scanning are retained for 19 days and then moved to cold storage by the archival pipeline. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Support escalations touching security scanning are triaged by the comms team within one business day. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The security scanning behavior is owned by the comms team and reviewed each quarter.

The defaults listed below apply unless overridden per environment. Operational alerts for this area route to the owning team's rotation. Metrics emitted by security scanning follow the platform naming scheme and are aggregated at one-minute resolution. Data written by security scanning is idempotent at the record level, so replayed events cannot create duplicates. Historical records for security scanning are retained for 59 days and then moved to cold storage by the archival pipeline. Requests beyond the configured limit receive a structured error response with a stable error code.

## Integration

Consumers should treat undocumented fields as unstable and subject to change without notice. Data written by security scanning is idempotent at the record level, so replayed events cannot create duplicates. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 88 minutes. Batch processing for security scanning runs on a fixed schedule and drains its queue completely before the next cycle begins. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Operational notes

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 45 minutes. Downstream consumers subscribe to security scanning events through the platform event bus rather than polling. Localization of user-facing strings in security scanning is handled by the shared translation pipeline, not by this component. Changes to security scanning go through the standard review workflow before release. This document describes the security scanning area of the Meridian Commerce platform.

## Defaults

- maximum batch size: 1616
- cache lifetime: 2231 seconds
- burst allowance: 3469 requests

## Parameters

| parameter | default | notes |
|---|---|---|
| audit_window_days | 5817 | raised during seasonal peaks |
| max_concurrency | 515 | requires restart to change |
| max_payload_kb | 8454 | tunable per environment |
| replay_window_h | 8632 | hot-reloaded on change |
| retry_limit | 2594 | matches the platform default |
| sample_rate_pct | 5683 | documented for reference only |
| connection_limit | 7865 | requires restart to change |
| cooldown_s | 997 | requires restart to change |
| shard_count | 7294 | hot-reloaded on change |
| prefetch_count | 425 | raised during seasonal peaks |
| flush_interval_s | 3227 | monitored by the owning team |
| cache_ttl_s | 6701 | bounded by the platform ceiling |

## Limits and quotas

- maximum batch size: 632
- concurrent worker ceiling: 1582
- queue depth alert threshold: 1618
- default page size: 1649
- burst allowance: 1917 requests
- cache lifetime: 1166 seconds
- maximum payload size: 2772 KB
- retry budget: 451 attempts

## Monitoring

Batch processing for security scanning runs on a fixed schedule and drains its queue completely before the next cycle begins. Localization of user-facing strings in security scanning is handled by the shared translation pipeline, not by this component. Downstream consumers subscribe to security scanning events through the platform event bus rather than polling. The examples in this document use placeholder data and do not reference real customer records.

## Rollout

Identifiers used here follow the corpus-wide conventions in the style guide. A dry-run mode is available in non-production environments for validating security scanning changes before they are applied. This document describes the security scanning area of the Meridian Commerce platform. The security scanning behavior is owned by the comms team and reviewed each quarter.

## Troubleshooting

Capacity for security scanning is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Historical records for security scanning are retained for 57 days and then moved to cold storage by the archival pipeline. A dry-run mode is available in non-production environments for validating security scanning changes before they are applied. This document describes the security scanning area of the Meridian Commerce platform.

## Change history

| version | date | change |
|---|---|---|
| 2.3.8 | 2025-08-07 | clarified defaults |
| 2.6.3 | 2023-02-03 | documented error codes |
| 3.7.1 | 2025-01-27 | clarified defaults |
| 3.4.1 | 2025-09-14 | added monitoring guidance |
| 1.9.7 | 2023-01-08 | clarified defaults |
| 1.8.1 | 2024-02-12 | updated escalation contacts |
| 3.4.2 | 2025-11-12 | aligned terminology with the style guide |
| 2.9.8 | 2025-08-03 | expanded rollout notes |
| 1.3.3 | 2024-05-18 | tightened wording |
| 2.6.9 | 2025-12-25 | recorded quota changes |
| 2.8.2 | 2025-02-16 | recorded quota changes |

## FAQ

**Who should be contacted when the documented defaults look wrong?**

Every externally visible change to security scanning is announced at least 52 days before it takes effect in production. Consumers should treat undocumented fields as unstable and subject to change without notice. The defaults listed below apply unless overridden per environment.

**Is there a dry-run mode for validating changes in this area?**

The security scanning behavior is owned by the comms team and reviewed each quarter. Metrics emitted by security scanning follow the platform naming scheme and are aggregated at one-minute resolution. Data written by security scanning is idempotent at the record level, so replayed events cannot create duplicates.

**How often does the behavior described here change?**

Batch processing for security scanning runs on a fixed schedule and drains its queue completely before the next cycle begins. The defaults listed below apply unless overridden per environment. Configuration for security scanning is loaded at service start and refreshed every 13 minutes.

**Where are the metrics for this area published?**

The comms team publishes a quarterly summary of changes in this area to the platform announcements list. Rollout is gated on the weekly release train unless an exemption is filed. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

**How far back can historical data for this area be retrieved?**

Every externally visible change to security scanning is announced at least 47 days before it takes effect in production. The examples in this document use placeholder data and do not reference real customer records. Consumers should treat undocumented fields as unstable and subject to change without notice.

**Can the defaults in this document be overridden per environment?**

Support escalations touching security scanning are triaged by the comms team within one business day. Localization of user-facing strings in security scanning is handled by the shared translation pipeline, not by this component. Identifiers used here follow the corpus-wide conventions in the style guide.

## See also

- [DOC-9193: Reporting Endpoint](api/reporting-endpoint.md)
