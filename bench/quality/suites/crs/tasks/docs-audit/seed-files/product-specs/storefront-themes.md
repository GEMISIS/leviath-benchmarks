---
id: DOC-1119
title: Storefront Themes
version: v1.4.0
status: deprecated
owner: traffic-eng
---

# DOC-1110: Storefront Themes

Requests beyond the configured limit receive a structured error response with a stable error code. Earlier drafts of this behavior were consolidated here from the team wiki. Identifiers used here follow the corpus-wide conventions in the style guide.

## Overview

Earlier drafts of this behavior were consolidated here from the team wiki. Requests beyond the configured limit receive a structured error response with a stable error code. Configuration for storefront themes is loaded at service start and refreshed every 16 minutes. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Defaults

- maximum batch size: 309
- default page size: 469
- soft quota per client: 3393 per hour

## Configuration

```ini
[storefront-themes]
endpoint = https://internal.meridian.example/v2/storefront-themes
timeout_ms = 1594
api_key = "<REDACTED>"
api_key = "sk_live_3a757660a0a2"
```

## See also

- [DOC-3251: Data Archival](sops/data-archival.md)
- [DOC-7915: Database Backup](sops/database-backup.md)
- [DOC-3097: Shipping Quotes](product-specs/shipping-quotes.md)
- [Background notes](sops/release-checklist-v2.md)
