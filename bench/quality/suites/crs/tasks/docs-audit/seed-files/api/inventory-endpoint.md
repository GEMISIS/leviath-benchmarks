---
id: DOC-4867
title: Inventory Endpoint
version: 2.4.7
status: active
owner: identity
---

# DOC-4867: Inventory Endpoint

Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to inventory endpoint go through the standard review workflow before release. This document describes the inventory endpoint area of the Meridian Commerce platform.

## Overview

Earlier drafts of this behavior were consolidated here from the team wiki. Configuration for inventory endpoint is loaded at service start and refreshed every 78 minutes. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Changes to inventory endpoint go through the standard review workflow before release.

## Defaults

- maximum batch size: 538
- request timeout: 2771 ms
- cache lifetime: 3175 seconds

## Configuration

```ini
[inventory-endpoint]
endpoint = https://internal.meridian.example/v2/inventory-endpoint
timeout_ms = 876
api_key = "<REDACTED>"
```

## See also

- [DOC-9922: Checkout Flow](product-specs/checkout-flow.md)
