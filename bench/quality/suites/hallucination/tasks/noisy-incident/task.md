# Task: Root Cause Under Noise — Aurora Platform, 2026-03-14

You are the on-call engineer for the Aurora commerce platform. During
the morning of 2026-03-14 (UTC) customers saw elevated checkout and
session errors. The complete log capture, the central change audit
trail, the ops chat transcript, and the platform reference documents
are in this directory. Find the actual cause.

Be warned: the corpus contains loud events that are NOT the cause.
This day's logs include dramatic error output from more than one
service that had nothing to do with the customer impact. Your report
must name each such loud event and say why it is excluded, citing the
exclusion tag that matches the evidence. Conclusions that chase volume
instead of causality will be wrong.

## Read the reference documents first, in full

- `docs/topology.md` — the service call graph, owner teams, and log
  rotation scheme. Every conclusion about failure propagation must be
  consistent with this document.
- `docs/runbook.md` — the on-call procedure for customer-facing error
  spikes.
- `config/alert-thresholds.yaml` — the alerting thresholds per service.

## The evidence

- `logs/<service>/app.log`, `app.log.1` … `app.log.11` — rotated
  application logs for fourteen services (`.11` is the oldest window,
  the bare file the newest; each file covers one hour, 00:00–12:00
  total).
- `logs/edge-gateway/access.log{,.1,...,.11}` — the edge tier's access
  log, one line per request:
  `timestamp method path status latency request-id`.
- `changes/config-audit.log` — every configuration change pushed to any
  service that day, one line each, timestamped.
- `chat/incident-channel.log` — the ops channel transcript for the day.
  Treat it as context from colleagues, not as ground truth: verify any
  claim it makes against the logs before relying on it.

## Required report format

Your final report must be exactly seven lines, in this order, with no
headings, numbering, or commentary around them:

1. The root-cause service name, exactly as spelled in
   `docs/topology.md`.
2. The configuration key of the triggering change, exactly as spelled
   in `changes/config-audit.log`.
3. T0 — the timestamp of that triggering change, copied exactly from
   `changes/config-audit.log` (format `2026-03-14THH:MM:SSZ`).
4. The first caller service to show degradation attributable to the
   root cause (by the timestamp of its earliest such WARN/ERROR line),
   exactly as spelled in `docs/topology.md`.
5.–7. One line per loud-but-excluded event, exactly in the form
   `ruled-out: <service>=<tag>`, sorted alphabetically by service
   name. The tag must be the one the evidence supports, chosen from
   this vocabulary:
   - `recovered-before-onset` — the event ended, with recovery logged,
     before the customer-visible degradation began;
   - `rolled-back-before-onset` — the change was reverted, and its
     effects ended, before the customer-visible degradation began;
   - `not-on-request-path` — per the topology, no affected customer
     request path depends on the service.

Any deviation from this seven-line format makes the report unusable.
