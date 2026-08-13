---
id: DOC-3097
title: Shipping Quotes
version: 1.6.4
status: active
owner: comms
---

# DOC-3097: Shipping Quotes

Rollout is gated on the weekly release train unless an exemption is filed. The shipping quotes behavior is owned by the comms team and reviewed each quarter. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Overview

This document describes the shipping quotes area of the Meridian Commerce platform. Configuration for shipping quotes is loaded at service start and refreshed every 75 minutes. Identifiers used here follow the corpus-wide conventions in the style guide. Requests beyond the configured limit receive a structured error response with a stable error code.

## Behavior

Changes to shipping quotes go through the standard review workflow before release. Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code. Rollout is gated on the weekly release train unless an exemption is filed. Configuration for shipping quotes is loaded at service start and refreshed every 86 minutes.

## Defaults

- soft quota per client: 3156 per hour
- maximum batch size: 3558
- retry budget: 615 attempts
- request timeout: 3437 ms

## See also

- [DOC-1417: Deploy Procedure](sops/deploy-procedure.md)
