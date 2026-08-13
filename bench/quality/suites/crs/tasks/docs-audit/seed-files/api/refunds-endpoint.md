---
id: DOC-7657
title: Refunds Endpoint
version: 3.3.3
status: deprecated
superseded_by: api/errors-reference.md
owner: payments-platform
---

# DOC-7657: Refunds Endpoint

Consumers should treat undocumented fields as unstable and subject to change without notice. Requests beyond the configured limit receive a structured error response with a stable error code. Operational alerts for this area route to the owning team's rotation.

## Overview

This document describes the refunds endpoint area of the Meridian Commerce platform. Requests beyond the configured limit receive a structured error response with a stable error code. Identifiers used here follow the corpus-wide conventions in the style guide. Earlier drafts of this behavior were consolidated here from the team wiki.

## Behavior

Changes to refunds endpoint go through the standard review workflow before release. The defaults listed below apply unless overridden per environment. Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for refunds endpoint is loaded at service start and refreshed every 17 minutes. Earlier drafts of this behavior were consolidated here from the team wiki.

## Defaults

- request timeout: 3575 ms
- maximum batch size: 195
- soft quota per client: 2900 per hour

## Configuration

```ini
[refunds-endpoint]
endpoint = https://internal.meridian.example/v2/refunds-endpoint
timeout_ms = 5779
api_key = "<REDACTED>"
```

## See also

- [DOC-6678: Access Review](sops/access-review.md)
- [DOC-6860: Tax Engine](product-specs/tax-engine.md)
- [DOC-3067: Payments Endpoint](api/payments-endpoint.md)
