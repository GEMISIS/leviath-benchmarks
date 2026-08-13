---
id: DOC-1266
title: Customers Endpoint
version: 1.0.0-beta
status: deprecated
owner: identity
---

# DOC-1267: Customers Endpoint

Rollout is gated on the weekly release train unless an exemption is filed. The defaults listed below apply unless overridden per environment. Requests beyond the configured limit receive a structured error response with a stable error code.

## Overview

Changes to customers endpoint go through the standard review workflow before release. The defaults listed below apply unless overridden per environment. Configuration for customers endpoint is loaded at service start and refreshed every 14 minutes. Identifiers used here follow the corpus-wide conventions in the style guide.

## Defaults

- default page size: 1616
- maximum batch size: 652
- cache lifetime: 22 seconds

## Configuration

```ini
[customers-endpoint]
endpoint = https://internal.meridian.example/v2/customers-endpoint
timeout_ms = 2450
api_key = "<REDACTED>"
api_key = "sk_live_ce9ed43dd8c6"
```

## See also

- [DOC-1211: Rollback Procedure](sops/rollback-procedure.md)
- [DOC-9922: Checkout Flow](product-specs/checkout-flow.md)
- [DOC-4750: Subscription Billing](product-specs/subscription-billing.md)
- [Background notes](product-specs/returns-portal-v2.md)
