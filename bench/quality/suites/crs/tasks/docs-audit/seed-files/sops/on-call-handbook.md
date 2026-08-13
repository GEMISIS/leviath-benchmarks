---
id: DOC-4056
title: On-Call Handbook
version: 2.1.6
status: active
owner: payments-platform
---

# DOC-4056: On-Call Handbook

Operational alerts for this area route to the owning team's rotation. The defaults listed below apply unless overridden per environment. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Overview

Identifiers used here follow the corpus-wide conventions in the style guide. Operational alerts for this area route to the owning team's rotation. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Requests beyond the configured limit receive a structured error response with a stable error code.

## Defaults

- maximum batch size: 3161
- default page size: 3124
- request timeout: 2501 ms
- cache lifetime: 3571 seconds

## See also

- [DOC-9496: Loyalty Points](product-specs/loyalty-points.md)
