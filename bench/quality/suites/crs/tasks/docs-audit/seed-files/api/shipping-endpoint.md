---
id: DOC-9622
title: Shipping Endpoint
version: 1.6.2
status: active
owner: discovery
---

# DOC-9622: Shipping Endpoint

Identifiers used here follow the corpus-wide conventions in the style guide. Rollout is gated on the weekly release train unless an exemption is filed. The defaults listed below apply unless overridden per environment.

## Overview

Rollout is gated on the weekly release train unless an exemption is filed. The defaults listed below apply unless overridden per environment. Configuration for shipping endpoint is loaded at service start and refreshed every 34 minutes. Changes to shipping endpoint go through the standard review workflow before release.

## Defaults

- request timeout: 1712 ms
- cache lifetime: 3631 seconds
- maximum batch size: 658

## Configuration

```ini
[shipping-endpoint]
endpoint = https://internal.meridian.example/v2/shipping-endpoint
timeout_ms = 6496
api_key = "<REDACTED>"
```

## See also

- [DOC-3928: Vendor Onboarding](sops/vendor-onboarding.md)
- [DOC-9496: Loyalty Points](product-specs/loyalty-points.md)
