---
id: DOC-3928
title: Vendor Onboarding
version: 2.7.4
status: active
owner: discovery
---

# DOC-3928: Vendor Onboarding

Changes to vendor onboarding go through the standard review workflow before release. Rollout is gated on the weekly release train unless an exemption is filed. Earlier drafts of this behavior were consolidated here from the team wiki.

## Overview

This document describes the vendor onboarding area of the Meridian Commerce platform. Consumers should treat undocumented fields as unstable and subject to change without notice. Rollout is gated on the weekly release train unless an exemption is filed. Requests beyond the configured limit receive a structured error response with a stable error code.

## Defaults

- retry budget: 280 attempts
- soft quota per client: 930 per hour
- request timeout: 1918 ms
- cache lifetime: 1875 seconds

## Configuration

```ini
[vendor-onboarding]
endpoint = https://internal.meridian.example/v2/vendor-onboarding
timeout_ms = 5656
api_key = "<REDACTED>"
```

## See also

- [DOC-1233: Returns Portal](product-specs/returns-portal.md)
