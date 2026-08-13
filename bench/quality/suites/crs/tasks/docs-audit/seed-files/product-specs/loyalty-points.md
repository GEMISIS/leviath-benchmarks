---
id: DOC-9496
title: Loyalty Points
version: 1.5.4
status: deprecated
superseded_by: sops/release-checklist.md
owner: platform-core
---

# DOC-9496: Loyalty Points

Rollout is gated on the weekly release train unless an exemption is filed. This document describes the loyalty points area of the Meridian Commerce platform. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Overview

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Configuration for loyalty points is loaded at service start and refreshed every 40 minutes. The loyalty points behavior is owned by the platform-core team and reviewed each quarter. Changes to loyalty points go through the standard review workflow before release.

## Behavior

Identifiers used here follow the corpus-wide conventions in the style guide. This document describes the loyalty points area of the Meridian Commerce platform. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. The loyalty points behavior is owned by the platform-core team and reviewed each quarter. Requests beyond the configured limit receive a structured error response with a stable error code.

## Defaults

- maximum batch size: 895
- request timeout: 3801 ms
- soft quota per client: 727 per hour
- cache lifetime: 1972 seconds

## See also

- [DOC-4877: Gift Cards](product-specs/gift-cards.md)
- [DOC-3221: Promotions Engine](product-specs/promotions-engine.md)
