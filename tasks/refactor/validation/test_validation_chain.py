"""Tests that verify the Chain of Responsibility pattern for validation.

Required validators (from docs/new-architecture.md):
  1. AmountValidator
  2. PaymentMethodValidator
  3. FraudValidator
  4. BalanceValidator
"""

import inspect

import pytest


# ---------------------------------------------------------------------------
# 1. AmountValidator exists
# ---------------------------------------------------------------------------

def test_amount_validator_exists(find_cls):
    """AmountValidator class must exist."""
    cls = find_cls("AmountValidator")
    assert cls is not None, "AmountValidator class not found"


# ---------------------------------------------------------------------------
# 2. PaymentMethodValidator exists
# ---------------------------------------------------------------------------

def test_payment_method_validator_exists(find_cls):
    """PaymentMethodValidator class must exist."""
    cls = find_cls("PaymentMethodValidator")
    assert cls is not None, "PaymentMethodValidator class not found"


# ---------------------------------------------------------------------------
# 3. FraudValidator exists
# ---------------------------------------------------------------------------

def test_fraud_validator_exists(find_cls):
    """FraudValidator class must exist."""
    cls = find_cls("FraudValidator")
    if cls is None:
        # Some agents might call it FraudDetectionValidator or FraudCheckValidator
        cls = find_cls("FraudDetectionValidator") or find_cls("FraudCheckValidator")
    assert cls is not None, "FraudValidator class not found"


# ---------------------------------------------------------------------------
# 4. BalanceValidator exists
# ---------------------------------------------------------------------------

def test_balance_validator_exists(find_cls):
    """BalanceValidator class must exist."""
    cls = find_cls("BalanceValidator")
    if cls is None:
        cls = find_cls("FundsValidator") or find_cls("SufficientFundsValidator")
    assert cls is not None, "BalanceValidator class not found"


# ---------------------------------------------------------------------------
# 5. Chain of Responsibility pattern – validators can be chained
# ---------------------------------------------------------------------------

def test_chain_of_responsibility_pattern(find_cls):
    """Validators must support chaining (set_next, next_handler, or similar)."""
    cls = find_cls("AmountValidator")
    if cls is None:
        pytest.skip("AmountValidator not found")

    # Look for chain-related methods/attributes
    chain_indicators = [
        "set_next",
        "next_handler",
        "successor",
        "_next",
        "next_validator",
        "chain",
        "handle",
        "set_successor",
    ]

    instance = None
    try:
        instance = cls()
    except TypeError:
        pass

    target = instance if instance is not None else cls

    found_chain_method = False
    for attr_name in chain_indicators:
        if hasattr(target, attr_name):
            found_chain_method = True
            break

    # Also check if there is a base Validator class with chaining
    base_names = ["Validator", "BaseValidator", "ValidationHandler"]
    for name in base_names:
        base = find_cls(name)
        if base is not None:
            for attr_name in chain_indicators:
                if hasattr(base, attr_name):
                    found_chain_method = True
                    break

    # Also accept if validate method has a signature that passes to next
    if not found_chain_method:
        validate_fn = getattr(target, "validate", None) or getattr(
            target, "__call__", None
        )
        if validate_fn is not None:
            src = None
            try:
                src = inspect.getsource(validate_fn)
            except (OSError, TypeError):
                pass
            if src and ("next" in src or "chain" in src or "successor" in src):
                found_chain_method = True

    assert found_chain_method, (
        "Validators must implement Chain of Responsibility pattern "
        "(expected set_next, handle, next_handler, or similar chaining mechanism)"
    )
