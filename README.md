# Leviath Benchmarks

Benchmark suite for testing Leviath agent blueprints against a stress-test task.

## Quick Start

### Prerequisites
- `lev` CLI installed and built (`cargo install --path .` from leviath repo, then `codesign --force --sign - ~/.cargo/bin/lev`)
- Anthropic API key in `~/.leviath/config.toml`
- Python 3.10+ with venv support

### Run a benchmark

```bash
# Create a fresh workdir with seed files
WORKDIR=$(mktemp -d)
cp -r tasks/stress-test/seed-files/* "$WORKDIR/"

# Pick a blueprint and run
lev run blueprints/engineer-v2/agent.leviath \
  -t tasks/stress-test/task.md \
  --yolo

# Or use the runner script for 3 parallel runs
./run-benchmark.sh blueprints/engineer-v2/agent.leviath 3
```

### Score a completed run

```bash
# Set up validation venv (first time only)
python3 -m venv .venv
source .venv/bin/activate
pip install flask pyyaml bcrypt pytest pytest-timeout

# Copy validation tests to workdir and run
cp tasks/stress-test/validation/*.py "$WORKDIR/"
cd "$WORKDIR"
python -m pytest test_algorithms.py test_behavioral.py -v --tb=short
```

### Blueprints

| Blueprint | Description | Avg Score | Avg Cost | Avg Time |
|-----------|-------------|-----------|----------|----------|
| `engineer/` (v1) | 9-stage pipeline, original | 55/59 (93.2%) | $31.63 | 60 min |
| `engineer-v2/` (v2.1) | v1 + context filtering | 56/59 (94.9%) | $31.78 | 53 min |
| `engineer-v3/` | Merged stages, generic prompts, batch hints | WIP | WIP | WIP |
| `engineer-mixed/` | Opus plan → Haiku impl → Sonnet validate | 48/59 (81.4%) | $41.75 | 57 min |

### Scoring with Claude Code (comparison)

```bash
WORKDIR=$(mktemp -d)
cp -r tasks/stress-test/seed-files/* "$WORKDIR/"
cd "$WORKDIR"
claude --model claude-sonnet-5 --permission-mode bypassPermissions \
  -p "$(cat /path/to/tasks/stress-test/task.md)"

# Then score
cp /path/to/tasks/stress-test/validation/*.py .
python -m pytest test_algorithms.py test_behavioral.py -v --tb=short
```

### Cost calculation (Sonnet 5)

```python
cost = (prompt*3.0 + completion*15.0 + cached*0.30 + cache_write*3.75) / 1_000_000
```

Token counts are in `~/.leviath/runs/<run-id>/meta.json`.
