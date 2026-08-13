---
id: DOC-4750
title: Subscription Billing
version: 1.7.1
status: active
owner: discovery
---

# DOC-4750: Subscription Billing

Consumers should treat undocumented fields as unstable and subject to change without notice. Configuration for subscription billing is loaded at service start and refreshed every 80 minutes. Earlier drafts of this behavior were consolidated here from the team wiki.

## Overview

Earlier drafts of this behavior were consolidated here from the team wiki. Changes to subscription billing go through the standard review workflow before release. Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code.

## Defaults

- request timeout: 3826 ms
- maximum batch size: 1825
- cache lifetime: 2880 seconds

## See also

- [DOC-6678: Access Review](sops/access-review.md)
- [DOC-9169: Errors Reference](api/errors-reference.md)
- [DOC-1328: Key Rotation](sops/key-rotation.md)
