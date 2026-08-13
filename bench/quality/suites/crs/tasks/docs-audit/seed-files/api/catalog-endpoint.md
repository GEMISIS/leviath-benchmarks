---
id: DOC-7694
title: Catalog Endpoint
version: 3.8.2
status: active
owner: payments-platform
---

# DOC-7694: Catalog Endpoint

Consumers should treat undocumented fields as unstable and subject to change without notice. Operational alerts for this area route to the owning team's rotation. Rollout is gated on the weekly release train unless an exemption is filed.

## Overview

Rollout is gated on the weekly release train unless an exemption is filed. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Configuration for catalog endpoint is loaded at service start and refreshed every 81 minutes. Operational alerts for this area route to the owning team's rotation.

## Behavior

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Rollout is gated on the weekly release train unless an exemption is filed. Requests beyond the configured limit receive a structured error response with a stable error code. The defaults listed below apply unless overridden per environment. Changes to catalog endpoint go through the standard review workflow before release.

## Defaults

- retry budget: 14 attempts
- default page size: 3558
- maximum batch size: 1674
- soft quota per client: 539 per hour

## See also

- [DOC-7657: Refunds Endpoint](api/refunds-endpoint.md)
