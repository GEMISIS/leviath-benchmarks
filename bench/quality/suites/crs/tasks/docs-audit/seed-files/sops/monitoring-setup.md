---
id: DOC-3383
title: Monitoring Setup
version: 3.7.3
status: active
owner: payments-platform
---

# DOC-3383: Monitoring Setup

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Identifiers used here follow the corpus-wide conventions in the style guide. This document describes the monitoring setup area of the Meridian Commerce platform.

## Overview

Operational alerts for this area route to the owning team's rotation. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Configuration for monitoring setup is loaded at service start and refreshed every 43 minutes. Rollout is gated on the weekly release train unless an exemption is filed.

## Behavior

Configuration for monitoring setup is loaded at service start and refreshed every 40 minutes. Operational alerts for this area route to the owning team's rotation. Consumers should treat undocumented fields as unstable and subject to change without notice. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. This document describes the monitoring setup area of the Meridian Commerce platform.

## Defaults

- soft quota per client: 2310 per hour
- cache lifetime: 1593 seconds
- request timeout: 673 ms

## See also

- [DOC-3572: Capacity Planning](sops/capacity-planning.md)
