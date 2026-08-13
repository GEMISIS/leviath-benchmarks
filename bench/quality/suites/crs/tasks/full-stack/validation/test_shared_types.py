"""Tests for shared type definitions in shared/types.ts."""

import os
import glob as globmod

import pytest

from conftest import WORKDIR


def _find_shared_types_file() -> str | None:
    """Locate the shared types TypeScript file."""
    candidates = [
        os.path.join(WORKDIR, "shared", "types.ts"),
        os.path.join(WORKDIR, "shared", "types", "index.ts"),
    ]
    # Also search with glob in case it is nested differently.
    glob_matches = globmod.glob(
        os.path.join(WORKDIR, "**", "shared", "types.ts"), recursive=True
    )
    candidates.extend(glob_matches)

    for path in candidates:
        if os.path.isfile(path):
            return path
    return None


def _read_shared_types() -> str:
    """Read and return the shared types file content."""
    path = _find_shared_types_file()
    if path is None:
        pytest.fail("shared/types.ts file not found")
    with open(path, "r") as f:
        return f.read()


class TestSharedTypesFile:
    """Validate the shared TypeScript type definitions."""

    def test_shared_types_file_exists(self):
        """shared/types.ts must exist."""
        path = _find_shared_types_file()
        assert path is not None, (
            "shared/types.ts not found under the project directory"
        )

    def test_shared_types_has_notification_type(self):
        """shared/types.ts must define the NotificationType enum."""
        content = _read_shared_types()
        assert "NotificationType" in content, (
            "shared/types.ts must contain a NotificationType enum"
        )
        # Verify all enum values are present.
        for value in ["comment", "mention", "system", "security"]:
            assert value in content.lower(), (
                f"NotificationType should include '{value}'"
            )

    def test_shared_types_has_notification_priority(self):
        """shared/types.ts must define the NotificationPriority enum."""
        content = _read_shared_types()
        assert "NotificationPriority" in content, (
            "shared/types.ts must contain a NotificationPriority enum"
        )
        for value in ["low", "medium", "high", "urgent"]:
            assert value in content.lower(), (
                f"NotificationPriority should include '{value}'"
            )

    def test_shared_types_has_websocket_message(self):
        """shared/types.ts must define the WebSocketMessage interface."""
        content = _read_shared_types()
        assert "WebSocketMessage" in content, (
            "shared/types.ts must contain a WebSocketMessage interface"
        )
        # Check for required fields.
        for field in ["type", "payload", "timestamp"]:
            assert field in content, (
                f"WebSocketMessage should include field '{field}'"
            )

    def test_backend_uses_shared_type_values(self):
        """Backend code should reference the same type/priority values as shared/types.ts."""
        # Read all backend Python files.
        backend_files = globmod.glob(
            os.path.join(WORKDIR, "backend", "**", "*.py"), recursive=True
        )
        assert len(backend_files) > 0, "No Python files found in backend/"

        all_source = ""
        for filepath in backend_files:
            try:
                with open(filepath, "r") as f:
                    all_source += f.read() + "\n"
            except OSError:
                continue

        source_lower = all_source.lower()

        # The backend must reference the same type values.
        for type_val in ["comment", "mention", "system", "security"]:
            assert type_val in source_lower, (
                f"Backend should reference notification type '{type_val}' "
                "matching shared/types.ts"
            )

        # The backend must reference the same priority values.
        for prio_val in ["low", "medium", "high", "urgent"]:
            assert prio_val in source_lower, (
                f"Backend should reference priority '{prio_val}' "
                "matching shared/types.ts"
            )
