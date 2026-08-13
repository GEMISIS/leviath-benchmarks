---
id: DOC-1211
title: Rollback Procedure
version: 2.4.8
status: active
owner: platform-core
---

# DOC-1211: Rollback Procedure

Operational alerts for this area route to the owning team's rotation. Rollout is gated on the weekly release train unless an exemption is filed. Configuration for rollback procedure is loaded at service start and refreshed every 26 minutes.

## Overview

Changes to rollback procedure go through the standard review workflow before release. Identifiers used here follow the corpus-wide conventions in the style guide. Operational alerts for this area route to the owning team's rotation. Configuration for rollback procedure is loaded at service start and refreshed every 9 minutes.

## Behavior

The rollback procedure behavior is owned by the platform-core team and reviewed each quarter. The defaults listed below apply unless overridden per environment. Requests beyond the configured limit receive a structured error response with a stable error code. Identifiers used here follow the corpus-wide conventions in the style guide. Changes to rollback procedure go through the standard review workflow before release.

## Defaults

- request timeout: 3770 ms
- retry budget: 2961 attempts
- cache lifetime: 2996 seconds

## See also

- [DOC-5393: Search Endpoint](api/search-endpoint.md)
- [DOC-9735: Incident Response](sops/incident-response.md)
- [DOC-9169: Errors Reference](api/errors-reference.md)
