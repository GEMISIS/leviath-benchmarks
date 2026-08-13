# Task: Ledger Reconciliation — Meridian Payments, FY2024-H2/FY2025

You are the reconciliation analyst for Meridian Payments. The books
for July 2024 through December 2025 must be certified, and the raw
records contain errors. Find every discrepancy, classify it, and
compute the correction the ledger needs.

## Read the reference documents first, in full

- `reference/fee-schedule.md` — the fee rates per account tier and
  transaction type, and the rounding policy. Every fee judgment below
  is defined by this document.
- `reference/ledger-format.md` — the file formats, the posting
  pipeline, and the transaction-id uniqueness policy.
- `reference/account-registry.csv` — the sole source of each account's
  fee tier and status.

Read all three completely before opening any transaction file; the
audit rules come from them and you will need them throughout.

## The records

- `transactions/2024-07.csv` … `transactions/2025-12.csv` — eighteen
  monthly transaction files.
- `ledger/master-ledger.csv` — one posting per transaction row, in
  file order, as described in the format document.

## Classification rules

Audit every transaction row in every monthly file:

- **Duplicate**: a `txn_id` that appears more than once across all
  monthly files combined. Count each such id once, however many times
  it appears.
- **Orphaned account**: a row whose `account_id` is absent from the
  registry. These rows are counted here and nowhere else — with no
  registry tier, their stated fee is not judged.
- **Misapplied fee**: a registered, non-duplicate row whose
  `fee_amount` differs from the schedule fee for its account's tier by
  $0.02 or more.
- **Rounding violation**: a registered, non-duplicate row whose
  `fee_amount` differs from the schedule fee by exactly $0.01.

Every discrepant transaction falls in exactly one category.

## Discrepancy amounts (for ranking)

- Duplicate: the `net_amount` of the duplicated transaction.
- Orphaned account: the row's `net_amount`.
- Misapplied fee: the absolute difference between charged and schedule
  fee.
- Rounding violation: the absolute difference ($0.01).

## Net ledger correction

The signed amount, in dollars, by which the master ledger's total
`net_amount` changes once the books are fixed: each duplicate's extra
posting is removed, each orphaned row's posting is removed, and each
fee error's posting is restated with the schedule fee
(`net = gross - schedule fee`).

## Required report format

Your final report must be exactly six lines, in this order, with no
headings, labels, or commentary around them:

1. Number of duplicate transaction ids. A bare integer.
2. Number of misapplied-fee transactions. A bare integer.
3. Number of orphaned-account transactions. A bare integer.
4. Number of rounding violations. A bare integer.
5. The transaction ids of the three discrepancies with the largest
   discrepancy amounts (ties broken by smaller txn_id first), listed
   in ascending id order, comma-separated, no spaces.
6. The net ledger correction in dollars to exactly two decimal places,
   with a leading minus sign if negative, no currency symbol, no
   thousands separators (e.g. `-12345.67`).

Any deviation from this six-line format makes the report unusable.
