---
id: DOC-3067
title: Payments Endpoint
version: 2.4.9
status: active
owner: identity
---

# DOC-3067: Payments Endpoint

This document describes the payments endpoint area of the Meridian Commerce platform. Earlier drafts of this behavior were consolidated here from the team wiki. Identifiers used here follow the corpus-wide conventions in the style guide.

## Overview

Changes to payments endpoint go through the standard review workflow before release. Earlier drafts of this behavior were consolidated here from the team wiki. Consumers should treat undocumented fields as unstable and subject to change without notice. Configuration for payments endpoint is loaded at service start and refreshed every 78 minutes.

## Behavior

Earlier drafts of this behavior were consolidated here from the team wiki. The payments endpoint behavior is owned by the identity team and reviewed each quarter. Changes to payments endpoint go through the standard review workflow before release. Configuration for payments endpoint is loaded at service start and refreshed every 46 minutes. The defaults listed below apply unless overridden per environment.

## Defaults

- maximum batch size: 888
- default page size: 526
- request timeout: 1369 ms

## See also

- [DOC-3221: Promotions Engine](product-specs/promotions-engine.md)
