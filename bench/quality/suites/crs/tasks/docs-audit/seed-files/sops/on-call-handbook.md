---
id: DOC-4056
title: On-Call Handbook
version: 2.1.6
status: active
owner: payments-platform
---

# DOC-4056: On-Call Handbook

Operational alerts for this area route to the owning team's rotation. Configuration for on-call handbook is loaded at service start and refreshed every 61 minutes. Changes to on-call handbook go through the standard review workflow before release.

## Overview

Configuration for on-call handbook is loaded at service start and refreshed every 50 minutes. Identifiers used here follow the corpus-wide conventions in the style guide. The on-call handbook behavior is owned by the payments-platform team and reviewed each quarter. Requests beyond the configured limit receive a structured error response with a stable error code.

## Behavior

Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to on-call handbook go through the standard review workflow before release. The defaults listed below apply unless overridden per environment. This document describes the on-call handbook area of the Meridian Commerce platform. Rollout is gated on the weekly release train unless an exemption is filed.

## Defaults

- soft quota per client: 2653 per hour
- cache lifetime: 3249 seconds
- request timeout: 3946 ms
- default page size: 2666

## Configuration

```ini
[on-call-handbook]
endpoint = https://internal.meridian.example/v2/on-call-handbook
timeout_ms = 4186
api_key = "<REDACTED>"
```

## See also

- [DOC-3572: Capacity Planning](sops/capacity-planning.md)
