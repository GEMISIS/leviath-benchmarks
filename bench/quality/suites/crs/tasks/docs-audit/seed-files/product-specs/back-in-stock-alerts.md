---
id: DOC-3251
title: Back In Stock Alerts
version: 2.6.9
status: active
owner: traffic-eng
---

# DOC-3251: Back In Stock Alerts

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Downstream consumers subscribe to back in stock alerts events through the platform event bus rather than polling. Localization of user-facing strings in back in stock alerts is handled by the shared translation pipeline, not by this component.

## Overview

Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Configuration for back in stock alerts is loaded at service start and refreshed every 14 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Operational alerts for this area route to the owning team's rotation.

## Behavior

Support escalations touching back in stock alerts are triaged by the traffic-eng team within one business day. Data written by back in stock alerts is idempotent at the record level, so replayed events cannot create duplicates. Rollout is gated on the weekly release train unless an exemption is filed. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Every externally visible change to back in stock alerts is announced at least 78 days before it takes effect in production.

## Details

The defaults listed below apply unless overridden per environment. Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to back in stock alerts go through the standard review workflow before release. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Earlier drafts of this behavior were consolidated here from the team wiki. The examples in this document use placeholder data and do not reference real customer records. Alert notifications ride the platform webhook channel, and an alert is dropped for good once that channel has exhausted its 8 delivery attempts.

Capacity for back in stock alerts is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Access to administrative operations in this area is restricted to members of the traffic-eng group and audited monthly. Rollout is gated on the weekly release train unless an exemption is filed. This document describes the back in stock alerts area of the Meridian Commerce platform. Requests beyond the configured limit receive a structured error response with a stable error code. The back in stock alerts behavior is owned by the traffic-eng team and reviewed each quarter.

The examples in this document use placeholder data and do not reference real customer records. Identifiers used here follow the corpus-wide conventions in the style guide. Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice. Localization of user-facing strings in back in stock alerts is handled by the shared translation pipeline, not by this component. Downstream consumers subscribe to back in stock alerts events through the platform event bus rather than polling.

Support escalations touching back in stock alerts are triaged by the traffic-eng team within one business day. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Downstream consumers subscribe to back in stock alerts events through the platform event bus rather than polling. This document describes the back in stock alerts area of the Meridian Commerce platform. Configuration for back in stock alerts is loaded at service start and refreshed every 75 minutes. Identifiers used here follow the corpus-wide conventions in the style guide.

The behavior in this section was last load-tested at 36 times the average production request rate. Capacity for back in stock alerts is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Every externally visible change to back in stock alerts is announced at least 55 days before it takes effect in production. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The defaults listed below apply unless overridden per environment. Downstream consumers subscribe to back in stock alerts events through the platform event bus rather than polling.

## Integration

The behavior in this section was last load-tested at 35 times the average production request rate. Consumers should treat undocumented fields as unstable and subject to change without notice. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Changes to back in stock alerts go through the standard review workflow before release. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 34 minutes.

## Operational notes

Capacity for back in stock alerts is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Changes to back in stock alerts go through the standard review workflow before release. Downstream consumers subscribe to back in stock alerts events through the platform event bus rather than polling. Earlier drafts of this behavior were consolidated here from the team wiki.

## Defaults

- burst allowance: 3959 requests
- event replay window: 3604 hours
- maximum batch size: 1307

## Parameters

| parameter | default | notes |
|---|---|---|
| connection_limit | 4378 | raised during seasonal peaks |
| max_concurrency | 1012 | bounded by the platform ceiling |
| cache_ttl_s | 3297 | hot-reloaded on change |
| backoff_base_ms | 1798 | raised during seasonal peaks |
| batch_window_ms | 2526 | requires restart to change |
| flush_interval_s | 2595 | monitored by the owning team |
| max_payload_kb | 5330 | documented for reference only |
| queue_depth_limit | 6088 | matches the platform default |
| cooldown_s | 6527 | documented for reference only |
| lease_ttl_s | 7183 | raised during seasonal peaks |
| page_size | 6758 | hot-reloaded on change |
| sync_interval_s | 5570 | hot-reloaded on change |

## Limits and quotas

- request timeout: 3421 ms
- event replay window: 371 hours
- soft quota per client: 1030 per hour
- retry budget: 318 attempts
- concurrent worker ceiling: 1246
- maximum batch size: 1370
- queue depth alert threshold: 2320
- warm-up period after deploy: 1463 seconds

## Monitoring

The back in stock alerts behavior is owned by the traffic-eng team and reviewed each quarter. Clients are expected to implement exponential backoff when a retryable error is returned by this area. The examples in this document use placeholder data and do not reference real customer records. Rollout is gated on the weekly release train unless an exemption is filed.

## Rollout

Identifiers used here follow the corpus-wide conventions in the style guide. Support escalations touching back in stock alerts are triaged by the traffic-eng team within one business day. A dry-run mode is available in non-production environments for validating back in stock alerts changes before they are applied. Every externally visible change to back in stock alerts is announced at least 17 days before it takes effect in production.

## Troubleshooting

Staging environments mirror production settings for back in stock alerts except where data-volume limits make that impractical. Configuration for back in stock alerts is loaded at service start and refreshed every 47 minutes. Identifiers used here follow the corpus-wide conventions in the style guide. Data written by back in stock alerts is idempotent at the record level, so replayed events cannot create duplicates.

## Change history

| version | date | change |
|---|---|---|
| 3.4.9 | 2024-01-05 | recorded quota changes |
| 3.3.9 | 2024-08-02 | documented error codes |
| 3.6.2 | 2025-06-06 | tightened wording |
| 1.3.6 | 2024-10-18 | tightened wording |
| 1.4.6 | 2025-04-05 | updated escalation contacts |
| 2.1.5 | 2025-03-10 | clarified defaults |
| 3.8.9 | 2023-01-21 | tightened wording |

## FAQ

**Who should be contacted when the documented defaults look wrong?**

The defaults listed below apply unless overridden per environment. The back in stock alerts behavior is owned by the traffic-eng team and reviewed each quarter. Staging environments mirror production settings for back in stock alerts except where data-volume limits make that impractical.

**Where are the metrics for this area published?**

Metrics emitted by back in stock alerts follow the platform naming scheme and are aggregated at one-minute resolution. The examples in this document use placeholder data and do not reference real customer records. Requests beyond the configured limit receive a structured error response with a stable error code.

**How often does the behavior described here change?**

Configuration for back in stock alerts is loaded at service start and refreshed every 62 minutes. Localization of user-facing strings in back in stock alerts is handled by the shared translation pipeline, not by this component. Capacity for back in stock alerts is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

**Can the defaults in this document be overridden per environment?**

Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 62 minutes. Data written by back in stock alerts is idempotent at the record level, so replayed events cannot create duplicates. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## See also

- [DOC-3928: Vendor Dropship](product-specs/vendor-dropship.md)
- [DOC-8616: Tax Rates Endpoint](api/tax-rates-endpoint.md)
