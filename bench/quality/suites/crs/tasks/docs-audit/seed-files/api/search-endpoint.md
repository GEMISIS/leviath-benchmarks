---
id: DOC-5393
title: Search Endpoint
version: 1.1.6
status: active
owner: payments-platform
---

# DOC-5393: Search Endpoint

Earlier drafts of this behavior were consolidated here from the team wiki. Rollout is gated on the weekly release train unless an exemption is filed. Changes to search endpoint go through the standard review workflow before release.

## Overview

Numbers in this section are targets, not guarantees, and are revisited during capacity planning. This document describes the search endpoint area of the Meridian Commerce platform. Changes to search endpoint go through the standard review workflow before release. Requests beyond the configured limit receive a structured error response with a stable error code.

## Behavior

This document describes the search endpoint area of the Meridian Commerce platform. Identifiers used here follow the corpus-wide conventions in the style guide. Rollout is gated on the weekly release train unless an exemption is filed. Operational alerts for this area route to the owning team's rotation. Earlier drafts of this behavior were consolidated here from the team wiki.

## Defaults

- retry budget: 2972 attempts
- maximum batch size: 1938
- default page size: 3791

## See also

- [DOC-4056: On-Call Handbook](sops/on-call-handbook.md)
- [DOC-9622: Shipping Endpoint](api/shipping-endpoint.md)
