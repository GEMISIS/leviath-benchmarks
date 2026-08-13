---
id: DOC-6418
title: Chaos Drills
version: 1.5.4
status: active
owner: identity
---

# DOC-6418: Chaos Drills

The defaults listed below apply unless overridden per environment. Changes to chaos drills go through the standard review workflow before release. Historical records for chaos drills are retained for 76 days and then moved to cold storage by the archival pipeline.

## Overview

Downstream consumers subscribe to chaos drills events through the platform event bus rather than polling. This document describes the chaos drills area of the Meridian Commerce platform. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Changes to chaos drills go through the standard review workflow before release.

## Behavior

Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for chaos drills except where data-volume limits make that impractical. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Metrics emitted by chaos drills follow the platform naming scheme and are aggregated at one-minute resolution. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Details

Metrics emitted by chaos drills follow the platform naming scheme and are aggregated at one-minute resolution. The defaults listed below apply unless overridden per environment. Configuration for chaos drills is loaded at service start and refreshed every 11 minutes. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Staging environments mirror production settings for chaos drills except where data-volume limits make that impractical. Batch processing for chaos drills runs on a fixed schedule and drains its queue completely before the next cycle begins.

A dry-run mode is available in non-production environments for validating chaos drills changes before they are applied. Historical records for chaos drills are retained for 10 days and then moved to cold storage by the archival pipeline. Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for chaos drills is loaded at service start and refreshed every 55 minutes. Earlier drafts of this behavior were consolidated here from the team wiki. Every externally visible change to chaos drills is announced at least 40 days before it takes effect in production.

Data written by chaos drills is idempotent at the record level, so replayed events cannot create duplicates. Staging environments mirror production settings for chaos drills except where data-volume limits make that impractical. Downstream consumers subscribe to chaos drills events through the platform event bus rather than polling. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 24 minutes. The examples in this document use placeholder data and do not reference real customer records. Batch processing for chaos drills runs on a fixed schedule and drains its queue completely before the next cycle begins.

Rollout is gated on the weekly release train unless an exemption is filed. The examples in this document use placeholder data and do not reference real customer records. The behavior in this section was last load-tested at 11 times the average production request rate. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 44 minutes. Staging environments mirror production settings for chaos drills except where data-volume limits make that impractical. Every externally visible change to chaos drills is announced at least 35 days before it takes effect in production.

Support escalations touching chaos drills are triaged by the identity team within one business day. Metrics emitted by chaos drills follow the platform naming scheme and are aggregated at one-minute resolution. Capacity for chaos drills is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Consumers should treat undocumented fields as unstable and subject to change without notice. The examples in this document use placeholder data and do not reference real customer records. Localization of user-facing strings in chaos drills is handled by the shared translation pipeline, not by this component.

## Integration

Data written by chaos drills is idempotent at the record level, so replayed events cannot create duplicates. Capacity for chaos drills is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The chaos drills behavior is owned by the identity team and reviewed each quarter. Identifiers used here follow the corpus-wide conventions in the style guide.

## Operational notes

This document describes the chaos drills area of the Meridian Commerce platform. The examples in this document use placeholder data and do not reference real customer records. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. The defaults listed below apply unless overridden per environment.

## Defaults

- cache lifetime: 252 seconds
- event replay window: 793 hours
- soft quota per client: 3712 per hour

## Parameters

| parameter | default | notes |
|---|---|---|
| max_concurrency | 7443 | hot-reloaded on change |
| prefetch_count | 7429 | monitored by the owning team |
| page_size | 6832 | hot-reloaded on change |
| sample_rate_pct | 5248 | documented for reference only |
| cache_ttl_s | 6305 | hot-reloaded on change |
| shard_count | 7044 | documented for reference only |
| batch_window_ms | 5567 | tunable per environment |
| retry_limit | 8654 | documented for reference only |
| cooldown_s | 3809 | documented for reference only |
| drain_timeout_s | 7831 | hot-reloaded on change |
| max_payload_kb | 4781 | documented for reference only |
| queue_depth_limit | 3282 | monitored by the owning team |

## Limits and quotas

- soft quota per client: 3538 per hour
- concurrent worker ceiling: 3708
- queue depth alert threshold: 1826
- request timeout: 2238 ms
- default page size: 3292
- cache lifetime: 2795 seconds
- event replay window: 1123 hours

## Monitoring

Changes to chaos drills go through the standard review workflow before release. The chaos drills behavior is owned by the identity team and reviewed each quarter. Operational alerts for this area route to the owning team's rotation. A dry-run mode is available in non-production environments for validating chaos drills changes before they are applied.

## Rollout

Capacity for chaos drills is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The behavior in this section was last load-tested at 67 times the average production request rate. Downstream consumers subscribe to chaos drills events through the platform event bus rather than polling. Requests beyond the configured limit receive a structured error response with a stable error code.

## Troubleshooting

Batch processing for chaos drills runs on a fixed schedule and drains its queue completely before the next cycle begins. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The chaos drills behavior is owned by the identity team and reviewed each quarter. Configuration for chaos drills is loaded at service start and refreshed every 12 minutes.

## Change history

| version | date | change |
|---|---|---|
| 1.7.4 | 2023-04-06 | documented regional exceptions |
| 1.0.0 | 2024-12-16 | tightened wording |
| 2.7.4 | 2023-12-22 | updated escalation contacts |
| 3.9.6 | 2025-04-28 | updated escalation contacts |
| 3.8.2 | 2025-06-20 | updated escalation contacts |
| 2.4.9 | 2023-08-09 | documented regional exceptions |
| 3.0.6 | 2024-10-12 | expanded rollout notes |
| 2.4.1 | 2025-09-16 | refreshed examples |
| 3.6.0 | 2023-09-26 | recorded quota changes |

## FAQ

**Who should be contacted when the documented defaults look wrong?**

Access to administrative operations in this area is restricted to members of the identity group and audited monthly. Consumers should treat undocumented fields as unstable and subject to change without notice. The defaults listed below apply unless overridden per environment.

**How often does the behavior described here change?**

The chaos drills behavior is owned by the identity team and reviewed each quarter. Every externally visible change to chaos drills is announced at least 87 days before it takes effect in production. Access to administrative operations in this area is restricted to members of the identity group and audited monthly.

**What happens when a request exceeds the documented limits?**

Downstream consumers subscribe to chaos drills events through the platform event bus rather than polling. Localization of user-facing strings in chaos drills is handled by the shared translation pipeline, not by this component. Batch processing for chaos drills runs on a fixed schedule and drains its queue completely before the next cycle begins.

**Does this area behave differently in staging than in production?**

Every externally visible change to chaos drills is announced at least 50 days before it takes effect in production. Capacity for chaos drills is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Requests beyond the configured limit receive a structured error response with a stable error code.

**Can the defaults in this document be overridden per environment?**

Rollout is gated on the weekly release train unless an exemption is filed. This document describes the chaos drills area of the Meridian Commerce platform. Configuration for chaos drills is loaded at service start and refreshed every 77 minutes.

**How far back can historical data for this area be retrieved?**

Support escalations touching chaos drills are triaged by the identity team within one business day. Access to administrative operations in this area is restricted to members of the identity group and audited monthly. The identity team publishes a quarterly summary of changes in this area to the platform announcements list.

## Configuration

```ini
[chaos-drills]
endpoint = https://internal.meridian.example/v2/chaos-drills
timeout_ms = 2339
api_key = "<REDACTED>"
```

## See also

- [DOC-6815: Deploy Procedure](sops/deploy-procedure.md)
- [DOC-1266: Cart Merge](product-specs/cart-merge.md)
- [DOC-6887: Oncall Handoff](sops/oncall-handoff.md)
