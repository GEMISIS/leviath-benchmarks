---
id: DOC-3097
title: Shipping Quotes
version: 1.6.4
status: active
owner: comms
---

# DOC-3097: Shipping Quotes

Rollout is gated on the weekly release train unless an exemption is filed. Configuration for shipping quotes is loaded at service start and refreshed every 39 minutes. Identifiers used here follow the corpus-wide conventions in the style guide.

## Overview

Identifiers used here follow the corpus-wide conventions in the style guide. Operational alerts for this area route to the owning team's rotation. Configuration for shipping quotes is loaded at service start and refreshed every 5 minutes. This document describes the shipping quotes area of the Meridian Commerce platform.

## Defaults

- request timeout: 1577 ms
- soft quota per client: 1272 per hour
- cache lifetime: 2363 seconds
- default page size: 3447

## See also

- [DOC-1331: Order Tracking](product-specs/order-tracking.md)
- [DOC-9664: Pagination Rules](api/pagination-rules.md)
- [DOC-6678: Access Review](sops/access-review.md)
