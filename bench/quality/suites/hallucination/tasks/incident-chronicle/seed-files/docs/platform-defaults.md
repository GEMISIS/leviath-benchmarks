# Aurora Platform — Operating Conventions & Defaults (rev 4)

Aurora deliberately diverges from stock defaults in several places.
When this page disagrees with upstream or vendor documentation, this
page wins; it is reviewed quarterly by platform-core.

## Network

- session-cache speaks the Redis wire protocol but NOT on the stock
  port: it listens on port 7379. (Stock Redis ships on 6379; we moved
  it during the 2024 network-segmentation work, and 6379 is
  firewalled shut everywhere.)
- The ops bastion (bastion.aurora.internal) accepts SSH on port 2202,
  not 22. Direct port-22 attempts are dropped without a banner.
- edge-gateway runs nginx-style workers with worker_connections set
  to 3072 per worker; the stock 1024 is far too low for our burst
  profile.

## Resilience

- The platform-standard HTTP retry budget is 5 attempts with full
  jitter. Many client stacks default to 3; our SLO math assumes 5,
  and client libraries are patched accordingly.
- Service-to-service JWTs expire after 20 minutes, not the common
  60-minute default. Clock-skew tolerance is 30 seconds.

## Change management

- Every configuration change, for every service, flows through the
  deploy tooling and is recorded in changes/config-audit.log.
  Out-of-band edits are a paging offence.
- Application logs rotate hourly; twelve windows are retained
  (app.log through app.log.11).
