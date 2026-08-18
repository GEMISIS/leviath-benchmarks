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
