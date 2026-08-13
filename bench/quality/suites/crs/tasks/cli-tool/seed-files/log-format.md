# Log Format Specification

Each log line follows this format:

```
<timestamp> <level> <component> <message> [<metadata>]
```

## Fields

- **timestamp**: ISO 8601 format with milliseconds - `2024-01-15T10:30:45.123Z`
- **level**: One of: `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`
- **component**: Alphanumeric string identifying the component (e.g., `http-server`, `database`, `auth`)
- **message**: Free-form text message (may contain spaces)
- **metadata** (optional): JSON object with additional fields - `{"user_id": 123, "ip": "1.2.3.4"}`

## Examples

```
2024-01-15T10:30:45.123Z INFO http-server Request received {"method": "GET", "path": "/api/users"}
2024-01-15T10:30:45.456Z ERROR database Connection failed {"host": "db.example.com", "error": "timeout"}
2024-01-15T10:30:46.789Z WARN auth Invalid token {"user_id": 456}
```

## Malformed Lines

Lines that don't match this format should be:
1. Logged to stderr with line number
2. Skipped in processing
3. Counted in stats as "malformed"
