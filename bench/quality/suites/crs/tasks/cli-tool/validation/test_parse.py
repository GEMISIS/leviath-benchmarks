"""Tests for the ``logviz parse`` command."""

import os


# ------------------------------------------------------------------ #
# test_parse_valid_log_file
# ------------------------------------------------------------------ #
def test_parse_valid_log_file(cli, sample_log_file):
    """Parsing a well-formed log file should exit with code 0."""
    result = cli("parse", sample_log_file)
    assert result.returncode == 0, f"stderr: {result.stderr}"


# ------------------------------------------------------------------ #
# test_parse_reports_malformed_lines
# ------------------------------------------------------------------ #
def test_parse_reports_malformed_lines(cli, sample_log_with_malformed):
    """Malformed lines should be reported in stdout or stderr."""
    result = cli("parse", sample_log_with_malformed)
    output = result.stdout + result.stderr
    # The file has 2 malformed lines; the tool should mention them.
    assert "malformed" in output.lower() or "invalid" in output.lower() or "error" in output.lower(), (
        "Expected a mention of malformed/invalid lines in output"
    )


# ------------------------------------------------------------------ #
# test_parse_file_not_found
# ------------------------------------------------------------------ #
def test_parse_file_not_found(cli, tmp_dir):
    """Parsing a non-existent file should exit with code 2."""
    missing = os.path.join(tmp_dir, "no_such_file.log")
    result = cli("parse", missing)
    assert result.returncode == 2


# ------------------------------------------------------------------ #
# test_parse_empty_file
# ------------------------------------------------------------------ #
def test_parse_empty_file(cli, empty_log_file):
    """Parsing an empty file should not crash (exit 0 or 3 accepted)."""
    result = cli("parse", empty_log_file)
    # An empty file is not an error per se; accept 0 (no lines) or 3
    # (nothing to parse).  It must NOT be 2 (file error) since the
    # file exists.
    assert result.returncode in (0, 3), f"Unexpected exit code {result.returncode}"


# ------------------------------------------------------------------ #
# test_parse_counts_correct
# ------------------------------------------------------------------ #
def test_parse_counts_correct(cli, sample_log_file):
    """The parse output should include or imply a correct line count (15)."""
    result = cli("parse", sample_log_file)
    output = result.stdout + result.stderr
    # We expect the tool to mention the number 15 somewhere, either as
    # a total or as individual parsed lines.
    assert "15" in output, (
        "Expected the number 15 (total lines) to appear in parse output"
    )
