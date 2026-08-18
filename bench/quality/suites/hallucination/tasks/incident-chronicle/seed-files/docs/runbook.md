# On-Call Runbook — Customer-Facing Error Spike (rev 7)

Follow the steps in order. Do not skip step 4: most spikes of this
shape are change-induced.

1. Acknowledge the page within 5 minutes; open an incident channel
   (#inc-<date>) and assign an incident commander.
2. Pull the edge-gateway error-rate dashboard and confirm the
   customer-facing impact window (first and last 5xx).
3. Sample distributed traces from edge-gateway downward to identify
   the deepest failing service — the first service in the call chain
   whose errors are not caused by one of its own dependencies.
4. Check changes/config-audit.log: freeze all deploys, then identify
   every configuration change in the 60 minutes preceding symptom
   onset for the failing service.
5. If connection-pool exhaustion is confirmed (pool utilization at
   1.00, permits at 0), apply the emergency pool override
   (pool.emergency_max=200) and roll back the offending change.
6. If client timeout budgets were reduced, restore the previous timeout
   values from the audit log and roll back the offending change.
7. If cache heap eviction is confirmed (heap-limit eviction lines in
   the cache tier's log, hit rate degrading), raise the heap ceiling
   back to its previous value from the audit log (cache.heap_limit_mb)
   and roll back the offending change.
8. If the edge error rate has not halved within 20 minutes of
   mitigation, escalate to sev-1 and page the on-call director.
9. Write the post-incident timeline within 24 hours and attach the
   relevant audit-log entries and the incident channel transcript.
