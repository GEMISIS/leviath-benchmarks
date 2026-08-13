"""Tests for the ``logviz filter`` command."""

import os


# ------------------------------------------------------------------ #
# test_filter_by_level
# ------------------------------------------------------------------ #
def test_filter_by_level(cli, sample_log_file):
    """Filtering by --level=ERROR should only show ERROR lines."""
    result = cli("filter", sample_log_file, "--level=ERROR")
    assert result.returncode == 0, f"stderr: {result.stderr}"
    lines = [l for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) > 0, "Expected at least one ERROR line"
    for line in lines:
        assert "ERROR" in line, f"Non-ERROR line in output: {line}"


# ------------------------------------------------------------------ #
# test_filter_by_since
# ------------------------------------------------------------------ #
def test_filter_by_since(cli, sample_log_file):
    """Filtering by --since should only return lines at or after that time."""
    # The sample log runs from 10:30:45 to 10:30:59.
    # Filtering since 10:30:55 should return only lines from :55 onward.
    result = cli("filter", sample_log_file, "--since=2024-01-15 10:30:55")
    assert result.returncode == 0, f"stderr: {result.stderr}"
    lines = [l for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) > 0, "Expected some lines after the since time"
    for line in lines:
        # Each matching line should have a timestamp >= 10:30:55
        assert "10:30:5" in line or "10:31:" in line, (
            f"Line appears to be before the --since time: {line}"
        )


# ------------------------------------------------------------------ #
# test_filter_combined
# ------------------------------------------------------------------ #
def test_filter_combined(cli, sample_log_file):
    """Combining --level and --since should apply both filters."""
    result = cli("filter", sample_log_file, "--level=INFO", "--since=2024-01-15 10:30:55")
    assert result.returncode == 0, f"stderr: {result.stderr}"
    lines = [l for l in result.stdout.strip().splitlines() if l.strip()]
    for line in lines:
        assert "INFO" in line, f"Non-INFO line: {line}"


# ------------------------------------------------------------------ #
# test_filter_invalid_level
# ------------------------------------------------------------------ #
def test_filter_invalid_level(cli, sample_log_file):
    """Filtering with an invalid level like TRACE should exit with code 1."""
    result = cli("filter", sample_log_file, "--level=TRACE")
    assert result.returncode == 1, (
        f"Expected exit code 1 for invalid level, got {result.returncode}"
    )
    output = result.stdout + result.stderr
    assert "TRACE" in output or "invalid" in output.lower() or "error" in output.lower(), (
        "Expected error message mentioning invalid level"
    )


# ------------------------------------------------------------------ #
# test_filter_no_matches
# ------------------------------------------------------------------ #
def test_filter_no_matches(cli, sample_log_file):
    """When no lines match the filter, exit code should be 0 with no output lines."""
    # Filter for FATAL -- the basic sample_log_file has no FATAL except
    # in multi_level. Use a since far in the future to guarantee no match.
    result = cli("filter", sample_log_file, "--level=FATAL", "--since=2099-01-01 00:00:00")
    assert result.returncode == 0, (
        f"Expected exit code 0 when no matches, got {result.returncode}"
    )
    lines = [l for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 0, "Expected no output lines when nothing matches"


# ------------------------------------------------------------------ #
# test_filter_file_not_found
# ------------------------------------------------------------------ #
def test_filter_file_not_found(cli, tmp_dir):
    """Filtering a non-existent file should exit with code 2."""
    missing = os.path.join(tmp_dir, "missing.log")
    result = cli("filter", missing, "--level=ERROR")
    assert result.returncode == 2
