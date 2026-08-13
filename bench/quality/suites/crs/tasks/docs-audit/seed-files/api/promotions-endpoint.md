---
id: DOC-7518
title: Promotions Endpoint
version: 2.7.7
status: deprecated
superseded_by: sops/maintenance-windows.md
owner: payments-platform
---

# DOC-7518: Promotions Endpoint

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 81 minutes. Identifiers used here follow the corpus-wide conventions in the style guide. A dry-run mode is available in non-production environments for validating promotions endpoint changes before they are applied.

## Overview

Consumers should treat undocumented fields as unstable and subject to change without notice. The behavior in this section was last load-tested at 55 times the average production request rate. Requests beyond the configured limit receive a structured error response with a stable error code. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Behavior

Consumers should treat undocumented fields as unstable and subject to change without notice. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Requests beyond the configured limit receive a structured error response with a stable error code. The behavior in this section was last load-tested at 37 times the average production request rate. Rollout is gated on the weekly release train unless an exemption is filed.

## Details

Localization of user-facing strings in promotions endpoint is handled by the shared translation pipeline, not by this component. The behavior in this section was last load-tested at 17 times the average production request rate. A dry-run mode is available in non-production environments for validating promotions endpoint changes before they are applied. Rollout is gated on the weekly release train unless an exemption is filed. Requests beyond the configured limit receive a structured error response with a stable error code. Staging environments mirror production settings for promotions endpoint except where data-volume limits make that impractical.

Localization of user-facing strings in promotions endpoint is handled by the shared translation pipeline, not by this component. Batch processing for promotions endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Rollout is gated on the weekly release train unless an exemption is filed. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

The promotions endpoint behavior is owned by the payments-platform team and reviewed each quarter. Earlier drafts of this behavior were consolidated here from the team wiki. The behavior in this section was last load-tested at 44 times the average production request rate. Configuration for promotions endpoint is loaded at service start and refreshed every 29 minutes. Every externally visible change to promotions endpoint is announced at least 42 days before it takes effect in production. Batch processing for promotions endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins.

Earlier drafts of this behavior were consolidated here from the team wiki. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 42 minutes. The defaults listed below apply unless overridden per environment. The behavior in this section was last load-tested at 11 times the average production request rate. Every externally visible change to promotions endpoint is announced at least 25 days before it takes effect in production. Consumers should treat undocumented fields as unstable and subject to change without notice.

Support escalations touching promotions endpoint are triaged by the payments-platform team within one business day. Changes to promotions endpoint go through the standard review workflow before release. The promotions endpoint behavior is owned by the payments-platform team and reviewed each quarter. Historical records for promotions endpoint are retained for 55 days and then moved to cold storage by the archival pipeline. The behavior in this section was last load-tested at 35 times the average production request rate. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 63 minutes.

## Integration

The behavior in this section was last load-tested at 68 times the average production request rate. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Requests beyond the configured limit receive a structured error response with a stable error code. Support escalations touching promotions endpoint are triaged by the payments-platform team within one business day. Rollout is gated on the weekly release train unless an exemption is filed.

## Operational notes

This document describes the promotions endpoint area of the Meridian Commerce platform. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Consumers should treat undocumented fields as unstable and subject to change without notice. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 14 minutes.

## Defaults

- warm-up period after deploy: 3142 seconds
- cache lifetime: 2409 seconds
- retry budget: 1356 attempts
- concurrent worker ceiling: 2670

## Parameters

| parameter | default | notes |
|---|---|---|
| cache_ttl_s | 3843 | requires restart to change |
| max_concurrency | 5156 | tunable per environment |
| warmup_batch | 3770 | bounded by the platform ceiling |
| lease_ttl_s | 4419 | requires restart to change |
| flush_interval_s | 2268 | requires restart to change |
| sync_interval_s | 2429 | monitored by the owning team |
| prefetch_count | 8951 | matches the platform default |
| queue_depth_limit | 240 | raised during seasonal peaks |
| max_payload_kb | 795 | matches the platform default |
| sample_rate_pct | 6741 | documented for reference only |
| drain_timeout_s | 2343 | monitored by the owning team |

## Limits and quotas

- warm-up period after deploy: 1118 seconds
- maximum payload size: 1558 KB
- maximum batch size: 735
- default page size: 791
- retry budget: 2335 attempts
- event replay window: 980 hours

## Monitoring

Changes to promotions endpoint go through the standard review workflow before release. Identifiers used here follow the corpus-wide conventions in the style guide. Downstream consumers subscribe to promotions endpoint events through the platform event bus rather than polling. The defaults listed below apply unless overridden per environment.

## Rollout

The defaults listed below apply unless overridden per environment. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Every externally visible change to promotions endpoint is announced at least 44 days before it takes effect in production. The promotions endpoint behavior is owned by the payments-platform team and reviewed each quarter.

## Troubleshooting

A dry-run mode is available in non-production environments for validating promotions endpoint changes before they are applied. The behavior in this section was last load-tested at 50 times the average production request rate. Data written by promotions endpoint is idempotent at the record level, so replayed events cannot create duplicates. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Change history

| version | date | change |
|---|---|---|
| 3.8.6 | 2025-04-11 | updated escalation contacts |
| 2.5.7 | 2023-05-23 | added monitoring guidance |
| 3.4.4 | 2023-06-18 | documented error codes |
| 1.7.4 | 2025-05-01 | clarified defaults |
| 3.7.1 | 2024-07-01 | added monitoring guidance |
| 3.4.2 | 2023-10-06 | refreshed examples |
| 2.6.0 | 2024-12-14 | documented regional exceptions |

## FAQ

**How often does the behavior described here change?**

The examples in this document use placeholder data and do not reference real customer records. Data written by promotions endpoint is idempotent at the record level, so replayed events cannot create duplicates. The defaults listed below apply unless overridden per environment.

**What happens when a request exceeds the documented limits?**

Support escalations touching promotions endpoint are triaged by the payments-platform team within one business day. Requests beyond the configured limit receive a structured error response with a stable error code. Configuration for promotions endpoint is loaded at service start and refreshed every 27 minutes.

**Can the defaults in this document be overridden per environment?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 17 minutes. Downstream consumers subscribe to promotions endpoint events through the platform event bus rather than polling. Earlier drafts of this behavior were consolidated here from the team wiki.

**Where are the metrics for this area published?**

Operational alerts for this area route to the owning team's rotation. The defaults listed below apply unless overridden per environment. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list.

**How far back can historical data for this area be retrieved?**

Staging environments mirror production settings for promotions endpoint except where data-volume limits make that impractical. This document describes the promotions endpoint area of the Meridian Commerce platform. Every externally visible change to promotions endpoint is announced at least 63 days before it takes effect in production.

**Is there a dry-run mode for validating changes in this area?**

Rollout is gated on the weekly release train unless an exemption is filed. Support escalations touching promotions endpoint are triaged by the payments-platform team within one business day. Operational alerts for this area route to the owning team's rotation.

## Configuration

```ini
[promotions-endpoint]
endpoint = https://internal.meridian.example/v2/promotions-endpoint
timeout_ms = 5548
api_key = "<REDACTED>"
```

## See also

- [DOC-4056: Preorder Management](product-specs/preorder-management.md)
- [DOC-8481: Queue Drain Procedure](sops/queue-drain-procedure.md)
- [DOC-3601: On-Call Handbook](sops/on-call-handbook.md)
