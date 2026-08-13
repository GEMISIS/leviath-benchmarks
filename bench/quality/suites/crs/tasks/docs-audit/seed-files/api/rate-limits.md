---
id: DOC-5284
title: Rate Limits
version: 2.2.4
status: active
owner: comms
---

# DOC-5284: Rate Limits

The rate limits behavior is owned by the comms team and reviewed each quarter. Rollout is gated on the weekly release train unless an exemption is filed. Configuration for rate limits is loaded at service start and refreshed every 58 minutes.

## Overview

The rate limits behavior is owned by the comms team and reviewed each quarter. Requests beyond the configured limit receive a structured error response with a stable error code. Identifiers used here follow the corpus-wide conventions in the style guide. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Defaults

- retry budget: 2721 attempts
- maximum batch size: 1944
- request timeout: 3059 ms
- soft quota per client: 2753 per hour

## See also

- [DOC-9195: Price Rules](product-specs/price-rules.md)
- [DOC-4877: Gift Cards](product-specs/gift-cards.md)
