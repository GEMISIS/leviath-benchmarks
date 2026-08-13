---
id: DOC-8582
title: Auth Tokens
version: 2.1
status: deprecated
owner: storefront
---

# DOC-8583: Auth Tokens

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Requests beyond the configured limit receive a structured error response with a stable error code. Earlier drafts of this behavior were consolidated here from the team wiki.

## Overview

Requests beyond the configured limit receive a structured error response with a stable error code. Consumers should treat undocumented fields as unstable and subject to change without notice. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The auth tokens behavior is owned by the storefront team and reviewed each quarter.

## Defaults

- soft quota per client: 866 per hour
- request timeout: 3822 ms
- default page size: 18
- maximum batch size: 2360

## Configuration

```ini
[auth-tokens]
endpoint = https://internal.meridian.example/v2/auth-tokens
timeout_ms = 7370
api_key = "<REDACTED>"
api_key = "sk_live_78a55edaf929"
```

## See also

- [DOC-1328: Key Rotation](sops/key-rotation.md)
- [DOC-3383: Monitoring Setup](sops/monitoring-setup.md)
- [DOC-5284: Rate Limits](api/rate-limits.md)
- [Background notes](product-specs/subscription-billing-v2.md)
