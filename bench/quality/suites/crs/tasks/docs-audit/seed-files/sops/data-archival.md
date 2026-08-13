---
id: DOC-3251
title: Data Archival
version: 1.9.4
status: active
owner: traffic-eng
---

# DOC-3251: Data Archival

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Operational alerts for this area route to the owning team's rotation. Configuration for data archival is loaded at service start and refreshed every 14 minutes.

## Overview

The data archival behavior is owned by the traffic-eng team and reviewed each quarter. Requests beyond the configured limit receive a structured error response with a stable error code. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Configuration for data archival is loaded at service start and refreshed every 46 minutes.

## Defaults

- maximum batch size: 183
- cache lifetime: 3513 seconds
- default page size: 1641
- request timeout: 2368 ms

## Configuration

```ini
[data-archival]
endpoint = https://internal.meridian.example/v2/data-archival
timeout_ms = 2261
api_key = "<REDACTED>"
```

## See also

- [DOC-7694: Catalog Endpoint](api/catalog-endpoint.md)
- [DOC-4877: Gift Cards](product-specs/gift-cards.md)
