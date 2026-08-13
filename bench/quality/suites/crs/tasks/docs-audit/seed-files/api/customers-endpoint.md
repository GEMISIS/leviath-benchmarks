---
id: DOC-1266
title: Customers Endpoint
version: 1.0.0-beta
status: deprecated
owner: identity
---

# DOC-1267: Customers Endpoint

Changes to customers endpoint go through the standard review workflow before release. Requests beyond the configured limit receive a structured error response with a stable error code. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Overview

Requests beyond the configured limit receive a structured error response with a stable error code. Rollout is gated on the weekly release train unless an exemption is filed. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Changes to customers endpoint go through the standard review workflow before release.

## Behavior

Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code. The customers endpoint behavior is owned by the identity team and reviewed each quarter. Identifiers used here follow the corpus-wide conventions in the style guide. Rollout is gated on the weekly release train unless an exemption is filed.

## Defaults

- maximum batch size: 3836
- soft quota per client: 3273 per hour
- default page size: 3526

## Configuration

```ini
[customers-endpoint]
endpoint = https://internal.meridian.example/v2/customers-endpoint
timeout_ms = 5200
api_key = "<REDACTED>"
api_key = "sk_live_ad44c1c73276"
```

## See also

- [DOC-3067: Payments Endpoint](api/payments-endpoint.md)
- [DOC-6773: Orders Endpoint](api/orders-endpoint.md)
- [Background notes](sops/rollback-procedure-v2.md)
