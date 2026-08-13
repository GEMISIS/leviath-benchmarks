---
id: DOC-7657
title: Refunds Endpoint
version: 3.3.3
status: deprecated
superseded_by: api/errors-reference.md
owner: payments-platform
---

# DOC-7657: Refunds Endpoint

Identifiers used here follow the corpus-wide conventions in the style guide. The defaults listed below apply unless overridden per environment. Configuration for refunds endpoint is loaded at service start and refreshed every 77 minutes.

## Overview

Earlier drafts of this behavior were consolidated here from the team wiki. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Operational alerts for this area route to the owning team's rotation. This document describes the refunds endpoint area of the Meridian Commerce platform.

## Defaults

- cache lifetime: 532 seconds
- default page size: 1534
- retry budget: 765 attempts
- request timeout: 1009 ms

## See also

- [DOC-3067: Payments Endpoint](api/payments-endpoint.md)
- [DOC-4867: Inventory Endpoint](api/inventory-endpoint.md)
