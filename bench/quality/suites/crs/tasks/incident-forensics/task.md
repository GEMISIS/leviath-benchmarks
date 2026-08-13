# Task: Root-Cause Forensics — Aurora Platform, 2026-03-14

You are the forensics engineer for the Aurora commerce platform. During
the early hours of 2026-03-14 (UTC) customers saw elevated errors. The
complete log capture, the central change audit trail, and the platform
reference documents are in this directory. Reconstruct what happened.

## Read the reference documents first, in full

- `docs/topology.md` — the service call graph, owner teams, and log
  rotation scheme. Every conclusion about failure propagation must be
  consistent with this document.
- `docs/runbook.md` — the on-call procedure for customer-facing error
  spikes.
- `config/alert-thresholds.yaml` — the alerting thresholds per service.

You will need details from all three throughout the investigation; read
them completely before opening any log file.

## The evidence

- `logs/<service>/app.log`, `app.log.1` … `app.log.5` — rotated
  application logs for fourteen services (`.5` is the oldest window,
  the bare file the newest; each file covers two hours, 00:00–12:00
  total).
- `logs/edge-gateway/access.log{,.1,...,.5}` — the edge tier's access
  log, one line per request:
  `timestamp method path status latency request-id`.
- `changes/config-audit.log` — every configuration change pushed to any
  service that day, one line each, timestamped.

Work the incident end to end: find the customer-visible impact in the
edge access logs, trace it to the deepest failing service, identify the
configuration change that triggered it, establish how the failure
spread, quantify the impact, and identify the runbook step whose
mitigation matches this failure mode. The review board also requires a
per-service impact assessment for the incident window, an attestation
of which services stayed clean, and a summary of the platform's
background warning noise — so examining every service's logs is part
of the job, not optional diligence.

## Required report format

Your final report must be exactly nine lines, in this order, with no
headings, numbering, or commentary around them:

1. The root-cause service name, exactly as spelled in `docs/topology.md`.
2. The configuration key of the triggering change, exactly as spelled
   in `changes/config-audit.log`.
3. T0 — the timestamp of that triggering change, copied exactly from
   `changes/config-audit.log` (format `2026-03-14THH:MM:SSZ`).
4. The propagation order: the root-cause service first, then every
   service that subsequently logged upstream failures caused by it,
   ordered by the timestamp of each service's first such error, ending
   with `edge-gateway`. Comma-separated, no spaces.
5. The number of requests in the edge-gateway access logs with status
   500–599 and timestamp at or after T0 and strictly before
   T0 + 15 minutes. A bare integer.
6. The runbook step number whose mitigation matches this failure mode.
   A bare integer.
7. Per-service impact assessment: how many error-level lines each of
   the fifteen services logged in the same window as line 5 (at or
   after T0, strictly before T0 + 15 minutes). Counting rule: a line
   in an application log is error-level exactly when the token
   immediately after its timestamp is `ERROR`; count across all six
   rotated files of that service's `app.log`. For edge-gateway, whose
   access log has no level field, count its access-log lines with
   status 500–599 in the window instead (the same rule as line 5).
   One line, all fifteen services in the exact order the table in
   `docs/topology.md` lists them, each formatted `service=count`,
   comma-separated, no spaces.
8. Clean-services attestation: the services whose line-7 count is
   zero, sorted alphabetically, comma-separated, no spaces — or the
   literal word `none` if every service logged at least one
   error-level line in the window.
9. Background-noise summary: the application service that logged the
   most `WARN`-level lines across the entire 00:00–12:00 capture (all
   six rotated files, every WARN line regardless of cause;
   edge-gateway is excluded because its access log carries no level).
   Formatted `service=count`. If two services tie for the most, give
   the alphabetically first.

Line 5 counts every 5xx access-log line in that window, whatever its
cause; line 7 likewise counts every error-level line in the window,
incident-related or not. Any deviation from this nine-line format
makes the report unusable.
