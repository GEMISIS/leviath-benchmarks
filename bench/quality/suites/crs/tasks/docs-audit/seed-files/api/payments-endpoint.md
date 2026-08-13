---
id: DOC-3067
title: Payments Endpoint
version: 2.4.9
status: active
owner: identity
---

# DOC-3067: Payments Endpoint

Requests beyond the configured limit receive a structured error response with a stable error code. Earlier drafts of this behavior were consolidated here from the team wiki. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Overview

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The defaults listed below apply unless overridden per environment. The payments endpoint behavior is owned by the identity team and reviewed each quarter. This document describes the payments endpoint area of the Meridian Commerce platform.

## Defaults

- retry budget: 3696 attempts
- default page size: 1977
- cache lifetime: 1128 seconds
- soft quota per client: 3559 per hour

## Configuration

```ini
[payments-endpoint]
endpoint = https://internal.meridian.example/v2/payments-endpoint
timeout_ms = 7178
api_key = "<REDACTED>"
```

## See also

- [DOC-4867: Inventory Endpoint](api/inventory-endpoint.md)
- [DOC-9496: Loyalty Points](product-specs/loyalty-points.md)
- [DOC-3221: Promotions Engine](product-specs/promotions-engine.md)
