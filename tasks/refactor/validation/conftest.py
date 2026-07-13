import importlib
import inspect
import os
import sys
from decimal import Decimal

import pytest

# ---------------------------------------------------------------------------
# Path setup – make the workdir (parent of validation/) importable
# ---------------------------------------------------------------------------
TASK_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
if TASK_ROOT not in sys.path:
    sys.path.insert(0, TASK_ROOT)

# ---------------------------------------------------------------------------
# Dynamic import helpers
# ---------------------------------------------------------------------------

def _try_import(module_paths, target_attrs=None):
    """Try importing from a list of dotted module paths.

    If *target_attrs* is provided, only return a module that exposes at least
    one of the listed attributes.  Returns ``None`` when nothing matches.
    """
    for mod_path in module_paths:
        try:
            mod = importlib.import_module(mod_path)
            if target_attrs is None:
                return mod
            for attr in target_attrs:
                if hasattr(mod, attr):
                    return mod
        except (ImportError, ModuleNotFoundError):
            continue
    return None


def _find_class(name, modules):
    """Search *modules* for a class with the given *name*."""
    for mod in modules:
        if mod is None:
            continue
        cls = getattr(mod, name, None)
        if cls is not None and inspect.isclass(cls):
            return cls
        # Also search sub-attributes one level deep (e.g. mod.strategies.X)
        for attr_name in dir(mod):
            attr = getattr(mod, attr_name, None)
            if attr is not None and inspect.ismodule(attr):
                cls = getattr(attr, name, None)
                if cls is not None and inspect.isclass(cls):
                    return cls
    return None


# ---------------------------------------------------------------------------
# Attempt imports
# ---------------------------------------------------------------------------

# Main processor / entry-point module
processor_module = _try_import(
    [
        "src.payment_processor",
        "src.processor",
        "src.main",
        "src.payments",
        "src",
        "payment_processor",
    ],
    target_attrs=["PaymentProcessor", "process_payment"],
)

# Strategy classes
strategies_module = _try_import(
    [
        "src.strategies",
        "src.strategies.credit_card",
        "src.payment_strategies",
        "src.strategy",
    ],
    target_attrs=["CreditCardStrategy", "PaymentStrategy"],
)

# Individual strategy modules (agents may split into separate files)
cc_module = _try_import(
    ["src.strategies.credit_card", "src.strategies.creditcard"],
    target_attrs=["CreditCardStrategy"],
)
paypal_module = _try_import(
    ["src.strategies.paypal"],
    target_attrs=["PayPalStrategy"],
)
bank_module = _try_import(
    ["src.strategies.bank_transfer", "src.strategies.bank"],
    target_attrs=["BankTransferStrategy"],
)
crypto_module = _try_import(
    ["src.strategies.crypto", "src.strategies.cryptocurrency"],
    target_attrs=["CryptoStrategy"],
)

# Validators / validation chain
validators_module = _try_import(
    [
        "src.validators",
        "src.validation",
        "src.validation_chain",
        "src.validator",
    ],
    target_attrs=["AmountValidator"],
)

# Collect all discovered modules for class lookups
ALL_MODULES = [
    m
    for m in [
        processor_module,
        strategies_module,
        cc_module,
        paypal_module,
        bank_module,
        crypto_module,
        validators_module,
    ]
    if m is not None
]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def dec():
    """Convenience wrapper around Decimal for concise test expressions."""
    return Decimal


@pytest.fixture
def processor_mod():
    """Return the imported processor module (or None)."""
    return processor_module


@pytest.fixture
def strategies_mod():
    """Return the imported strategies module (or None)."""
    return strategies_module


@pytest.fixture
def validators_mod():
    """Return the imported validators module (or None)."""
    return validators_module


@pytest.fixture
def find_cls():
    """Return a callable that searches all discovered modules for a class."""
    def _finder(name):
        return _find_class(name, ALL_MODULES)
    return _finder


@pytest.fixture
def credit_card_strategy(find_cls):
    """Return an instance of CreditCardStrategy if available."""
    cls = find_cls("CreditCardStrategy")
    if cls is None:
        pytest.skip("CreditCardStrategy not found")
    try:
        return cls()
    except TypeError:
        return cls


@pytest.fixture
def paypal_strategy(find_cls):
    """Return an instance of PayPalStrategy if available."""
    cls = find_cls("PayPalStrategy")
    if cls is None:
        pytest.skip("PayPalStrategy not found")
    try:
        return cls()
    except TypeError:
        return cls


@pytest.fixture
def bank_transfer_strategy(find_cls):
    """Return an instance of BankTransferStrategy if available."""
    cls = find_cls("BankTransferStrategy")
    if cls is None:
        pytest.skip("BankTransferStrategy not found")
    try:
        return cls()
    except TypeError:
        return cls


@pytest.fixture
def crypto_strategy(find_cls):
    """Return an instance of CryptoStrategy if available."""
    cls = find_cls("CryptoStrategy")
    if cls is None:
        pytest.skip("CryptoStrategy not found")
    try:
        return cls()
    except TypeError:
        return cls
