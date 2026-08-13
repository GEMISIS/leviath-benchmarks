#!/usr/bin/env python3
"""Generate the records-reconciliation corpus.

Eighteen monthly transaction files, a master ledger mirroring them, an
account registry, and a fee schedule. The generator injects an exact
set of discrepancies - duplicated transaction ids, fees computed at the
wrong tier, transactions against unregistered accounts, and exactly one
one-cent rounding-policy violation - among otherwise clean records, and
computes the answer key from what it injected. A self-test then
re-audits the emitted files from scratch (rates re-parsed out of the
emitted fee-schedule markdown, not taken from the constants), so the
corpus provably supports the key.

Hard constraints:

- Determinism: pure function of --seed; byte-identical re-runs
  (--check verifies against the committed copy). All money arithmetic
  is integer cents - floats never touch an amount.
- Stable reference docs: reference/fee-schedule.md and
  reference/ledger-format.md are constants, independent of the seed;
  probes.json quotes facts from them.
- Category separation must be provable, not probable: misapplied fees
  are asserted to differ from the correct fee by at least two cents,
  and the rounding violation by exactly one, so the classification
  rule stated to the auditor ("one cent off = rounding") can never be
  ambiguous.

Usage:
    python3 generate.py [--seed N] [--out DIR] [--check]
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import tempfile
from pathlib import Path

DEFAULT_SEED = 2207

MONTHS = [f"2024-{m:02d}" for m in range(7, 13)] + \
         [f"2025-{m:02d}" for m in range(1, 13)]

TIERS = ["standard", "plus", "enterprise"]
TYPES = ["payment", "refund", "transfer"]

# (basis points on gross, fixed cents). Refunds are flat fees (0 bp).
# Must stay in exact agreement with the fee-schedule table below; the
# self-test re-parses the table rather than trusting this dict.
FEES = {
    ("standard", "payment"): (290, 30),
    ("standard", "refund"): (0, 25),
    ("standard", "transfer"): (80, 10),
    ("plus", "payment"): (240, 25),
    ("plus", "refund"): (0, 25),
    ("plus", "transfer"): (60, 10),
    ("enterprise", "payment"): (190, 20),
    ("enterprise", "refund"): (0, 20),
    ("enterprise", "transfer"): (40, 5),
}

FEE_SCHEDULE_MD = """\
# Fee Schedule — Meridian Payments (effective 2024-07-01)

All amounts are USD with exactly two decimal places. Percentage fees
are computed on the gross amount and rounded half away from zero to
the nearest cent; the fixed component is added after rounding. An
account's tier comes from reference/account-registry.csv and applies
to every transaction on that account.

| Tier | Payment | Refund | Transfer |
|---|---|---|---|
| standard | 2.9% + $0.30 | flat $0.25 | 0.8% + $0.10 |
| plus | 2.4% + $0.25 | flat $0.25 | 0.6% + $0.10 |
| enterprise | 1.9% + $0.20 | flat $0.20 | 0.4% + $0.05 |

Worked example: a standard-tier payment of $100.00 carries a fee of
$100.00 x 2.9% = $2.90, plus $0.30 fixed = $3.20; net $96.80.

Rounding half away from zero means $0.435 becomes $0.44, never $0.43.
Rounding half down is a policy violation even when the result is only
one cent off.
"""

LEDGER_FORMAT_MD = """\
# Ledger and File Formats — Meridian Payments (rev 3)

All amounts are USD, two decimal places, no thousands separators, no
currency symbol. Fee rounding follows the fee schedule: half away from
zero, to the nearest cent.

## Monthly transaction files (transactions/YYYY-MM.csv)

Columns: `txn_id,date,account_id,type,gross_amount,fee_amount,net_amount`.
One row per transaction; `net_amount = gross_amount - fee_amount`.
A `txn_id` must appear exactly once across ALL monthly files combined;
a repeated id means the same transaction was posted twice.

## Master ledger (ledger/master-ledger.csv)

Columns: `txn_id,account_id,net_amount,source_file`. The monthly close
job appends one posting per transaction row, walking the monthly files
in calendar order and each file top to bottom. The ledger is a mirror:
it adds no information, but its running total is what the books report,
so every bad transaction row is also a bad posting.

## Account registry (reference/account-registry.csv)

Columns: `account_id,name,tier,status,opened`. The registry is the
sole source of an account's fee tier. A transaction whose account_id
is absent from the registry cannot be priced or settled and must be
escalated, whatever its stated fee.
"""

FIRST_WORDS = ["Northwind", "Cascade", "Harbor", "Summit", "Aurora",
               "Pinnacle", "Redwood", "Lakeside", "Ironclad", "Bluebird",
               "Granite", "Silverline", "Copperleaf", "Bright", "Orchard",
               "Falcon", "Juniper", "Beacon", "Crescent", "Marble"]
SECOND_WORDS = ["Trading", "Logistics", "Outfitters", "Analytics",
                "Foods", "Media", "Robotics", "Textiles", "Supply",
                "Studios", "Freight", "Labs", "Goods", "Works",
                "Systems"]
SUFFIXES = ["LLC", "Inc", "Co", "Group", "Ltd"]


def money(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{cents // 100}.{cents % 100:02d}"


def fee_cents(gross: int, bp: int, fixed: int) -> int:
    """Half away from zero on the percentage part; gross is cents."""
    q, r = divmod(gross * bp, 10000)
    return q + (1 if r * 2 >= 10000 else 0) + fixed


# ---------------------------------------------------------------------
# Corpus construction
# ---------------------------------------------------------------------


def build(seed: int) -> tuple[dict[str, str], list[str]]:
    rng = random.Random(seed)

    # --- registry ----------------------------------------------------
    accounts: dict[str, str] = {}  # id -> tier
    registry_rows = []
    used_names: set[str] = set()
    for i in range(40):
        acct = f"ACC-{1001 + i}"
        while True:
            name = (f"{rng.choice(FIRST_WORDS)} "
                    f"{rng.choice(SECOND_WORDS)} {rng.choice(SUFFIXES)}")
            if name not in used_names:
                used_names.add(name)
                break
        tier = rng.choices(TIERS, weights=[5, 3, 2], k=1)[0]
        status = "closed" if rng.random() < 0.1 else "active"
        opened = (f"{rng.randrange(2019, 2024)}-"
                  f"{rng.randrange(1, 13):02d}-{rng.randrange(1, 29):02d}")
        accounts[acct] = tier
        registry_rows.append(f"{acct},{name},{tier},{status},{opened}")
    account_ids = sorted(accounts)
    standard_accounts = [a for a in account_ids
                         if accounts[a] == "standard"]

    # --- clean transactions -----------------------------------------
    used_ids: set[int] = set()

    def new_txn_id() -> str:
        while True:
            n = rng.randrange(10 ** 6, 10 ** 7)
            if n not in used_ids:
                used_ids.add(n)
                return f"TXN-{n}"

    def make_row(month_i: int, acct: str, tier: str) -> dict:
        typ = rng.choices(TYPES, weights=[7, 1, 2], k=1)[0]
        if typ == "payment":
            gross = rng.randrange(500, 250001)
        elif typ == "transfer":
            gross = rng.randrange(1000, 500001)
        else:
            gross = rng.randrange(300, 40001)
        bp, fixed = FEES[(tier, typ)]
        fee = fee_cents(gross, bp, fixed)
        return {"id": new_txn_id(), "month": month_i,
                "date": f"{MONTHS[month_i]}-{rng.randrange(1, 29):02d}",
                "acct": acct, "type": typ, "gross": gross, "fee": fee}

    txns: list[dict] = []
    for month_i in range(len(MONTHS)):
        for _ in range(rng.randrange(60, 86)):
            acct = rng.choice(account_ids)
            txns.append(make_row(month_i, acct, accounts[acct]))

    # --- inject discrepancies ---------------------------------------
    # Misapplied fees: reprice at a wrong tier. Restricting to
    # non-refund rows with gross >= $20 guarantees the wrong-tier fee
    # differs by >= 2 cents, keeping the category unconfusable with
    # the one-cent rounding violation.
    eligible = [t for t in txns if t["type"] != "refund"
                and t["gross"] >= 2000]
    n_fee = rng.randrange(4, 8)
    fee_wrong = rng.sample(eligible, n_fee)
    for t in fee_wrong:
        correct = t["fee"]
        wrong_tier = rng.choice([x for x in TIERS
                                 if x != accounts[t["acct"]]])
        bp, fixed = FEES[(wrong_tier, t["type"])]
        t["fee"] = fee_cents(t["gross"], bp, fixed)
        assert abs(t["fee"] - correct) >= 2, "fee delta too small"

    # Rounding violation: a standard-tier payment whose percentage fee
    # lands exactly on a half cent (gross = k*1000+500 cents makes
    # gross*290 = ...5000), charged the rounded-half-down value.
    r_gross = rng.randrange(2, 200) * 1000 + 500
    assert (r_gross * 290) % 10000 == 5000
    r_acct = rng.choice(standard_accounts)
    rounding_txn = {"id": new_txn_id(),
                    "month": (mi := rng.randrange(len(MONTHS))),
                    "date": f"{MONTHS[mi]}-{rng.randrange(1, 29):02d}",
                    "acct": r_acct, "type": "payment", "gross": r_gross,
                    "fee": fee_cents(r_gross, 290, 30) - 1}
    for tier in TIERS:
        bp, fixed = FEES[(tier, "payment")]
        assert rounding_txn["fee"] != fee_cents(r_gross, bp, fixed), \
            "half-down fee collides with a real tier's fee"
    txns.append(rounding_txn)

    # Orphaned accounts: valid-looking ids the registry never issued.
    n_orph = rng.randrange(2, 6)
    orphans = []
    orphan_ids = rng.sample(range(9700, 9800), n_orph)
    for oid in orphan_ids:
        mi = rng.randrange(len(MONTHS))
        t = {"id": new_txn_id(), "month": mi,
             "date": f"{MONTHS[mi]}-{rng.randrange(1, 29):02d}",
             "acct": f"ACC-{oid}", "type": "payment",
             "gross": rng.randrange(5000, 400001), "fee": 0}
        t["fee"] = fee_cents(t["gross"], *FEES[("standard", "payment")])
        orphans.append(t)
        txns.append(t)

    # Duplicates: an exact re-post of a clean row into a later month.
    tainted = {t["id"] for t in fee_wrong} | {rounding_txn["id"]} | \
        {t["id"] for t in orphans}
    dup_eligible = [t for t in txns if t["id"] not in tainted
                    and t["month"] < len(MONTHS) - 2]
    n_dup = rng.randrange(3, 7)
    dup_sources = rng.sample(dup_eligible, n_dup)
    duplicates = []
    for src in dup_sources:
        copy = dict(src)
        copy["month"] = rng.randrange(src["month"] + 1, len(MONTHS))
        duplicates.append(copy)
        txns.append(copy)

    # --- render files -----------------------------------------------
    header = "txn_id,date,account_id,type,gross_amount,fee_amount,net_amount"
    by_month: dict[int, list[dict]] = {i: [] for i in range(len(MONTHS))}
    for t in txns:
        by_month[t["month"]].append(t)
    corpus: dict[str, str] = {
        "reference/fee-schedule.md": FEE_SCHEDULE_MD,
        "reference/ledger-format.md": LEDGER_FORMAT_MD,
        "reference/account-registry.csv":
            "account_id,name,tier,status,opened\n"
            + "\n".join(registry_rows) + "\n",
    }
    ledger_rows = []
    for mi, month in enumerate(MONTHS):
        rows = sorted(by_month[mi], key=lambda t: (t["date"], t["id"]))
        lines = [header]
        for t in rows:
            net = t["gross"] - t["fee"]
            lines.append(f"{t['id']},{t['date']},{t['acct']},{t['type']},"
                         f"{money(t['gross'])},{money(t['fee'])},"
                         f"{money(net)}")
            ledger_rows.append(f"{t['id']},{t['acct']},{money(net)},"
                               f"transactions/{month}.csv")
        corpus[f"transactions/{month}.csv"] = "\n".join(lines) + "\n"
    corpus["ledger/master-ledger.csv"] = \
        "txn_id,account_id,net_amount,source_file\n" \
        + "\n".join(ledger_rows) + "\n"

    # --- answers from the injected ground truth ---------------------
    impacts: list[tuple[int, str]] = []
    correction = 0
    for src in dup_sources:
        net = src["gross"] - src["fee"]
        impacts.append((net, src["id"]))
        correction -= net
    for t in fee_wrong:
        bp, fixed = FEES[(accounts[t["acct"]], t["type"])]
        correct = fee_cents(t["gross"], bp, fixed)
        impacts.append((abs(t["fee"] - correct), t["id"]))
        correction += t["fee"] - correct
    for t in orphans:
        net = t["gross"] - t["fee"]
        impacts.append((net, t["id"]))
        correction -= net
    impacts.append((1, rounding_txn["id"]))
    correction -= 1

    ranked = sorted(impacts, key=lambda x: (-x[0], x[1]))
    assert ranked[2][0] > ranked[3][0], \
        "top-3 impact ranking is ambiguous for this seed"
    top3 = ",".join(sorted(txn_id for _, txn_id in ranked[:3]))
    answers = [str(n_dup), str(n_fee), str(n_orph), "1", top3,
               money(correction)]
    return corpus, answers


# ---------------------------------------------------------------------
# Self-test: independent audit of the emitted corpus.
# ---------------------------------------------------------------------

_RATE_CELL = re.compile(r"^(\d+(?:\.\d+)?)% \+ \$(\d+)\.(\d{2})$")
_FLAT_CELL = re.compile(r"^flat \$(\d+)\.(\d{2})$")


def _parse_schedule(md: str) -> dict[tuple[str, str], tuple[int, int]]:
    """Rates from the emitted markdown table, not from the constants."""
    rates: dict[tuple[str, str], tuple[int, int]] = {}
    for line in md.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 4 or cells[0] not in TIERS:
            continue
        for typ, cell in zip(TYPES, cells[1:]):
            m = _RATE_CELL.match(cell)
            if m:
                bp = round(float(m.group(1)) * 100)
                fixed = int(m.group(2)) * 100 + int(m.group(3))
            else:
                f = _FLAT_CELL.match(cell)
                if not f:
                    raise SystemExit(f"unparseable fee cell: {cell!r}")
                bp, fixed = 0, int(f.group(1)) * 100 + int(f.group(2))
            rates[(cells[0], typ)] = (bp, fixed)
    if len(rates) != 9:
        raise SystemExit("fee schedule table did not parse")
    return rates


def _cents(text: str) -> int:
    sign = -1 if text.startswith("-") else 1
    whole, frac = text.lstrip("-").split(".")
    return sign * (int(whole) * 100 + int(frac))


def derive_answers(corpus: dict[str, str]) -> list[str]:
    rates = _parse_schedule(corpus["reference/fee-schedule.md"])
    registry = {}
    for line in corpus["reference/account-registry.csv"] \
            .splitlines()[1:]:
        acct, _, tier, _, _ = line.split(",")
        registry[acct] = tier

    rows = []
    for path in sorted(corpus):
        if not path.startswith("transactions/"):
            continue
        for line in corpus[path].splitlines()[1:]:
            txn_id, date, acct, typ, gross, fee, net = line.split(",")
            rows.append({"id": txn_id, "acct": acct, "type": typ,
                         "gross": _cents(gross), "fee": _cents(fee),
                         "net": _cents(net)})

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["id"]] = counts.get(r["id"], 0) + 1
    dup_ids = sorted(i for i, c in counts.items() if c > 1)

    impacts: list[tuple[int, str]] = []
    correction = 0
    seen: set[str] = set()
    for r in rows:
        if r["id"] in dup_ids:
            if r["id"] not in seen:
                seen.add(r["id"])
                extra = counts[r["id"]] - 1
                impacts.append((r["net"], r["id"]))
                correction -= extra * r["net"]
            continue
        if r["acct"] not in registry:
            impacts.append((r["net"], r["id"]))
            correction -= r["net"]
            continue
        bp, fixed = rates[(registry[r["acct"]], r["type"])]
        correct = fee_cents(r["gross"], bp, fixed)
        delta = r["fee"] - correct
        if delta == 0:
            continue
        impacts.append((abs(delta), r["id"]))
        correction += delta
    n_fee = sum(1 for r in rows if r["id"] not in dup_ids
                and r["acct"] in registry
                and abs(r["fee"] - fee_cents(
                    r["gross"], *rates[(registry[r["acct"]],
                                        r["type"])])) >= 2)
    n_round = sum(1 for r in rows if r["id"] not in dup_ids
                  and r["acct"] in registry
                  and abs(r["fee"] - fee_cents(
                      r["gross"], *rates[(registry[r["acct"]],
                                          r["type"])])) == 1)
    n_orph = sum(1 for r in rows if r["acct"] not in registry)

    ranked = sorted(impacts, key=lambda x: (-x[0], x[1]))
    top3 = ",".join(sorted(txn_id for _, txn_id in ranked[:3]))
    return [str(len(dup_ids)), str(n_fee), str(n_orph), str(n_round),
            top3, money(correction)]


def self_test(corpus: dict[str, str], answers: list[str]) -> None:
    derived = derive_answers(corpus)
    if derived != answers:
        for i, (d, a) in enumerate(zip(derived, answers)):
            if d != a:
                print(f"  answer {i + 1}: derived {d!r} != key {a!r}",
                      file=sys.stderr)
        raise SystemExit("self-test FAILED: corpus does not support "
                         "the answer key")


# ---------------------------------------------------------------------
# Output + --check
# ---------------------------------------------------------------------


def write_out(out_dir: Path, corpus: dict[str, str],
              answers: list[str], seed: int) -> None:
    for rel, text in sorted(corpus.items()):
        path = out_dir / "seed-files" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
    (out_dir / "answers.json").write_bytes(json.dumps(
        {"seed": seed, "answers": answers},
        indent=2).encode("utf-8") + b"\n")


def _tree(root: Path) -> dict[str, bytes]:
    return {str(p.relative_to(root)): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def run_check(task_dir: Path, seed: int) -> int:
    corpus, answers = build(seed)
    self_test(corpus, answers)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        write_out(tmp_dir, corpus, answers, seed)
        fresh = _tree(tmp_dir)
    committed = {k: v for k, v in _tree(task_dir).items()
                 if k == "answers.json" or k.startswith("seed-files/")}
    problems = []
    for rel in sorted(set(fresh) | set(committed)):
        if rel not in committed:
            problems.append(f"missing from committed corpus: {rel}")
        elif rel not in fresh:
            problems.append(f"stale committed file: {rel}")
        elif fresh[rel] != committed[rel]:
            problems.append(f"byte mismatch: {rel}")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        print(f"check FAILED for seed {seed}", file=sys.stderr)
        return 1
    print(f"check OK: {len(fresh)} files byte-identical for seed {seed}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out",
                        default=str(Path(__file__).resolve().parent))
    parser.add_argument("--check", action="store_true",
                        help="regenerate into a temp dir and diff "
                             "against the committed corpus")
    args = parser.parse_args()
    task_dir = Path(args.out)
    if args.check:
        return run_check(task_dir, args.seed)
    corpus, answers = build(args.seed)
    self_test(corpus, answers)
    write_out(task_dir, corpus, answers, args.seed)
    total = sum(len(t.encode()) for t in corpus.values())
    lines = sum(t.count("\n") for t in corpus.values())
    print(f"seed {args.seed}: {len(corpus)} files, {lines} lines, "
          f"{total / 1024:.0f} KiB")
    print(f"  duplicates={answers[0]} misapplied_fees={answers[1]} "
          f"orphans={answers[2]} rounding={answers[3]}")
    print(f"  top3={answers[4]} correction={answers[5]}")
    print("self-test OK: all answers re-derived from the emitted corpus")
    return 0


if __name__ == "__main__":
    sys.exit(main())
