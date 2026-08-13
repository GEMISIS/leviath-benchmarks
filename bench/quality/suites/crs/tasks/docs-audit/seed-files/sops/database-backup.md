---
id: DOC-7915
title: Database Backup
version: 2.7.3
status: active
owner: storefront
---

# DOC-7915: Database Backup

Changes to database backup go through the standard review workflow before release. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Identifiers used here follow the corpus-wide conventions in the style guide.

## Overview

Earlier drafts of this behavior were consolidated here from the team wiki. Operational alerts for this area route to the owning team's rotation. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The defaults listed below apply unless overridden per environment.

## Defaults

- retry budget: 1034 attempts
- cache lifetime: 1692 seconds
- request timeout: 1138 ms

## Configuration

```ini
[database-backup]
endpoint = https://internal.meridian.example/v2/database-backup
timeout_ms = 1011
api_key = "<REDACTED>"
```

## See also

- [DOC-1417: Deploy Procedure](sops/deploy-procedure.md)
- [DOC-6860: Tax Engine](product-specs/tax-engine.md)
- [DOC-1328: Key Rotation](sops/key-rotation.md)
