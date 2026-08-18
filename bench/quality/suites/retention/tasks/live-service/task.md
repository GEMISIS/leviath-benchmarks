# On-call escalation: intermittent slow orders

Customers report that placing orders is intermittently slow. You have
the service checkout in this directory: its code and seed under
`service/`, API notes in `docs/api.md`, and the on-call runbook in
`docs/runbook.md`.

Start the service yourself:

    python3 service/srv.py &

It writes its port to `service/port.txt` and its runtime log to
`service/service.log`. Interact with it over HTTP (curl or python).
The symptom only shows under load - you will need to place orders,
watch `/inventory` and `/metrics` between them, and correlate what
you see over time. `/metrics` only covers a trailing window, so
observations you do not record are observations you lose.

Diagnose the incident end to end, apply and VERIFY a mitigation, and
before you finish: save a full state dump to the working directory
(`curl .../admin/state > state.json`), then stop the service
(`POST /admin/shutdown`).

Report EXACTLY these six numbered lines and nothing else:

1. The root-cause request path and category, formatted exactly:
   `/orders category=<category>`
2. The item id whose stock is being drained as a side effect (the
   item, not the category).
3. The metric name, exactly as `/metrics` spells it, that exposes the
   background-worker symptom.
4. The mitigation that worked, formatted `<config-key>=<value>` with
   the key exactly as the LIVE service accepts it.
5. The runbook discrepancy, formatted exactly:
   `runbook says <key>, actual <key>`
6. The total orders processed during your diagnosis, per the
   service's own count (an integer).

A wrong line is worse when it names something that does not exist:
report only what you verified against the running service.
