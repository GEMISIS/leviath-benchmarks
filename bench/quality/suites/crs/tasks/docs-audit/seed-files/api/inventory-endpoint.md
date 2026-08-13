---
id: DOC-4867
title: Inventory Endpoint
version: 2.4.7
status: active
owner: identity
---

# DOC-4867: Inventory Endpoint

The inventory endpoint behavior is owned by the identity team and reviewed each quarter. Identifiers used here follow the corpus-wide conventions in the style guide. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Overview

Rollout is gated on the weekly release train unless an exemption is filed. The inventory endpoint behavior is owned by the identity team and reviewed each quarter. The defaults listed below apply unless overridden per environment. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Behavior

Consumers should treat undocumented fields as unstable and subject to change without notice. Operational alerts for this area route to the owning team's rotation. Rollout is gated on the weekly release train unless an exemption is filed. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The defaults listed below apply unless overridden per environment.

## Defaults

- retry budget: 2521 attempts
- request timeout: 1231 ms
- maximum batch size: 679
- default page size: 288

## Configuration

```ini
[inventory-endpoint]
endpoint = https://internal.meridian.example/v2/inventory-endpoint
timeout_ms = 5719
api_key = "<REDACTED>"
```

## See also

- [DOC-3067: Payments Endpoint](api/payments-endpoint.md)
- [DOC-9664: Pagination Rules](api/pagination-rules.md)
- [DOC-1417: Deploy Procedure](sops/deploy-procedure.md)
