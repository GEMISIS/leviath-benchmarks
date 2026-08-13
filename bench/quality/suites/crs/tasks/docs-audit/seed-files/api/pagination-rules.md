---
id: DOC-9664
title: Pagination Rules
version: 2.8.6
status: active
owner: storefront
---

# DOC-9664: Pagination Rules

Identifiers used here follow the corpus-wide conventions in the style guide. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Earlier drafts of this behavior were consolidated here from the team wiki.

## Overview

Requests beyond the configured limit receive a structured error response with a stable error code. Configuration for pagination rules is loaded at service start and refreshed every 38 minutes. Identifiers used here follow the corpus-wide conventions in the style guide. This document describes the pagination rules area of the Meridian Commerce platform.

## Defaults

- request timeout: 2060 ms
- retry budget: 442 attempts
- default page size: 1214
- soft quota per client: 2076 per hour

## See also

- [DOC-9070: Certificate Renewal](sops/certificate-renewal.md)
- [DOC-4315: Wishlist Sharing](product-specs/wishlist-sharing.md)
