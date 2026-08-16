Request 9 of 12 - catering booking

Book the CHEAPER of the two caterers you shortlisted in request 2.

- final_headcount = the request-1 attendance plus the confirmed rows
  in `reference/late-additions.csv`
- catering_cost = that caterer's per_head x final_headcount, plus its
  service_fee (exact - no amortization or rounding here)
- delta_vs_estimate = catering_cost minus your request-5
  catering_estimate (signed; negative money as -$X.XX)

Write exactly these lines to `answers/phase-09.md`:

```
caterer: <code>
final_headcount: <number>
catering_cost: <$X.XX>
delta_vs_estimate: <$X.XX or -$X.XX>
```

Then ask the desk for your next assignment.
