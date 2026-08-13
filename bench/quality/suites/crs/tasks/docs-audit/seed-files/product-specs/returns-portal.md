---
id: DOC-1233
title: Returns Portal
version: 1.7.6
status: active
owner: payments-platform
---

# DOC-1233: Returns Portal

Rollout is gated on the weekly release train unless an exemption is filed. Changes to returns portal go through the standard review workflow before release. The returns portal behavior is owned by the payments-platform team and reviewed each quarter.

## Overview

The defaults listed below apply unless overridden per environment. Changes to returns portal go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki. Configuration for returns portal is loaded at service start and refreshed every 76 minutes.

## Behavior

Configuration for returns portal is loaded at service start and refreshed every 60 minutes. Consumers should treat undocumented fields as unstable and subject to change without notice. Earlier drafts of this behavior were consolidated here from the team wiki. The defaults listed below apply unless overridden per environment. Changes to returns portal go through the standard review workflow before release.

## Defaults

- default page size: 3826
- request timeout: 1825 ms
- maximum batch size: 2880
- soft quota per client: 2388 per hour

## See also

- [DOC-9169: Errors Reference](api/errors-reference.md)
- [DOC-1328: Key Rotation](sops/key-rotation.md)
- [DOC-1266: Customers Endpoint](api/customers-endpoint.md)
