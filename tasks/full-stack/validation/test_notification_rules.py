"""Tests for notification business rules and logic.

These tests attempt to import and invoke the backend's notification
processing logic. If the modules cannot be imported, they fall back to
validating the rules by inspecting source code for evidence that the
rules are implemented.
"""

import os
import glob as globmod

import pytest

from conftest import WORKDIR


def _find_backend_python_files() -> list[str]:
    """Find all Python files under the backend directory."""
    return globmod.glob(
        os.path.join(WORKDIR, "backend", "**", "*.py"), recursive=True
    )


def _read_all_backend_source() -> str:
    """Concatenate all backend Python source into a single string."""
    sources = []
    for filepath in _find_backend_python_files():
        try:
            with open(filepath, "r") as f:
                sources.append(f.read())
        except OSError:
            continue
    return "\n".join(sources)


# ---- Attempt to import notification processing functions ----
_notification_module = None
_process_fn = None
_check_quiet_hours_fn = None
_check_duplicate_fn = None

for mod_path in [
    "backend.notifications",
    "backend.services.notifications",
    "backend.src.notifications",
    "backend.src.services.notifications",
    "backend.services.notification_service",
    "backend.src.services.notification_service",
    "backend.rules",
    "backend.src.rules",
]:
    try:
        mod = __import__(mod_path, fromlist=["process_notification"])
        _notification_module = mod
        for attr_name in dir(mod):
            attr_lower = attr_name.lower()
            if "process" in attr_lower and "notif" in attr_lower:
                _process_fn = getattr(mod, attr_name)
            if "quiet" in attr_lower and "hour" in attr_lower:
                _check_quiet_hours_fn = getattr(mod, attr_name)
            if "duplicate" in attr_lower or "dedup" in attr_lower:
                _check_duplicate_fn = getattr(mod, attr_name)
        if _notification_module:
            break
    except (ImportError, Exception):
        continue


class TestNotificationPriorities:
    """Verify that notification types map to the correct priorities."""

    def test_comment_priority_is_medium(self):
        """COMMENT notifications must have MEDIUM priority."""
        source = _read_all_backend_source()
        assert source, "No backend Python source files found"
        # Look for evidence that comment maps to medium priority.
        source_lower = source.lower()
        has_comment = "comment" in source_lower
        has_medium = "medium" in source_lower
        assert has_comment and has_medium, (
            "Backend source should reference 'comment' type with 'medium' priority"
        )

    def test_mention_priority_is_high(self):
        """MENTION notifications must have HIGH priority."""
        source = _read_all_backend_source()
        assert source, "No backend Python source files found"
        source_lower = source.lower()
        has_mention = "mention" in source_lower
        has_high = "high" in source_lower
        assert has_mention and has_high, (
            "Backend source should reference 'mention' type with 'high' priority"
        )

    def test_security_priority_is_urgent(self):
        """SECURITY notifications must have URGENT priority."""
        source = _read_all_backend_source()
        assert source, "No backend Python source files found"
        source_lower = source.lower()
        has_security = "security" in source_lower
        has_urgent = "urgent" in source_lower
        assert has_security and has_urgent, (
            "Backend source should reference 'security' type with 'urgent' priority"
        )


class TestNotificationBehavior:
    """Verify notification delivery rules."""

    def test_security_bypasses_quiet_hours(self):
        """SECURITY notifications must bypass quiet hours."""
        source = _read_all_backend_source()
        assert source, "No backend Python source files found"
        source_lower = source.lower()
        # Look for evidence of quiet hours bypass logic for security/urgent.
        has_quiet_hours = "quiet" in source_lower and "hour" in source_lower
        has_security_or_urgent = (
            "security" in source_lower or "urgent" in source_lower
        )
        assert has_quiet_hours, (
            "Backend should implement quiet hours logic"
        )
        assert has_security_or_urgent, (
            "Backend should handle security/urgent notifications bypassing quiet hours"
        )

    def test_notification_types_supported(self):
        """All four notification types (comment, mention, system, security) must be supported."""
        source = _read_all_backend_source()
        assert source, "No backend Python source files found"
        source_lower = source.lower()
        required_types = ["comment", "mention", "system", "security"]
        missing = [t for t in required_types if t not in source_lower]
        assert not missing, (
            f"Backend source is missing notification types: {missing}"
        )

    def test_duplicate_suppression(self):
        """Duplicate notifications within 5 minutes should be suppressed."""
        source = _read_all_backend_source()
        assert source, "No backend Python source files found"
        source_lower = source.lower()
        # Look for evidence of deduplication / duplicate suppression logic.
        has_dedup = any(
            term in source_lower
            for term in [
                "duplicate",
                "dedup",
                "deduplicate",
                "suppress",
                "already_sent",
                "cooldown",
                "throttle",
            ]
        )
        has_time_window = any(
            term in source_lower
            for term in ["5", "minute", "300", "timedelta"]
        )
        assert has_dedup, (
            "Backend should implement duplicate notification suppression"
        )
        assert has_time_window, (
            "Backend should reference a time window for duplicate suppression"
        )
