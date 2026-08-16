# On-call runbook - slow orders (rev 2)

1. Confirm the symptom: place a few orders and read the reported
   `latency_ms` against the recent average in `/metrics`.
2. Check `/admin/workers`. A worker stuck retrying is the usual
   suspect when latency degrades across ALL order categories.
3. Known mitigation for restock retry storms: set `restock_backoff` to
   `exponential` via `PUT /config`. This backs the worker off and
   lets order latency recover while supply catches up.
4. Verify recovery with fresh orders and `/metrics` before closing
   the incident.
