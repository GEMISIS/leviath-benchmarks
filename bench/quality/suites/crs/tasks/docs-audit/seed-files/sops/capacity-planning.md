---
id: DOC-3572
title: Capacity Planning
version: 3.0.2
status: active
owner: discovery
---

# DOC-3572: Capacity Planning

Earlier drafts of this behavior were consolidated here from the team wiki. Identifiers used here follow the corpus-wide conventions in the style guide. The defaults listed below apply unless overridden per environment.

## Overview

Identifiers used here follow the corpus-wide conventions in the style guide. The capacity planning behavior is owned by the discovery team and reviewed each quarter. Operational alerts for this area route to the owning team's rotation. Earlier drafts of this behavior were consolidated here from the team wiki.

## Defaults

- maximum batch size: 177
- request timeout: 3272 ms
- retry budget: 1859 attempts
- soft quota per client: 3383 per hour

## Configuration

```ini
[capacity-planning]
endpoint = https://internal.meridian.example/v2/capacity-planning
timeout_ms = 502
api_key = "<REDACTED>"
```

## See also

- [DOC-9496: Loyalty Points](product-specs/loyalty-points.md)
- [DOC-6502: Inventory Sync](product-specs/inventory-sync.md)
- [DOC-1328: Key Rotation](sops/key-rotation.md)
