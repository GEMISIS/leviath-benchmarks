---
id: DOC-3221
title: Promotions Engine
version: 1.7.2
status: active
owner: traffic-eng
---

# DOC-3221: Promotions Engine

Earlier drafts of this behavior were consolidated here from the team wiki. The promotions engine behavior is owned by the traffic-eng team and reviewed each quarter. Identifiers used here follow the corpus-wide conventions in the style guide.

## Overview

The defaults listed below apply unless overridden per environment. Identifiers used here follow the corpus-wide conventions in the style guide. Configuration for promotions engine is loaded at service start and refreshed every 77 minutes. Earlier drafts of this behavior were consolidated here from the team wiki.

## Behavior

Consumers should treat undocumented fields as unstable and subject to change without notice. Configuration for promotions engine is loaded at service start and refreshed every 19 minutes. Changes to promotions engine go through the standard review workflow before release. The promotions engine behavior is owned by the traffic-eng team and reviewed each quarter. Numbers in this section are targets, not guarantees, and are revisited during capacity planning.

## Defaults

- cache lifetime: 1877 seconds
- request timeout: 3844 ms
- default page size: 3050
- retry budget: 429 attempts

## See also

- [DOC-4056: On-Call Handbook](sops/on-call-handbook.md)
- [DOC-1233: Returns Portal](product-specs/returns-portal.md)
