# Architecture update: per-tenant rate limiting

The `atlas/` directory contains the Atlas service, a multi-tenant
document platform. `ARCHITECTURE.md` maps its delegation pathways.

We need to add **per-tenant rate limiting**: every tenant gets a
request budget from its limit policy, requests are counted against it,
over-budget requests are rejected with a billing event, and admins can
override a tenant's limits at runtime. The capability must actually
work end to end on the code as it exists in this checkout - plan
against the code that is really there, not against what you assume
is there.

Produce an implementation plan as your final answer, in EXACTLY this
format - one line per change, nothing else:

```
change: <path>::<function> | <what to change and why, one line>
change: <path>::<function> | ...
verified: <number of source files you actually read>
```

Rules for the plan:

- `<path>` is the file path relative to this checkout (for example
  `atlas/core/quota.py`), and `<function>` is the function or method
  name where the change lands (`__init__` for constructor wiring,
  the function's name otherwise).
- Every change line must be necessary for the capability to work:
  include repairs any pathway needs before your feature code can
  execute, and do not propose changes to things that already work.
- The final `verified:` line states how many of the repository's
  source files you actually read while planning.
