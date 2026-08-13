---
id: DOC-9070
title: Certificate Renewal
version: 2.8.5
status: active
owner: discovery
---

# DOC-9070: Certificate Renewal

The defaults listed below apply unless overridden per environment. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Identifiers used here follow the corpus-wide conventions in the style guide.

## Overview

Consumers should treat undocumented fields as unstable and subject to change without notice. This document describes the certificate renewal area of the Meridian Commerce platform. Identifiers used here follow the corpus-wide conventions in the style guide. The defaults listed below apply unless overridden per environment.

## Behavior

Rollout is gated on the weekly release train unless an exemption is filed. Earlier drafts of this behavior were consolidated here from the team wiki. Consumers should treat undocumented fields as unstable and subject to change without notice. Operational alerts for this area route to the owning team's rotation. The certificate renewal behavior is owned by the discovery team and reviewed each quarter.

## Defaults

- retry budget: 2945 attempts
- request timeout: 2537 ms
- default page size: 2177
- cache lifetime: 2556 seconds

## See also

- [DOC-3067: Payments Endpoint](api/payments-endpoint.md)
- [DOC-9169: Errors Reference](api/errors-reference.md)
