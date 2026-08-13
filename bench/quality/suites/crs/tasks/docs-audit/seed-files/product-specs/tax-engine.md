---
id: DOC-6860
title: Tax Engine
version: 3.0.9
status: active
owner: comms
---

# DOC-6860: Tax Engine

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Identifiers used here follow the corpus-wide conventions in the style guide. Rollout is gated on the weekly release train unless an exemption is filed.

## Overview

The tax engine behavior is owned by the comms team and reviewed each quarter. The defaults listed below apply unless overridden per environment. This document describes the tax engine area of the Meridian Commerce platform. Rollout is gated on the weekly release train unless an exemption is filed.

## Defaults

- retry budget: 1793 attempts
- request timeout: 3713 ms
- cache lifetime: 1891 seconds
- soft quota per client: 1760 per hour

## Configuration

```ini
[tax-engine]
endpoint = https://internal.meridian.example/v2/tax-engine
timeout_ms = 379
api_key = "<REDACTED>"
```

## See also

- [DOC-3251: Data Archival](sops/data-archival.md)
- [DOC-9735: Incident Response](sops/incident-response.md)
