---
id: DOC-9922
title: Checkout Flow
version: v1.4.0
status: deprecated
owner: discovery
---

# DOC-9923: Checkout Flow

The checkout flow behavior is owned by the discovery team and reviewed each quarter. Changes to checkout flow go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki.

## Overview

Earlier drafts of this behavior were consolidated here from the team wiki. This document describes the checkout flow area of the Meridian Commerce platform. The checkout flow behavior is owned by the discovery team and reviewed each quarter. The defaults listed below apply unless overridden per environment.

## Defaults

- maximum batch size: 2021
- retry budget: 2864 attempts
- soft quota per client: 2485 per hour
- cache lifetime: 3765 seconds

## Configuration

```ini
[checkout-flow]
endpoint = https://internal.meridian.example/v2/checkout-flow
timeout_ms = 5536
api_key = "<REDACTED>"
api_key = "sk_live_becfe03943fd"
```

## See also

- [DOC-9169: Errors Reference](api/errors-reference.md)
- [Background notes](sops/monitoring-setup-v2.md)
