---
id: DOC-6678
title: Access Review
version: 2.4.0
status: active
owner: platform-core
---

# DOC-6678: Access Review

Configuration for access review is loaded at service start and refreshed every 54 minutes. Identifiers used here follow the corpus-wide conventions in the style guide. This document describes the access review area of the Meridian Commerce platform.

## Overview

The defaults listed below apply unless overridden per environment. Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to access review go through the standard review workflow before release.

## Behavior

This document describes the access review area of the Meridian Commerce platform. Changes to access review go through the standard review workflow before release. Consumers should treat undocumented fields as unstable and subject to change without notice. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Operational alerts for this area route to the owning team's rotation.

## Defaults

- retry budget: 490 attempts
- soft quota per client: 2741 per hour
- cache lifetime: 278 seconds
- request timeout: 2176 ms

## See also

- [DOC-1233: Returns Portal](product-specs/returns-portal.md)
- [DOC-1331: Order Tracking](product-specs/order-tracking.md)
- [DOC-3221: Promotions Engine](product-specs/promotions-engine.md)
