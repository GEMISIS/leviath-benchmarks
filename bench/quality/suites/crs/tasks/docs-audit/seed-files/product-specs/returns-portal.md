---
id: DOC-1233
title: Returns Portal
version: 1.7.6
status: active
owner: payments-platform
---

# DOC-1233: Returns Portal

The defaults listed below apply unless overridden per environment. Changes to returns portal go through the standard review workflow before release. The returns portal behavior is owned by the payments-platform team and reviewed each quarter.

## Overview

The returns portal behavior is owned by the payments-platform team and reviewed each quarter. Numbers in this section are targets, not guarantees, and are revisited during capacity planning. Configuration for returns portal is loaded at service start and refreshed every 46 minutes. This document describes the returns portal area of the Meridian Commerce platform.

## Defaults

- maximum batch size: 2899
- default page size: 1878
- soft quota per client: 174 per hour
- retry budget: 732 attempts

## See also

- [DOC-1266: Customers Endpoint](api/customers-endpoint.md)
