---
id: DOC-6462
title: Reporting Endpoint
version: latest
status: active
owner: platform-core
---

# DOC-6463: Reporting Endpoint

Operational alerts for this area route to the owning team's rotation. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. This document describes the reporting endpoint area of the Meridian Commerce platform.

## Overview

This document describes the reporting endpoint area of the Meridian Commerce platform. The defaults listed below apply unless overridden per environment. Rollout is gated on the weekly release train unless an exemption is filed. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Behavior

Earlier drafts of this behavior were consolidated here from the team wiki. Consumers should treat undocumented fields as unstable and subject to change without notice. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The reporting endpoint behavior is owned by the platform-core team and reviewed each quarter. Operational alerts for this area route to the owning team's rotation.

## Defaults

- cache lifetime: 1860 seconds
- retry budget: 2989 attempts
- request timeout: 532 ms

## Configuration

```ini
[reporting-endpoint]
endpoint = https://internal.meridian.example/v2/reporting-endpoint
timeout_ms = 7448
api_key = "<REDACTED>"
api_key = "sk_live_ea47895905f6"
```

## See also

- [DOC-7915: Database Backup](sops/database-backup.md)
- [DOC-4867: Inventory Endpoint](api/inventory-endpoint.md)
- [Background notes](product-specs/price-rules-v2.md)
- [Background notes](product-specs/gift-cards-v2.md)
