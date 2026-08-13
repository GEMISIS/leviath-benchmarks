---
id: DOC-9735
title: Incident Response
version: 3.5.2
status: active
owner: discovery
---

# DOC-9735: Incident Response

Operational alerts for this area route to the owning team's rotation. Identifiers used here follow the corpus-wide conventions in the style guide. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Overview

The defaults listed below apply unless overridden per environment. Rollout is gated on the weekly release train unless an exemption is filed. Consumers should treat undocumented fields as unstable and subject to change without notice. This document describes the incident response area of the Meridian Commerce platform.

## Behavior

Earlier drafts of this behavior were consolidated here from the team wiki. Operational alerts for this area route to the owning team's rotation. The incident response behavior is owned by the discovery team and reviewed each quarter. Requests beyond the configured limit receive a structured error response with a stable error code. Configuration for incident response is loaded at service start and refreshed every 74 minutes.

## Defaults

- maximum batch size: 1047
- retry budget: 883 attempts
- cache lifetime: 1374 seconds

## See also

- [DOC-9169: Errors Reference](api/errors-reference.md)
- [DOC-7694: Catalog Endpoint](api/catalog-endpoint.md)
