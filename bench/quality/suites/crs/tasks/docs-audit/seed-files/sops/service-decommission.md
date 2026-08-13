---
id: DOC-8014
title: Service Decommission
version: 2.0.3
status: active
owner: platform-core
---

# DOC-8014: Service Decommission

Support escalations touching service decommission are triaged by the platform-core team within one business day. Localization of user-facing strings in service decommission is handled by the shared translation pipeline, not by this component. Identifiers used here follow the corpus-wide conventions in the style guide.

## Overview

Data written by service decommission is idempotent at the record level, so replayed events cannot create duplicates. Earlier drafts of this behavior were consolidated here from the team wiki. Downstream consumers subscribe to service decommission events through the platform event bus rather than polling. The defaults listed below apply unless overridden per environment.

## Behavior

Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Batch processing for service decommission runs on a fixed schedule and drains its queue completely before the next cycle begins. Data written by service decommission is idempotent at the record level, so replayed events cannot create duplicates. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Identifiers used here follow the corpus-wide conventions in the style guide.

## Details

Staging environments mirror production settings for service decommission except where data-volume limits make that impractical. The service decommission behavior is owned by the platform-core team and reviewed each quarter. A dry-run mode is available in non-production environments for validating service decommission changes before they are applied. Changes to service decommission go through the standard review workflow before release. Capacity for service decommission is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Rollout is gated on the weekly release train unless an exemption is filed.

Metrics emitted by service decommission follow the platform naming scheme and are aggregated at one-minute resolution. This document describes the service decommission area of the Meridian Commerce platform. Downstream consumers subscribe to service decommission events through the platform event bus rather than polling. Data written by service decommission is idempotent at the record level, so replayed events cannot create duplicates. Rollout is gated on the weekly release train unless an exemption is filed. Localization of user-facing strings in service decommission is handled by the shared translation pipeline, not by this component.

Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for service decommission except where data-volume limits make that impractical. A dry-run mode is available in non-production environments for validating service decommission changes before they are applied. The defaults listed below apply unless overridden per environment. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

Consumers should treat undocumented fields as unstable and subject to change without notice. Identifiers used here follow the corpus-wide conventions in the style guide. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Downstream consumers subscribe to service decommission events through the platform event bus rather than polling. Historical records for service decommission are retained for 47 days and then moved to cold storage by the archival pipeline. A dry-run mode is available in non-production environments for validating service decommission changes before they are applied.

Data written by service decommission is idempotent at the record level, so replayed events cannot create duplicates. The defaults listed below apply unless overridden per environment. The service decommission behavior is owned by the platform-core team and reviewed each quarter. Capacity for service decommission is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Operational alerts for this area route to the owning team's rotation. Changes to service decommission go through the standard review workflow before release.

## Integration

Localization of user-facing strings in service decommission is handled by the shared translation pipeline, not by this component. Metrics emitted by service decommission follow the platform naming scheme and are aggregated at one-minute resolution. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Earlier drafts of this behavior were consolidated here from the team wiki. Batch processing for service decommission runs on a fixed schedule and drains its queue completely before the next cycle begins.

## Operational notes

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 62 minutes. Every externally visible change to service decommission is announced at least 34 days before it takes effect in production. Configuration for service decommission is loaded at service start and refreshed every 37 minutes. Capacity for service decommission is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The defaults listed below apply unless overridden per environment.

## Defaults

- cache lifetime: 3803 seconds
- burst allowance: 442 requests
- default page size: 3668
- concurrent worker ceiling: 3086

## Parameters

| parameter | default | notes |
|---|---|---|
| sample_rate_pct | 4516 | matches the platform default |
| warmup_batch | 1359 | raised during seasonal peaks |
| prefetch_count | 6789 | tunable per environment |
| shard_count | 3319 | matches the platform default |
| replay_window_h | 89 | raised during seasonal peaks |
| max_payload_kb | 3450 | matches the platform default |
| batch_window_ms | 6761 | raised during seasonal peaks |
| audit_window_days | 73 | tunable per environment |
| page_size | 7237 | tunable per environment |
| drain_timeout_s | 8754 | monitored by the owning team |
| cooldown_s | 7426 | monitored by the owning team |
| flush_interval_s | 5282 | requires restart to change |

## Limits and quotas

- cache lifetime: 1495 seconds
- burst allowance: 602 requests
- warm-up period after deploy: 1718 seconds
- default page size: 2967
- retry budget: 704 attempts
- maximum batch size: 2489

## Monitoring

The examples in this document use placeholder data and do not reference real customer records. The defaults listed below apply unless overridden per environment. Batch processing for service decommission runs on a fixed schedule and drains its queue completely before the next cycle begins. Staging environments mirror production settings for service decommission except where data-volume limits make that impractical.

## Rollout

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The service decommission behavior is owned by the platform-core team and reviewed each quarter. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 18 minutes. Capacity for service decommission is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

## Troubleshooting

Operational alerts for this area route to the owning team's rotation. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Data written by service decommission is idempotent at the record level, so replayed events cannot create duplicates. This document describes the service decommission area of the Meridian Commerce platform.

## Change history

| version | date | change |
|---|---|---|
| 1.2.0 | 2023-07-24 | updated escalation contacts |
| 1.0.2 | 2025-07-26 | aligned terminology with the style guide |
| 3.8.3 | 2025-07-09 | recorded quota changes |
| 1.4.0 | 2024-06-05 | updated escalation contacts |
| 2.0.5 | 2024-04-13 | documented error codes |
| 3.9.0 | 2025-11-11 | documented regional exceptions |
| 1.1.0 | 2024-12-10 | recorded quota changes |

## FAQ

**Who should be contacted when the documented defaults look wrong?**

Batch processing for service decommission runs on a fixed schedule and drains its queue completely before the next cycle begins. The behavior in this section was last load-tested at 49 times the average production request rate. Every externally visible change to service decommission is announced at least 78 days before it takes effect in production.

**How often does the behavior described here change?**

Every externally visible change to service decommission is announced at least 39 days before it takes effect in production. Requests beyond the configured limit receive a structured error response with a stable error code. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

**What happens when a request exceeds the documented limits?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 44 minutes. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Consumers should treat undocumented fields as unstable and subject to change without notice.

**Can the defaults in this document be overridden per environment?**

Data written by service decommission is idempotent at the record level, so replayed events cannot create duplicates. Operational alerts for this area route to the owning team's rotation. This document describes the service decommission area of the Meridian Commerce platform.

## Configuration

```ini
[service-decommission]
endpoint = https://internal.meridian.example/v2/service-decommission
timeout_ms = 4143
api_key = "<REDACTED>"
```

## See also

- [DOC-2266: Carts Endpoint](api/carts-endpoint.md)
