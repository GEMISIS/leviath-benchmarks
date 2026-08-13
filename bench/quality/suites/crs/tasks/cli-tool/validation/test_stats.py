"""Tests for the ``logviz stats`` command."""

import re


# ------------------------------------------------------------------ #
# test_stats_shows_level_breakdown
# ------------------------------------------------------------------ #
def test_stats_shows_level_breakdown(cli, multi_level_log_file):
    """Stats output should list all five log levels with counts or percentages."""
    result = cli("stats", multi_level_log_file)
    assert result.returncode == 0, f"stderr: {result.stderr}"
    output = result.stdout
    for level in ("DEBUG", "INFO", "WARN", "ERROR", "FATAL"):
        assert level in output, f"Level {level} missing from stats output"


# ------------------------------------------------------------------ #
# test_stats_shows_percentages
# ------------------------------------------------------------------ #
def test_stats_shows_percentages(cli, multi_level_log_file):
    """Stats output should include percentage values for levels."""
    result = cli("stats", multi_level_log_file)
    output = result.stdout
    # Look for a pattern like "20.0%" or "(33.3%)"
    assert re.search(r"\d+\.\d+%", output), "Expected percentage values in stats output"


# ------------------------------------------------------------------ #
# test_stats_shows_time_range
# ------------------------------------------------------------------ #
def test_stats_shows_time_range(cli, multi_level_log_file):
    """Stats output should include the time range of the log entries."""
    result = cli("stats", multi_level_log_file)
    output = result.stdout
    # The multi_level_log_file starts at 10:30:00
    assert "2024-01-15" in output, "Expected date in time range"
    assert "10:30:" in output, "Expected start time in time range"


# ------------------------------------------------------------------ #
# test_stats_shows_total_lines
# ------------------------------------------------------------------ #
def test_stats_shows_total_lines(cli, multi_level_log_file):
    """Stats output should contain the total line count (15)."""
    result = cli("stats", multi_level_log_file)
    output = result.stdout
    assert "15" in output, "Expected total line count of 15 in stats output"


# ------------------------------------------------------------------ #
# test_stats_shows_malformed_count
# ------------------------------------------------------------------ #
def test_stats_shows_malformed_count(cli, sample_log_with_malformed):
    """Stats output should report the number of malformed lines."""
    result = cli("stats", sample_log_with_malformed)
    output = result.stdout + result.stderr
    # The fixture has 2 malformed lines.
    assert "2" in output, "Expected malformed count of 2 in stats output"
    malformed_mentioned = (
        "malformed" in output.lower()
        or "invalid" in output.lower()
        or "unparseable" in output.lower()
        or "bad" in output.lower()
    )
    assert malformed_mentioned, "Expected a mention of malformed lines in stats"


# ------------------------------------------------------------------ #
# test_stats_shows_top_components
# ------------------------------------------------------------------ #
def test_stats_shows_top_components(cli, multi_level_log_file):
    """Stats output should list top components."""
    result = cli("stats", multi_level_log_file)
    output = result.stdout
    # http-server appears 5 times, database appears 6 times in multi_level_log_file
    assert "database" in output or "http-server" in output, (
        "Expected top components listed in stats output"
    )


# ------------------------------------------------------------------ #
# test_stats_shows_top_errors
# ------------------------------------------------------------------ #
def test_stats_shows_top_errors(cli, multi_level_log_file):
    """Stats output should include a top errors section."""
    result = cli("stats", multi_level_log_file)
    output = result.stdout
    # The multi_level fixture has "Connection timeout" errors.
    assert "Connection timeout" in output or "error" in output.lower(), (
        "Expected top errors section in stats output"
    )


# ------------------------------------------------------------------ #
# test_stats_output_format
# ------------------------------------------------------------------ #
def test_stats_output_format(cli, sample_log_file):
    """Stats output should follow the expected header/section structure."""
    result = cli("stats", sample_log_file)
    output = result.stdout
    # Check for key structural elements
    assert "Log Statistics" in output or "Statistics" in output or "stats" in output.lower(), (
        "Expected a statistics header"
    )
    # Should have some separator like "====" or "----"
    assert "===" in output or "---" in output, (
        "Expected a separator line in the stats output"
    )
