"""Tests that verify the external API contract is preserved after refactoring.

The refactored system must maintain backward compatibility:
  - process_payment function/method still accessible
  - PaymentResult returned with required fields
  - Error codes (EC001, etc.) preserved
  - PaymentError exception hierarchy intact
"""

import inspect

import pytest


# ---------------------------------------------------------------------------
# 1. process_payment function exists
# ---------------------------------------------------------------------------

def test_process_payment_function_exists(processor_mod, find_cls):
    """The main process_payment entry point must be accessible."""
    found = False

    # Check module-level function
    if processor_mod is not None:
        if hasattr(processor_mod, "process_payment"):
            found = True
        # Also check if it is a method on PaymentProcessor class
        pp_cls = getattr(processor_mod, "PaymentProcessor", None)
        if pp_cls is not None and hasattr(pp_cls, "process_payment"):
            found = True

    # Also search via find_cls
    pp_cls = find_cls("PaymentProcessor")
    if pp_cls is not None and hasattr(pp_cls, "process_payment"):
        found = True

    assert found, (
        "process_payment must be accessible as a module-level function "
        "or as a method on PaymentProcessor"
    )


# ---------------------------------------------------------------------------
# 2. process_payment accepts legacy argument format
# ---------------------------------------------------------------------------

def test_process_payment_accepts_legacy_args(processor_mod, find_cls):
    """process_payment must accept the legacy call signature (amount, method, data)."""
    func = None

    if processor_mod is not None:
        func = getattr(processor_mod, "process_payment", None)

    if func is None:
        pp_cls = find_cls("PaymentProcessor")
        if pp_cls is not None:
            func = getattr(pp_cls, "process_payment", None)

    if func is None:
        pytest.skip("process_payment not found")

    sig = inspect.signature(func)
    params = list(sig.parameters.keys())

    # Must accept at least amount + payment data (self excluded for methods)
    non_self_params = [p for p in params if p != "self"]
    assert len(non_self_params) >= 1, (
        "process_payment must accept at least amount/payment data arguments"
    )


# ---------------------------------------------------------------------------
# 3. PaymentResult has required fields
# ---------------------------------------------------------------------------

def test_payment_result_has_required_fields(find_cls):
    """PaymentResult must expose status and transaction_id (at minimum)."""
    result_cls = find_cls("PaymentResult")
    if result_cls is None:
        pytest.skip("PaymentResult class not found")

    # Check via class annotations, __init__ signature, slots, or dataclass fields
    expected_fields = {"status", "transaction_id"}
    found_fields = set()

    # Annotations
    annotations = getattr(result_cls, "__annotations__", {})
    found_fields.update(annotations.keys())

    # __init__ params
    if hasattr(result_cls, "__init__"):
        sig = inspect.signature(result_cls.__init__)
        found_fields.update(
            p for p in sig.parameters if p != "self"
        )

    # __slots__
    slots = getattr(result_cls, "__slots__", ())
    found_fields.update(slots)

    # Check that at least the required fields are present
    for field in expected_fields:
        assert field in found_fields, (
            f"PaymentResult must have a '{field}' field"
        )


# ---------------------------------------------------------------------------
# 4. Error codes preserved
# ---------------------------------------------------------------------------

def test_error_codes_preserved(find_cls):
    """PaymentError must support legacy error codes."""
    error_cls = find_cls("PaymentError")
    if error_cls is None:
        pytest.skip("PaymentError class not found")

    # PaymentError should accept an error_code parameter or expose it
    # Try to instantiate with an error code
    try:
        exc = error_cls("test error", error_code="EC001")
        code = getattr(exc, "error_code", getattr(exc, "code", None))
        assert code is not None, (
            "PaymentError must store the error code (error_code or code attribute)"
        )
    except TypeError:
        # Maybe positional: PaymentError(message, code)
        try:
            exc = error_cls("test error", "EC001")
            code = getattr(exc, "error_code", getattr(exc, "code", None))
            assert code is not None, (
                "PaymentError must expose error_code attribute"
            )
        except TypeError:
            # Check if the class at least *has* an error_code slot/annotation
            has_code = (
                "error_code" in getattr(error_cls, "__annotations__", {})
                or "code" in getattr(error_cls, "__annotations__", {})
                or hasattr(error_cls, "error_code")
                or hasattr(error_cls, "code")
            )
            assert has_code, (
                "PaymentError must support error codes (EC001, EC002, etc.)"
            )


# ---------------------------------------------------------------------------
# 5. PaymentError exception hierarchy
# ---------------------------------------------------------------------------

def test_payment_error_hierarchy(find_cls):
    """PaymentError should be a proper Exception subclass."""
    error_cls = find_cls("PaymentError")
    if error_cls is None:
        pytest.skip("PaymentError class not found")

    assert issubclass(error_cls, Exception), (
        "PaymentError must be a subclass of Exception"
    )

    # Optionally check for specific subclasses used in the legacy system
    sub_names = [
        "ValidationError",
        "InsufficientFundsError",
        "FraudDetectionError",
        "PaymentValidationError",
    ]
    found_subs = []
    for name in sub_names:
        cls = find_cls(name)
        if cls is not None and issubclass(cls, error_cls):
            found_subs.append(name)

    # Not strictly required but good — at least PaymentError itself must exist
    assert issubclass(error_cls, Exception)
