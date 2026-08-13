---
id: DOC-6773
title: Orders Endpoint
version: 2.6.3
status: active
owner: identity
---

# DOC-6773: Orders Endpoint

Earlier drafts of this behavior were consolidated here from the team wiki. Consumers should treat undocumented fields as unstable and subject to change without notice. Configuration for orders endpoint is loaded at service start and refreshed every 65 minutes.

## Overview

Rollout is gated on the weekly release train unless an exemption is filed. Earlier drafts of this behavior were consolidated here from the team wiki. Consumers should treat undocumented fields as unstable and subject to change without notice. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Behavior

Configuration for orders endpoint is loaded at service start and refreshed every 10 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Identifiers used here follow the corpus-wide conventions in the style guide. Changes to orders endpoint go through the standard review workflow before release. The orders endpoint behavior is owned by the identity team and reviewed each quarter.

## Defaults

- maximum batch size: 3126
- soft quota per client: 1366 per hour
- default page size: 2568
- retry budget: 1869 attempts

## See also

- [DOC-4056: On-Call Handbook](sops/on-call-handbook.md)
- [DOC-8582: Auth Tokens](api/auth-tokens.md)
