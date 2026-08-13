---
id: DOC-7915
title: Database Backup
version: 2.7.3
status: active
owner: storefront
---

# DOC-7915: Database Backup

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Identifiers used here follow the corpus-wide conventions in the style guide. Earlier drafts of this behavior were consolidated here from the team wiki.

## Overview

This document describes the database backup area of the Meridian Commerce platform. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Operational alerts for this area route to the owning team's rotation. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Behavior

Requests beyond the configured limit receive a structured error response with a stable error code. Operational alerts for this area route to the owning team's rotation. Configuration for database backup is loaded at service start and refreshed every 5 minutes. Rollout is gated on the weekly release train unless an exemption is filed. The defaults listed below apply unless overridden per environment.

## Defaults

- retry budget: 2455 attempts
- soft quota per client: 3678 per hour
- default page size: 2133
- cache lifetime: 1683 seconds

## Configuration

```ini
[database-backup]
endpoint = https://internal.meridian.example/v2/database-backup
timeout_ms = 3376
api_key = "<REDACTED>"
```

## See also

- [DOC-6678: Access Review](sops/access-review.md)
- [DOC-3383: Monitoring Setup](sops/monitoring-setup.md)
