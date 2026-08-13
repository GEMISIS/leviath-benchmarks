---
id: DOC-9195
title: Price Rules
version: 2.4.3
status: active
owner: discovery
---

# DOC-9195: Price Rules

Identifiers used here follow the corpus-wide conventions in the style guide. Operational alerts for this area route to the owning team's rotation. The defaults listed below apply unless overridden per environment.

## Overview

This document describes the price rules area of the Meridian Commerce platform. Identifiers used here follow the corpus-wide conventions in the style guide. Requests beyond the configured limit receive a structured error response with a stable error code. Rollout is gated on the weekly release train unless an exemption is filed.

## Behavior

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The defaults listed below apply unless overridden per environment. Rollout is gated on the weekly release train unless an exemption is filed. Configuration for price rules is loaded at service start and refreshed every 46 minutes. Identifiers used here follow the corpus-wide conventions in the style guide.

## Defaults

- default page size: 2353
- retry budget: 1514 attempts
- soft quota per client: 1525 per hour

## Configuration

```ini
[price-rules]
endpoint = https://internal.meridian.example/v2/price-rules
timeout_ms = 5829
api_key = "<REDACTED>"
```

## See also

- [DOC-7915: Database Backup](sops/database-backup.md)
- [DOC-1119: Storefront Themes](product-specs/storefront-themes.md)
- [DOC-3097: Shipping Quotes](product-specs/shipping-quotes.md)
