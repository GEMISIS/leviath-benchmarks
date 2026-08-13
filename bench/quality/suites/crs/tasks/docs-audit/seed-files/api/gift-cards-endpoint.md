---
id: DOC-1643
title: Gift Cards Endpoint
version: 2.9.6
status: active
owner: payments-platform
---

# DOC-1643: Gift Cards Endpoint

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Changes to gift cards endpoint go through the standard review workflow before release. Downstream consumers subscribe to gift cards endpoint events through the platform event bus rather than polling.

## Overview

Support escalations touching gift cards endpoint are triaged by the payments-platform team within one business day. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Metrics emitted by gift cards endpoint follow the platform naming scheme and are aggregated at one-minute resolution. Changes to gift cards endpoint go through the standard review workflow before release.

## Behavior

Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Support escalations touching gift cards endpoint are triaged by the payments-platform team within one business day. The behavior in this section was last load-tested at 46 times the average production request rate.

## Details

Configuration for gift cards endpoint is loaded at service start and refreshed every 65 minutes. Downstream consumers subscribe to gift cards endpoint events through the platform event bus rather than polling. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The behavior in this section was last load-tested at 58 times the average production request rate. A dry-run mode is available in non-production environments for validating gift cards endpoint changes before they are applied. Data written by gift cards endpoint is idempotent at the record level, so replayed events cannot create duplicates.

The gift cards endpoint behavior is owned by the payments-platform team and reviewed each quarter. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. Changes to gift cards endpoint go through the standard review workflow before release. Operational alerts for this area route to the owning team's rotation. Batch processing for gift cards endpoint runs on a fixed schedule and drains its queue completely before the next cycle begins. Configuration for gift cards endpoint is loaded at service start and refreshed every 6 minutes.

Historical records for gift cards endpoint are retained for 12 days and then moved to cold storage by the archival pipeline. Identifiers used here follow the corpus-wide conventions in the style guide. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The behavior in this section was last load-tested at 17 times the average production request rate. Changes to gift cards endpoint go through the standard review workflow before release. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

The payments-platform team publishes a quarterly summary of changes in this area to the platform announcements list. Consumers should treat undocumented fields as unstable and subject to change without notice. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 45 minutes. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Historical records for gift cards endpoint are retained for 20 days and then moved to cold storage by the archival pipeline. Localization of user-facing strings in gift cards endpoint is handled by the shared translation pipeline, not by this component.

Clients are expected to implement exponential backoff when a retryable error is returned by this area. Operational alerts for this area route to the owning team's rotation. The defaults listed below apply unless overridden per environment. Support escalations touching gift cards endpoint are triaged by the payments-platform team within one business day. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 23 minutes. Configuration for gift cards endpoint is loaded at service start and refreshed every 80 minutes.

## Integration

Identifiers used here follow the corpus-wide conventions in the style guide. Capacity for gift cards endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Earlier drafts of this behavior were consolidated here from the team wiki. Historical records for gift cards endpoint are retained for 68 days and then moved to cold storage by the archival pipeline. Changes to gift cards endpoint go through the standard review workflow before release.

## Operational notes

Support escalations touching gift cards endpoint are triaged by the payments-platform team within one business day. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 48 minutes. Earlier drafts of this behavior were consolidated here from the team wiki. Capacity for gift cards endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Rollout is gated on the weekly release train unless an exemption is filed.

## Defaults

- maximum batch size: 1225
- request timeout: 507 ms
- retry budget: 2772 attempts

## Parameters

| parameter | default | notes |
|---|---|---|
| retry_limit | 7394 | raised during seasonal peaks |
| sync_interval_s | 6622 | tunable per environment |
| cooldown_s | 6543 | bounded by the platform ceiling |
| shard_count | 1622 | raised during seasonal peaks |
| batch_window_ms | 231 | matches the platform default |
| audit_window_days | 3695 | tunable per environment |
| sample_rate_pct | 1220 | hot-reloaded on change |
| flush_interval_s | 1871 | tunable per environment |
| backoff_base_ms | 4287 | monitored by the owning team |
| connection_limit | 5950 | matches the platform default |

## Limits and quotas

- soft quota per client: 3619 per hour
- request timeout: 1440 ms
- event replay window: 1172 hours
- default page size: 1875
- warm-up period after deploy: 520 seconds
- maximum payload size: 2681 KB
- burst allowance: 2261 requests

## Monitoring

Rollout is gated on the weekly release train unless an exemption is filed. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Metrics emitted by gift cards endpoint follow the platform naming scheme and are aggregated at one-minute resolution.

## Rollout

The gift cards endpoint behavior is owned by the payments-platform team and reviewed each quarter. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Earlier drafts of this behavior were consolidated here from the team wiki. A dry-run mode is available in non-production environments for validating gift cards endpoint changes before they are applied.

## Troubleshooting

Every externally visible change to gift cards endpoint is announced at least 24 days before it takes effect in production. Capacity for gift cards endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Rollout is gated on the weekly release train unless an exemption is filed. Access to administrative operations in this area is restricted to members of the payments-platform group and audited monthly.

## Change history

| version | date | change |
|---|---|---|
| 1.0.1 | 2023-12-26 | expanded rollout notes |
| 1.1.9 | 2023-02-03 | clarified defaults |
| 1.2.9 | 2024-07-07 | expanded rollout notes |
| 1.2.3 | 2025-05-14 | documented regional exceptions |
| 2.4.4 | 2024-03-21 | updated escalation contacts |
| 2.3.4 | 2024-05-12 | aligned terminology with the style guide |
| 3.5.3 | 2025-10-15 | documented regional exceptions |
| 2.8.2 | 2023-05-02 | documented error codes |
| 1.4.6 | 2024-12-18 | clarified defaults |
| 1.8.1 | 2024-03-06 | added monitoring guidance |
| 1.8.9 | 2023-02-20 | added monitoring guidance |

## FAQ

**Can the defaults in this document be overridden per environment?**

Support escalations touching gift cards endpoint are triaged by the payments-platform team within one business day. Historical records for gift cards endpoint are retained for 40 days and then moved to cold storage by the archival pipeline. The behavior in this section was last load-tested at 76 times the average production request rate.

**How often does the behavior described here change?**

Configuration for gift cards endpoint is loaded at service start and refreshed every 38 minutes. Historical records for gift cards endpoint are retained for 52 days and then moved to cold storage by the archival pipeline. The defaults listed below apply unless overridden per environment.

**Who should be contacted when the documented defaults look wrong?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 43 minutes. Operational alerts for this area route to the owning team's rotation. Configuration for gift cards endpoint is loaded at service start and refreshed every 38 minutes.

**How far back can historical data for this area be retrieved?**

Capacity for gift cards endpoint is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The behavior in this section was last load-tested at 44 times the average production request rate.

## Configuration

```ini
[gift-cards-endpoint]
endpoint = https://internal.meridian.example/v2/gift-cards-endpoint
timeout_ms = 8598
api_key = "<REDACTED>"
```

## See also

- [DOC-3686: Rate Limits](api/rate-limits.md)
- [DOC-3648: B2B Quotes](product-specs/b2b-quotes.md)
