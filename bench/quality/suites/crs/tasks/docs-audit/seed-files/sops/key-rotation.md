---
id: DOC-1328
title: Key Rotation
version: 3.7.5
status: active
owner: traffic-eng
---

# DOC-1328: Key Rotation

Operational alerts for this area route to the owning team's rotation. Consumers should treat undocumented fields as unstable and subject to change without notice. Configuration for key rotation is loaded at service start and refreshed every 24 minutes.

## Overview

Requests beyond the configured limit receive a structured error response with a stable error code. Configuration for key rotation is loaded at service start and refreshed every 68 minutes. The defaults listed below apply unless overridden per environment. Operational alerts for this area route to the owning team's rotation.

## Defaults

- soft quota per client: 2918 per hour
- default page size: 3547
- cache lifetime: 2720 seconds
- maximum batch size: 111

## Configuration

```ini
[key-rotation]
endpoint = https://internal.meridian.example/v2/key-rotation
timeout_ms = 8080
api_key = "<REDACTED>"
```

## See also

- [DOC-9664: Pagination Rules](api/pagination-rules.md)
- [DOC-6462: Reporting Endpoint](api/reporting-endpoint.md)
