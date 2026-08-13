---
id: DOC-9735
title: Incident Response
version: 3.5.2
status: active
owner: discovery
---

# DOC-9735: Incident Response

Changes to incident response go through the standard review workflow before release. The incident response behavior is owned by the discovery team and reviewed each quarter. The defaults listed below apply unless overridden per environment.

## Overview

Identifiers used here follow the corpus-wide conventions in the style guide. The incident response behavior is owned by the discovery team and reviewed each quarter. Earlier drafts of this behavior were consolidated here from the team wiki. Rollout is gated on the weekly release train unless an exemption is filed.

## Defaults

- retry budget: 1586 attempts
- cache lifetime: 2640 seconds
- request timeout: 1147 ms

## See also

- [DOC-3928: Vendor Onboarding](sops/vendor-onboarding.md)
- [DOC-3251: Data Archival](sops/data-archival.md)
