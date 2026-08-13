---
id: DOC-3648
title: Webhooks
version: 2.4.2
status: active
owner: discovery
---

# DOC-3648: Webhooks

Identifiers used here follow the corpus-wide conventions in the style guide. The defaults listed below apply unless overridden per environment. Rollout is gated on the weekly release train unless an exemption is filed.

## Overview

Changes to webhooks go through the standard review workflow before release. Consumers should treat undocumented fields as unstable and subject to change without notice. Requests beyond the configured limit receive a structured error response with a stable error code. The webhooks behavior is owned by the discovery team and reviewed each quarter.

## Behavior

The defaults listed below apply unless overridden per environment. The webhooks behavior is owned by the discovery team and reviewed each quarter. Earlier drafts of this behavior were consolidated here from the team wiki. Operational alerts for this area route to the owning team's rotation. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Defaults

- maximum batch size: 1635
- cache lifetime: 1264 seconds
- request timeout: 2279 ms
- retry budget: 3689 attempts

## See also

- [DOC-9922: Checkout Flow](product-specs/checkout-flow.md)
- [DOC-9664: Pagination Rules](api/pagination-rules.md)
- [DOC-6860: Tax Engine](product-specs/tax-engine.md)
