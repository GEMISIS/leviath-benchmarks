# Meridian Summit 2026 - Operations Desk

You are running the operations desk for the Meridian Summit 2026
conference. All planning material lives in this workspace:
`reference/` (venue, catering, speaker, hotel, transport, sponsor,
insurance, budget and constraint files) and `registrations/` (eight
registration batch files). Read `reference/constraints.md` and
`reference/policies.md` before anything else - they govern every
request.

## How this session works

The desk will hand you one request at a time. For every request:

1. Do the work using the reference files and, where a request says so,
   your OWN results from earlier requests in this session.
2. Write the deliverable to `answers/phase-NN.md` (NN = the request
   number, zero-padded: phase-01.md, phase-02.md, ...) containing
   EXACTLY the lines the request specifies - no extra prose, no
   headers, one `key: value` per line. Money is always `$X.XX` (or
   `-$X.XX` when negative), with no thousands separators.
3. Then ask the desk for your next assignment (use the ask tool). Do
   not invent follow-on work, and never skip the ask - the next
   request only arrives when you ask for it.

When a request refers to an earlier decision ("the caterer you
shortlisted", "the remainder you computed"), it means your result from
this session. Keep track of what you decide and compute - later
requests will need those exact values.

## Request 1 of 12 - attendance baseline and venue

From the eight files under `registrations/` (and ONLY those files):
count confirmed attendance (rows with status `confirmed`), and count
how many of those confirmed attendees need dietary accommodation
(dietary value other than `none`).

Then pick the venue from `reference/venues.md`: the venue with the
LOWEST daily_rate whose capacity is at least attendance plus a 10%
buffer (buffer = 10% of attendance, rounded up to a whole person).

Write exactly these lines to `answers/phase-01.md`:

```
attendance: <number>
dietary: <number>
venue: <venue code>
venue_daily_rate: <$X.XX>
```

Then ask the desk for your next assignment.
