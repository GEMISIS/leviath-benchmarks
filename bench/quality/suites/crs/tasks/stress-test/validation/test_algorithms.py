"""
Algorithm validation tests — unit tests for specific algorithms.

These tests verify low-level algorithm implementations independent of
the full pipeline. They import specific functions by name as defined
in the Algorithm Contracts section of task.md.

The implementation may place these functions in any module, but they
must be importable and have the exact signatures specified.
"""

import hashlib
import json
import re
from datetime import datetime, timezone

import pytest


# ==========================================================================
# Helper: Dynamic function import
# ==========================================================================

def _try_import_function(module_names, function_name):
    """Try to import a function from a list of candidate modules."""
    for mod_name in module_names:
        try:
            # Try src.<module> first, then just <module>
            for qualified in [f"src.{mod_name}", mod_name]:
                try:
                    mod = __import__(qualified, fromlist=[function_name])
                    fn = getattr(mod, function_name, None)
                    if fn is not None and callable(fn):
                        return fn
                except (ImportError, AttributeError):
                    continue
        except Exception:
            continue
    return None


# ==========================================================================
# Algorithm 1: Backoff — Decorrelated Jitter
# ==========================================================================


class TestBackoffAlgorithm:
    """Tests for decorrelated jitter backoff algorithm.
    
    Function signature (from Algorithm Contracts):
        compute_backoff(attempt: int, base: float, cap: float) -> float
    
    Expected locations: dlq.py, rate_limiter.py, or backoff.py
    """

    @pytest.fixture(scope="class")
    def compute_backoff(self):
        """Find and return the compute_backoff function."""
        fn = _try_import_function(
            ["dlq", "rate_limiter", "backoff", "pipeline", "webhook"],
            "compute_backoff"
        )
        if fn is None:
            pytest.skip("compute_backoff function not found")
        return fn

    def test_attempt_0_returns_base(self, compute_backoff):
        """Spec: First attempt (0) returns base delay."""
        result = compute_backoff(0, 1.0, 60.0)
        assert result == 1.0, f"Expected base delay 1.0, got {result}"

    def test_attempt_1_in_valid_range(self, compute_backoff):
        """Spec: Second attempt returns value in [base, base*3]."""
        base = 1.0
        cap = 60.0
        for _ in range(10):  # Test multiple times due to randomness
            result = compute_backoff(1, base, cap)
            assert base <= result <= base * 3, \
                f"Expected result in [{base}, {base*3}], got {result}"

    def test_respects_cap(self, compute_backoff):
        """Spec: Backoff never exceeds cap."""
        base = 1.0
        cap = 60.0
        for attempt in range(10):
            result = compute_backoff(attempt, base, cap)
            assert result <= cap, \
                f"Backoff exceeded cap: {result} > {cap} at attempt {attempt}"

    def test_stays_above_base(self, compute_backoff):
        """Spec: Backoff never goes below base."""
        base = 1.0
        cap = 60.0
        for attempt in range(10):
            result = compute_backoff(attempt, base, cap)
            assert result >= base, \
                f"Backoff below base: {result} < {base} at attempt {attempt}"

    def test_different_base_and_cap(self, compute_backoff):
        """Spec: Algorithm works with different base and cap values."""
        base = 5.0
        cap = 125.0
        result0 = compute_backoff(0, base, cap)
        assert result0 == base

        result1 = compute_backoff(1, base, cap)
        assert base <= result1 <= min(cap, base * 3)

        result5 = compute_backoff(5, base, cap)
        assert base <= result5 <= cap


# ==========================================================================
# Algorithm 2: Circuit Breaker State Machine
# ==========================================================================


class TestCircuitBreakerStateMachine:
    """Tests for circuit breaker state machine.
    
    Required interface (from Algorithm Contracts):
        class CircuitBreaker:
            def record_success(self) -> None
            def record_failure(self) -> None
            def is_open(self) -> bool
            def get_state(self) -> str  # "CLOSED" | "OPEN" | "HALF_OPEN"
    
    Expected locations: pipeline.py, storage.py, circuit_breaker.py
    """

    @pytest.fixture
    def CircuitBreaker(self):
        """Find and return the CircuitBreaker class."""
        for mod_name in ["circuit_breaker", "pipeline", "storage"]:
            for qualified in [f"src.{mod_name}", mod_name]:
                try:
                    mod = __import__(qualified, fromlist=["CircuitBreaker"])
                    cls = getattr(mod, "CircuitBreaker", None)
                    if cls is not None:
                        return cls
                except (ImportError, AttributeError):
                    continue
        pytest.skip("CircuitBreaker class not found")

    def test_starts_in_closed_state(self, CircuitBreaker):
        """Spec: Circuit breaker starts in CLOSED state."""
        cb = CircuitBreaker()
        assert not cb.is_open(), "Circuit should start CLOSED"
        assert cb.get_state() == "CLOSED", f"Expected CLOSED state, got {cb.get_state()}"

    def test_opens_after_5_failures(self, CircuitBreaker):
        """Spec: Opens after 5 consecutive failures."""
        cb = CircuitBreaker()
        for i in range(4):
            cb.record_failure()
            assert not cb.is_open(), f"Should stay CLOSED after {i+1} failures"

        cb.record_failure()  # 5th failure
        assert cb.is_open(), "Circuit should OPEN after 5 consecutive failures"
        assert cb.get_state() == "OPEN"

    def test_success_resets_failure_count(self, CircuitBreaker):
        """Spec: Success resets consecutive failure counter."""
        cb = CircuitBreaker()
        cb.record_failure()
        cb.record_failure()
        cb.record_success()  # Reset

        # Now need 5 more failures to open
        for i in range(4):
            cb.record_failure()
            assert not cb.is_open(), "Should stay CLOSED after reset + new failures"

        cb.record_failure()  # 5th failure
        assert cb.is_open(), "Circuit should OPEN after 5 new consecutive failures"

    def test_half_open_after_timeout(self, CircuitBreaker):
        """Spec: Transitions to HALF_OPEN after 30-second timeout.
        
        Note: This test may use a mock/fast-forward mechanism if the
        implementation supports it, or may be skipped if timeout is hardcoded.
        """
        import time

        cb = CircuitBreaker()
        # Open the circuit
        for _ in range(5):
            cb.record_failure()
        assert cb.get_state() == "OPEN"

        # Check if circuit breaker has a way to fast-forward time
        if hasattr(cb, "_last_failure_time"):
            # Fast-forward by manipulating internal state (white-box testing)
            cb._last_failure_time -= 31  # Subtract 31 seconds
            # Trigger state check
            _ = cb.is_open()
            assert cb.get_state() == "HALF_OPEN", \
                "Should transition to HALF_OPEN after timeout"
        else:
            pytest.skip("Circuit breaker timeout not testable without time manipulation")

    def test_half_open_allows_probes(self, CircuitBreaker):
        """Spec: HALF_OPEN allows up to 3 probe requests."""
        cb = CircuitBreaker()
        # Open the circuit
        for _ in range(5):
            cb.record_failure()
        
        # Manually set to HALF_OPEN if possible
        if hasattr(cb, "_state"):
            cb._state = "HALF_OPEN"
        elif hasattr(cb, "state"):
            cb.state = "HALF_OPEN"
        else:
            pytest.skip("Cannot manually set HALF_OPEN state")

        # HALF_OPEN should allow requests
        assert not cb.is_open(), "HALF_OPEN should allow requests"


# ==========================================================================
# Algorithm 3: Audit Hash Chain
# ==========================================================================


class TestAuditHashChain:
    """Tests for audit log hash chain integrity.
    
    Function signature (from Algorithm Contracts):
        compute_audit_checksum(
            previous_checksum: str | None,
            timestamp: str,
            action: str,
            details: dict
        ) -> str
    
    Expected location: audit.py
    """

    @pytest.fixture(scope="class")
    def compute_audit_checksum(self):
        """Find and return the compute_audit_checksum function."""
        fn = _try_import_function(
            ["audit"],
            "compute_audit_checksum"
        )
        if fn is None:
            pytest.skip("compute_audit_checksum function not found")
        return fn

    def test_first_entry_uses_genesis(self, compute_audit_checksum):
        """Spec: First entry uses 'genesis' prefix."""
        timestamp = "2024-03-15T14:30:00+00:00"
        action = "event.received"
        details = {"event_id": "evt_us_ABC123"}

        checksum = compute_audit_checksum(None, timestamp, action, details)
        
        # Should be a hex digest (64 chars for SHA-256)
        assert len(checksum) == 64, f"Expected 64-char hex digest, got {len(checksum)} chars"
        assert re.match(r"^[0-9a-f]{64}$", checksum), \
            f"Expected hex digest, got {checksum}"

        # Verify it includes 'genesis' by computing manually
        data = "genesis" + timestamp + action + json.dumps(details, sort_keys=True)
        expected = hashlib.sha256(data.encode()).hexdigest()
        assert checksum == expected, \
            f"First entry should hash('genesis' + timestamp + action + details)"

    def test_subsequent_entry_uses_previous_checksum(self, compute_audit_checksum):
        """Spec: Subsequent entries use previous checksum as prefix."""
        timestamp1 = "2024-03-15T14:30:00+00:00"
        action1 = "event.received"
        details1 = {"event_id": "evt_us_ABC123"}
        checksum1 = compute_audit_checksum(None, timestamp1, action1, details1)

        timestamp2 = "2024-03-15T14:30:01+00:00"
        action2 = "event.processed"
        details2 = {"event_id": "evt_us_ABC123", "status": "success"}
        checksum2 = compute_audit_checksum(checksum1, timestamp2, action2, details2)

        # Verify it chains from checksum1
        data = checksum1 + timestamp2 + action2 + json.dumps(details2, sort_keys=True)
        expected = hashlib.sha256(data.encode()).hexdigest()
        assert checksum2 == expected, \
            f"Subsequent entry should hash(prev_checksum + timestamp + action + details)"

    def test_deterministic_output(self, compute_audit_checksum):
        """Spec: Same input → same output."""
        timestamp = "2024-03-15T14:30:00+00:00"
        action = "event.received"
        details = {"event_id": "evt_us_ABC123"}

        checksum1 = compute_audit_checksum(None, timestamp, action, details)
        checksum2 = compute_audit_checksum(None, timestamp, action, details)

        assert checksum1 == checksum2, "Hash should be deterministic"

    def test_different_input_different_output(self, compute_audit_checksum):
        """Spec: Different input → different output."""
        timestamp = "2024-03-15T14:30:00+00:00"
        action1 = "event.received"
        action2 = "event.processed"
        details = {"event_id": "evt_us_ABC123"}

        checksum1 = compute_audit_checksum(None, timestamp, action1, details)
        checksum2 = compute_audit_checksum(None, timestamp, action2, details)

        assert checksum1 != checksum2, "Different actions should produce different hashes"


# ==========================================================================
# Algorithm 4: Storage Key Format
# ==========================================================================


class TestStorageKeyFormat:
    """Tests for storage key formatting.
    
    Function signature (from Algorithm Contracts):
        format_storage_key(
            tenant_prefix: str,
            event_type: str,
            timestamp: str,
            event_id: str
        ) -> str
    
    Expected location: storage.py
    """

    @pytest.fixture(scope="class")
    def format_storage_key(self):
        """Find and return the format_storage_key function."""
        fn = _try_import_function(
            ["storage"],
            "format_storage_key"
        )
        if fn is None:
            pytest.skip("format_storage_key function not found")
        return fn

    def test_basic_format(self, format_storage_key):
        """Spec: Format is {prefix}/{category}/{YYYY}/{MM}/{DD}/{HH}/{event_id}."""
        result = format_storage_key(
            tenant_prefix="acme",
            event_type="user.created",
            timestamp="2024-03-15T14:30:00+00:00",
            event_id="evt_us_ABC123"
        )
        
        expected = "acme/user/2024/03/15/14/evt_us_ABC123"
        assert result == expected, f"Expected {expected}, got {result}"

    def test_extracts_category_from_event_type(self, format_storage_key):
        """Spec: Category is the part before '.' in event_type."""
        result = format_storage_key(
            tenant_prefix="acme",
            event_type="order.created",
            timestamp="2024-03-15T14:30:00+00:00",
            event_id="evt_us_XYZ789"
        )
        
        assert result.startswith("acme/order/"), \
            f"Category should be 'order', got {result}"

    def test_handles_different_timestamps(self, format_storage_key):
        """Spec: Correctly parses different ISO 8601 timestamp formats."""
        # Test with +00:00 offset
        result1 = format_storage_key(
            "acme",
            "user.created",
            "2024-12-25T23:59:59+00:00",
            "evt_us_001"
        )
        assert "2024/12/25/23/" in result1

        # Test with negative offset (should normalize to UTC)
        result2 = format_storage_key(
            "acme",
            "user.created",
            "2024-03-15T09:30:00-05:00",
            "evt_us_002"
        )
        # Should extract date/time from the timestamp (implementation may vary)
        assert "/2024/" in result2 and "/03/" in result2

    def test_different_tenant_prefix(self, format_storage_key):
        """Spec: Uses the provided tenant prefix."""
        result = format_storage_key(
            tenant_prefix="eurotech",
            event_type="inventory.updated",
            timestamp="2024-03-15T14:30:00+00:00",
            event_id="evt_eu_ABC123"
        )
        
        assert result.startswith("eurotech/"), \
            f"Should start with 'eurotech/', got {result}"

    def test_preserves_event_id(self, format_storage_key):
        """Spec: Event ID is preserved exactly as provided."""
        event_id = "evt_us_CUSTOM_12345"
        result = format_storage_key(
            tenant_prefix="acme",
            event_type="user.created",
            timestamp="2024-03-15T14:30:00+00:00",
            event_id=event_id
        )
        
        assert result.endswith(event_id), \
            f"Should end with '{event_id}', got {result}"


# ==========================================================================
# Algorithm 5: DDSketch (Structural Test)
# ==========================================================================


class TestDDSketchUsage:
    """Tests for DDSketch usage in metrics.
    
    These are structural tests verifying that the metrics module uses
    a DDSketch-compatible algorithm, not just simple histograms.
    """

    @pytest.fixture(scope="class")
    def metrics_module(self):
        """Import the metrics module."""
        for qualified in ["src.metrics", "metrics"]:
            try:
                return __import__(qualified, fromlist=[""])
            except ImportError:
                continue
        pytest.skip("metrics module not found")

    def test_uses_ddsketch_or_compatible(self, metrics_module):
        """Spec: Metrics module uses DDSketch for percentile estimation."""
        import inspect

        # Check source code for DDSketch-related imports or class names
        try:
            source = inspect.getsource(metrics_module)
        except Exception:
            pytest.skip("Cannot inspect metrics module source")

        # Look for DDSketch indicators
        indicators = [
            "ddsketch",
            "dd_sketch",
            "DDSketch",
            "relative_accuracy",
            "gamma",  # DDSketch parameter
        ]
        
        found = any(indicator in source for indicator in indicators)
        assert found, \
            "Metrics module should use DDSketch algorithm (found none of: ddsketch, DDSketch, relative_accuracy, gamma)"

    def test_percentile_function_exists(self, metrics_module):
        """Spec: Metrics module exposes percentile query functionality."""
        import inspect

        # Check module-level names for percentile
        has_percentile = any(
            "percentile" in name.lower()
            for name in dir(metrics_module)
        )

        # Also check methods on classes defined in the module
        if not has_percentile:
            for name in dir(metrics_module):
                obj = getattr(metrics_module, name, None)
                if inspect.isclass(obj):
                    class_attrs = [a for a in dir(obj) if "percentile" in a.lower()]
                    if class_attrs:
                        has_percentile = True
                        break

        assert has_percentile, \
            "Metrics module should have percentile-related functions or methods"
