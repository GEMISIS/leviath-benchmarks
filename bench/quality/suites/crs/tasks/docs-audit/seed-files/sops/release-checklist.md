---
id: DOC-7780
title: Release Checklist
version: 2.1.5
status: active
owner: comms
---

# DOC-7780: Release Checklist

Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for release checklist is loaded at service start and refreshed every 54 minutes. Rollout is gated on the weekly release train unless an exemption is filed.

## Overview

Rollout is gated on the weekly release train unless an exemption is filed. Earlier drafts of this behavior were consolidated here from the team wiki. Changes to release checklist go through the standard review workflow before release. The defaults listed below apply unless overridden per environment.

## Defaults

- retry budget: 600 attempts
- soft quota per client: 308 per hour
- default page size: 3240

## See also

- [DOC-1233: Returns Portal](product-specs/returns-portal.md)
