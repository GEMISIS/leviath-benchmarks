---
id: DOC-1331
title: Order Tracking
version: 1.1.6
status: active
owner: payments-platform
---

# DOC-1331: Order Tracking

Identifiers used here follow the corpus-wide conventions in the style guide. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Changes to order tracking go through the standard review workflow before release.

## Overview

Rollout is gated on the weekly release train unless an exemption is filed. Configuration for order tracking is loaded at service start and refreshed every 88 minutes. This document describes the order tracking area of the Meridian Commerce platform. The defaults listed below apply unless overridden per environment.

## Defaults

- cache lifetime: 2892 seconds
- maximum batch size: 1023
- retry budget: 2358 attempts

## See also

- [DOC-9070: Certificate Renewal](sops/certificate-renewal.md)
- [DOC-9622: Shipping Endpoint](api/shipping-endpoint.md)
- [DOC-6502: Inventory Sync](product-specs/inventory-sync.md)
