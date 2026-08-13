---
id: DOC-3648
title: Webhooks
version: 2.4.2
status: active
owner: discovery
---

# DOC-3648: Webhooks

Operational alerts for this area route to the owning team's rotation. This document describes the webhooks area of the Meridian Commerce platform. Rollout is gated on the weekly release train unless an exemption is filed.

## Overview

This document describes the webhooks area of the Meridian Commerce platform. Changes to webhooks go through the standard review workflow before release. Rollout is gated on the weekly release train unless an exemption is filed. Configuration for webhooks is loaded at service start and refreshed every 21 minutes.

## Defaults

- default page size: 3609
- maximum batch size: 2415
- retry budget: 2819 attempts
- soft quota per client: 1010 per hour

## See also

- [DOC-3928: Vendor Onboarding](sops/vendor-onboarding.md)
- [DOC-1119: Storefront Themes](product-specs/storefront-themes.md)
