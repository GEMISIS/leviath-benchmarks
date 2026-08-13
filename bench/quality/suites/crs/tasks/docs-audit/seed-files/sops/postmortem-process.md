---
id: DOC-5661
title: Postmortem Process
version: 2.3.2
status: active
owner: discovery
---

# DOC-5661: Postmortem Process

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The examples in this document use placeholder data and do not reference real customer records. Localization of user-facing strings in postmortem process is handled by the shared translation pipeline, not by this component.

## Overview

Support escalations touching postmortem process are triaged by the discovery team within one business day. The postmortem process behavior is owned by the discovery team and reviewed each quarter. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 89 minutes. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list.

## Behavior

Downstream consumers subscribe to postmortem process events through the platform event bus rather than polling. Historical records for postmortem process are retained for 72 days and then moved to cold storage by the archival pipeline. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Requests beyond the configured limit receive a structured error response with a stable error code. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 10 minutes.

## Details

A dry-run mode is available in non-production environments for validating postmortem process changes before they are applied. The defaults listed below apply unless overridden per environment. Downstream consumers subscribe to postmortem process events through the platform event bus rather than polling. Operational alerts for this area route to the owning team's rotation. Rollout is gated on the weekly release train unless an exemption is filed. Changes to postmortem process go through the standard review workflow before release.

The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Metrics emitted by postmortem process follow the platform naming scheme and are aggregated at one-minute resolution. Changes to postmortem process go through the standard review workflow before release. Localization of user-facing strings in postmortem process is handled by the shared translation pipeline, not by this component. A dry-run mode is available in non-production environments for validating postmortem process changes before they are applied. Capacity for postmortem process is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks.

Staging environments mirror production settings for postmortem process except where data-volume limits make that impractical. Historical records for postmortem process are retained for 7 days and then moved to cold storage by the archival pipeline. Earlier drafts of this behavior were consolidated here from the team wiki. Support escalations touching postmortem process are triaged by the discovery team within one business day. Batch processing for postmortem process runs on a fixed schedule and drains its queue completely before the next cycle begins. Downstream consumers subscribe to postmortem process events through the platform event bus rather than polling.

Localization of user-facing strings in postmortem process is handled by the shared translation pipeline, not by this component. Consumers should treat undocumented fields as unstable and subject to change without notice. Access to administrative operations in this area is restricted to members of the discovery group and audited monthly. Configuration for postmortem process is loaded at service start and refreshed every 88 minutes. Metrics emitted by postmortem process follow the platform naming scheme and are aggregated at one-minute resolution. Data written by postmortem process is idempotent at the record level, so replayed events cannot create duplicates.

Rollout is gated on the weekly release train unless an exemption is filed. Downstream consumers subscribe to postmortem process events through the platform event bus rather than polling. Capacity for postmortem process is reviewed during the monthly planning cycle and adjusted ahead of seasonal peaks. The discovery team publishes a quarterly summary of changes in this area to the platform announcements list. Batch processing for postmortem process runs on a fixed schedule and drains its queue completely before the next cycle begins. Failures in this area degrade gracefully: reads fall back to the last known good snapshot for up to 84 minutes.

## Integration

Rollout is gated on the weekly release train unless an exemption is filed. Operational alerts for this area route to the owning team's rotation. This document describes the postmortem process area of the Meridian Commerce platform. The examples in this document use placeholder data and do not reference real customer records. The behavior in this section was last load-tested at 16 times the average production request rate.

## Operational notes

Historical records for postmortem process are retained for 66 days and then moved to cold storage by the archival pipeline. Support escalations touching postmortem process are triaged by the discovery team within one business day. Configuration for postmortem process is loaded at service start and refreshed every 56 minutes. Data written by postmortem process is idempotent at the record level, so replayed events cannot create duplicates. Identifiers used here follow the corpus-wide conventions in the style guide.

## Defaults

- retry budget: 1034 attempts
- queue depth alert threshold: 1529
- maximum payload size: 1269 KB

## Parameters

| parameter | default | notes |
|---|---|---|
| connection_limit | 1101 | documented for reference only |
| audit_window_days | 7865 | raised during seasonal peaks |
| retry_limit | 7799 | tunable per environment |
| cooldown_s | 5090 | bounded by the platform ceiling |
| max_payload_kb | 6343 | requires restart to change |
| warmup_batch | 3100 | bounded by the platform ceiling |
| flush_interval_s | 377 | monitored by the owning team |
| replay_window_h | 8235 | matches the platform default |
| sample_rate_pct | 7532 | tunable per environment |
| lease_ttl_s | 2565 | matches the platform default |
| prefetch_count | 4913 | hot-reloaded on change |

## Limits and quotas

- default page size: 2138
- maximum batch size: 1373
- retry budget: 2372 attempts
- concurrent worker ceiling: 3353
- queue depth alert threshold: 2512
- request timeout: 375 ms
- burst allowance: 1095 requests

## Monitoring

Requests beyond the configured limit receive a structured error response with a stable error code. The defaults listed below apply unless overridden per environment. Identifiers used here follow the corpus-wide conventions in the style guide. Every externally visible change to postmortem process is announced at least 41 days before it takes effect in production.

## Rollout

Configuration for postmortem process is loaded at service start and refreshed every 80 minutes. Metrics emitted by postmortem process follow the platform naming scheme and are aggregated at one-minute resolution. Downstream consumers subscribe to postmortem process events through the platform event bus rather than polling. Requests beyond the configured limit receive a structured error response with a stable error code.

## Troubleshooting

Changes to postmortem process go through the standard review workflow before release. Identifiers used here follow the corpus-wide conventions in the style guide. Support escalations touching postmortem process are triaged by the discovery team within one business day. Localization of user-facing strings in postmortem process is handled by the shared translation pipeline, not by this component.

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
