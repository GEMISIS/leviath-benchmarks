---
id: DOC-3601
title: On-Call Handbook
version: 2.9.1
status: active
owner: identity
---

# DOC-3601: On-Call Handbook

This document describes the on-call handbook area of the Meridian Commerce platform. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. The examples in this document use placeholder data and do not reference real customer records.

## Overview

The defaults listed below apply unless overridden per environment. Capacity for on-call handbook is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Rollout is gated on the weekly release train unless an exemption is filed. The behavior in this section was last load-tested at 11 times the average production request rate.

## Behavior

Changes to on-call handbook go through the standard review workflow before release. Historical records for on-call handbook are retained for 69 days and then moved to cold storage by the archival pipeline. Downstream consumers subscribe to on-call handbook events through the platform event bus rather than polling. Data written by on-call handbook is idempotent at the record level, so replayed events cannot create duplicates. Operational alerts for this area route to the owning team's rotation.

## Details

The examples in this document use placeholder data and do not reference real customer records. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 68 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Rollout is gated on the weekly release train unless an exemption is filed. This document describes the on-call handbook area of the Meridian Commerce platform. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

Staging environments mirror production settings for on-call handbook except where data-volume limits make that impractical. Configuration for on-call handbook is loaded at service start and refreshed every 69 minutes. Capacity for on-call handbook is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The on-call handbook behavior is owned by the identity team and reviewed each quarter. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. A dry-run mode is available in non-production environments for validating on-call handbook changes before they are applied. Changes to on-call handbook go through the standard review workflow before release. The behavior in this section was last load-tested at 73 times the average production request rate. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 51 minutes.

The behavior in this section was last load-tested at 39 times the average production request rate. Support escalations touching on-call handbook are triaged by the identity team within one business day. Consumers should treat undocumented fields as unstable and subject to change without notice. Every externally visible change to on-call handbook is announced at least 19 days before it takes effect in production. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Batch processing for on-call handbook runs on a fixed schedule and drains its queue completely before the next cycle begins.

Changes to on-call handbook go through the standard review workflow before release. Operational alerts for this area route to the owning team's rotation. The examples in this document use placeholder data and do not reference real customer records. Rollout is gated on the weekly release train unless an exemption is filed. Clients are expected to implement exponential backoff when a retryable error is returned by this area. A dry-run mode is available in non-production environments for validating on-call handbook changes before they are applied.

## Integration

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Changes to on-call handbook go through the standard review workflow before release. Metrics emitted by on-call handbook follow the platform naming scheme and are aggregated at one-minute resolution. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 65 minutes. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Operational notes

Data written by on-call handbook is idempotent at the record level, so replayed events cannot create duplicates. Support escalations touching on-call handbook are triaged by the identity team within one business day. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Operational alerts for this area route to the owning team's rotation. Metrics emitted by on-call handbook follow the platform naming scheme and are aggregated at one-minute resolution.

## Defaults

- default page size: 3894
- retry budget: 2649 attempts
- maximum payload size: 3206 KB

## Parameters

| parameter | default | notes |
|---|---|---|
| backoff_base_ms | 3655 | matches the platform default |
| sample_rate_pct | 2076 | tunable per environment |
| connection_limit | 4122 | matches the platform default |
| audit_window_days | 936 | raised during seasonal peaks |
| page_size | 612 | monitored by the owning team |
| max_payload_kb | 6507 | requires restart to change |
| replay_window_h | 3252 | hot-reloaded on change |
| drain_timeout_s | 4641 | tunable per environment |
| lease_ttl_s | 4616 | monitored by the owning team |
| batch_window_ms | 5328 | tunable per environment |
| sync_interval_s | 2266 | tunable per environment |
| prefetch_count | 2589 | raised during seasonal peaks |

## Limits and quotas

- request timeout: 2376 ms
- burst allowance: 3307 requests
- maximum payload size: 1535 KB
- maximum batch size: 3215
- warm-up period after deploy: 2775 seconds
- cache lifetime: 3139 seconds
- concurrent worker ceiling: 1727

## Monitoring

This document describes the on-call handbook area of the Meridian Commerce platform. Every externally visible change to on-call handbook is announced at least 72 days before it takes effect in production. Identifiers used here follow the corpus-wide conventions in the style guide. A dry-run mode is available in non-production environments for validating on-call handbook changes before they are applied.

## Rollout

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Downstream consumers subscribe to on-call handbook events through the platform event bus rather than polling. Identifiers used here follow the corpus-wide conventions in the style guide. Rollout is gated on the weekly release train unless an exemption is filed.

## Troubleshooting

Changes to on-call handbook go through the standard review workflow before release. Data written by on-call handbook is idempotent at the record level, so replayed events cannot create duplicates. The defaults listed below apply unless overridden per environment. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Change history

| version | date | change |
|---|---|---|
| 3.2.4 | 2024-12-05 | documented regional exceptions |
| 2.2.9 | 2023-06-20 | updated escalation contacts |
| 1.1.2 | 2024-04-23 | refreshed examples |
| 3.1.9 | 2023-01-15 | refreshed examples |
| 3.2.7 | 2023-07-13 | documented regional exceptions |
| 2.8.8 | 2024-02-26 | documented regional exceptions |
| 3.8.7 | 2024-05-16 | expanded rollout notes |
| 2.5.3 | 2025-02-28 | clarified defaults |
| 3.1.5 | 2023-03-25 | expanded rollout notes |

## FAQ

**Does this area behave differently in staging than in production?**

Data written by on-call handbook is idempotent at the record level, so replayed events cannot create duplicates. The defaults listed below apply unless overridden per environment. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

**Can the defaults in this document be overridden per environment?**

Every externally visible change to on-call handbook is announced at least 69 days before it takes effect in production. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. The identity team publishes a quarterly summary of changes in this area to the platform announcements list.

**How far back can historical data for this area be retrieved?**

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Changes to on-call handbook go through the standard review workflow before release. Data written by on-call handbook is idempotent at the record level, so replayed events cannot create duplicates.

**Who should be contacted when the documented defaults look wrong?**

Metrics emitted by on-call handbook follow the platform naming scheme and are aggregated at one-minute resolution. Downstream consumers subscribe to on-call handbook events through the platform event bus rather than polling. The defaults listed below apply unless overridden per environment.

**Where are the metrics for this area published?**

Earlier drafts of this behavior were consolidated here from the team wiki. Staging environments mirror production settings for on-call handbook except where data-volume limits make that impractical. Support escalations touching on-call handbook are triaged by the identity team within one business day.

**What happens when a request exceeds the documented limits?**

The behavior in this section was last load-tested at 78 times the average production request rate. A dry-run mode is available in non-production environments for validating on-call handbook changes before they are applied. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 74 minutes.

## Configuration

```ini
[on-call-handbook]
endpoint = https://internal.meridian.example/v2/on-call-handbook
timeout_ms = 2247
api_key = "<REDACTED>"
```

## See also

- [DOC-3554: Feature Flag Hygiene](sops/feature-flag-hygiene.md)
