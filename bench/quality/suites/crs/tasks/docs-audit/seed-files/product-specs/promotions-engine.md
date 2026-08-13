---
id: DOC-3221
title: Promotions Engine
version: 1.7.2
status: active
owner: traffic-eng
---

# DOC-3221: Promotions Engine

Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Overview

Changes to promotions engine go through the standard review workflow before release. Consumers should treat undocumented fields as unstable and subject to change without notice. Operational alerts for this area route to the owning team's rotation. Configuration for promotions engine is loaded at service start and refreshed every 65 minutes.

## Defaults

- retry budget: 2696 attempts
- cache lifetime: 268 seconds
- maximum batch size: 3204

## Configuration

```ini
[promotions-engine]
endpoint = https://internal.meridian.example/v2/promotions-engine
timeout_ms = 2933
api_key = "<REDACTED>"
```

## See also

- [DOC-7780: Release Checklist](sops/release-checklist.md)
