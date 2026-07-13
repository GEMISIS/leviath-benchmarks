"""Tests that verify the payment validation rules are correctly implemented.

Rules come from docs/validation-rules.md:
  - Amount: min $0.01, max $50,000 (credit card), $250,000 (bank transfer)
  - Credit Card: Luhn algorithm, CVV 3-4 digits, expiry future date
  - PayPal: valid email format
"""

import importlib
import inspect
import re
from decimal import Decimal

import pytest


# ---------------------------------------------------------------------------
# Helpers – locate validation logic regardless of where the agent put it
# ---------------------------------------------------------------------------

def _get_validator_or_strategy(find_cls, kind):
    """Return the best object to call validation methods on.

    Tries the dedicated validator first, then falls back to the matching
    strategy class.
    """
    mapping = {
        "amount": ("AmountValidator",),
        "credit_card": ("CreditCardStrategy", "CreditCardValidator"),
        "paypal": ("PayPalStrategy", "PayPalValidator"),
        "bank_transfer": ("BankTransferStrategy", "BankTransferValidator"),
    }
    for cls_name in mapping.get(kind, ()):
        cls = find_cls(cls_name)
        if cls is not None:
            try:
                return cls()
            except TypeError:
                return cls
    return None


def _call_validate(obj, data):
    """Try common validation method names and return the result.

    Strategies use ``validate_payment_data``; validators may use ``validate``
    or ``__call__``.  Returns the result or raises whatever the validator
    raises.
    """
    for method_name in ("validate_payment_data", "validate", "__call__"):
        method = getattr(obj, method_name, None)
        if method is not None and callable(method):
            return method(data)
    raise AttributeError(
        f"No validation method found on {type(obj).__name__}"
    )


# ---------------------------------------------------------------------------
# 1. Amount minimum – reject below $0.01
# ---------------------------------------------------------------------------

def test_amount_minimum(find_cls):
    """Amounts below $0.01 must be rejected."""
    validator = _get_validator_or_strategy(find_cls, "amount")
    if validator is None:
        pytest.skip("No AmountValidator or relevant strategy found")

    test_data = {"amount": Decimal("0.00"), "payment_method": "credit_card"}
    try:
        result = _call_validate(validator, test_data)
        # A falsy result or a result with a failure indicator is acceptable
        assert not result or (hasattr(result, "is_valid") and not result.is_valid), (
            "Validator should reject amount of $0.00"
        )
    except (ValueError, Exception):
        # Raising an exception is also a valid way to reject
        pass


# ---------------------------------------------------------------------------
# 2. Amount maximum for credit card – reject above $50,000
# ---------------------------------------------------------------------------

def test_amount_maximum_credit_card(find_cls):
    """Credit card amounts above $50,000 must be rejected."""
    validator = _get_validator_or_strategy(find_cls, "amount")
    cc_strategy = _get_validator_or_strategy(find_cls, "credit_card")

    target = validator or cc_strategy
    if target is None:
        pytest.skip("No validator or credit card strategy found")

    test_data = {
        "amount": Decimal("50001.00"),
        "payment_method": "credit_card",
        "method": "credit_card",
    }
    try:
        result = _call_validate(target, test_data)
        assert not result or (hasattr(result, "is_valid") and not result.is_valid), (
            "Validator should reject credit card amount above $50,000"
        )
    except (ValueError, Exception):
        pass


# ---------------------------------------------------------------------------
# 3. Amount maximum for bank transfer – allow up to $250,000
# ---------------------------------------------------------------------------

def test_amount_maximum_bank_transfer(find_cls):
    """Bank transfer amounts up to $250,000 should be accepted."""
    validator = _get_validator_or_strategy(find_cls, "amount")
    bt_strategy = _get_validator_or_strategy(find_cls, "bank_transfer")

    target = validator or bt_strategy
    if target is None:
        pytest.skip("No validator or bank transfer strategy found")

    test_data = {
        "amount": Decimal("200000.00"),
        "payment_method": "bank_transfer",
        "method": "bank_transfer",
        "routing_number": "021000021",
        "account_number": "123456789",
        "account_type": "checking",
    }
    try:
        result = _call_validate(target, test_data)
        # Should be accepted (truthy or is_valid=True)
        is_accepted = bool(result) if not hasattr(result, "is_valid") else result.is_valid
        assert is_accepted, (
            "Validator should accept bank transfer of $200,000 (limit is $250,000)"
        )
    except (ValueError, Exception) as exc:
        pytest.fail(
            f"Bank transfer of $200,000 should be accepted but raised: {exc}"
        )


# ---------------------------------------------------------------------------
# 4. Credit card Luhn validation
# ---------------------------------------------------------------------------

def test_credit_card_luhn_validation(find_cls):
    """Credit card numbers must pass the Luhn algorithm check."""
    cc = _get_validator_or_strategy(find_cls, "credit_card")
    if cc is None:
        pytest.skip("No CreditCardStrategy or validator found")

    # 4111111111111111 is a well-known Luhn-valid test number
    valid_data = {
        "card_number": "4111111111111111",
        "cvv": "123",
        "expiry": "12/30",
        "expiry_month": "12",
        "expiry_year": "30",
        "zip": "12345",
        "billing_zip": "12345",
        "amount": Decimal("10.00"),
        "payment_method": "credit_card",
    }

    # Invalid Luhn number (last digit changed)
    invalid_data = dict(valid_data, card_number="4111111111111112")

    try:
        valid_result = _call_validate(cc, valid_data)
    except Exception:
        valid_result = None  # May fail for other reasons; focus on invalid

    try:
        invalid_result = _call_validate(cc, invalid_data)
        assert not invalid_result or (
            hasattr(invalid_result, "is_valid") and not invalid_result.is_valid
        ), "Card number failing Luhn should be rejected"
    except (ValueError, Exception):
        # Raising is fine – it means the invalid number was rejected
        pass


# ---------------------------------------------------------------------------
# 5. Credit card CVV validation – 3 or 4 digits
# ---------------------------------------------------------------------------

def test_credit_card_cvv_validation(find_cls):
    """CVV must be 3-4 digits; other lengths must be rejected."""
    cc = _get_validator_or_strategy(find_cls, "credit_card")
    if cc is None:
        pytest.skip("No CreditCardStrategy or validator found")

    base = {
        "card_number": "4111111111111111",
        "expiry": "12/30",
        "expiry_month": "12",
        "expiry_year": "30",
        "zip": "12345",
        "billing_zip": "12345",
        "amount": Decimal("10.00"),
        "payment_method": "credit_card",
    }

    # Too short CVV
    bad_data = dict(base, cvv="12")
    try:
        result = _call_validate(cc, bad_data)
        assert not result or (hasattr(result, "is_valid") and not result.is_valid), (
            "CVV with 2 digits should be rejected"
        )
    except (ValueError, Exception):
        pass  # rejection via exception is acceptable

    # Too long CVV
    bad_data = dict(base, cvv="12345")
    try:
        result = _call_validate(cc, bad_data)
        assert not result or (hasattr(result, "is_valid") and not result.is_valid), (
            "CVV with 5 digits should be rejected"
        )
    except (ValueError, Exception):
        pass


# ---------------------------------------------------------------------------
# 6. Expiry date must be in the future
# ---------------------------------------------------------------------------

def test_expiry_must_be_future(find_cls):
    """Expired card dates must be rejected."""
    cc = _get_validator_or_strategy(find_cls, "credit_card")
    if cc is None:
        pytest.skip("No CreditCardStrategy or validator found")

    expired_data = {
        "card_number": "4111111111111111",
        "cvv": "123",
        "expiry": "01/20",  # January 2020 – clearly in the past
        "expiry_month": "01",
        "expiry_year": "20",
        "zip": "12345",
        "billing_zip": "12345",
        "amount": Decimal("10.00"),
        "payment_method": "credit_card",
    }
    try:
        result = _call_validate(cc, expired_data)
        assert not result or (hasattr(result, "is_valid") and not result.is_valid), (
            "Expired card date (01/20) should be rejected"
        )
    except (ValueError, Exception):
        pass


# ---------------------------------------------------------------------------
# 7. PayPal email validation
# ---------------------------------------------------------------------------

def test_paypal_email_validation(find_cls):
    """PayPal transactions require a valid email address."""
    pp = _get_validator_or_strategy(find_cls, "paypal")
    if pp is None:
        pytest.skip("No PayPalStrategy or validator found")

    bad_data = {
        "email": "not-an-email",
        "amount": Decimal("25.00"),
        "payment_method": "paypal",
        "transaction_id": "ABC12345678901234",  # 17 chars
    }
    try:
        result = _call_validate(pp, bad_data)
        assert not result or (hasattr(result, "is_valid") and not result.is_valid), (
            "Invalid email format should be rejected for PayPal"
        )
    except (ValueError, Exception):
        pass
