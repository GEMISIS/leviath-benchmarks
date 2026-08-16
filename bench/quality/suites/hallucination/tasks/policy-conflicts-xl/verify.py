"""Functional verification for policy-conflicts-xl.

The base task's verifier, re-barred: twelve registered conflicts, the
pass bar at eight matched pairs. All scoring, classifier, and
format-tolerance logic is imported from the base module so the two
variants can never drift; only the bar differs (score already divides
by the registry's own conflict count, so it scales by itself).
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_BASE_DIR = Path(__file__).resolve().parent.parent / "policy-conflicts"
_spec = importlib.util.spec_from_file_location(
    "policy_conflicts_verify_base", _BASE_DIR / "verify.py")
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)

FUNCTIONAL_BAR = 8  # of 12 pairs
_base.FUNCTIONAL_BAR = FUNCTIONAL_BAR

verify = _base.verify
