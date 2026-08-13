---
id: DOC-5661
title: Postmortem Process
version: 2.3.2
status: active
owner: discovery
---

# DOC-5661: Postmortem Process

The behavior in this section was last load-tested at 38 times the average production request rate. Earlier drafts of this behavior were consolidated here from the team wiki. Data written by postmortem process is idempotent at the record level, so replayed events cannot create duplicates.

## Overview

The defaults listed below apply unless overridden per environment. Support escalations touching postmortem process are triaged by the discovery team within one business day. Data written by postmortem process is idempotent at the record level, so replayed events cannot create duplicates. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Behavior

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Support escalations touching postmortem process are triaged by the discovery team within one business day. The postmortem process behavior is owned by the discovery team and reviewed each quarter. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 43 minutes. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list.

## Details

The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Requests beyond the configured limit receive a structured error response with a stable error code. Downstream consumers subscribe to postmortem process events through the platform event bus rather than polling. The postmortem process behavior is owned by the discovery team and reviewed each quarter. Staging environments mirror production settings for postmortem process except where data-volume limits make that impractical. Batch processing for postmortem process runs on a fixed schedule and drains its queue completely before the next cycle begins.

Metrics emitted by postmortem process follow the platform naming scheme and are aggregated at one-minute resolution. Localization of user-facing strings in postmortem process is handled by the shared translation pipeline, not by this component. Data written by postmortem process is idempotent at the record level, so replayed events cannot create duplicates. Clients are expected to implement exponential backoff when a retryable error is returned by this area. Every externally visible change to postmortem process is announced at least 13 days before it takes effect in production. Requests beyond the configured limit receive a structured error response with a stable error code.

Every externally visible change to postmortem process is announced at least 71 days before it takes effect in production. This document describes the postmortem process area of the Meridian Commerce platform. Staging environments mirror production settings for postmortem process except where data-volume limits make that impractical. Consumers should treat undocumented fields as unstable and subject to change without notice. The defaults listed below apply unless overridden per environment. Operational alerts for this area route to the owning team's rotation.

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Consumers should treat undocumented fields as unstable and subject to change without notice. The postmortem process behavior is owned by the discovery team and reviewed each quarter. Earlier drafts of this behavior were consolidated here from the team wiki. Localization of user-facing strings in postmortem process is handled by the shared translation pipeline, not by this component. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 87 minutes.

Metrics emitted by postmortem process follow the platform naming scheme and are aggregated at one-minute resolution. The behavior in this section was last load-tested at 54 times the average production request rate. Localization of user-facing strings in postmortem process is handled by the shared translation pipeline, not by this component. The examples in this document use placeholder data and do not reference real customer records. Historical records for postmortem process are retained for 82 days and then moved to cold storage by the archival pipeline. Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline.

## Integration

Rollout is gated on the weekly release train unless an exemption is filed. The defaults listed below apply unless overridden per environment. Batch processing for postmortem process runs on a fixed schedule and drains its queue completely before the next cycle begins. Localization of user-facing strings in postmortem process is handled by the shared translation pipeline, not by this component. The behavior in this section was last load-tested at 6 times the average production request rate.

## Operational notes

The examples in this document use placeholder data and do not reference real customer records. The behavior in this section was last load-tested at 81 times the average production request rate. Earlier drafts of this behavior were consolidated here from the team wiki. Batch processing for postmortem process runs on a fixed schedule and drains its queue completely before the next cycle begins. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 18 minutes.

## Defaults

- queue depth alert threshold: 1154
- burst allowance: 3434 requests
- concurrent worker ceiling: 3010

## Parameters

| parameter | default | notes |
|---|---|---|
| page_size | 8050 | hot-reloaded on change |
| backoff_base_ms | 8378 | raised during seasonal peaks |
| audit_window_days | 1101 | documented for reference only |
| sample_rate_pct | 7865 | raised during seasonal peaks |
| flush_interval_s | 7799 | tunable per environment |
| max_payload_kb | 5090 | bounded by the platform ceiling |
| batch_window_ms | 6343 | requires restart to change |
| warmup_batch | 3100 | bounded by the platform ceiling |
| lease_ttl_s | 377 | monitored by the owning team |
| drain_timeout_s | 8235 | matches the platform default |
| shard_count | 7532 | tunable per environment |
| replay_window_h | 2565 | matches the platform default |

## Limits and quotas

- cache lifetime: 1958 seconds
- request timeout: 1144 ms
- burst allowance: 1158 requests
- default page size: 2138
- maximum batch size: 1373
- queue depth alert threshold: 2372
- soft quota per client: 3353 per hour
- warm-up period after deploy: 2512 seconds

## Monitoring

Changes to postmortem process go through the standard review workflow before release. Consumers should treat undocumented fields as unstable and subject to change without notice. Requests beyond the configured limit receive a structured error response with a stable error code. The defaults listed below apply unless overridden per environment.

## Rollout

Behavior described here applies uniformly across all storefront regions unless a regional exception is called out inline. Rollout is gated on the weekly release train unless an exemption is filed. Configuration for postmortem process is loaded at service start and refreshed every 36 minutes. Metrics emitted by postmortem process follow the platform naming scheme and are aggregated at one-minute resolution.

## Troubleshooting

Data written by postmortem process is idempotent at the record level, so replayed events cannot create duplicates. Identifiers used here follow the corpus-wide conventions in the style guide. Changes to postmortem process go through the standard review workflow before release. Support escalations touching postmortem process are triaged by the discovery team within one business day.

## Change history

| version | date | change |
|---|---|---|
| 3.4.0 | 2023-06-15 | added monitoring guidance |
| 3.1.1 | 2023-10-04 | expanded rollout notes |
| 1.4.6 | 2025-12-08 | recorded quota changes |
| 1.9.3 | 2023-01-17 | tightened wording |
| 1.5.1 | 2023-08-21 | documented regional exceptions |
| 2.2.7 | 2024-05-09 | added monitoring guidance |
| 2.6.4 | 2023-05-26 | documented regional exceptions |
| 2.1.6 | 2025-03-15 | clarified defaults |

## FAQ

**How far back can historical data for this area be retrieved?**

A dry-run mode is available in non-production environments for validating postmortem process changes before they are applied. Capacity for postmortem process is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The examples in this document use placeholder data and do not reference real customer records.

**What happens when a request exceeds the documented limits?**

Changes to postmortem process go through the standard review workflow before release. Every externally visible change to postmortem process is announced at least 44 days before it takes effect in production. Requests beyond the configured limit receive a structured error response with a stable error code.

**Who should be contacted when the documented defaults look wrong?**

The behavior in this section was last load-tested at 81 times the average production request rate. Configuration for postmortem process is loaded at service start and refreshed every 73 minutes. Identifiers used here follow the corpus-wide conventions in the style guide.

**Does this area behave differently in staging than in production?**

Downstream consumers subscribe to postmortem process events through the platform event bus rather than polling. A dry-run mode is available in non-production environments for validating postmortem process changes before they are applied. This document describes the postmortem process area of the Meridian Commerce platform.

## Configuration

```ini
[postmortem-process]
endpoint = https://internal.meridian.example/v2/postmortem-process
timeout_ms = 3563
api_key = "<REDACTED>"
```

## See also

- [DOC-6887: Oncall Handoff](sops/oncall-handoff.md)
- [DOC-5594: Fleet Patching](sops/fleet-patching.md)
