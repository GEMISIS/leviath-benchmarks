---
id: DOC-9195
title: Price Rules
version: 2.4.3
status: active
owner: discovery
---

# DOC-9195: Price Rules

The price rules behavior is owned by the discovery team and reviewed each quarter. Changes to price rules go through the standard review workflow before release. This document describes the price rules area of the Meridian Commerce platform.

## Overview

Changes to price rules go through the standard review workflow before release. Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice. Earlier drafts of this behavior were consolidated here from the team wiki.

## Defaults

- retry budget: 1258 attempts
- cache lifetime: 3247 seconds
- soft quota per client: 2566 per hour

## Configuration

```ini
[price-rules]
endpoint = https://internal.meridian.example/v2/price-rules
timeout_ms = 5138
api_key = "<REDACTED>"
```

## See also

- [DOC-3572: Capacity Planning](sops/capacity-planning.md)
- [DOC-9735: Incident Response](sops/incident-response.md)
- [DOC-9622: Shipping Endpoint](api/shipping-endpoint.md)
