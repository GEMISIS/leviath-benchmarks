---
id: DOC-4877
title: Gift Cards
version: 2.7.9
status: active
owner: storefront
---

# DOC-4877: Gift Cards

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Operational alerts for this area route to the owning team's rotation. Earlier drafts of this behavior were consolidated here from the team wiki.

## Overview

Rollout is gated on the weekly release train unless an exemption is filed. Requests beyond the configured limit receive a structured error response with a stable error code. The gift cards behavior is owned by the storefront team and reviewed each quarter. Configuration for gift cards is loaded at service start and refreshed every 53 minutes.

## Behavior

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Earlier drafts of this behavior were consolidated here from the team wiki. Rollout is gated on the weekly release train unless an exemption is filed. Identifiers used here follow the corpus-wide conventions in the style guide. This document describes the gift cards area of the Meridian Commerce platform.

## Defaults

- maximum batch size: 17
- retry budget: 2835 attempts
- cache lifetime: 1425 seconds
- soft quota per client: 2809 per hour

## Configuration

```ini
[gift-cards]
endpoint = https://internal.meridian.example/v2/gift-cards
timeout_ms = 2735
api_key = "<REDACTED>"
```

## See also

- [DOC-7694: Catalog Endpoint](api/catalog-endpoint.md)
- [DOC-1328: Key Rotation](sops/key-rotation.md)
