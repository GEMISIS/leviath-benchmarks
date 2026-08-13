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

- `logs/<service>/app.log`, `app.log.1`, `app.log.2` — rotated
  application logs for nine services (`.2` is the oldest window, the
  bare file the newest; each file covers two hours, 00:00–06:00 total).
- `logs/edge-gateway/access.log{,.1,.2}` — the edge tier's access log,
  one line per request: `timestamp method path status latency request-id`.
- `changes/config-audit.log` — every configuration change pushed to any
  service that day, one line each, timestamped.

Work the incident end to end: find the customer-visible impact in the
edge access logs, trace it to the deepest failing service, identify the
configuration change that triggered it, establish how the failure
spread, quantify the impact, and identify the runbook step whose
mitigation matches this failure mode. Expect to examine every service's
logs — ruling services out is part of the job.

## Required report format

Your final report must be exactly six lines, in this order, with no
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

Line 5 counts every 5xx access-log line in that window, whatever its
cause. Any deviation from this six-line format makes the report
unusable.
