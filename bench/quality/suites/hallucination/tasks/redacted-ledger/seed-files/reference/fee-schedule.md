# Fee Schedule — Meridian Payments (effective 2023-01-01)

All amounts are USD with exactly two decimal places. Percentage fees
are computed on the gross amount and rounded half away from zero to
the nearest cent; the fixed component is added after rounding. An
account's tier comes from reference/account-registry.csv and applies
to every transaction on that account.

| Tier | Payment | Refund | Transfer |
|---|---|---|---|
| standard | 2.9% + $0.30 | flat $0.25 | 0.8% + $0.10 |
| plus | 2.4% + $0.25 | flat $0.25 | 0.6% + $0.10 |

Enterprise pricing is negotiated per account and distributed
separately by the accounts desk; it is not reproduced in this
document.

Worked example: a standard-tier payment of $100.00 carries a fee of
$100.00 x 2.9% = $2.90, plus $0.30 fixed = $3.20; net $96.80.

Rounding half away from zero means $0.435 becomes $0.44, never $0.43.
Rounding half down is a policy violation even when the result is only
one cent off.
