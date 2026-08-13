---
id: DOC-9169
title: Errors Reference
version: 2.5.7
status: active
owner: storefront
---

# DOC-9169: Errors Reference

Rollout is gated on the weekly release train unless an exemption is filed. Identifiers used here follow the corpus-wide conventions in the style guide. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Overview

Consumers should treat undocumented fields as unstable and subject to change without notice. Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for errors reference is loaded at service start and refreshed every 15 minutes. Changes to errors reference go through the standard review workflow before release.

## Defaults

- retry budget: 98 attempts
- soft quota per client: 1230 per hour
- default page size: 1368
- maximum batch size: 3064

## Configuration

```ini
[errors-reference]
endpoint = https://internal.meridian.example/v2/errors-reference
timeout_ms = 4805
api_key = "<REDACTED>"
```

## See also

- [DOC-6462: Reporting Endpoint](api/reporting-endpoint.md)
