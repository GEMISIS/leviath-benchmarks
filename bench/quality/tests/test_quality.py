#!/usr/bin/env python3
"""Unit tests for the quality track's deterministic pieces.

Stdlib unittest only (the repo deliberately has no test framework
dependency). Run directly:

    python3 bench/quality/tests/test_quality.py
"""
from __future__ import annotations

import datetime as dt
import json
import sys
import unittest
from pathlib import Path

QUALITY_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(QUALITY_DIR))

from core import cost, record, stats, subset  # noqa: E402

sys.path.insert(0, str(QUALITY_DIR / "suites" / "loganalysis"))
import verifier as log_verifier  # noqa: E402

sys.path.insert(0, str(QUALITY_DIR / "suites" / "dabstep"))
import scorer as dabstep_scorer  # noqa: E402

sys.path.insert(0, str(QUALITY_DIR / "suites" / "gaia"))
import scorer as gaia_scorer  # noqa: E402

ANTHROPIC_RATES = {
    "anthropic/x": {"input_per_mtok": 3.0, "output_per_mtok": 15.0,
                    "cache_read_per_mtok": 0.3, "cache_write_per_mtok": 3.75,
                    "prompt_includes_cache_read": False},
    "openai/x": {"input_per_mtok": 2.0, "output_per_mtok": 8.0,
                 "cache_read_per_mtok": 0.5, "cache_write_per_mtok": 0.0,
                 "prompt_includes_cache_read": True},
}


class CostTests(unittest.TestCase):
    def test_anthropic_semantics_prompt_excludes_cache(self):
        # prompt_tokens is the raw input_tokens field, which excludes
        # cache reads and writes; billing adds all four components.
        usage = {"prompt_tokens": 1000, "completion_tokens": 100,
                 "cached_tokens": 5000, "cache_write_tokens": 200}
        expected = (1000 * 3.0 + 5000 * 0.3 + 200 * 3.75 + 100 * 15.0) / 1e6
        self.assertAlmostEqual(
            cost.cost_usd(usage, "anthropic/x", ANTHROPIC_RATES), expected)
        self.assertEqual(cost.billed_tokens(usage, False), 6300)

    def test_openai_semantics_prompt_includes_cache(self):
        # The cached portion sits inside prompt_tokens and is re-priced
        # at the discounted rate, never double-charged.
        usage = {"prompt_tokens": 1000, "completion_tokens": 50,
                 "cached_tokens": 600, "cache_write_tokens": 0}
        expected = (400 * 2.0 + 600 * 0.5 + 50 * 8.0) / 1e6
        self.assertAlmostEqual(
            cost.cost_usd(usage, "openai/x", ANTHROPIC_RATES), expected)
        self.assertEqual(cost.billed_tokens(usage, True), 1050)

    def test_placeholder_rates_are_never_a_price(self):
        rates = {"m": {"input_per_mtok": 0.0, "output_per_mtok": 0.0,
                       "cache_read_per_mtok": 0.0,
                       "cache_write_per_mtok": 0.0,
                       "prompt_includes_cache_read": False}}
        self.assertFalse(cost.is_pinned(rates, "m"))
        self.assertFalse(cost.is_pinned(rates, "absent"))

    def test_unknown_model_raises(self):
        with self.assertRaises(KeyError):
            cost.cost_usd({}, "nope", ANTHROPIC_RATES)


class StatsTests(unittest.TestCase):
    def test_fully_separated_samples(self):
        # 3v3 fully separated: exactly 1 of C(6,3)=20 assignments is as
        # extreme, so the exact one-sided p is 0.05 for both tests.
        self.assertAlmostEqual(
            stats.mann_whitney_exact([1, 2, 3], [4, 5, 6]), 1 / 20)
        self.assertAlmostEqual(
            stats.permutation_exact([True] * 3, [False] * 3), 1 / 20)

    def test_identical_samples_are_not_significant(self):
        self.assertGreaterEqual(
            stats.mann_whitney_exact([1, 2], [1, 2]), 0.5)

    def test_enumeration_never_silently_approximates(self):
        with self.assertRaises(ValueError):
            stats.mann_whitney_exact(list(range(20)), list(range(20)))


class SubsetTests(unittest.TestCase):
    def test_selection_is_deterministic_and_sorted(self):
        ids = [f"t{i}" for i in range(50)]
        a = subset.select(7, 10, ids)
        b = subset.select(7, 10, ids)
        self.assertEqual(a, b)
        self.assertEqual(a, sorted(a))

    def test_exclusions_must_be_declared(self):
        ids = ["a", "b", "c"]
        picked = subset.select(1, 2, ids, excluded={"b": "image broken"})
        self.assertNotIn("b", picked)


class RecordTests(unittest.TestCase):
    def test_missing_keys_are_rejected(self):
        with self.assertRaises(ValueError):
            record.validate({"schema": record.SCHEMA})

    def test_filename_is_filesystem_safe(self):
        name = record.record_filename("t/1", "arm", "Claude Opus 5", 2)
        self.assertNotIn("/", name.replace(".json", ""))
        self.assertNotIn(" ", name)


class LogVerifierTests(unittest.TestCase):
    def test_integer_normalization(self):
        for text in ("226", " 226 ", "1,204", "Final answer: 226",
                     "The count is explained above.\n226"):
            got = log_verifier.normalize(text)
            self.assertIn(got, ("226", "1204"))

    def test_public_and_wrong_answers(self):
        task = {"id": "x", "answer": 42}
        self.assertTrue(log_verifier.check(task, "42")["passed"])
        self.assertFalse(log_verifier.check(task, "41")["passed"])


class DabstepScorerTests(unittest.TestCase):
    def test_published_answer_shapes(self):
        s = dabstep_scorer.question_scorer
        self.assertTrue(s("NL", "NL"))
        self.assertTrue(s("B. BE", "B. BE"))
        self.assertTrue(s("1,234.57", "1234.57"))
        self.assertTrue(s("not applicable", "Not Applicable"))
        self.assertFalse(s("BE", "NL"))
        self.assertFalse(s("1234.57", "1235.57"))


class GaiaScorerTests(unittest.TestCase):
    def test_numbers_lists_and_strings(self):
        s = gaia_scorer.question_scorer
        self.assertTrue(s("3", "3"))
        self.assertTrue(s("$1,234", "1234"))
        self.assertTrue(s("right, left", "right, left"))
        self.assertFalse(s("right, left, up", "right, left"))
        self.assertTrue(s("Paris", "paris"))
        self.assertFalse(s("Lyon", "paris"))


class RosterTests(unittest.TestCase):
    """The roster and the price list must not drift apart.

    A roster model with no pinned rate would be priced as free (or
    crash mid-round); a rate with no roster model is a stale price a
    reader would take for a model we ran.
    """

    def setUp(self):
        self.arms = json.loads((QUALITY_DIR / "arms.json").read_text())
        self.rates = cost.load_rates(QUALITY_DIR / "rates.json")
        self.real = {name: m["id"]
                     for name, m in self.arms["models"].items()
                     if m["tier"] != "smoke"}

    def test_every_roster_model_has_pinned_rates(self):
        for name, model_id in self.real.items():
            with self.subTest(model=name):
                self.assertTrue(cost.is_pinned(self.rates, model_id),
                                f"{name} ({model_id}) has no pinned rate")

    def test_no_rates_for_models_outside_the_roster(self):
        priced = {k for k in self.rates if not k.startswith("_")}
        self.assertEqual(priced - set(self.real.values()), set())

    def test_release_dates_parse_and_are_not_in_the_future(self):
        # Recency itself is judged at round time (run_quality.py records
        # each model's age in round.json); a test cannot assert it
        # without breaking every re-run of an older freeze tag.
        today = dt.date.today()
        for name, m in self.arms["models"].items():
            if m["tier"] == "smoke":
                continue
            with self.subTest(model=name):
                released = dt.date.fromisoformat(m["released"])
                self.assertLessEqual(released, today)

    def test_every_tier_is_declared(self):
        for name, m in self.arms["models"].items():
            with self.subTest(model=name):
                self.assertIn(m["tier"], self.arms["tiers"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
