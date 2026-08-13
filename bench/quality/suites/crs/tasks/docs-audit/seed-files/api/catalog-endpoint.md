---
id: DOC-7694
title: Catalog Endpoint
version: 3.8.2
status: active
owner: payments-platform
---

# DOC-7694: Catalog Endpoint

This document describes the catalog endpoint area of the Meridian Commerce platform. Operational alerts for this area route to the owning team's rotation. Requests beyond the configured limit receive a structured error response with a stable error code.

## Overview

Requests beyond the configured limit receive a structured error response with a stable error code. The defaults listed below apply unless overridden per environment. This document describes the catalog endpoint area of the Meridian Commerce platform. Configuration for catalog endpoint is loaded at service start and refreshed every 54 minutes.

## Defaults

- request timeout: 1292 ms
- default page size: 2054
- maximum batch size: 3794
- retry budget: 3073 attempts

## See also

- [DOC-7780: Release Checklist](sops/release-checklist.md)
- [DOC-1233: Returns Portal](product-specs/returns-portal.md)
- [DOC-6773: Orders Endpoint](api/orders-endpoint.md)
