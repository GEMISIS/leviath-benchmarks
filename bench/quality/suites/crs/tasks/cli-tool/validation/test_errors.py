"""Tests for error handling, exit codes, and miscellaneous flags."""

import os
import re


# ------------------------------------------------------------------ #
# test_file_not_found_exit_code
# ------------------------------------------------------------------ #
def test_file_not_found_exit_code(cli, tmp_dir):
    """Referencing a missing file should produce exit code 2."""
    missing = os.path.join(tmp_dir, "logs", "missing.log")
    result = cli("parse", missing)
    assert result.returncode == 2, (
        f"Expected exit code 2 for missing file, got {result.returncode}"
    )


# ------------------------------------------------------------------ #
# test_file_not_found_message
# ------------------------------------------------------------------ #
def test_file_not_found_message(cli, tmp_dir):
    """The error message for a missing file should mention 'not found'."""
    missing = os.path.join(tmp_dir, "logs", "missing.log")
    result = cli("parse", missing)
    output = (result.stdout + result.stderr).lower()
    assert "not found" in output or "no such file" in output, (
        f"Expected 'not found' in error output, got: {result.stdout + result.stderr}"
    )


# ------------------------------------------------------------------ #
# test_unknown_command_exit_code
# ------------------------------------------------------------------ #
def test_unknown_command_exit_code(cli):
    """An unknown subcommand should produce exit code 1."""
    result = cli("analyze")
    assert result.returncode == 1, (
        f"Expected exit code 1 for unknown command, got {result.returncode}"
    )


# ------------------------------------------------------------------ #
# test_unknown_command_message
# ------------------------------------------------------------------ #
def test_unknown_command_message(cli):
    """The error for an unknown command should mention it and hint at valid ones."""
    result = cli("analyze")
    output = (result.stdout + result.stderr).lower()
    assert "analyze" in output or "unknown" in output or "invalid" in output, (
        "Expected error output to mention the unknown command"
    )


# ------------------------------------------------------------------ #
# test_invalid_level_exit_code
# ------------------------------------------------------------------ #
def test_invalid_level_exit_code(cli, sample_log_file):
    """Using an invalid log level should produce exit code 1."""
    result = cli("filter", sample_log_file, "--level=TRACE")
    assert result.returncode == 1, (
        f"Expected exit code 1 for invalid level, got {result.returncode}"
    )


# ------------------------------------------------------------------ #
# test_no_color_flag
# ------------------------------------------------------------------ #
def test_no_color_flag(cli, sample_log_file):
    """The --no-color flag should suppress ANSI escape codes in output."""
    result = cli("stats", sample_log_file, "--no-color")
    output = result.stdout + result.stderr
    # ANSI escape codes start with ESC[ (\\x1b\\[)
    ansi_pattern = re.compile(r"\x1b\[")
    assert not ansi_pattern.search(output), (
        "Found ANSI escape codes in output despite --no-color flag"
    )
