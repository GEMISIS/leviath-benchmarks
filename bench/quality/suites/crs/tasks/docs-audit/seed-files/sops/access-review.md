---
id: DOC-6678
title: Access Review
version: 2.4.0
status: active
owner: platform-core
---

# DOC-6678: Access Review

Rollout is gated on the weekly release train unless an exemption is filed. Operational alerts for this area route to the owning team's rotation. The access review behavior is owned by the platform-core team and reviewed each quarter.

## Overview

The defaults listed below apply unless overridden per environment. Changes to access review go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki. Rollout is gated on the weekly release train unless an exemption is filed.

## Defaults

- maximum batch size: 3711
- request timeout: 3637 ms
- retry budget: 1475 attempts

## Configuration

```ini
[access-review]
endpoint = https://internal.meridian.example/v2/access-review
timeout_ms = 8941
api_key = "<REDACTED>"
```

## See also

- [DOC-6462: Reporting Endpoint](api/reporting-endpoint.md)
