---
id: DOC-9070
title: Certificate Renewal
version: 2.8.5
status: active
owner: discovery
---

# DOC-9070: Certificate Renewal

The certificate renewal behavior is owned by the discovery team and reviewed each quarter. The defaults listed below apply unless overridden per environment. Requests beyond the configured limit receive a structured error response with a stable error code.

## Overview

The defaults listed below apply unless overridden per environment. The certificate renewal behavior is owned by the discovery team and reviewed each quarter. Operational alerts for this area route to the owning team's rotation. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Defaults

- soft quota per client: 3299 per hour
- retry budget: 3643 attempts
- request timeout: 2777 ms
- maximum batch size: 2933

## See also

- [DOC-5393: Search Endpoint](api/search-endpoint.md)
- [DOC-1328: Key Rotation](sops/key-rotation.md)
