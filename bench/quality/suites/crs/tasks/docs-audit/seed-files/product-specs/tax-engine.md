---
id: DOC-6860
title: Tax Engine
version: 3.0.9
status: active
owner: comms
---

# DOC-6860: Tax Engine

Earlier drafts of this behavior were consolidated here from the team wiki. Rollout is gated on the weekly release train unless an exemption is filed. The defaults listed below apply unless overridden per environment.

## Overview

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Rollout is gated on the weekly release train unless an exemption is filed. This document describes the tax engine area of the Meridian Commerce platform. Configuration for tax engine is loaded at service start and refreshed every 80 minutes.

## Behavior

Operational alerts for this area route to the owning team's rotation. Changes to tax engine go through the standard review workflow before release. The tax engine behavior is owned by the comms team and reviewed each quarter. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Earlier drafts of this behavior were consolidated here from the team wiki.

## Defaults

- request timeout: 2290 ms
- default page size: 2245
- cache lifetime: 2901 seconds
- soft quota per client: 2116 per hour

## See also

- [DOC-9622: Shipping Endpoint](api/shipping-endpoint.md)
- [DOC-8582: Auth Tokens](api/auth-tokens.md)
- [DOC-9195: Price Rules](product-specs/price-rules.md)
