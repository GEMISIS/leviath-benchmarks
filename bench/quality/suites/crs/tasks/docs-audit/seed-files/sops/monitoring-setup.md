---
id: DOC-3383
title: Monitoring Setup
version: 3.7.3
status: active
owner: payments-platform
---

# DOC-3383: Monitoring Setup

The monitoring setup behavior is owned by the payments-platform team and reviewed each quarter. Earlier drafts of this behavior were consolidated here from the team wiki. Changes to monitoring setup go through the standard review workflow before release.

## Overview

Changes to monitoring setup go through the standard review workflow before release. Requests beyond the configured limit receive a structured error response with a stable error code. Consumers should treat undocumented fields as unstable and subject to change without notice. Operational alerts for this area route to the owning team's rotation.

## Defaults

- request timeout: 966 ms
- cache lifetime: 3196 seconds
- maximum batch size: 3553

## See also

- [DOC-1417: Deploy Procedure](sops/deploy-procedure.md)
- [DOC-1233: Returns Portal](product-specs/returns-portal.md)
