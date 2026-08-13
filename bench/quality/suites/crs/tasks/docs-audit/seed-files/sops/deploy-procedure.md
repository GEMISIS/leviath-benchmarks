---
id: DOC-1417
title: Deploy Procedure
version: 3.8.2
status: active
owner: storefront
---

# DOC-1417: Deploy Procedure

Consumers should treat undocumented fields as unstable and subject to change without notice. This document describes the deploy procedure area of the Meridian Commerce platform. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Overview

Changes to deploy procedure go through the standard review workflow before release. Rollout is gated on the weekly release train unless an exemption is filed. Identifiers used here follow the corpus-wide conventions in the style guide. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Behavior

Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code. This document describes the deploy procedure area of the Meridian Commerce platform. Rollout is gated on the weekly release train unless an exemption is filed. The deploy procedure behavior is owned by the storefront team and reviewed each quarter.

## Defaults

- maximum batch size: 1310
- retry budget: 2911 attempts
- soft quota per client: 306 per hour
- default page size: 409

## Configuration

```ini
[deploy-procedure]
endpoint = https://internal.meridian.example/v2/deploy-procedure
timeout_ms = 4845
api_key = "<REDACTED>"
```

## See also

- [DOC-3097: Shipping Quotes](product-specs/shipping-quotes.md)
- [DOC-9070: Certificate Renewal](sops/certificate-renewal.md)
- [DOC-4877: Gift Cards](product-specs/gift-cards.md)
