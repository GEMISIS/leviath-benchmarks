---
id: DOC-6418
title: Chaos Drills
version: 1.5.4
status: active
owner: identity
---

# DOC-6418: Chaos Drills

Earlier drafts of this behavior were consolidated here from the team wiki. Every externally visible change to chaos drills is announced at least 10 days before it takes effect in production. Downstream consumers subscribe to chaos drills events through the platform event bus rather than polling.

## Overview

Localization of user-facing strings in chaos drills is handled by the shared translation pipeline, not by this component. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Earlier drafts of this behavior were consolidated here from the team wiki. A dry-run mode is available in non-production environments for validating chaos drills changes before they are applied.

## Behavior

A dry-run mode is available in non-production environments for validating chaos drills changes before they are applied. Staging environments mirror production settings for chaos drills except where data-volume limits make that impractical. Requests beyond the configured limit receive a structured error response with a stable error code. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Downstream consumers subscribe to chaos drills events through the platform event bus rather than polling.

## Details

Every externally visible change to chaos drills is announced at least 6 days before it takes effect in production. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Operational alerts for this area route to the owning team's rotation. Localization of user-facing strings in chaos drills is handled by the shared translation pipeline, not by this component. The chaos drills behavior is owned by the identity team and reviewed each quarter. Rollout is gated on the weekly release train unless an exemption is filed.

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. This document describes the chaos drills area of the Meridian Commerce platform. Localization of user-facing strings in chaos drills is handled by the shared translation pipeline, not by this component. The chaos drills behavior is owned by the identity team and reviewed each quarter. Staging environments mirror production settings for chaos drills except where data-volume limits make that impractical. The examples in this document use placeholder data and do not reference real customer records.

This document describes the chaos drills area of the Meridian Commerce platform. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. The examples in this document use placeholder data and do not reference real customer records. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 16 minutes. The defaults listed below apply unless overridden per environment.

Consumers should treat undocumented fields as unstable and subject to change without notice. Rollout is gated on the weekly release train unless an exemption is filed. Earlier drafts of this behavior were consolidated here from the team wiki. The chaos drills behavior is owned by the identity team and reviewed each quarter. Operational alerts for this area route to the owning team's rotation. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 14 minutes.

Staging environments mirror production settings for chaos drills except where data-volume limits make that impractical. Operational alerts for this area route to the owning team's rotation. Downstream consumers subscribe to chaos drills events through the platform event bus rather than polling. Changes to chaos drills go through the standard review workflow before release. Data written by chaos drills is idempotent at the record level, so replayed events cannot create duplicates. Requests beyond the configured limit receive a structured error response with a stable error code.

## Integration

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 54 minutes. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Requests beyond the configured limit receive a structured error response with a stable error code.

## Operational notes

The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. This document describes the chaos drills area of the Meridian Commerce platform. Staging environments mirror production settings for chaos drills except where data-volume limits make that impractical. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Defaults

- burst allowance: 1397 requests
- retry budget: 2751 attempts
- soft quota per client: 1837 per hour
- cache lifetime: 700 seconds

## Parameters

| parameter | default | notes |
|---|---|---|
| replay_window_h | 1395 | hot-reloaded on change |
| audit_window_days | 6686 | matches the platform default |
| drain_timeout_s | 5780 | raised during seasonal peaks |
| sample_rate_pct | 7800 | documented for reference only |
| cache_ttl_s | 711 | requires restart to change |
| page_size | 7544 | tunable per environment |
| batch_window_ms | 1004 | monitored by the owning team |
| warmup_batch | 2922 | matches the platform default |
| cooldown_s | 4265 | bounded by the platform ceiling |
| shard_count | 3089 | hot-reloaded on change |

## Limits and quotas

- maximum batch size: 1053
- default page size: 119
- concurrent worker ceiling: 2938
- cache lifetime: 2786 seconds
- queue depth alert threshold: 2331
- retry budget: 2980 attempts
- request timeout: 2447 ms
- burst allowance: 1701 requests

## Monitoring

A dry-run mode is available in non-production environments for validating chaos drills changes before they are applied. The examples in this document use placeholder data and do not reference real customer records. Operational alerts for this area route to the owning team's rotation. Capacity for chaos drills is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Rollout

Historical records for chaos drills are retained for 38 days and then moved to cold storage by the archival pipeline. Earlier drafts of this behavior were consolidated here from the team wiki. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Every externally visible change to chaos drills is announced at least 66 days before it takes effect in production.

## Troubleshooting

Consumers should treat undocumented fields as unstable and subject to change without notice. Downstream consumers subscribe to chaos drills events through the platform event bus rather than polling. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. The examples in this document use placeholder data and do not reference real customer records.

## Change history

| version | date | change |
|---|---|---|
| 1.5.4 | 2025-02-18 | documented regional exceptions |
| 2.4.8 | 2024-01-02 | documented regional exceptions |
| 2.1.1 | 2024-06-15 | expanded rollout notes |
| 3.4.3 | 2023-06-21 | clarified defaults |
| 2.8.8 | 2025-12-06 | added monitoring guidance |
| 3.4.8 | 2024-03-12 | documented error codes |
| 2.4.0 | 2023-02-26 | clarified defaults |
| 3.8.6 | 2025-01-01 | tightened wording |
| 1.8.2 | 2025-06-01 | updated escalation contacts |

## FAQ

**Is there a dry-run mode for validating changes in this area?**

Data written by chaos drills is idempotent at the record level, so replayed events cannot create duplicates. The examples in this document use placeholder data and do not reference real customer records. Support escalations touching chaos drills are triaged by the identity team within one business day.

**Does this area behave differently in staging than in production?**

The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Downstream consumers subscribe to chaos drills events through the platform event bus rather than polling. The chaos drills behavior is owned by the identity team and reviewed each quarter.

**Can the defaults in this document be overridden per environment?**

Changes to chaos drills go through the standard review workflow before release. Rollout is gated on the weekly release train unless an exemption is filed. This document describes the chaos drills area of the Meridian Commerce platform.

**Who should be contacted when the documented defaults look wrong?**

Data written by chaos drills is idempotent at the record level, so replayed events cannot create duplicates. The identity team publishes a quarterly summary of changes in this area to the platform announcements list. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 24 minutes.

**How often does the behavior described here change?**

This document describes the chaos drills area of the Meridian Commerce platform. Historical records for chaos drills are retained for 78 days and then moved to cold storage by the archival pipeline. Downstream consumers subscribe to chaos drills events through the platform event bus rather than polling.

**Where are the metrics for this area published?**

Every externally visible change to chaos drills is announced at least 18 days before it takes effect in production. A dry-run mode is available in non-production environments for validating chaos drills changes before they are applied. Requests beyond the configured limit receive a structured error response with a stable error code.

## Configuration

```ini
[chaos-drills]
endpoint = https://internal.meridian.example/v2/chaos-drills
timeout_ms = 805
api_key = "<REDACTED>"
api_key = "sk_live_81f577bb6951"
```

## See also

- [DOC-5661: Postmortem Process](sops/postmortem-process.md)
