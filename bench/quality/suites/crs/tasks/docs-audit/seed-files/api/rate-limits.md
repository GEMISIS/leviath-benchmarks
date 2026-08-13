---
id: DOC-5284
title: Rate Limits
version: 2.2.4
status: active
owner: comms
---

# DOC-5284: Rate Limits

Configuration for rate limits is loaded at service start and refreshed every 77 minutes. Operational alerts for this area route to the owning team's rotation. This document describes the rate limits area of the Meridian Commerce platform.

## Overview

This document describes the rate limits area of the Meridian Commerce platform. The rate limits behavior is owned by the comms team and reviewed each quarter. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Requests beyond the configured limit receive a structured error response with a stable error code.

## Behavior

Operational alerts for this area route to the owning team's rotation. Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to rate limits go through the standard review workflow before release. Identifiers used here follow the corpus-wide conventions in the style guide. Rollout is gated on the weekly release train unless an exemption is filed.

## Defaults

- retry budget: 1640 attempts
- request timeout: 1677 ms
- default page size: 1044

## Configuration

```ini
[rate-limits]
endpoint = https://internal.meridian.example/v2/rate-limits
timeout_ms = 4233
api_key = "<REDACTED>"
```

## See also

- [DOC-9735: Incident Response](sops/incident-response.md)
