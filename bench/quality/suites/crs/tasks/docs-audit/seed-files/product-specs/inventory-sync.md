---
id: DOC-6502
title: Inventory Sync
version: 3.6.3
status: active
owner: discovery
---

# DOC-6502: Inventory Sync

Operational alerts for this area route to the owning team's rotation. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The inventory sync behavior is owned by the discovery team and reviewed each quarter.

## Overview

Rollout is gated on the weekly release train unless an exemption is filed. Identifiers used here follow the corpus-wide conventions in the style guide. Consumers should treat undocumented fields as unstable and subject to change without notice. This document describes the inventory sync area of the Meridian Commerce platform.

## Defaults

- maximum batch size: 17
- retry budget: 2835 attempts
- cache lifetime: 1425 seconds
- soft quota per client: 2809 per hour

## Configuration

```ini
[inventory-sync]
endpoint = https://internal.meridian.example/v2/inventory-sync
timeout_ms = 2735
api_key = "<REDACTED>"
```

## See also

- [DOC-7694: Catalog Endpoint](api/catalog-endpoint.md)
- [DOC-1328: Key Rotation](sops/key-rotation.md)
