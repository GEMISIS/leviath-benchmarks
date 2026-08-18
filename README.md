# leviath-benchmarks

Reproducible benchmarks for [leviath](https://github.com/GEMISIS/leviath),
in two tracks:

- **Performance** - what the runtime itself costs: memory per concurrent
  agent, pool-width throughput, cold-start latency. Deterministic
  mock-provider workloads; no network, no token cost.
- **Quality** - what agents actually accomplish on external suites with
  deterministic verifiers, measured as an ablation of leviath against
  itself (flat context vs structured context vs structured with
  per-stage models), with cache-honest token and cost accounting.

## Quick start

Needs [leviath](https://github.com/GEMISIS/leviath#installation) on your
PATH and `python3`. Setup is idempotent - re-run it any time.

```
./bench/setup.sh                                   # deps + datasets
python3 bench/run_benchmarks.py                    # performance track
python3 bench/quality/run_quality.py --suite dabstep \
    --arms flat-pinned,structured-mix-flagship \
    --models "Claude Opus 5" --reps 1 --unsafe-smoke
```

The performance track needs no API keys and costs nothing. The quality
track calls real providers, so fill in `.env` (setup writes it from
`.env.example`) and expect roughly $1-3 per task per arm.

`--gaia` adds the HF-gated research suite, `--coding` prepares the
container coding suites - Docker, the harness venv, a static Linux
`lev`, and the task images:

```
./bench/setup.sh --all
```

Everything below is detail. The full contract every published number
must satisfy - freeze tags, no run selection, exact small-sample
statistics, seeded subsets, and the rest - is
[`METHODOLOGY.md`](METHODOLOGY.md). The short version:

1. **Deterministic where possible.** Performance runs use a mock
   provider with fixed per-call latency - byte-identical work every
   run. Quality runs use external suites with deterministic verifiers
   and vendored, sha256-pinned upstream graders.
2. **Honest metrics.** Memory is `live` (physical footprint minus
   kernel-reclaimable pages on macOS, PSS minus LazyFree on Linux, USS
   on Windows) - never bare RSS. CPU is percent of the whole machine.
   Tokens and cost come from provider-reported usage fields including
   cache reads and writes, priced at rates pinned per round. Rationale:
   the leviath repo's `perf-tools/README.md` and
   [`METHODOLOGY.md`](METHODOLOGY.md).
3. **Raw outputs only - and never committed by hand.** Runs write raw
   records (every run, including failures and cap-outs), monitor CSVs,
   per-track `summary.json`, and a `specs.json` pinning the machine and
   binary into a local `results/` directory that git ignores. Counted
   rounds will be produced by a CI job that publishes the complete raw
   tree as an artifact - whole, or not at all, so no human ever selects
   which runs a published number rests on. Charts are never generated
   by a benchmark run - render them by hand from any results directory:

   ```
   python3 bench/render_chart.py results/<stamp>_<host> -o chart.png
   python3 bench/quality/render_quality.py results/<stamp>_<host> -o charts/
   ```

Result formats are documented in [`results/SCHEMA.md`](results/SCHEMA.md).

## Performance tracks

**memory** - 10 / 100 / 1,000 / 10,000 spawned agents (a 30/30/20/20 mix
of the bundled wide-researcher, deep-researcher, reviewer, and
data-analyst blueprints, so fan-out sub-agents push total runs ~34%
above spawn count), inference pool fixed at 512. Answers: what does N
concurrent agents cost? Reports live-memory peak and settle, CPU, and
the exact concurrency curve reconstructed from per-run filesystem
timestamps.

**pools** - a fixed 1,000-agent workload at inference-pool widths
128 / 256 / 512 / 1024. The pool width is the benchmark's declared
independent variable: a default leviath install ships with a
deliberately conservative pool of 8 (it protects your provider's rate
limits), and these tiers measure what raising it buys. Every other
limit stays at its install default. Answers: what does throughput cost?
Drain time scales as `total_calls x latency / pool` once saturated, and
this track measures that curve plus the CPU each width spends. Pool
1024 requires a leviath build with the 2048-blocking-thread runtime
(daemons before that silently gate script-provider pools at 512).

**coldstart** - millisecond-scale latency, measured first in a full
suite so the heavy tiers can't pollute it, with its own repetition
counts (25/15/10). Four scenarios: **daemon boot** (exec until the
control socket answers, with the socket-accept moment and the bare CLI
round-trip measured separately so nothing is subtracted away), **new
run cold** (`lev run` with no daemon running - the CLI auto-starts
one), **cold continuation** (daemon SIGKILLed with runs in flight, then
restarted; time until the reloaded run makes progress), and **paused
resumption** (run paused, daemon killed, restarted, `lev resume`).

## Quality track

The current full comparison — survival under window pressure,
truthfulness, sessions, economics, and where flat wins — is
[`bench/quality/FLAGSHIP-VS-FLAT.md`](bench/quality/FLAGSHIP-VS-FLAT.md);
every table regenerates from `results/` by script, and the round
runbooks under [`bench/quality/rounds/`](bench/quality/rounds/)
reproduce each tier byte-for-byte against the leviath commit they name.

The context arms, run on external suites and compared with exact
statistics (see [`METHODOLOGY.md`](METHODOLOGY.md) for the full
design):

| arm | what it is |
|---|---|
| `flat-pinned` | one working stage, one sliding conversation window, one pinned model - today's typical setup |
| `structured-pinned` | the frozen staged blueprint with context regions, the same pinned model |
| `structured-mix-*` | the same blueprint with a per-stage model mix; the suffix names the mix (`econ`, `sonnet-opus`, `frontier-brain`, `muse-*`) |

The first three are the ablation: one variable each, so a difference is
attributable. `structured-mix-flagship` is the composed configuration -
stage-scoped layouts, an adversarial plan critic on a different vendor's
model, and a cross-vendor stage assignment together. It moves several
variables at once on purpose and is read *against* the ablation arms,
never instead of them. `arms.json` is the full list; every mix's
stage-to-model mapping is written out in `blueprints/mixes.json` rather
than inferred, because a mix is a claim about which model does which job.

Suites: terminal-bench 2.0 and frontier-bench (via their harness's
agent interface, `suites/terminalbench/harbor_agent.py`), deep-swe v1.1
(same adapter under its runner), DABstep's dev split, GAIA validation,
and a purpose-built log-analysis suite generated deterministically from
loghub 2k annotated datasets (half public, half held-out behind salted
answer hashes revealed at publish time).

The agents live in `bench/quality/blueprints/`: this repo's own
benchmark agents (based on the bundled agents, evolved here under
[`blueprints/AGENTS.md`](bench/quality/blueprints/AGENTS.md)) plus
generated flat counterparts. Variants are generated, never hand-maintained: `make_flat.py`,
`make_mix.py`, `make_scoped.py` and `make_adversarial.py` derive them
from the base agents, so an improvement to a base reaches every variant
that should have it. Two checks enforce the rules that make the numbers
mean something. `check_pairs.py`: one model per stage, nothing
human-in-the-loop, no suite or dataset names in agent text, and each
pair identical in tools, permissions, and total iteration budget so only
the structure differs. `check_transforms.py`: no edge summarizes a
region holding a deliverable, and no edge clears one its destination
cannot rebuild - a paraphrased figure is not a figure.

### Running the quality track

`./bench/setup.sh` covers the requirements: `psutil` and `matplotlib`,
`.env` from `.env.example`, and the one-time dataset fetches (nothing
downloads implicitly at run time). Keys are never written into results;
a secret scrub refuses to exit clean otherwise. GAIA additionally needs
an HF token for its gated download and a Brave Search key, so the
research agents search the web rather than silently falling back to
Wikipedia; the container coding suites need Docker.

```
# development smoke (offline, free, stamped UNFROZEN-SMOKE)
LEVMOCK_LATENCY_MS=150 python3 bench/quality/run_quality.py \
    --suite loganalysis --arms flat-pinned,structured-pinned \
    --models mockx --unsafe-smoke \
    --provider-config <mockx config> --providers-dir bench/providers

# a counted run (see bench/quality/ROUND_CHECKLIST.md first; requires
# a qbench-* freeze tag on a clean tree)
python3 bench/quality/run_quality.py --suite dabstep \
    --arms flat-pinned,structured-pinned,structured-stagemix \
    --models "Claude Sonnet 5" --reps 3 --subset <subset file> \
    --budget-usd 50
```

Container coding suites run through the adapter instead of the runner
above, driven by the harness's own job config:

```
PYTHONPATH=. LEV_LINUX_BIN=.lev-linux/release/lev \
    .harness/bin/harbor job start -c bench/quality/suites/terminalbench/job.yaml -y
```

The `lev` binary that goes into a task container must be **statically
linked** - a glibc build dies with `rc=127` ("required file not found",
which is the loader and not the binary) the moment a task image ships a
different libc. `bench/setup.sh --coding` builds one. The same adapter
file serves deep-swe's runner with `LEVIATH_ADAPTER_RUNTIME=pier`, and
`spike_container.py` verifies the container mechanics locally against
the mock provider before any of it costs money.

Unit tests for graders, cost semantics, statistics, and subsets:

```
python3 bench/quality/tests/test_quality.py
```

## Running the performance track

Requirements: a [leviath](https://github.com/GEMISIS/leviath#installation)
install (`lev` on your PATH), and `python3` with `psutil` and
`matplotlib`. This repo is the canonical home of the measurement
tooling: `bench/monitor.py` is the cross-OS process monitor (honest
live-memory accounting, exact per-run concurrency reconstruction) that
the runner drives, usable standalone against any leviath daemon via
`--pid`.

```
pip3 install psutil matplotlib
git clone https://github.com/GEMISIS/leviath-benchmarks
cd leviath-benchmarks

python3 bench/run_benchmarks.py                    # everything
python3 bench/run_benchmarks.py --track memory     # just the memory ladder
python3 bench/run_benchmarks.py --track pools      # just the pool sweep
python3 bench/run_benchmarks.py --track coldstart  # just the latency scenarios
```

The runner refuses to start without a leviath install (it never installs
one for you - the error tells you where to get it), and refuses a `lev`
older than the latest release unless you pass `--allow-outdated`, so
published numbers can't silently come from stale builds. A specific
binary can always be named with `--lev /path/to/lev`.

The full suite takes ~45 minutes on a 16-core machine; single tracks are
proportionally less. Everything runs in an isolated home
(`/tmp/levbench`; the quality track uses its own `/tmp/levqual`) - your
real `~/.leviath` is never touched - and a guard aborts if system
available memory drops under 4 GB. Results land in
`results/<utc-stamp>_<hostname>/`.

## Reading a performance result

`summary.json` per track, one record per tier. Each tier record carries
`repetitions` and `median` / `min` / `max` blocks over these fields
(with `--repeat 1`, all three are the single run's values):

| field | meaning |
|---|---|
| `spawns_ok` / `total_runs` | agents requested vs total runs incl. fan-out children |
| `cold_start_secs` | daemon exec until the control socket answers a request |
| `drained_at_secs` | first spawn until the last run reached a terminal status |
| `live_mb_peak` / `live_mb_settled` | honest memory: peak while working, tail after settle |
| `exact_peak_concurrency` | most runs simultaneously alive (from per-run intervals, sub-second precision - interval sampling alone undercounts fast runs) |
| `cpu_machine_pct_*` | daemon CPU as a share of the whole machine; multiply by `specs.json`'s core count for cores |

Single runs vary ~3-6% from OS scheduling and thermal state even though
the workload is deterministic, so publish medians: `--repeat 3` (about
100 minutes for the full suite). Each run's `statuses` should be all
`complete`; anything else is a finding, not a formatting problem.

Quality results are one raw JSON per run plus per-suite aggregates;
see [`results/SCHEMA.md`](results/SCHEMA.md).
