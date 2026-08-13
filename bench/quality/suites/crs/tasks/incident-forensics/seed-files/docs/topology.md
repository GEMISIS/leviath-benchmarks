# Aurora Platform — Service Topology (rev 14)

Customer traffic enters at edge-gateway, which authenticates via
auth-service and fans out to checkout-api and search-api. The only
path from edge-gateway to payment-gateway runs through checkout-api;
edge-gateway never calls payment-gateway, inventory-service,
order-service, session-cache, notification-service, or billing-worker
directly.

| service | owner team | port | direct dependencies |
|---|---|---|---|
| edge-gateway | traffic-eng | 8080 | auth-service, checkout-api, search-api |
| auth-service | identity | 8091 | session-cache |
| checkout-api | storefront | 8100 | payment-gateway, inventory-service, order-service, session-cache |
| search-api | discovery | 8110 | inventory-service |
| payment-gateway | payments-platform | 8120 | billing-worker |
| inventory-service | supply-chain | 8130 | (none) |
| order-service | storefront | 8140 | notification-service, billing-worker |
| session-cache | platform-core | 8150 | (none) |
| notification-service | comms | 8160 | (none) |
| billing-worker | payments-platform | 8170 | (none) |

Notes:

- A dependency edge means the left service issues synchronous RPCs to
  the right service on the request path. Failures propagate upward:
  when a service degrades, its direct callers log upstream errors
  first, and edge-gateway surfaces customer-visible 5xx last.
- All configuration changes, for every service, are recorded centrally
  in changes/config-audit.log by the deploy tooling.
- Log rotation: app.log is the current file, app.log.1 the previous
  two-hour window, app.log.2 the one before that.
