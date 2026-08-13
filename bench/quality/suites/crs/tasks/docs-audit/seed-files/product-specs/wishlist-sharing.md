---
id: DOC-4315
title: Wishlist Sharing
version: 3.8.6
status: active
owner: traffic-eng
---

# DOC-4315: Wishlist Sharing

Requests beyond the configured limit receive a structured error response with a stable error code. Identifiers used here follow the corpus-wide conventions in the style guide. The defaults listed below apply unless overridden per environment.

## Overview

Earlier drafts of this behavior were consolidated here from the team wiki. Configuration for wishlist sharing is loaded at service start and refreshed every 16 minutes. Consumers should treat undocumented fields as unstable and subject to change without notice. Identifiers used here follow the corpus-wide conventions in the style guide.

## Behavior

Configuration for wishlist sharing is loaded at service start and refreshed every 15 minutes. The wishlist sharing behavior is owned by the traffic-eng team and reviewed each quarter. Earlier drafts of this behavior were consolidated here from the team wiki. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Defaults

- soft quota per client: 2137 per hour
- cache lifetime: 2794 seconds
- retry budget: 3444 attempts
- default page size: 1223

## Configuration

```ini
[wishlist-sharing]
endpoint = https://internal.meridian.example/v2/wishlist-sharing
timeout_ms = 6714
api_key = "<REDACTED>"
```

## See also

- [DOC-8582: Auth Tokens](api/auth-tokens.md)
- [DOC-7694: Catalog Endpoint](api/catalog-endpoint.md)
- [DOC-6462: Reporting Endpoint](api/reporting-endpoint.md)
