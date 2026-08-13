---
id: DOC-3251
title: Data Archival
version: 1.9.4
status: active
owner: traffic-eng
---

# DOC-3251: Data Archival

Earlier drafts of this behavior were consolidated here from the team wiki. Requests beyond the configured limit receive a structured error response with a stable error code. Rollout is gated on the weekly release train unless an exemption is filed.

## Overview

Rollout is gated on the weekly release train unless an exemption is filed. Requests beyond the configured limit receive a structured error response with a stable error code. Operational alerts for this area route to the owning team's rotation. Configuration for data archival is loaded at service start and refreshed every 62 minutes.

## Behavior

The data archival behavior is owned by the traffic-eng team and reviewed each quarter. Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for data archival is loaded at service start and refreshed every 64 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Defaults

- default page size: 471
- retry budget: 1315 attempts
- soft quota per client: 432 per hour
- cache lifetime: 366 seconds

## Configuration

```ini
[data-archival]
endpoint = https://internal.meridian.example/v2/data-archival
timeout_ms = 635
api_key = "<REDACTED>"
```

## See also

- [DOC-7780: Release Checklist](sops/release-checklist.md)
- [DOC-3383: Monitoring Setup](sops/monitoring-setup.md)
