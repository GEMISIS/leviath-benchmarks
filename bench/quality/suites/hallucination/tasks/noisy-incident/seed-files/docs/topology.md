# Aurora Platform — Service Topology (rev 16)

Customer traffic enters at edge-gateway, which authenticates via
auth-service and fans out to cart-api, checkout-api, and search-api.
The only path from edge-gateway to payment-gateway runs through
checkout-api; edge-gateway never calls payment-gateway, cart-api's or
search-api's downstreams, inventory-service, order-service,
pricing-service, recommendation-api, session-cache, fraud-detector,
shipping-service, notification-service, or billing-worker directly.

| service | owner team | port | direct dependencies |
|---|---|---|---|
| edge-gateway | traffic-eng | 8080 | auth-service, cart-api, checkout-api, search-api |
| auth-service | identity | 8091 | session-cache |
| cart-api | storefront | 8095 | session-cache, pricing-service, inventory-service |
| checkout-api | storefront | 8100 | payment-gateway, inventory-service, order-service, session-cache |
| search-api | discovery | 8110 | inventory-service, recommendation-api |
| recommendation-api | discovery | 8115 | inventory-service |
| payment-gateway | payments-platform | 8120 | billing-worker, fraud-detector |
| inventory-service | supply-chain | 8130 | (none) |
| order-service | storefront | 8140 | notification-service, billing-worker, shipping-service |
| pricing-service | pricing-eng | 8145 | (none) |
| session-cache | platform-core | 8150 | (none) |
| fraud-detector | risk-eng | 8125 | (none) |
| shipping-service | fulfillment | 8155 | (none) |
| notification-service | comms | 8160 | (none) |
| billing-worker | payments-platform | 8170 | (none) |

Notes:

- A dependency edge means the left service issues synchronous RPCs to
  the right service on the request path. Failures propagate upward:
  when a service degrades, its direct callers log upstream errors
  first, and edge-gateway surfaces customer-visible 5xx last.
- notification-service handles asynchronous comms for order-service
  only; nothing on a customer request path waits on it.
- All configuration changes, for every service, are recorded centrally
  in changes/config-audit.log by the deploy tooling.
- Log rotation: app.log is the current file, app.log.1 the previous
  one-hour window, and so on back through app.log.11, the oldest
  retained window.
