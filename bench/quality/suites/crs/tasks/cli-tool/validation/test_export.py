"""Tests for the ``logviz export`` command."""

import csv
import io
import json


# ------------------------------------------------------------------ #
# test_export_json_format
# ------------------------------------------------------------------ #
def test_export_json_format(cli, sample_log_file):
    """Exporting with --format=json should produce valid JSON."""
    result = cli("export", sample_log_file, "--format=json")
    assert result.returncode == 0, f"stderr: {result.stderr}"
    # Should be parseable as JSON (array or object).
    data = json.loads(result.stdout)
    assert isinstance(data, (list, dict)), "Expected JSON array or object"


# ------------------------------------------------------------------ #
# test_export_json_contains_fields
# ------------------------------------------------------------------ #
def test_export_json_contains_fields(cli, sample_log_file):
    """Each JSON entry should contain timestamp, level, component, message."""
    result = cli("export", sample_log_file, "--format=json")
    data = json.loads(result.stdout)
    entries = data if isinstance(data, list) else data.get("entries", data.get("logs", []))
    assert len(entries) > 0, "Expected at least one entry"
    first = entries[0]
    for field in ("timestamp", "level", "component", "message"):
        # Accept minor variations in field names (e.g. "msg" for "message").
        matching = [k for k in first if field in k.lower()]
        assert matching, f"Expected field containing '{field}' in JSON entry, got keys: {list(first.keys())}"


# ------------------------------------------------------------------ #
# test_export_csv_format
# ------------------------------------------------------------------ #
def test_export_csv_format(cli, sample_log_file):
    """Exporting with --format=csv should produce valid CSV."""
    result = cli("export", sample_log_file, "--format=csv")
    assert result.returncode == 0, f"stderr: {result.stderr}"
    reader = csv.reader(io.StringIO(result.stdout))
    rows = list(reader)
    # Header + at least one data row
    assert len(rows) >= 2, f"Expected header + data rows, got {len(rows)} rows"


# ------------------------------------------------------------------ #
# test_export_csv_has_header
# ------------------------------------------------------------------ #
def test_export_csv_has_header(cli, sample_log_file):
    """CSV output should have a header row with expected column names."""
    result = cli("export", sample_log_file, "--format=csv")
    reader = csv.reader(io.StringIO(result.stdout))
    header = next(reader)
    header_lower = [h.lower() for h in header]
    for expected in ("timestamp", "level", "component", "message"):
        matching = [h for h in header_lower if expected in h]
        assert matching, f"Expected header column containing '{expected}', got: {header}"


# ------------------------------------------------------------------ #
# test_export_default_format
# ------------------------------------------------------------------ #
def test_export_default_format(cli, sample_log_file):
    """Exporting without an explicit --format should default to JSON."""
    result = cli("export", sample_log_file)
    assert result.returncode == 0, f"stderr: {result.stderr}"
    # Attempt to parse as JSON; should succeed.
    data = json.loads(result.stdout)
    assert isinstance(data, (list, dict)), "Default export should produce valid JSON"


# ------------------------------------------------------------------ #
# test_export_json_entry_count
# ------------------------------------------------------------------ #
def test_export_json_entry_count(cli, sample_log_file):
    """JSON export should contain one entry per valid log line (15)."""
    result = cli("export", sample_log_file, "--format=json")
    data = json.loads(result.stdout)
    entries = data if isinstance(data, list) else data.get("entries", data.get("logs", []))
    assert len(entries) == 15, f"Expected 15 entries, got {len(entries)}"
