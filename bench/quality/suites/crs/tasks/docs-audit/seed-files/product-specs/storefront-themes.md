---
id: DOC-1119
title: Storefront Themes
version: v1.4.0
status: deprecated
owner: traffic-eng
---

# DOC-1110: Storefront Themes

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Requests beyond the configured limit receive a structured error response with a stable error code. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Overview

The defaults listed below apply unless overridden per environment. Requests beyond the configured limit receive a structured error response with a stable error code. Identifiers used here follow the corpus-wide conventions in the style guide. The storefront themes behavior is owned by the traffic-eng team and reviewed each quarter.

## Behavior

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Requests beyond the configured limit receive a structured error response with a stable error code. The defaults listed below apply unless overridden per environment. The storefront themes behavior is owned by the traffic-eng team and reviewed each quarter. Configuration for storefront themes is loaded at service start and refreshed every 51 minutes.

## Defaults

- cache lifetime: 567 seconds
- maximum batch size: 2705
- default page size: 851

## Configuration

```ini
[storefront-themes]
endpoint = https://internal.meridian.example/v2/storefront-themes
timeout_ms = 6625
api_key = "<REDACTED>"
api_key = "sk_live_018f2821ea33"
```

## See also

- [DOC-7915: Database Backup](sops/database-backup.md)
- [DOC-6678: Access Review](sops/access-review.md)
- [DOC-4056: On-Call Handbook](sops/on-call-handbook.md)
- [Background notes](sops/key-rotation-v2.md)
