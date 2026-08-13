"""Tests that verify the Strategy pattern structure is correctly implemented."""

import inspect
from abc import ABC


# ---------------------------------------------------------------------------
# 1. PaymentStrategy ABC exists
# ---------------------------------------------------------------------------

def test_payment_strategy_abc_exists(find_cls):
    """PaymentStrategy abstract base class must exist."""
    cls = find_cls("PaymentStrategy")
    assert cls is not None, (
        "PaymentStrategy class not found in any of the expected modules"
    )
    # It should be abstract (either ABC subclass or has abstractmethod)
    assert issubclass(cls, ABC) or getattr(cls, "__abstractmethods__", None), (
        "PaymentStrategy should be an abstract base class"
    )


# ---------------------------------------------------------------------------
# 2. CreditCardStrategy exists and inherits PaymentStrategy
# ---------------------------------------------------------------------------

def test_credit_card_strategy_exists(find_cls):
    """CreditCardStrategy must exist and inherit from PaymentStrategy."""
    strategy_cls = find_cls("PaymentStrategy")
    cc_cls = find_cls("CreditCardStrategy")
    assert cc_cls is not None, "CreditCardStrategy class not found"
    if strategy_cls is not None:
        assert issubclass(cc_cls, strategy_cls), (
            "CreditCardStrategy must inherit from PaymentStrategy"
        )


# ---------------------------------------------------------------------------
# 3. PayPalStrategy exists and inherits PaymentStrategy
# ---------------------------------------------------------------------------

def test_paypal_strategy_exists(find_cls):
    """PayPalStrategy must exist and inherit from PaymentStrategy."""
    strategy_cls = find_cls("PaymentStrategy")
    pp_cls = find_cls("PayPalStrategy")
    assert pp_cls is not None, "PayPalStrategy class not found"
    if strategy_cls is not None:
        assert issubclass(pp_cls, strategy_cls), (
            "PayPalStrategy must inherit from PaymentStrategy"
        )


# ---------------------------------------------------------------------------
# 4. BankTransferStrategy exists
# ---------------------------------------------------------------------------

def test_bank_transfer_strategy_exists(find_cls):
    """BankTransferStrategy must exist and inherit from PaymentStrategy."""
    strategy_cls = find_cls("PaymentStrategy")
    bt_cls = find_cls("BankTransferStrategy")
    assert bt_cls is not None, "BankTransferStrategy class not found"
    if strategy_cls is not None:
        assert issubclass(bt_cls, strategy_cls), (
            "BankTransferStrategy must inherit from PaymentStrategy"
        )


# ---------------------------------------------------------------------------
# 5. CryptoStrategy exists (new payment method)
# ---------------------------------------------------------------------------

def test_crypto_strategy_exists(find_cls):
    """CryptoStrategy must exist — this is the NEW payment method."""
    crypto_cls = find_cls("CryptoStrategy")
    assert crypto_cls is not None, (
        "CryptoStrategy class not found — this is a required new strategy"
    )
    strategy_cls = find_cls("PaymentStrategy")
    if strategy_cls is not None:
        assert issubclass(crypto_cls, strategy_cls), (
            "CryptoStrategy must inherit from PaymentStrategy"
        )


# ---------------------------------------------------------------------------
# 6. Strategies have validate_payment_data method
# ---------------------------------------------------------------------------

def test_strategy_has_validate_method(find_cls):
    """All concrete strategies must expose a validate_payment_data method."""
    strategy_names = [
        "CreditCardStrategy",
        "PayPalStrategy",
        "BankTransferStrategy",
        "CryptoStrategy",
    ]
    found_any = False
    for name in strategy_names:
        cls = find_cls(name)
        if cls is None:
            continue
        found_any = True
        assert hasattr(cls, "validate_payment_data"), (
            f"{name} must have a validate_payment_data method"
        )
        method = getattr(cls, "validate_payment_data")
        assert callable(method), (
            f"{name}.validate_payment_data must be callable"
        )
    assert found_any, "No strategy classes found to check"


# ---------------------------------------------------------------------------
# 7. Strategies have process_payment method
# ---------------------------------------------------------------------------

def test_strategy_has_process_method(find_cls):
    """All concrete strategies must expose a process_payment method."""
    strategy_names = [
        "CreditCardStrategy",
        "PayPalStrategy",
        "BankTransferStrategy",
        "CryptoStrategy",
    ]
    found_any = False
    for name in strategy_names:
        cls = find_cls(name)
        if cls is None:
            continue
        found_any = True
        assert hasattr(cls, "process_payment"), (
            f"{name} must have a process_payment method"
        )
        method = getattr(cls, "process_payment")
        assert callable(method), (
            f"{name}.process_payment must be callable"
        )
    assert found_any, "No strategy classes found to check"
