---
id: DOC-9496
title: Loyalty Points
version: 1.5.4
status: deprecated
superseded_by: sops/release-checklist.md
owner: platform-core
---

# DOC-9496: Loyalty Points

Rollout is gated on the weekly release train unless an exemption is filed. Operational alerts for this area route to the owning team's rotation. Configuration for loyalty points is loaded at service start and refreshed every 47 minutes.

## Overview

Requests beyond the configured limit receive a structured error response with a stable error code. Earlier drafts of this behavior were consolidated here from the team wiki. Changes to loyalty points go through the standard review workflow before release. The defaults listed below apply unless overridden per environment.

## Defaults

- cache lifetime: 2711 seconds
- maximum batch size: 485
- soft quota per client: 638 per hour

## See also

- [DOC-9922: Checkout Flow](product-specs/checkout-flow.md)
- [DOC-5393: Search Endpoint](api/search-endpoint.md)
