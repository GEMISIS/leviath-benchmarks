---
id: DOC-6502
title: Inventory Sync
version: 3.6.3
status: active
owner: discovery
---

# DOC-6502: Inventory Sync

Identifiers used here follow the corpus-wide conventions in the style guide. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Changes to inventory sync go through the standard review workflow before release.

## Overview

Rollout is gated on the weekly release train unless an exemption is filed. Configuration for inventory sync is loaded at service start and refreshed every 88 minutes. This document describes the inventory sync area of the Meridian Commerce platform. The defaults listed below apply unless overridden per environment.

## Behavior

This document describes the inventory sync area of the Meridian Commerce platform. Consumers should treat undocumented fields as unstable and subject to change without notice. Changes to inventory sync go through the standard review workflow before release. The defaults listed below apply unless overridden per environment. Configuration for inventory sync is loaded at service start and refreshed every 49 minutes.

## Defaults

- default page size: 2689
- maximum batch size: 3519
- soft quota per client: 1940 per hour

## See also

- [DOC-9070: Certificate Renewal](sops/certificate-renewal.md)
