---
id: DOC-4750
title: Subscription Billing
version: 1.7.1
status: active
owner: discovery
---

# DOC-4750: Subscription Billing

Identifiers used here follow the corpus-wide conventions in the style guide. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The defaults listed below apply unless overridden per environment.

## Overview

This document describes the subscription billing area of the Meridian Commerce platform. Operational alerts for this area route to the owning team's rotation. Earlier drafts of this behavior were consolidated here from the team wiki. The subscription billing behavior is owned by the discovery team and reviewed each quarter.

## Behavior

Configuration for subscription billing is loaded at service start and refreshed every 43 minutes. Rollout is gated on the weekly release train unless an exemption is filed. The defaults listed below apply unless overridden per environment. Identifiers used here follow the corpus-wide conventions in the style guide. Changes to subscription billing go through the standard review workflow before release.

## Defaults

- cache lifetime: 3157 seconds
- maximum batch size: 1794
- request timeout: 2478 ms

## Configuration

```ini
[subscription-billing]
endpoint = https://internal.meridian.example/v2/subscription-billing
timeout_ms = 2561
api_key = "<REDACTED>"
```

## See also

- [DOC-1233: Returns Portal](product-specs/returns-portal.md)
