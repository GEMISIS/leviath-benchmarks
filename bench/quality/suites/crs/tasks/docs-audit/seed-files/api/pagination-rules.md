---
id: DOC-9664
title: Pagination Rules
version: 2.8.6
status: active
owner: storefront
---

# DOC-9664: Pagination Rules

Earlier drafts of this behavior were consolidated here from the team wiki. Identifiers used here follow the corpus-wide conventions in the style guide. The defaults listed below apply unless overridden per environment.

## Overview

Identifiers used here follow the corpus-wide conventions in the style guide. The pagination rules behavior is owned by the storefront team and reviewed each quarter. Operational alerts for this area route to the owning team's rotation. Earlier drafts of this behavior were consolidated here from the team wiki.

## Behavior

Operational alerts for this area route to the owning team's rotation. Configuration for pagination rules is loaded at service start and refreshed every 10 minutes. Requests beyond the configured limit receive a structured error response with a stable error code. Consumers should treat undocumented fields as unstable and subject to change without notice. The defaults listed below apply unless overridden per environment.

## Defaults

- maximum batch size: 98
- soft quota per client: 3702 per hour
- cache lifetime: 3478 seconds

## See also

- [DOC-1417: Deploy Procedure](sops/deploy-procedure.md)
