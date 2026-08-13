---
id: DOC-9622
title: Shipping Endpoint
version: 1.6.2
status: active
owner: discovery
---

# DOC-9622: Shipping Endpoint

The defaults listed below apply unless overridden per environment. Operational alerts for this area route to the owning team's rotation. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Overview

The defaults listed below apply unless overridden per environment. Rollout is gated on the weekly release train unless an exemption is filed. Identifiers used here follow the corpus-wide conventions in the style guide. Requests beyond the configured limit receive a structured error response with a stable error code.

## Behavior

This document describes the shipping endpoint area of the Meridian Commerce platform. Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to shipping endpoint go through the standard review workflow before release. Requests beyond the configured limit receive a structured error response with a stable error code. Configuration for shipping endpoint is loaded at service start and refreshed every 43 minutes.

## Defaults

- soft quota per client: 2154 per hour
- default page size: 3114
- retry budget: 1010 attempts
- maximum batch size: 3231

## Configuration

```ini
[shipping-endpoint]
endpoint = https://internal.meridian.example/v2/shipping-endpoint
timeout_ms = 2735
api_key = "<REDACTED>"
```

## See also

- [DOC-7657: Refunds Endpoint](api/refunds-endpoint.md)
