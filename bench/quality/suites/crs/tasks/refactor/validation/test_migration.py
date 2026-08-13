"""Tests that verify the migration script and backward compatibility."""

import importlib
import os
import sys

import pytest

TASK_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


# ---------------------------------------------------------------------------
# 1. migrate.py file exists
# ---------------------------------------------------------------------------

def test_migrate_script_exists():
    """A migration script (migrate.py) must exist at the project root."""
    candidates = [
        os.path.join(TASK_ROOT, "migrate.py"),
        os.path.join(TASK_ROOT, "migration.py"),
        os.path.join(TASK_ROOT, "src", "migrate.py"),
    ]
    found = any(os.path.isfile(p) for p in candidates)
    assert found, (
        f"migrate.py not found in any expected location: {candidates}"
    )


# ---------------------------------------------------------------------------
# 2. migrate.py is importable
# ---------------------------------------------------------------------------

def test_migrate_script_importable():
    """The migration script must be importable as a Python module."""
    imported = False
    for mod_name in ("migrate", "migration", "src.migrate"):
        try:
            importlib.import_module(mod_name)
            imported = True
            break
        except (ImportError, ModuleNotFoundError):
            continue

    # Fallback: try direct file import
    if not imported:
        migrate_path = os.path.join(TASK_ROOT, "migrate.py")
        if os.path.isfile(migrate_path):
            import importlib.util
            spec = importlib.util.spec_from_file_location("migrate", migrate_path)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(mod)
                    imported = True
                except Exception:
                    pass

    assert imported, "migrate.py must be importable without errors"


# ---------------------------------------------------------------------------
# 3. Backward compatibility – old API calls still work
# ---------------------------------------------------------------------------

def test_backward_compatibility(processor_mod, find_cls):
    """The refactored system must still expose the legacy API entry points."""
    has_api = False

    # Check for process_payment function or PaymentProcessor class
    if processor_mod is not None:
        if hasattr(processor_mod, "process_payment"):
            has_api = True
        if hasattr(processor_mod, "PaymentProcessor"):
            pp_cls = processor_mod.PaymentProcessor
            if hasattr(pp_cls, "process_payment"):
                has_api = True

    pp_cls = find_cls("PaymentProcessor")
    if pp_cls is not None and hasattr(pp_cls, "process_payment"):
        has_api = True

    assert has_api, (
        "Legacy API must remain accessible after migration "
        "(PaymentProcessor.process_payment or module-level process_payment)"
    )


# ---------------------------------------------------------------------------
# 4. All four payment methods are supported
# ---------------------------------------------------------------------------

def test_payment_methods_supported(find_cls):
    """All four payment method strategies must be available."""
    required = {
        "CreditCardStrategy": False,
        "PayPalStrategy": False,
        "BankTransferStrategy": False,
        "CryptoStrategy": False,
    }

    for name in required:
        cls = find_cls(name)
        if cls is not None:
            required[name] = True

    missing = [name for name, found in required.items() if not found]
    assert not missing, (
        f"Missing payment method strategies: {', '.join(missing)}"
    )
