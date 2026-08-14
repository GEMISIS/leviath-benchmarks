# Task: Post-Incident Review — Aurora Platform, 2026-03-14

You are writing the consolidated post-incident review for the Aurora
commerce platform. On 2026-03-14 (UTC, 00:00–12:00) the platform had
THREE separate production incidents. The complete log capture, the
central change audit trail, the ops incident-channel transcript, and
the platform reference documents are all in this directory.
Reconstruct all three incidents and answer the review questions.

## Read the reference documents first, in full

- `docs/topology.md` — the service call graph, owner teams, and log
  rotation scheme. Every conclusion about failure propagation must be
  consistent with this document.
- `docs/runbook.md` — the on-call procedure for customer-facing error
  spikes, including the prescribed mitigation for each failure mode.
- `docs/platform-defaults.md` — Aurora's operating conventions. Where
  this platform diverges from common defaults, this document is the
  authority; several review questions are answerable only from it.
- `config/alert-thresholds.yaml` — alerting thresholds per service.

You will need details from all of these throughout; read them
completely before opening any log file.

## The evidence

- `logs/<service>/app.log`, `app.log.1` … `app.log.5` — rotated
  application logs for fourteen services (`.5` is the oldest window,
  the bare file the newest; each file covers two hours, 00:00–12:00
  total).
- `logs/edge-gateway/access.log{,.1,...,.5}` — the edge tier's access
  log, one line per request:
  `timestamp method path status latency request-id`.
- `changes/config-audit.log` — every configuration change pushed to
  any service that day, one line each, timestamped.
- `chat/incident-channel.log` — the ops incident channel for the day
  (`timestamp @handle: message`). Who ran each incident and what
  mitigation was actually applied is established here and nowhere
  else.

## Definitions the report depends on

- The incidents are numbered INC-1, INC-2, INC-3 in order of their
  triggering change's timestamp (T0), earliest first.
- An incident's T0 is the timestamp of the configuration change that
  triggered it, exactly as recorded in `changes/config-audit.log`.
- An incident's customer-impact count is the number of edge-gateway
  access-log lines with a 5xx status in the window from its T0 up to
  but not including T0 + 15 minutes.
- An incident's propagation chain is: the root-cause service first,
  then every service that subsequently logged upstream failures caused
  by it, ordered by each service's first such error, ending with
  `edge-gateway`.

## Required report format

Exactly 17 numbered lines, `N. value`, one fact per line, no headings
and no commentary. Spellings exactly as they appear in the source
files; comma-separated lists carry no spaces.

1. INC-1 root-cause service
2. INC-1 triggering configuration key
3. INC-1 T0 (format `2026-03-14THH:MM:SSZ`)
4. INC-2 root-cause service
5. INC-2 triggering configuration key
6. INC-2 T0
7. INC-3 root-cause service
8. INC-3 triggering configuration key
9. INC-3 T0
10. The three incident numbers ordered by customer-impact count,
    largest first (e.g. `2,1,3`)
11. Every service that appears in more than one of the three
    propagation chains, alphabetical, comma-separated (or `none`)
12. Total customer-impact count summed across the three incidents
13. The incident commanders for INC-1, INC-2, INC-3 in that order,
    comma-separated handles without the `@` (from the channel
    transcript)
14. The one incident whose applied mitigation deviated from what the
    runbook prescribes, as `INC-<n>:<key>=<value-actually-applied>`
15. The port session-cache serves its wire protocol on
16. The SSH port of the ops bastion
17. The platform-standard HTTP retry budget, in attempts

Any deviation from this 17-line format makes the report unusable.
