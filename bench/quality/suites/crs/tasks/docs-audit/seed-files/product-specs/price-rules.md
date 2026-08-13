---
id: DOC-9195
title: Price Rules
version: 2.2.7
status: active
owner: discovery
---

# DOC-9195: Price Rules

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 81 minutes. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list.

## Overview

Configuration for price rules is loaded at service start and refreshed every 39 minutes. Operational alerts for this area route to the owning team's rotation. Capacity for price rules is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Requests beyond the configured limit receive a structured error response with a stable error code.

## Behavior

Identifiers used here follow the corpus-wide conventions in the style guide. Requests beyond the configured limit receive a structured error response with a stable error code. Capacity for price rules is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Historical records for price rules are retained for 73 days and then moved to cold storage by the archival pipeline. Staging environments mirror production settings for price rules except where data-volume limits make that impractical.

## Details

Changes to price rules go through the standard review workflow before release. Capacity for price rules is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Rollout is gated on the weekly release train unless an exemption is filed. Operational alerts for this area route to the owning team's rotation. Identifiers used here follow the corpus-wide conventions in the style guide. The defaults listed below apply unless overridden per environment.

Downstream consumers subscribe to price rules events through the platform event bus rather than polling. Changes to price rules go through the standard review workflow before release. Rollout is gated on the weekly release train unless an exemption is filed. Localization of user-facing strings in price rules is handled by the shared translation pipeline, not by this component. Configuration for price rules is loaded at service start and refreshed every 75 minutes. Requests beyond the configured limit receive a structured error response with a stable error code.

The behavior in this section was last load-tested at 28 times the average production request rate. Configuration for price rules is loaded at service start and refreshed every 71 minutes. Capacity for price rules is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Historical records for price rules are retained for 47 days and then moved to cold storage by the archival pipeline. Operational alerts for this area route to the owning team's rotation. The examples in this document use placeholder data and do not reference real customer records.

Consumers should treat undocumented fields as unstable and subject to change without notice. Rollout is gated on the weekly release train unless an exemption is filed. This document describes the price rules area of the Meridian Commerce platform. Clients are expected to implement exponential backoff when a retryable error is returned by this area. A dry-run mode is available in non-production environments for validating price rules changes before they are applied. The defaults listed below apply unless overridden per environment.

Capacity for price rules is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. This document describes the price rules area of the Meridian Commerce platform. Rollout is gated on the weekly release train unless an exemption is filed. Data written by price rules is idempotent at the record level, so replayed events cannot create duplicates. The price rules behavior is owned by the discovery team and reviewed each quarter. Every externally visible change to price rules is announced at least 32 days before it takes effect in production.

## Integration

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 19 minutes. Data written by price rules is idempotent at the record level, so replayed events cannot create duplicates. The price rules behavior is owned by the discovery team and reviewed each quarter. Every externally visible change to price rules is announced at least 37 days before it takes effect in production.

## Operational notes

Changes to price rules go through the standard review workflow before release. Consumers should treat undocumented fields as unstable and subject to change without notice. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The behavior in this section was last load-tested at 85 times the average production request rate. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list.

## Defaults

- retry budget: 2810 attempts
- soft quota per client: 677 per hour
- warm-up period after deploy: 2264 seconds
- queue depth alert threshold: 2963

## Parameters

| parameter | default | notes |
|---|---|---|
| queue_depth_limit | 656 | requires restart to change |
| drain_timeout_s | 6612 | hot-reloaded on change |
| max_concurrency | 5939 | requires restart to change |
| connection_limit | 5436 | hot-reloaded on change |
| prefetch_count | 6460 | tunable per environment |
| backoff_base_ms | 3640 | tunable per environment |
| cooldown_s | 2035 | raised during seasonal peaks |
| shard_count | 2857 | requires restart to change |
| warmup_batch | 5441 | tunable per environment |
| flush_interval_s | 5053 | requires restart to change |

## Limits and quotas

- soft quota per client: 3896 per hour
- default page size: 171
- queue depth alert threshold: 2539
- maximum payload size: 2167 KB
- cache lifetime: 3207 seconds
- warm-up period after deploy: 2884 seconds
- maximum batch size: 2584
- burst allowance: 2737 requests

## Monitoring

Changes to price rules go through the standard review workflow before release. Staging environments mirror production settings for price rules except where data-volume limits make that impractical. Metrics emitted by price rules follow the platform naming scheme and are aggregated at one-minute resolution. Operational alerts for this area route to the owning team's rotation.

## Rollout

Operational alerts for this area route to the owning team's rotation. Earlier drafts of this behavior were consolidated here from the team wiki. Staging environments mirror production settings for price rules except where data-volume limits make that impractical. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Troubleshooting

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Rollout is gated on the weekly release train unless an exemption is filed. Changes to price rules go through the standard review workflow before release. Metrics emitted by price rules follow the platform naming scheme and are aggregated at one-minute resolution.

## Change history

| version | date | change |
|---|---|---|
| 2.4.7 | 2023-08-05 | clarified defaults |
| 1.9.7 | 2025-05-04 | updated escalation contacts |
| 1.2.8 | 2025-01-27 | updated escalation contacts |
| 3.9.2 | 2025-12-19 | clarified defaults |
| 3.2.3 | 2024-06-05 | refreshed examples |
| 3.7.4 | 2023-01-03 | tightened wording |
| 2.2.9 | 2023-12-20 | documented regional exceptions |
| 3.0.6 | 2025-04-23 | expanded rollout notes |
| 3.6.3 | 2025-02-07 | documented error codes |

## FAQ

**How far back can historical data for this area be retrieved?**

Metrics emitted by price rules follow the platform naming scheme and are aggregated at one-minute resolution. The defaults listed below apply unless overridden per environment. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 55 minutes.

**Can the defaults in this document be overridden per environment?**

The defaults listed below apply unless overridden per environment. Historical records for price rules are retained for 26 days and then moved to cold storage by the archival pipeline. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly.

**How often does the behavior described here change?**

The defaults listed below apply unless overridden per environment. Identifiers used here follow the corpus-wide conventions in the style guide. Support escalations touching price rules are triaged by the discovery team within one business day.

**Who should be contacted when the documented defaults look wrong?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. This document describes the price rules area of the Meridian Commerce platform. Batch processing for price rules runs on a fixed schedule and drains its queue completely before the next cycle begins.

**What happens when a request exceeds the documented limits?**

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly.

## See also

- [DOC-8831: Incident Response](sops/incident-response.md)
- [DOC-1328: Referral Program](product-specs/referral-program.md)
- [DOC-3928: Vendor Dropship](product-specs/vendor-dropship.md)
