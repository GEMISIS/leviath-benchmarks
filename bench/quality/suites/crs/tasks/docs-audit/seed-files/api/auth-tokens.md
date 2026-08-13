---
id: DOC-8582
title: Auth Tokens
version: 2.1
status: deprecated
owner: storefront
---

# DOC-8583: Auth Tokens

Identifiers used here follow the corpus-wide conventions in the style guide. Consumers should treat undocumented fields as unstable and subject to change without notice. Operational alerts for this area route to the owning team's rotation.

## Overview

Requests beyond the configured limit receive a structured error response with a stable error code. Earlier drafts of this behavior were consolidated here from the team wiki. Consumers should treat undocumented fields as unstable and subject to change without notice. Rollout is gated on the weekly release train unless an exemption is filed.

## Behavior

Earlier drafts of this behavior were consolidated here from the team wiki. The auth tokens behavior is owned by the storefront team and reviewed each quarter. This document describes the auth tokens area of the Meridian Commerce platform. Identifiers used here follow the corpus-wide conventions in the style guide. Operational alerts for this area route to the owning team's rotation.

## Defaults

- request timeout: 3805 ms
- retry budget: 3621 attempts
- cache lifetime: 696 seconds
- default page size: 1556

## Configuration

```ini
[auth-tokens]
endpoint = https://internal.meridian.example/v2/auth-tokens
timeout_ms = 7998
api_key = "<REDACTED>"
api_key = "sk_live_363b450c598a"
```

## See also

- [DOC-9496: Loyalty Points](product-specs/loyalty-points.md)
- [DOC-3221: Promotions Engine](product-specs/promotions-engine.md)
- [DOC-9622: Shipping Endpoint](api/shipping-endpoint.md)
- [Background notes](sops/incident-response-v2.md)
