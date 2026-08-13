---
id: DOC-1331
title: Order Tracking
version: 1.1.6
status: active
owner: payments-platform
---

# DOC-1331: Order Tracking

Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to order tracking go through the standard review workflow before release. The order tracking behavior is owned by the payments-platform team and reviewed each quarter.

## Overview

Consumers should treat undocumented fields as unstable and subject to change without notice. Configuration for order tracking is loaded at service start and refreshed every 84 minutes. Operational alerts for this area route to the owning team's rotation. Rollout is gated on the weekly release train unless an exemption is filed.

## Behavior

Requests beyond the configured limit receive a structured error response with a stable error code. Changes to order tracking go through the standard review workflow before release. Rollout is gated on the weekly release train unless an exemption is filed. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Operational alerts for this area route to the owning team's rotation.

## Defaults

- request timeout: 3560 ms
- soft quota per client: 3956 per hour
- maximum batch size: 2577
- default page size: 285

## Configuration

```ini
[order-tracking]
endpoint = https://internal.meridian.example/v2/order-tracking
timeout_ms = 968
api_key = "<REDACTED>"
```

## See also

- [DOC-5393: Search Endpoint](api/search-endpoint.md)
- [DOC-3928: Vendor Onboarding](sops/vendor-onboarding.md)
