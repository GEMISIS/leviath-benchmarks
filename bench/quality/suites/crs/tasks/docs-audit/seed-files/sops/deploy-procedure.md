---
id: DOC-1417
title: Deploy Procedure
version: 3.8.2
status: active
owner: storefront
---

# DOC-1417: Deploy Procedure

Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for deploy procedure is loaded at service start and refreshed every 33 minutes. Rollout is gated on the weekly release train unless an exemption is filed.

## Overview

Changes to deploy procedure go through the standard review workflow before release. Configuration for deploy procedure is loaded at service start and refreshed every 77 minutes. Rollout is gated on the weekly release train unless an exemption is filed. Operational alerts for this area route to the owning team's rotation.

## Defaults

- maximum batch size: 1267
- retry budget: 1894 attempts
- request timeout: 169 ms

## See also

- [DOC-4867: Inventory Endpoint](api/inventory-endpoint.md)
