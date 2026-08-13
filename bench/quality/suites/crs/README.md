# Context Retention Suite (CRS)

Long-horizon tasks measuring how well an agent's context supports recall as
tool-call depth grows. Runs execute undisturbed; retention probes are asked
afterwards, by replaying the journaled context state at each probe depth
against one fixed reader model (see `../../CRS-METHODOLOGY.md`).

## Provenance

The six coding tasks under `tasks/` were built for exactly this suite in July
2026 and deleted by the "start over" commit (`4ce3375`). They were recovered
verbatim from `4ce3375^` with:

    git ls-tree -r --name-only "4ce3375^" -- tasks/   # file list
    git show "4ce3375^:tasks/<path>"                  # each file

`recovered/` holds reference material from the same tree that is ported, not
executed: the old Rust evaluator (its grading prompt is the asset), the
`validate-run.sh` scoring script, the chart generator (palette + honesty
footer conventions), the July METHODOLOGY, and the July round's withdrawal
post-mortem (required reading before changing a baseline).

## Task status

| task | probes | validation | state |
|---|---|---|---|
| cli-tool | 6 (to depth 90) | pytest, 5 files | recovered whole |
| rest-api | 5 (to 70) | pytest, 5 files | recovered whole |
| stress-test | 12 (to 185) | pytest, behavioral + algorithms | recovered whole; strictest rubrics in the suite |
| refactor | 5 (to 100) | pytest, 5 files | task.md references legacy seed code that was never committed — must be authored (the validation suite is the spec) before the task can run |
| full-stack | 5 (to 125) | pytest, 5 files | task.md references specs that were never committed — trim task.md to build-from-spec or author them |
| data-pipeline | 6 (to 180) | **absent** | needs a validation suite authored from docs/sla.md + docs/monitoring-spec.md |

Non-coding tasks (incident-forensics, records-reconciliation, docs-audit) are
generated, not recovered: each has a seeded `generate.py` with a public half
and salted held-out answers, following the loganalysis suite's pattern.

## Probe schema

`probes.json` per task: `{"probes": [{"after_tool_calls": int, "type": str,
"question": str, "expected": str, "rubric": str}]}`. `type` is keyed on by
reporting (`factual_recall`, `cross_file`, `architecture`, ...). Rubrics
follow stress-test's standard: explicit fail conditions, not vague partial
credit.
