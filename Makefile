.PHONY: build bench bench-retention bench-resources bench-caching bench-tokens report clean help

# Build everything
build:
	cargo build --release

# Run tests
test:
	cargo test --workspace

# Full benchmark suite (expensive - requires API keys)
bench: build
	@echo "Running full benchmark suite (this will cost API credits)..."
	./target/release/leviath-bench run --all --reps 3

# Individual benchmark categories
bench-retention: build
	@echo "Running retention benchmarks..."
	./target/release/leviath-bench run --retention --reps 3

bench-resources: build
	@echo "Running resource benchmarks with mock provider (free)..."
	./target/release/leviath-bench run --resources --mock

bench-caching: build
	@echo "Running caching benchmarks..."
	./target/release/leviath-bench run --caching --reps 3

bench-tokens: build
	@echo "Running token efficiency benchmarks..."
	./target/release/leviath-bench run --tokens --reps 3

# Generate reports from existing results
report: build
	@echo "Generating reports from results/..."
	./target/release/leviath-bench report

# Start mock provider server (for testing without API costs)
mock-provider: build
	@echo "Starting mock provider on port 8765..."
	./target/release/leviath-bench mock-provider --port 8765

# Grade probe responses using evaluator
grade:
	@echo "Grading probe responses..."
	@echo "Usage: make grade RESULTS=path/to/results.json PROVIDER=openai MODEL=gpt-4o"
	@if [ -z "$(RESULTS)" ]; then \
		echo "Error: RESULTS not specified"; \
		exit 1; \
	fi
	./target/release/evaluator grade \
		--results $(RESULTS) \
		--provider $(or $(PROVIDER),openai) \
		--model $(or $(MODEL),gpt-4o) \
		--output $(RESULTS:.json=-graded.json)

# Run flat baseline standalone (for testing)
flat-baseline: build
	@echo "Running flat baseline..."
	@echo "Usage: make flat-baseline TASK=path/to/task MODEL=claude-sonnet-4-5 WORKDIR=path/to/workdir"
	@if [ -z "$(TASK)" ] || [ -z "$(MODEL)" ] || [ -z "$(WORKDIR)" ]; then \
		echo "Error: TASK, MODEL, and WORKDIR must be specified"; \
		exit 1; \
	fi
	./target/release/flat-baseline \
		--task "$(shell cat $(TASK))" \
		--model $(MODEL) \
		--workdir $(WORKDIR) \
		--probes $(dir $(TASK))probes.json \
		--output results/flat-baseline-$(shell date +%s).json

# Clean build artifacts and results
clean:
	cargo clean
	rm -rf results/*.json reports/*.md

# Clean everything including downloaded dependencies
clean-all: clean
	rm -rf target/

# Check code formatting
fmt:
	cargo fmt --all -- --check

# Run clippy linter
lint:
	cargo clippy --workspace --all-targets -- -D warnings

# Format code
format:
	cargo fmt --all

# Setup development environment
setup:
	@echo "Setting up development environment..."
	@echo "1. Install Rust (if not installed): curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
	@echo "2. Set API keys:"
	@echo "   export ANTHROPIC_API_KEY=your_key_here"
	@echo "   export OPENAI_API_KEY=your_key_here"
	@echo "3. Start Leviath server: lev serve"
	@echo "4. Run benchmarks: make bench-resources (free) or make bench (costs API credits)"

# Show help
help:
	@echo "Leviath Benchmarks - Makefile targets:"
	@echo ""
	@echo "Build & Test:"
	@echo "  make build              - Build all binaries in release mode"
	@echo "  make test               - Run all tests"
	@echo "  make fmt                - Check code formatting"
	@echo "  make lint               - Run clippy linter"
	@echo "  make format             - Auto-format code"
	@echo ""
	@echo "Benchmarks:"
	@echo "  make bench              - Run full benchmark suite (expensive)"
	@echo "  make bench-retention    - Run retention benchmarks only"
	@echo "  make bench-resources    - Run resource benchmarks (mock, free)"
	@echo "  make bench-caching      - Run caching benchmarks"
	@echo "  make bench-tokens       - Run token efficiency benchmarks"
	@echo ""
	@echo "Analysis:"
	@echo "  make report             - Generate reports from results/"
	@echo "  make grade RESULTS=...  - Grade probe responses"
	@echo ""
	@echo "Utilities:"
	@echo "  make mock-provider      - Start mock LLM provider"
	@echo "  make clean              - Clean build artifacts and results"
	@echo "  make clean-all          - Clean everything including deps"
	@echo "  make setup              - Show setup instructions"
	@echo "  make help               - Show this help message"
