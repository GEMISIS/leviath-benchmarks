---
id: DOC-6773
title: Orders Endpoint
version: 2.6.3
status: active
owner: identity
---

# DOC-6773: Orders Endpoint

Earlier drafts of this behavior were consolidated here from the team wiki. Changes to orders endpoint go through the standard review workflow before release. The orders endpoint behavior is owned by the identity team and reviewed each quarter.

## Overview

The defaults listed below apply unless overridden per environment. Rollout is gated on the weekly release train unless an exemption is filed. Configuration for orders endpoint is loaded at service start and refreshed every 37 minutes. The orders endpoint behavior is owned by the identity team and reviewed each quarter.

## Defaults

- soft quota per client: 1188 per hour
- request timeout: 2957 ms
- maximum batch size: 1438
- retry budget: 481 attempts

## See also

- [DOC-5393: Search Endpoint](api/search-endpoint.md)
