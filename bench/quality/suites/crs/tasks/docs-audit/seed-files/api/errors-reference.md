---
id: DOC-9169
title: Errors Reference
version: 2.5.7
status: active
owner: storefront
---

# DOC-9169: Errors Reference

Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice. Configuration for errors reference is loaded at service start and refreshed every 5 minutes.

## Overview

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Configuration for errors reference is loaded at service start and refreshed every 53 minutes. Changes to errors reference go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki.

## Behavior

Rollout is gated on the weekly release train unless an exemption is filed. The defaults listed below apply unless overridden per environment. Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code. Changes to errors reference go through the standard review workflow before release.

## Defaults

- retry budget: 600 attempts
- soft quota per client: 308 per hour
- default page size: 3240

## See also

- [DOC-1233: Returns Portal](product-specs/returns-portal.md)
