---
id: DOC-1211
title: Rollback Procedure
version: 2.4.8
status: active
owner: platform-core
---

# DOC-1211: Rollback Procedure

This document describes the rollback procedure area of the Meridian Commerce platform. Operational alerts for this area route to the owning team's rotation. Changes to rollback procedure go through the standard review workflow before release.

## Overview

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Requests beyond the configured limit receive a structured error response with a stable error code. Rollout is gated on the weekly release train unless an exemption is filed. Changes to rollback procedure go through the standard review workflow before release.

## Defaults

- maximum batch size: 3270
- request timeout: 1688 ms
- default page size: 3101

## Configuration

```ini
[rollback-procedure]
endpoint = https://internal.meridian.example/v2/rollback-procedure
timeout_ms = 422
api_key = "<REDACTED>"
```

## See also

- [DOC-7915: Database Backup](sops/database-backup.md)
