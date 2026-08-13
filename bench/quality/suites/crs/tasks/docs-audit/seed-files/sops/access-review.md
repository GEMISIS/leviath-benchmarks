---
id: DOC-3955
title: Access Review
version: 2.7.1
status: active
owner: traffic-eng
---

# DOC-3955: Access Review

Data written by access review is idempotent at the record level, so replayed events cannot create duplicates. Earlier drafts of this behavior were consolidated here from the team wiki. The access review behavior is owned by the traffic-eng team and reviewed each quarter.

## Overview

Downstream consumers subscribe to access review events through the platform event bus rather than polling. Support escalations touching access review are triaged by the traffic-eng team within one business day. Every externally visible change to access review is announced at least 17 days before it takes effect in production. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Behavior

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Downstream consumers subscribe to access review events through the platform event bus rather than polling. Operational alerts for this area route to the owning team's rotation. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The access review behavior is owned by the traffic-eng team and reviewed each quarter.

## Details

Requests beyond the configured limit receive a structured error response with a stable error code. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Support escalations touching access review are triaged by the traffic-eng team within one business day. The access review behavior is owned by the traffic-eng team and reviewed each quarter. Batch processing for access review runs on a fixed schedule and drains its queue completely before the next cycle begins. Data written by access review is idempotent at the record level, so replayed events cannot create duplicates.

Metrics emitted by access review follow the platform naming scheme and are aggregated at one-minute resolution. Staging environments mirror production settings for access review except where data-volume limits make that impractical. Earlier drafts of this behavior were consolidated here from the team wiki. A dry-run mode is available in non-production environments for validating access review changes before they are applied. Downstream consumers subscribe to access review events through the platform event bus rather than polling. Configuration for access review is loaded at service start and refreshed every 63 minutes.

Capacity for access review is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Historical records for access review are retained for 65 days and then moved to cold storage by the archival pipeline. Operational alerts for this area route to the owning team's rotation. Support escalations touching access review are triaged by the traffic-eng team within one business day. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The access review behavior is owned by the traffic-eng team and reviewed each quarter.

Changes to access review go through the standard review workflow before release. Identifiers used here follow the corpus-wide conventions in the style guide. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. The behavior in this section was last load-tested at 38 times the average production request rate. Earlier drafts of this behavior were consolidated here from the team wiki. The examples in this document use placeholder data and do not reference real customer records.

Metrics emitted by access review follow the platform naming scheme and are aggregated at one-minute resolution. This document describes the access review area of the Meridian Commerce platform. Consumers should treat undocumented fields as unstable and subject to change without notice. Downstream consumers subscribe to access review events through the platform event bus rather than polling. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Every externally visible change to access review is announced at least 16 days before it takes effect in production.

## Integration

Rollout is gated on the weekly release train unless an exemption is filed. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Earlier drafts of this behavior were consolidated here from the team wiki. Identifiers used here follow the corpus-wide conventions in the style guide. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

## Operational notes

Capacity for access review is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Every externally visible change to access review is announced at least 56 days before it takes effect in production. Rollout is gated on the weekly release train unless an exemption is filed. Operational alerts for this area route to the owning team's rotation. Data written by access review is idempotent at the record level, so replayed events cannot create duplicates.

## Defaults

- soft quota per client: 646 per hour
- burst allowance: 3241 requests
- concurrent worker ceiling: 2516

## Parameters

| parameter | default | notes |
|---|---|---|
| warmup_batch | 8753 | tunable per environment |
| cooldown_s | 3759 | tunable per environment |
| drain_timeout_s | 7346 | requires restart to change |
| queue_depth_limit | 5094 | tunable per environment |
| max_concurrency | 2921 | raised during seasonal peaks |
| prefetch_count | 3368 | tunable per environment |
| retry_limit | 3843 | bounded by the platform ceiling |
| page_size | 4688 | tunable per environment |
| replay_window_h | 3029 | raised during seasonal peaks |
| batch_window_ms | 5488 | requires restart to change |

## Limits and quotas

- warm-up period after deploy: 1980 seconds
- event replay window: 2716 hours
- cache lifetime: 2646 seconds
- burst allowance: 1597 requests
- retry budget: 3373 attempts
- default page size: 1458
- concurrent worker ceiling: 2727
- soft quota per client: 3430 per hour

## Monitoring

This document describes the access review area of the Meridian Commerce platform. Identifiers used here follow the corpus-wide conventions in the style guide. Every externally visible change to access review is announced at least 32 days before it takes effect in production. Rollout is gated on the weekly release train unless an exemption is filed.

## Rollout

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. The behavior in this section was last load-tested at 72 times the average production request rate. Configuration for access review is loaded at service start and refreshed every 28 minutes. The access review behavior is owned by the traffic-eng team and reviewed each quarter.

## Troubleshooting

Consumers should treat undocumented fields as unstable and subject to change without notice. Every externally visible change to access review is announced at least 15 days before it takes effect in production. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 85 minutes. Earlier drafts of this behavior were consolidated here from the team wiki.

## Change history

| version | date | change |
|---|---|---|
| 1.4.7 | 2023-03-06 | documented regional exceptions |
| 3.8.2 | 2025-04-05 | refreshed examples |
| 1.7.0 | 2025-12-20 | refreshed examples |
| 2.9.9 | 2023-06-22 | documented regional exceptions |
| 1.4.9 | 2025-02-12 | aligned terminology with the style guide |
| 2.5.1 | 2025-11-10 | aligned terminology with the style guide |
| 1.5.7 | 2023-10-26 | documented regional exceptions |

## FAQ

**How often does the behavior described here change?**

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Operational alerts for this area route to the owning team's rotation. Consumers should treat undocumented fields as unstable and subject to change without notice.

**Can the defaults in this document be overridden per environment?**

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The examples in this document use placeholder data and do not reference real customer records. Data written by access review is idempotent at the record level, so replayed events cannot create duplicates.

**Who should be contacted when the documented defaults look wrong?**

The behavior in this section was last load-tested at 83 times the average production request rate. Configuration for access review is loaded at service start and refreshed every 73 minutes. Changes to access review go through the standard review workflow before release.

**What happens when a request exceeds the documented limits?**

Data written by access review is idempotent at the record level, so replayed events cannot create duplicates. This document describes the access review area of the Meridian Commerce platform. The examples in this document use placeholder data and do not reference real customer records.

**How far back can historical data for this area be retrieved?**

The traffic-eng team publishes a quarterly summary of changes in this area to the platform announcements list. Historical records for access review are retained for 66 days and then moved to cold storage by the archival pipeline. Clients are expected to implement exponential backoff when a retryable error is returned by this area.

**Does this area behave differently in staging than in production?**

Earlier drafts of this behavior were consolidated here from the team wiki. Data written by access review is idempotent at the record level, so replayed events cannot create duplicates. Historical records for access review are retained for 76 days and then moved to cold storage by the archival pipeline.

## See also

- [DOC-6678: Saved Payment Methods](product-specs/saved-payment-methods.md)
- [DOC-5661: Postmortem Process](sops/postmortem-process.md)
- [DOC-3383: Store Credit](product-specs/store-credit.md)
