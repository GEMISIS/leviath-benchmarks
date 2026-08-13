---
id: DOC-5393
title: Search Endpoint
version: 1.1.6
status: active
owner: payments-platform
---

# DOC-5393: Search Endpoint

The search endpoint behavior is owned by the payments-platform team and reviewed each quarter. Earlier drafts of this behavior were consolidated here from the team wiki. Consumers should treat undocumented fields as unstable and subject to change without notice.

## Overview

The search endpoint behavior is owned by the payments-platform team and reviewed each quarter. The defaults listed below apply unless overridden per environment. Operational alerts for this area route to the owning team's rotation. Earlier drafts of this behavior were consolidated here from the team wiki.

## Defaults

- soft quota per client: 3424 per hour
- cache lifetime: 3304 seconds
- retry budget: 589 attempts

## See also

- [DOC-9664: Pagination Rules](api/pagination-rules.md)
- [DOC-7657: Refunds Endpoint](api/refunds-endpoint.md)
- [DOC-3383: Monitoring Setup](sops/monitoring-setup.md)
