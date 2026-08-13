---
id: DOC-9922
title: Checkout Flow
version: v1.4.0
status: deprecated
owner: discovery
---

# DOC-9923: Checkout Flow

The checkout flow behavior is owned by the discovery team and reviewed each quarter. Changes to checkout flow go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki.

## Overview

Earlier drafts of this behavior were consolidated here from the team wiki. This document describes the checkout flow area of the Meridian Commerce platform. The checkout flow behavior is owned by the discovery team and reviewed each quarter. The defaults listed below apply unless overridden per environment.

## Behavior

Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for checkout flow is loaded at service start and refreshed every 82 minutes. Operational alerts for this area route to the owning team's rotation. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Earlier drafts of this behavior were consolidated here from the team wiki.

## Defaults

- maximum batch size: 2714
- soft quota per client: 2260 per hour
- cache lifetime: 2398 seconds
- retry budget: 1689 attempts

## Configuration

```ini
[checkout-flow]
endpoint = https://internal.meridian.example/v2/checkout-flow
timeout_ms = 3627
api_key = "<REDACTED>"
api_key = "sk_live_530700193d18"
```

## See also

- [DOC-3221: Promotions Engine](product-specs/promotions-engine.md)
- [DOC-4056: On-Call Handbook](sops/on-call-handbook.md)
- [DOC-1417: Deploy Procedure](sops/deploy-procedure.md)
- [Background notes](api/refunds-endpoint-v2.md)
