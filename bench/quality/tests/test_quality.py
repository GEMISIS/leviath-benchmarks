#!/usr/bin/env python3
"""Unit tests for the quality track's deterministic pieces.

Stdlib unittest only (the repo deliberately has no test framework
dependency). Run directly:

    python3 bench/quality/tests/test_quality.py
"""
from __future__ import annotations

import datetime as dt
import gzip
import json
import sys
import unittest
from pathlib import Path

QUALITY_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(QUALITY_DIR))

from core import assemble, cost, lvr, record, stats, subset  # noqa: E402

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

    def test_wrapper_uses_exact_enumeration_when_it_fits(self):
        r = stats.pass_rate_test([True] * 3, [False] * 3)
        self.assertEqual(r["method"], "exact_enumeration")
        self.assertAlmostEqual(r["p"], 0.05)
        self.assertIsNone(r["resamples"])

    def test_wrapper_declares_when_it_resamples(self):
        a, b = [True] * 30 + [False] * 6, [False] * 30 + [True] * 6
        r = stats.pass_rate_test(a, b, resamples=2000, seed=7)
        self.assertEqual(r["method"], "random_permutation")
        self.assertEqual(r["resamples"], 2000)
        self.assertEqual(r["seed"], 7)
        # (r+1)/(m+1) never reports a p below one resample's resolution.
        self.assertGreaterEqual(r["p"], 1 / 2001)
        self.assertEqual(r, stats.pass_rate_test(a, b, resamples=2000, seed=7))

    def test_resampled_p_is_near_the_exact_one(self):
        # A case small enough to enumerate, forced down both paths.
        a, b = [True, True, True, False], [False, False, False, True]
        exact = stats.permutation_exact(a, b)
        mc = stats._test(a, b, stats._pass_gap, stats.permutation_exact,
                         resamples=20000, seed=3)
        # _test picks exact here; drive the Monte-Carlo path directly.
        approx = stats._monte_carlo(a + b, len(a), stats._pass_gap,
                                    stats._pass_gap(a, b), 20000, 3)
        self.assertEqual(mc["method"], "exact_enumeration")
        self.assertAlmostEqual(exact, approx, delta=0.02)

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


# ─── run.lvr journal parsing + fold ─────────────────────────────────────


def _frame(rec: dict) -> bytes:
    payload = json.dumps(rec).encode()
    return len(payload).to_bytes(8, "big") + payload


def _archive(records: list[dict], version: int = 1) -> bytes:
    return b"LVR1" + version.to_bytes(2, "big") + b"".join(
        _frame(r) for r in records)


def _meta(**overrides) -> dict:
    meta = {"run_id": "r1", "status": "running", "current_stage": "work",
            "iteration": 0, "tool_calls": 0}
    meta.update(overrides)
    return meta


def _raw_entry(content: str, tokens: int = 1, kind: dict | None = None,
               **extra) -> dict:
    e = {"content": content, "tokens": tokens,
         "kind": kind or {"type": "Text"}, "taint": "Internal"}
    e.update(extra)
    return e


def _raw_region(name: str, entries: list[dict], kind: str = "clearable",
                max_tokens: int = 1000) -> dict:
    return {"name": name, "kind": kind,
            "current_tokens": sum(e["tokens"] for e in entries),
            "max_tokens": max_tokens, "entries": entries}


def _snapshot(regions: list[dict], stage: str = "work") -> dict:
    return {"stage_name": stage,
            "total_tokens": sum(r["current_tokens"] for r in regions),
            "max_tokens": 10_000, "regions": regions}


def _header(meta: dict | None = None) -> dict:
    return {"Header": {"identity": {"run_id": "r1", "machine_id": "m",
                                    "world_id": "w", "created_at": 1},
                       "meta": meta or _meta()}}


class LvrTests(unittest.TestCase):
    def test_framing_roundtrip(self):
        records = [_header(),
                   {"ContextCheckpoint": {
                       "snapshot": _snapshot(
                           [_raw_region("conv", [_raw_entry("hi")])]),
                       "at": 10}}]
        version, got, warnings = lvr.read_archive(_archive(records))
        self.assertEqual(version, 1)
        self.assertEqual(got, records)
        self.assertEqual(warnings, [])

    def test_gzipped_archive_is_sniffed_not_named(self):
        records = [_header(),
                   {"ContextCheckpoint": {
                       "snapshot": _snapshot(
                           [_raw_region("conv", [_raw_entry("hi")])]),
                       "at": 10}}]
        plain = lvr.fold(_archive(records))
        gz = lvr.fold(gzip.compress(_archive(records)))
        self.assertEqual(plain, gz)
        self.assertEqual(len(plain), 1)

    def test_truncated_tail_is_lenient(self):
        records = [_header(),
                   {"ContextCheckpoint": {
                       "snapshot": _snapshot(
                           [_raw_region("conv", [_raw_entry("hi")])]),
                       "at": 10}}]
        # A torn frame: a length prefix promising more than exists.
        torn = _archive(records) + (1000).to_bytes(8, "big") + b"partial"
        points = lvr.fold(torn)
        self.assertEqual(len(points), 1)
        # And a tear inside the length prefix itself.
        points = lvr.fold(_archive(records) + b"\x00\x00\x00")
        self.assertEqual(len(points), 1)

    def test_bad_magic_is_rejected(self):
        with self.assertRaises(ValueError):
            lvr.read_archive(b"not an archive at all")

    def test_unknown_variant_is_skipped_with_a_warning(self):
        records = [_header(),
                   {"SomeFutureRecord": {"at": 5}},
                   {"ContextCheckpoint": {
                       "snapshot": _snapshot(
                           [_raw_region("conv", [_raw_entry("hi")])]),
                       "at": 10}}]
        warnings: list[str] = []
        points = lvr.fold(_archive(records), warnings=warnings)
        self.assertEqual(len(points), 1)
        self.assertTrue(any("SomeFutureRecord" in w for w in warnings))

    def test_fold_applies_set_append_clear_remove(self):
        checkpoint = _snapshot([
            _raw_region("conv", [_raw_entry("hi")]),
            _raw_region("plan", [_raw_entry("p", 3)]),
        ])
        records = [
            _header(),
            {"ContextCheckpoint": {"snapshot": checkpoint, "at": 10}},
            {"ContextDiff": {"delta": {
                "stage_name": "work", "total_tokens": 7, "max_tokens": 10_000,
                "regions": [
                    {"Append": {"name": "conv",
                                "entries": [_raw_entry("there", 2)],
                                "current_tokens": 3}},
                    {"Set": _raw_region("fresh", [_raw_entry("f", 4)])},
                ]}, "at": 11}},
            {"ContextDiff": {"delta": {
                "stage_name": "work", "total_tokens": 4, "max_tokens": 10_000,
                "regions": [
                    {"Clear": {"name": "conv"}},
                    {"Remove": {"name": "plan"}},
                ]}, "at": 12}},
        ]
        points = lvr.fold(_archive(records))
        self.assertEqual(len(points), 3)
        self.assertEqual(list(points[0].regions), ["conv", "plan"])
        self.assertEqual(
            [e["content"] for e in points[1].regions["conv"]["entries"]],
            ["hi", "there"])
        self.assertEqual(list(points[1].regions), ["conv", "plan", "fresh"])
        self.assertEqual(points[1].regions["conv"]["current_tokens"], 3)
        self.assertEqual(list(points[2].regions), ["conv", "fresh"])
        self.assertEqual(points[2].regions["conv"]["entries"], [])
        self.assertEqual(points[2].regions["conv"]["current_tokens"], 0)
        # A Clear must not reach back into an already-yielded point.
        self.assertEqual(len(points[1].regions["conv"]["entries"]), 2)

    def test_fold_meta_and_status_updates(self):
        records = [
            _header(),
            {"ContextCheckpoint": {"snapshot": _snapshot(
                [_raw_region("conv", [_raw_entry("hi")])]), "at": 10}},
            {"StatusChanged": {"status": "complete", "at": 11}},
            {"Progress": {"meta": _meta(tool_calls=4, iteration=2),
                          "delta": {"stage_name": "work", "total_tokens": 1,
                                    "max_tokens": 10_000, "regions": []},
                          "at": 12}},
        ]
        points = lvr.fold(_archive(records))
        # StatusChanged updates the carried meta without adding a point.
        self.assertEqual(len(points), 2)
        self.assertEqual(points[0].meta["tool_calls"], 0)
        self.assertEqual(points[1].meta["status"], "running")
        self.assertEqual(points[1].meta["tool_calls"], 4)
        self.assertEqual(points[1].meta["current_stage"], "work")

    def test_no_header_means_no_points(self):
        records = [{"ContextCheckpoint": {"snapshot": _snapshot([]), "at": 1}}]
        self.assertEqual(lvr.fold(_archive(records)), [])
        self.assertEqual(lvr.fold(_archive([])), [])

    def test_typed_entry_kinds_convert(self):
        entries = [
            _raw_entry("q", kind={"type": "UserMessage"}),
            _raw_entry("a", kind={"type": "AssistantTurn", "tool_calls": [
                {"id": "c1", "name": "bash", "arguments": {"cmd": "ls"}}]}),
            _raw_entry("out", kind={"type": "ToolResult",
                                    "tool_call_id": "c1",
                                    "tool_name": "bash",
                                    "is_error": False}),
            {"content": "no kind field", "tokens": 1},
        ]
        got = [lvr.entry_dict(e) for e in entries]
        self.assertEqual([e["kind"] for e in got],
                         ["user_message", "assistant_turn", "tool_result",
                          "text"])
        self.assertEqual(got[1]["tool_calls"][0]["id"], "c1")
        self.assertEqual(got[2]["tool_call_id"], "c1")

    def test_point_at_depth(self):
        records = [_header()]
        for n, calls in enumerate([0, 3, 7]):
            records.append(
                {"Progress": {"meta": _meta(tool_calls=calls),
                              "delta": {"stage_name": "work",
                                        "total_tokens": 0,
                                        "max_tokens": 10_000, "regions": []},
                              "at": 100 + n}})
        points = lvr.fold(_archive(records))
        point, actual = lvr.point_at_depth(points, 2)
        self.assertEqual((point.at, actual), (101, 3))
        point, actual = lvr.point_at_depth(points, 0)
        self.assertEqual((point.at, actual), (100, 0))
        self.assertIsNone(lvr.point_at_depth(points, 8))


# ─── provider-request reconstruction ────────────────────────────────────


def _point(regions: dict) -> dict:
    return {"regions": regions}


def _entry(kind: str, content: str, **extra) -> dict:
    return {"kind": kind, "content": content, "tokens": 1, **extra}


def _region(kind: str, entries: list[dict]) -> dict:
    return {"kind": kind, "current_tokens": 0, "max_tokens": 1000,
            "entries": entries}


class AssembleTests(unittest.TestCase):
    def test_pinned_joins_without_label(self):
        out = assemble.assemble(_point({
            "task": _region("pinned", [_entry("text", "one"),
                                       _entry("text", "two")])}))
        self.assertEqual(out["system"][0],
                         {"text": "one\n\ntwo", "cache_hint": "always"})

    def test_labeled_block_formats(self):
        out = assemble.assemble(_point({
            "notes": _region("compacting", [_entry("text", "n1")]),
            "scratch": _region("clearable", [_entry("text", "s1")]),
            "tmp": _region("temporary", [_entry("text", "t1")]),
            "files": _region("hashmap", [
                _entry("text", "body", key="a.txt"),
                _entry("text", "keyless")]),
        }))
        texts = {b["text"]: b["cache_hint"] for b in out["system"]}
        self.assertEqual(texts["[notes]:\nn1"], "until_changed")
        self.assertEqual(texts["[scratch]:\ns1"], "never")
        self.assertEqual(texts["[tmp]:\nt1"], "never")
        self.assertEqual(texts["[files]:\n### [a.txt]\nbody\n\nkeyless"],
                         "until_changed")

    def test_tier_ordering_is_a_stable_sort(self):
        # Region vector order: never, until_changed, always, never -
        # sorted by tier with order preserved within a tier.
        out = assemble.assemble(_point({
            "t1": _region("temporary", [_entry("text", "a")]),
            "c": _region("compacting", [_entry("text", "b")]),
            "p": _region("pinned", [_entry("text", "d")]),
            "t2": _region("clearable", [_entry("text", "e")]),
        }))
        self.assertEqual([b["cache_hint"] for b in out["system"]],
                         ["always", "until_changed", "never", "never"])
        self.assertEqual([b["text"] for b in out["system"]],
                         ["d", "[c]:\nb", "[t1]:\na", "[t2]:\ne"])

    def test_consecutive_tool_results_merge_into_one_user_message(self):
        out = assemble.assemble(_point({"conv": _region("sliding", [
            _entry("user_message", "go"),
            _entry("assistant_turn", "running", tool_calls=[
                {"id": "c1", "name": "bash", "arguments": {"cmd": "ls"}},
                {"id": "c2", "name": "read", "arguments": {"path": "x"}}]),
            _entry("tool_result", "out1", tool_call_id="c1",
                   tool_name="bash", is_error=False),
            _entry("tool_result", "out2", tool_call_id="c2",
                   tool_name="read", is_error=True),
            _entry("assistant_turn", "done"),
        ])}))
        msgs = out["messages"]
        self.assertEqual([m["role"] for m in msgs],
                         ["user", "assistant", "user", "assistant", "user"])
        merged = msgs[2]["content"]
        self.assertEqual([b["type"] for b in merged],
                         ["tool_result", "tool_result"])
        self.assertEqual(merged[0]["tool_use_id"], "c1")
        self.assertTrue(merged[1]["is_error"])
        # The trailing assistant turn gets the Continue. nudge.
        self.assertEqual(msgs[4]["content"],
                         [{"type": "text", "text": "Continue."}])

    def test_assistant_turn_renders_tool_use_blocks(self):
        out = assemble.assemble(_point({"conv": _region("sliding_window", [
            _entry("assistant_turn", "thinking", tool_calls=[
                {"id": "c9", "name": "bash", "arguments": {"cmd": "pwd"}}]),
            _entry("tool_result", "/", tool_call_id="c9",
                   tool_name="bash", is_error=False),
        ])}))
        blocks = out["messages"][0]["content"]
        self.assertEqual(blocks[0], {"type": "text", "text": "thinking"})
        self.assertEqual(blocks[1]["type"], "tool_use")
        self.assertEqual(blocks[1]["id"], "c9")
        self.assertEqual(blocks[1]["name"], "bash")
        self.assertEqual(blocks[1]["input"], {"cmd": "pwd"})
        self.assertEqual(out["tool_names"], ["bash"])

    def test_text_entries_use_prefix_fallback(self):
        out = assemble.assemble(_point({"conv": _region("sliding", [
            _entry("text", "User: hello"),
            _entry("text", "Assistant: hi"),
            _entry("text", "no prefix at all"),
        ])}))
        msgs = out["messages"]
        self.assertEqual([m["role"] for m in msgs],
                         ["user", "assistant", "user"])
        self.assertEqual(msgs[0]["content"], [{"type": "text",
                                               "text": "hello"}])
        self.assertEqual(msgs[1]["content"], [{"type": "text", "text": "hi"}])
        self.assertEqual(msgs[2]["content"],
                         [{"type": "text", "text": "no prefix at all"}])

    def test_empty_regions_emit_nothing(self):
        out = assemble.assemble(_point({
            "empty_pin": _region("pinned", []),
            "empty_conv": _region("sliding", []),
            "task": _region("pinned", [_entry("text", "t")]),
        }))
        self.assertEqual(len(out["system"]), 1)
        # No user message anywhere -> the Begin. fallback.
        self.assertEqual(out["messages"],
                         [{"role": "user",
                           "content": [{"type": "text", "text": "Begin."}],
                           "cache_breakpoint": False}])

    def test_orphaned_tool_blocks_are_stripped(self):
        out = assemble.assemble(_point({"conv": _region("sliding", [
            _entry("user_message", "go"),
            _entry("assistant_turn", "", tool_calls=[
                {"id": "lost", "name": "bash", "arguments": {}}]),
        ])}))
        # The unanswered tool_use is stripped; its message, left empty,
        # is dropped, and the conversation ends on the user turn.
        self.assertEqual([m["role"] for m in out["messages"]], ["user"])
        self.assertEqual(out["tool_names"], [])

    def test_message_cache_breakpoint_placement(self):
        entries = [_entry("user_message", f"m{i}") for i in range(6)]
        out = assemble.assemble(_point({"conv": _region("sliding", entries)}))
        flags = [m["cache_breakpoint"] for m in out["messages"]]
        self.assertEqual(flags.index(True), len(flags) - 4)
        self.assertEqual(sum(flags), 1)

    def test_unsupported_kinds_raise(self):
        for kind in ("checklist", "custom", "who_knows"):
            with self.subTest(kind=kind):
                with self.assertRaises(ValueError):
                    assemble.assemble(_point({
                        "x": _region(kind, [_entry("text", "t")])}))


# ─── oracle: real archives vs their persisted context.json ─────────────


REPO_ROOT = QUALITY_DIR.parent.parent
REAL_RUN_DIRS = sorted(
    d for d in REPO_ROOT.glob("results/*/quality/*/runs/*.artifacts/run")
    if (d / "run.lvr.gz").exists() and (d / "context.json").exists())


@unittest.skipUnless(REAL_RUN_DIRS, "no archived runs under results/")
class LvrOracleTests(unittest.TestCase):
    """Folding a real run.lvr.gz to its final point must reproduce the
    run's persisted context.json.

    Two knowingly tolerated journal-vs-snapshot divergences (both are the
    Rust fold's own semantics, verified against the journals):

    - region ORDER: fold order is the first checkpoint's order, because
      apply_delta's Set overwrites a region in place and never reorders,
      while context.json is written in the live window's layout order
      (mixed-model arms rebuild the window per stage, reordering it);
    - max_tokens on a cleared region: diff_context emits Clear (name
      only) whenever a region was emptied, so a per-stage budget
      re-resolution happening on the same tick (percentage budgets
      against a different stage model) never reaches the journal.

    Everything else - region names, kinds, entry counts, entry contents,
    current_tokens, stage name - must match exactly, and at least one
    archive must match exactly in full (order and max_tokens included).
    """

    def test_final_fold_point_matches_context_json(self):
        strict_matches = 0
        for run_dir in REAL_RUN_DIRS:
            with self.subTest(run=str(run_dir)):
                warnings: list[str] = []
                points = lvr.fold(run_dir / "run.lvr.gz", warnings=warnings)
                self.assertTrue(points, "journal folded to no points")
                self.assertEqual(warnings, [])
                snap = json.loads((run_dir / "context.json").read_text())
                want = lvr.snapshot_regions(snap)
                got = points[-1].regions
                self.assertEqual(set(got), set(want), "region names differ")
                self.assertEqual(points[-1].stage_name, snap["stage_name"])
                for name in want:
                    g, w = got[name], want[name]
                    self.assertEqual(g["kind"], w["kind"], name)
                    self.assertEqual(len(g["entries"]), len(w["entries"]),
                                     f"{name}: entry count differs")
                    self.assertEqual(g["entries"], w["entries"],
                                     f"{name}: entry contents differ")
                    self.assertEqual(g["current_tokens"], w["current_tokens"],
                                     name)
                if got == want and list(got) == list(want):
                    strict_matches += 1
        self.assertGreaterEqual(
            strict_matches, 1,
            "no archive matched exactly (order + budgets included)")

    def test_point_at_depth_walks_a_real_run(self):
        points = lvr.fold(REAL_RUN_DIRS[0] / "run.lvr.gz")
        hit = lvr.point_at_depth(points, 1)
        if hit is not None:
            point, actual = hit
            self.assertGreaterEqual(actual, 1)
            self.assertGreaterEqual(point.meta["tool_calls"], 1)

    def test_real_final_point_assembles(self):
        # Not an equality oracle (requests are not journaled); asserts
        # the assembled shape is well-formed on real data.
        assembled = 0
        for run_dir in REAL_RUN_DIRS[:8]:
            points = lvr.fold(run_dir / "run.lvr.gz")
            try:
                out = assemble.assemble(points[-1])
            except ValueError:
                continue  # a checklist/custom region - out of scope
            assembled += 1
            self.assertTrue(out["system"] or out["messages"])
            hints = [b["cache_hint"] for b in out["system"]]
            self.assertEqual(
                hints,
                sorted(hints, key=lambda h: assemble._HINT_PRIORITY[h]))
            self.assertEqual(out["messages"][-1]["role"], "user")
        self.assertGreaterEqual(assembled, 1)


class RecordV2Tests(unittest.TestCase):
    BASE = {
        "schema": "quality-run-v2", "freeze_tag": "UNFROZEN-SMOKE",
        "suite": "crs", "task_id": "t", "arm": "flat-pinned",
        "model_label": "m", "model_policy": "anthropic/x", "rep": 1,
        "blueprint": {}, "lev": {}, "status": "complete",
        "started_utc": "", "ended_utc": "", "wall_clock_secs": 1.0,
        "usage": {}, "tool_calls": 3, "cost_usd": 0.1,
        "rates_sha256": "x", "score": {"passed": True},
    }

    def test_v1_and_v2_both_validate(self):
        record.validate(dict(self.BASE))
        record.validate(dict(self.BASE, schema="quality-run-v1"))
        with self.assertRaises(ValueError):
            record.validate(dict(self.BASE, schema="quality-run-v0"))

    def test_v2_blocks_are_shape_checked(self):
        rec = dict(self.BASE, validation={"passed": 1})
        with self.assertRaises(ValueError):
            record.validate(rec)
        rec["validation"] = {"passed": 1, "failed": 0, "errors": 0,
                             "total": 1, "suite_hash": "abc"}
        record.validate(rec)

    def test_reached_probe_needs_a_score(self):
        rec = dict(self.BASE, retention=[
            {"after_tool_calls": 15, "probe_type": "factual_recall",
             "reached": True}])
        with self.assertRaises(ValueError):
            record.validate(rec)
        rec["retention"][0]["score"] = 1.0
        record.validate(rec)
        rec["retention"].append({"after_tool_calls": 30,
                                 "probe_type": "cross_file",
                                 "reached": False})
        record.validate(rec)

    def test_retention_mean_reaches_aggregate(self):
        rec = dict(self.BASE, retention_summary={
            "mean_score": 0.75, "n_probes": 4, "n_reached": 4,
            "n_hallucinated": 0})
        cells = record.aggregate([rec])["cells"]
        self.assertIn("retention_mean_score", cells[0])


class EvaluatorTests(unittest.TestCase):
    def test_exact_match_short_circuits_without_a_model(self):
        from core import evaluator
        probe = {"question": "q", "expected": "e", "rubric": "r",
                 "exact": "Exit Code 3"}
        out = evaluator.grade_answer(
            probe, "the spec says exit code 3 here",
            grader_model_id="openai/x", keys={},
            transport=lambda *a: self.fail("model consulted"))
        self.assertEqual(out["method"], "exact")
        self.assertEqual(out["score"], 1.0)

    def test_model_grade_parses_fenced_json(self):
        from core import evaluator

        def transport(url, headers, payload):
            return {"choices": [{"message": {"content":
                    '```json\n{"grade": "hallucinated", "score": -0.5, '
                    '"reasoning": "made up"}\n```'}}],
                    "usage": {"prompt_tokens": 10,
                              "completion_tokens": 5}}
        out = evaluator.grade_answer(
            {"question": "q", "expected": "e", "rubric": "r"}, "a",
            grader_model_id="openai/gpt-x",
            keys={"OPENAI_API_KEY": "k"}, transport=transport)
        self.assertEqual(out["grade"], "hallucinated")
        self.assertTrue(out["hallucinated"])
        self.assertEqual(out["score"], 0.0)  # never negative on the curve

    def test_unusable_grader_output_is_a_grading_error(self):
        from core import evaluator
        out = evaluator.grade_answer(
            {"question": "q", "expected": "e", "rubric": "r"}, "a",
            grader_model_id="openai/gpt-x",
            keys={"OPENAI_API_KEY": "k"},
            transport=lambda *a: {"choices": [{"message":
                                  {"content": "no json here"}}],
                                  "usage": {}})
        self.assertEqual(out["method"], "grading_error")
        self.assertIsNone(out["score"])


class FootprintSuiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fp_dir = QUALITY_DIR / "suites" / "footprint"
        sys.path.insert(0, str(fp_dir))
        from suites.footprint.suite import Suite
        cls.suite = Suite()
        cls.tasks = cls.suite.load_tasks(None)

    def test_all_three_tasks_load(self):
        ids = {t["id"] for t in self.tasks}
        self.assertEqual(ids, {"snake-cpp", "log-search", "explain-repo"})
        families = {t["id"]: t["family"] for t in self.tasks}
        self.assertEqual(families["snake-cpp"], "coder")
        self.assertEqual(families["log-search"], "loganalyzer")
        self.assertEqual(families["explain-repo"], "researcher")

    def test_blueprint_mapping(self):
        task = next(t for t in self.tasks if t["family"] == "coder")
        cases = {
            ("flat", None): "flat-coder",
            ("flat", "compacting"): "flat-coder-compacting",
            ("structured", "adversarial-scoped-flagship"):
                "coder-bench-adversarial-scoped-flagship",
        }
        for (role, variant), expected in cases.items():
            got, _ = self.suite.agent_for_task(
                task, {"role": role, "variant": variant})
            self.assertEqual(got, expected)

    def test_grade_hoists_functional_and_footprint(self):
        verdict = self.suite.grade(self.tasks[0], {
            "functional_pass": False, "score": 0.5,
            "detail": {"points": 2, "of": 4},
            "request_footprint": {
                "n_requests": 3, "input_p50": 5000, "input_max": 9000,
                "input_growth": 1.4, "output_p50": 400,
                "requests": []}})
        self.assertFalse(verdict["passed"])
        self.assertEqual(
            verdict["record_fields"]["functional"]["score"], 0.5)
        self.assertEqual(
            verdict["record_fields"]["request_footprint"]["input_p50"],
            5000)

    def test_footprint_fold_on_real_archive(self):
        import glob
        from suites.footprint import footprint as fp_mod
        archives = glob.glob(str(
            QUALITY_DIR.parent.parent / "results" / "*" / "quality" / "*"
            / "runs" / "*.artifacts" / "run" / "run.lvr.gz"))
        if not archives:
            self.skipTest("no real archives on this machine")
        fp = fp_mod.from_archive(Path(archives[0]))
        if fp is None:
            self.skipTest("archive folded to no requests")
        self.assertGreater(fp["n_requests"], 0)
        self.assertGreaterEqual(fp["input_max"], fp["input_p50"])
        for req in fp["requests"]:
            self.assertGreaterEqual(req["input_tokens"], 0)

    def test_log_search_verifier_scores_partials(self):
        task = next(t for t in self.tasks if t["id"] == "log-search")
        sys.path.insert(0, str(task["dir"]))
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "ls_verify", task["dir"] / "verify.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        import json as _json
        key = _json.loads(
            (task["dir"] / "answers.json").read_text())["answers"]
        perfect = "\n".join(str(a) for a in key[:4])
        out = mod.verify(task["dir"], Path("."), Path("."), perfect)
        self.assertTrue(out["functional_pass"])
        self.assertEqual(out["score"], 1.0)
        wrong_root = "\n".join(["nope"] + [str(a) for a in key[1:4]])
        out2 = mod.verify(task["dir"], Path("."), Path("."), wrong_root)
        self.assertTrue(out2["functional_pass"])  # 3 of 4 still passes
        self.assertLess(out2["score"], 1.0)


class ProvidersTests(unittest.TestCase):
    def test_flatten_renders_tool_traffic_as_text(self):
        from core import providers
        msgs = [{"role": "assistant", "content": [
                    {"type": "text", "text": "doing"},
                    {"type": "tool_use", "id": "1", "name": "bash",
                     "input": {"cmd": "ls"}}]},
                {"role": "user", "content": [
                    {"type": "tool_result", "tool_call_id": "1",
                     "content": "files"}]}]
        flat = providers.flatten_messages(msgs)
        self.assertEqual([m["role"] for m in flat], ["assistant", "user"])
        self.assertIn("bash", flat[0]["content"])
        self.assertIn("files", flat[1]["content"])

    def test_openai_mapping_carries_tool_calls(self):
        from core import providers
        msgs = providers._to_openai_messages(
            [{"text": "sys", "cache_hint": "always"}],
            [{"role": "assistant", "content": [
                {"type": "tool_use", "id": "c1", "name": "bash",
                 "input": {}}]},
             {"role": "user", "content": [
                 {"type": "tool_result", "tool_use_id": "c1",
                  "content": "out"}]}])
        self.assertEqual(msgs[0]["role"], "system")
        self.assertEqual(msgs[1]["tool_calls"][0]["function"]["name"],
                         "bash")
        self.assertEqual(msgs[2]["role"], "tool")
        self.assertEqual(msgs[2]["tool_call_id"], "c1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
