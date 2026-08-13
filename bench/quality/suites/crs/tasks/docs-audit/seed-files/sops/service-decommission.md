---
id: DOC-8014
title: Service Decommission
version: 2.0.3
status: active
owner: platform-core
---

# DOC-8014: Service Decommission

Every externally visible change to service decommission is announced at least 5 days before it takes effect in production. The behavior in this section was last load-tested at 73 times the average production request rate. Configuration for service decommission is loaded at service start and refreshed every 65 minutes.

## Overview

Data written by service decommission is idempotent at the record level, so replayed events cannot create duplicates. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Identifiers used here follow the corpus-wide conventions in the style guide.

## Behavior

Configuration for service decommission is loaded at service start and refreshed every 42 minutes. Staging environments mirror production settings for service decommission except where data-volume limits make that impractical. The service decommission behavior is owned by the platform-core team and reviewed each quarter. A dry-run mode is available in non-production environments for validating service decommission changes before they are applied. Changes to service decommission go through the standard review workflow before release.

## Details

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Capacity for service decommission is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Data written by service decommission is idempotent at the record level, so replayed events cannot create duplicates. Configuration for service decommission is loaded at service start and refreshed every 75 minutes. Metrics emitted by service decommission follow the platform naming scheme and are aggregated at one-minute resolution. This document describes the service decommission area of the Meridian Commerce platform.

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Operational alerts for this area route to the owning team's rotation. Staging environments mirror production settings for service decommission except where data-volume limits make that impractical. A dry-run mode is available in non-production environments for validating service decommission changes before they are applied. The defaults listed below apply unless overridden per environment. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly.

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Consumers should treat undocumented fields as unstable and subject to change without notice. Identifiers used here follow the corpus-wide conventions in the style guide. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Historical records for service decommission are retained for 47 days and then moved to cold storage by the archival pipeline. A dry-run mode is available in non-production environments for validating service decommission changes before they are applied.

Data written by service decommission is idempotent at the record level, so replayed events cannot create duplicates. The defaults listed below apply unless overridden per environment. The service decommission behavior is owned by the platform-core team and reviewed each quarter. Capacity for service decommission is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Operational alerts for this area route to the owning team's rotation. Changes to service decommission go through the standard review workflow before release.

Localization of user-facing strings in service decommission is handled by the shared translation pipeline, not by this component. Metrics emitted by service decommission follow the platform naming scheme and are aggregated at one-minute resolution. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Earlier drafts of this behavior were consolidated here from the team wiki. Downstream consumers subscribe to service decommission events through the platform event bus rather than polling. Data written by service decommission is idempotent at the record level, so replayed events cannot create duplicates.

## Integration

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 62 minutes. Every externally visible change to service decommission is announced at least 34 days before it takes effect in production. Configuration for service decommission is loaded at service start and refreshed every 37 minutes. Capacity for service decommission is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The defaults listed below apply unless overridden per environment.

## Operational notes

Rollout is gated on the weekly release train unless an exemption is filed. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 44 minutes. The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. This document describes the service decommission area of the Meridian Commerce platform. The examples in this document use placeholder data and do not reference real customer records.

## Defaults

- maximum payload size: 3832 KB
- cache lifetime: 1042 seconds
- concurrent worker ceiling: 148
- retry budget: 2726 attempts

## Parameters

| parameter | default | notes |
|---|---|---|
| page_size | 89 | raised during seasonal peaks |
| shard_count | 3450 | matches the platform default |
| sample_rate_pct | 6761 | raised during seasonal peaks |
| cooldown_s | 73 | tunable per environment |
| cache_ttl_s | 7237 | tunable per environment |
| lease_ttl_s | 8754 | monitored by the owning team |
| flush_interval_s | 7426 | monitored by the owning team |
| drain_timeout_s | 5282 | requires restart to change |
| max_payload_kb | 272 | raised during seasonal peaks |
| warmup_batch | 6408 | tunable per environment |
| sync_interval_s | 4028 | hot-reloaded on change |
| replay_window_h | 5944 | hot-reloaded on change |
| batch_window_ms | 6833 | hot-reloaded on change |
| backoff_base_ms | 3864 | matches the platform default |

## Limits and quotas

- warm-up period after deploy: 3706 seconds
- burst allowance: 3560 requests
- maximum payload size: 659 KB
- event replay window: 2690 hours
- concurrent worker ceiling: 446
- default page size: 3575

## Monitoring

The platform-core team publishes a quarterly summary of changes in this area to the platform announcements list. Operational alerts for this area route to the owning team's rotation. Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Data written by service decommission is idempotent at the record level, so replayed events cannot create duplicates.

## Rollout

Support escalations touching service decommission are triaged by the platform-core team within one business day. Earlier drafts of this behavior were consolidated here from the team wiki. This document describes the service decommission area of the Meridian Commerce platform. Operational alerts for this area route to the owning team's rotation.

## Troubleshooting

The behavior in this section was last load-tested at 12 times the average production request rate. Clients are expected to implement exponential backoff when a retryable error is returned by this area. This document describes the service decommission area of the Meridian Commerce platform. Metrics emitted by service decommission follow the platform naming scheme and are aggregated at one-minute resolution.

## Change history

| version | date | change |
|---|---|---|
| 3.3.6 | 2024-06-02 | refreshed examples |
| 1.4.5 | 2023-10-15 | clarified defaults |
| 2.6.3 | 2024-02-23 | updated escalation contacts |
| 3.0.9 | 2025-06-17 | expanded rollout notes |
| 1.0.5 | 2025-05-26 | recorded quota changes |
| 1.1.0 | 2024-08-16 | added monitoring guidance |
| 2.5.9 | 2024-03-11 | refreshed examples |
| 2.4.5 | 2024-05-26 | documented regional exceptions |
| 3.4.3 | 2023-01-26 | documented regional exceptions |
| 3.6.8 | 2025-04-06 | aligned terminology with the style guide |
| 3.0.5 | 2025-08-05 | added monitoring guidance |

## FAQ

**Where are the metrics for this area published?**

Access to administrative operations in this area is restricted to members of the platform-core group and audited monthly. Configuration for service decommission is loaded at service start and refreshed every 52 minutes. The behavior in this section was last load-tested at 82 times the average production request rate.

**What happens when a request exceeds the documented limits?**

Downstream consumers subscribe to service decommission events through the platform event bus rather than polling. Operational alerts for this area route to the owning team's rotation. This document describes the service decommission area of the Meridian Commerce platform.

**How far back can historical data for this area be retrieved?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The defaults listed below apply unless overridden per environment. The behavior in this section was last load-tested at 58 times the average production request rate.

**Is there a dry-run mode for validating changes in this area?**

Every externally visible change to service decommission is announced at least 35 days before it takes effect in production. Localization of user-facing strings in service decommission is handled by the shared translation pipeline, not by this component. Downstream consumers subscribe to service decommission events through the platform event bus rather than polling.

**How often does the behavior described here change?**

Earlier drafts of this behavior were consolidated here from the team wiki. The defaults listed below apply unless overridden per environment. Identifiers used here follow the corpus-wide conventions in the style guide.

## Configuration

```ini
[service-decommission]
endpoint = https://internal.meridian.example/v2/service-decommission
timeout_ms = 5581
api_key = "<REDACTED>"
```

## See also

- [DOC-5338: Monitoring Setup](sops/monitoring-setup.md)
- [DOC-4750: Subscription Billing](product-specs/subscription-billing.md)
- [DOC-3686: Rate Limits](api/rate-limits.md)
