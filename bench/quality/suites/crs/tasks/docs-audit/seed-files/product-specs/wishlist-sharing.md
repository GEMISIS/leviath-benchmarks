---
id: DOC-4315
title: Wishlist Sharing
version: 3.8.6
status: active
owner: traffic-eng
---

# DOC-4315: Wishlist Sharing

Identifiers used here follow the corpus-wide conventions in the style guide. The wishlist sharing behavior is owned by the traffic-eng team and reviewed each quarter. This document describes the wishlist sharing area of the Meridian Commerce platform.

## Overview

Earlier drafts of this behavior were consolidated here from the team wiki. Consumers should treat undocumented fields as unstable and subject to change without notice. Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for wishlist sharing is loaded at service start and refreshed every 73 minutes.

## Defaults

- maximum batch size: 2768
- default page size: 1127
- soft quota per client: 2555 per hour
- retry budget: 3875 attempts

## See also

- [DOC-9169: Errors Reference](api/errors-reference.md)
- [DOC-1233: Returns Portal](product-specs/returns-portal.md)
