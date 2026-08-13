# Task: Build a Log Analyzer CLI Tool

Create a command-line tool for analyzing structured log files with multiple commands and rich output formatting.

## Requirements

1. **Commands**:
   - `logviz parse <file>` - Parse and validate log file format
   - `logviz stats <file>` - Display statistics (count by level, time range, top errors)
   - `logviz filter <file> --level=<LEVEL> --since=<TIME>` - Filter logs by criteria
   - `logviz export <file> --format=<json|csv>` - Export to different formats
   - `logviz tail <file> --follow` - Real-time log tailing (like tail -f)

2. **Configuration**:
   - Support config file at `~/.logviz/config.yaml` (see `config-example.yaml`)
   - Config specifies: default output format, color scheme, date format
   - CLI flags override config values

3. **Input Format**:
   - Parse the log format specified in `log-format.md`
   - Handle malformed lines gracefully (report but don't crash)

4. **Output Requirements**:
   - Match the example outputs in `expected-output/` directory exactly
   - Use color output when TTY is detected (colors defined in config)
   - Support --no-color flag

5. **Error Handling**:
   - Validate file exists and is readable
   - Provide helpful error messages matching examples in `error-examples.txt`
   - Exit codes: 0 = success, 1 = usage error, 2 = file error, 3 = parse error

6. **Performance**:
   - Must handle files up to 1GB
   - Use streaming for large files (don't load entire file into memory)

## Constraints

- Use only standard library (no external dependencies)
- Support Python 3.9+
- All times should be in UTC unless config specifies otherwise

## Deliverables

- Complete CLI implementation in `logviz/` directory
- Unit tests in `tests/` directory
- README with installation and usage examples
