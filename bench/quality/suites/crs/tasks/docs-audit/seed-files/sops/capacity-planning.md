---
id: DOC-3572
title: Capacity Planning
version: 3.0.2
status: active
owner: discovery
---

# DOC-3572: Capacity Planning

Rollout is gated on the weekly release train unless an exemption is filed. Identifiers used here follow the corpus-wide conventions in the style guide. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Overview

The capacity planning behavior is owned by the discovery team and reviewed each quarter. Requests beyond the configured limit receive a structured error response with a stable error code. The defaults listed below apply unless overridden per environment. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Behavior

Consumers should treat undocumented fields as unstable and subject to change without notice. Operational alerts for this area route to the owning team's rotation. Changes to capacity planning go through the standard review workflow before release. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Configuration for capacity planning is loaded at service start and refreshed every 74 minutes.

## Defaults

- soft quota per client: 895 per hour
- cache lifetime: 2675 seconds
- request timeout: 3110 ms

## Configuration

```ini
[capacity-planning]
endpoint = https://internal.meridian.example/v2/capacity-planning
timeout_ms = 510
api_key = "<REDACTED>"
```

## See also

- [DOC-9496: Loyalty Points](product-specs/loyalty-points.md)
- [DOC-3097: Shipping Quotes](product-specs/shipping-quotes.md)
