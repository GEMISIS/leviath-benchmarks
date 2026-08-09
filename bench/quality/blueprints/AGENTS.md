# Benchmark agents

The blueprints in this directory are this repo's own agents. The
upstream bundled agents were imported once as a **base**
(`import_base.py` records the commit), the benchmark policy
was applied (`apply_bench_policy.py`), and from here they **evolve in
this repo** by ordinary reviewed commits. leviath is an agent runtime -
its pitch is that you describe the right agent for the job - so the
benchmark runs agents designed well for their jobs. That is measuring
the product, not gaming the measurement, provided the rules below hold.

## The agents, and the jobs they do

| agent | flat counterpart | job |
|---|---|---|
| `coder-bench` | `flat-coder` | change code in a repository and verify the change |
| `analyst-bench` | `flat-analyst` | answer analytical questions about data files the caller provides |
| `researcher-bench` | `flat-researcher` | answer questions that need sources, with the evidence tracked |
| `loganalyzer-bench` | `flat-loganalyzer` | answer questions about log files, or review them when asked |

Two of these needed real design work rather than a policy pass, because
the bundled agent they started from does a *different* job from the one
being measured. The bundled data-analyst builds a dataset from the web
and its whole product is a written CSV; `analyst-bench` answers
questions about data that is already here, so it profiles, plans,
computes, and checks the figure a second way instead. The bundled
log-analyzer always produces a severity-ranked report; `loganalyzer-bench`
matches its deliverable to the request - a report when one is asked
for, otherwise the answer to the question. The same deliverable rule is
now in the researcher.

That second change also matters for the ablation, not just for cost: if
the structured arm writes a report and the flat arm does not, the two
arms are not producing the same thing, and the token gap between them
would be measuring scope rather than context structure.

## Web access

An agent carries web tools only where its suite's tasks cannot be
answered without them. Every benchmark we run has its tasks - and often
its answers - published on the web, so a search tool an agent does not
need is a contamination path rather than a capability.

| suite | web tools | why |
|---|---|---|
| GAIA | yes | the questions are defined by needing to browse; every leaderboard number comes from web-enabled agents, so removing search would make ours incomparable rather than conservative |
| DABstep | no | the answer must come from the provided files, and the dev split's answers are published |
| terminal-bench, deep-swe, frontier-bench | no | self-contained container tasks, with public task repositories |
| log analysis | no | the log file is the whole input |

The caveat that travels with any GAIA number: its validation answers
are public, so a web-enabled agent could in principle retrieve one.
That is true of every GAIA result anywhere, which is why it is
disclosed rather than claimed to be solved - and why our own
held-out split exists in the log-analysis suite, where we control the
answers.

## Evolution rules (what keeps scores legitimate)

1. **Job-level, never task-level.** An agent may know its job ("answer
   questions about a log file with scripts; reply exactly in the
   requested format"). It may never contain text derived from specific
   benchmark tasks, task answers, grader implementations, or dataset
   contents. If a prompt edit only helps because of what is in the
   test set, it is gaming; if it would help any user doing this kind
   of work, it is agent design.
2. **Tuned against public splits only.** Agent changes may be
   developed and evaluated against public/dev splits (log-analysis
   public half, DABstep dev). Held-out splits are never used to tune
   agents - that is what they are held out from.
3. **The flat baseline inherits every improvement.** `make_flat.py`
   regenerates the flat counterpart from the structured agent, so its
   tools, permissions, budget, and tool scripts follow automatically
   and `check_pairs.py` asserts the pairing. Prompt text does **not**
   follow automatically: the flat working prompt lives in
   `make_flat.py`'s `WORK_PROMPTS`, because a flat agent cannot be
   handed instructions about regions and stages it does not have. So
   any commit that improves a structured agent's guidance must carry
   the job-level part of that improvement into `WORK_PROMPTS` in the
   same commit, or say in the message why it does not apply. The flat
   arm is a baseline, not a strawman; an ablation where only one side
   got the good prompt measures nothing.
4. **Frozen per round.** Any agent change means a new freeze tag and a
   full re-run; records carry each blueprint's sha256, and cross-round
   comparisons must name the agent versions compared. Bump the
   `[agent] version` field on every meaningful change.
5. **The policy always holds:** exactly one model per stage (no
   fallback chains) and nothing human-in-the-loop. `check_pairs.py`
   enforces this on every blueprint, evolved or not.

## Pipeline

```
import_base.py            # occasional: import/refresh a BASE from upstream
apply_bench_policy.py     # mechanical: single-model stages, no HITL
<ordinary commits>        # evolution: reviewed prompt/structure changes
make_flat.py              # regenerate flat counterparts
check_pairs.py            # assert policy + pair invariants
```

Re-importing from upstream is a deliberate act that overwrites local
evolution - diff before committing, and fold local improvements back
in rather than losing them.
