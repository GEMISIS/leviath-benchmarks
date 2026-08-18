# Order Service - API notes (rev 4)

The service listens on the port written to `service/port.txt` after
startup. All bodies are JSON. It keeps a runtime log in
`service/service.log`.

| endpoint | verbs | notes |
|---|---|---|
| /health | GET | liveness + logical tick |
| /orders | POST, GET | place an order {"item", "qty"} (qty 1..3); GET lists recent |
| /inventory | GET | current stock per item |
| /config | GET, PUT | live keys; PUT rejects unknown keys and lists valid ones |
| /metrics | GET | sliding window over the last 20 ticks only |
| /admin/workers | GET | background worker status |
| /admin/state | GET | full state dump (diagnostics) |
| /admin/shutdown | POST | stop the service |

Every handled request advances the service's logical clock by one
tick. `/metrics` reports ONLY the trailing 20-tick window - history
you did not observe is history you no longer have.
