---
id: DOC-6462
title: Reporting Endpoint
version: latest
status: active
owner: platform-core
---

# DOC-6463: Reporting Endpoint

Configuration for reporting endpoint is loaded at service start and refreshed every 12 minutes. Changes to reporting endpoint go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki.

## Overview

The defaults listed below apply unless overridden per environment. Operational alerts for this area route to the owning team's rotation. This document describes the reporting endpoint area of the Meridian Commerce platform. Identifiers used here follow the corpus-wide conventions in the style guide.

## Defaults

- default page size: 2726
- soft quota per client: 997 per hour
- request timeout: 536 ms
- retry budget: 568 attempts

## Configuration

```ini
[reporting-endpoint]
endpoint = https://internal.meridian.example/v2/reporting-endpoint
timeout_ms = 2449
api_key = "<REDACTED>"
api_key = "sk_live_73bdb239bd53"
```

## See also

- [DOC-7915: Database Backup](sops/database-backup.md)
- [Background notes](sops/key-rotation-v2.md)
- [Background notes](sops/vendor-onboarding-v2.md)
