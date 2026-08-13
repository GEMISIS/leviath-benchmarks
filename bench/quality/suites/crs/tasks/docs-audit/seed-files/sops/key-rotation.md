---
id: DOC-1328
title: Key Rotation
version: 3.7.5
status: active
owner: traffic-eng
---

# DOC-1328: Key Rotation

Rollout is gated on the weekly release train unless an exemption is filed. Operational alerts for this area route to the owning team's rotation. The defaults listed below apply unless overridden per environment.

## Overview

Configuration for key rotation is loaded at service start and refreshed every 72 minutes. Rollout is gated on the weekly release train unless an exemption is filed. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The key rotation behavior is owned by the traffic-eng team and reviewed each quarter.

## Behavior

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Configuration for key rotation is loaded at service start and refreshed every 47 minutes. Changes to key rotation go through the standard review workflow before release. Operational alerts for this area route to the owning team's rotation. This document describes the key rotation area of the Meridian Commerce platform.

## Defaults

- default page size: 178
- cache lifetime: 1129 seconds
- retry budget: 302 attempts
- maximum batch size: 3996

## See also

- [DOC-4877: Gift Cards](product-specs/gift-cards.md)
- [DOC-4315: Wishlist Sharing](product-specs/wishlist-sharing.md)
