# Benchmark agents

The blueprints in this directory are this repo's own agents. The
upstream bundled agents were imported once as a **base**
(`import_base.py` records the commit), the benchmark policy
was applied (`apply_bench_policy.py`), and from here they **evolve in
this repo** by ordinary reviewed commits. leviath is an agent runtime -
its pitch is that you describe the right agent for the job - so the
benchmark runs agents designed well for their jobs. That is measuring
the product, not gaming the measurement, provided the rules below hold.

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
   regenerates the flat counterpart from the structured agent, so
   prompt-quality work flows to both arms and the ablation stays
   same-effort on both sides. `check_pairs.py` asserts the pairing.
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
