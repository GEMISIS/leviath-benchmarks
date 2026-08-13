---
id: DOC-4877
title: Gift Cards
version: 2.7.9
status: active
owner: storefront
---

# DOC-4877: Gift Cards

This document describes the gift cards area of the Meridian Commerce platform. Earlier drafts of this behavior were consolidated here from the team wiki. The gift cards behavior is owned by the storefront team and reviewed each quarter.

## Overview

Rollout is gated on the weekly release train unless an exemption is filed. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Configuration for gift cards is loaded at service start and refreshed every 36 minutes. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Defaults

- cache lifetime: 1972 seconds
- maximum batch size: 3463
- soft quota per client: 3364 per hour

## Configuration

```ini
[gift-cards]
endpoint = https://internal.meridian.example/v2/gift-cards
timeout_ms = 2645
api_key = "<REDACTED>"
```

## See also

- [DOC-3067: Payments Endpoint](api/payments-endpoint.md)
- [DOC-3097: Shipping Quotes](product-specs/shipping-quotes.md)
- [DOC-8582: Auth Tokens](api/auth-tokens.md)
