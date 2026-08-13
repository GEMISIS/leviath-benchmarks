"""Tests for frontend structure and component existence.

These are file-existence checks since we cannot run React/TypeScript
in a pytest environment. They verify the agent created the expected
frontend file structure.
"""

import os
import glob as globmod

import pytest

from conftest import WORKDIR


def _find_files(pattern: str) -> list[str]:
    """Find files matching a glob pattern under the project root."""
    return globmod.glob(os.path.join(WORKDIR, "**", pattern), recursive=True)


class TestFrontendStructure:
    """Verify the frontend directory and key files exist."""

    def test_frontend_directory_exists(self, workdir):
        """frontend/ directory must exist."""
        frontend_dir = os.path.join(workdir, "frontend")
        assert os.path.isdir(frontend_dir), (
            f"Expected frontend/ directory at {frontend_dir}"
        )

    def test_frontend_has_package_json(self, workdir):
        """frontend/package.json must exist."""
        candidates = [
            os.path.join(workdir, "frontend", "package.json"),
        ]
        # Also check nested paths.
        candidates.extend(
            globmod.glob(
                os.path.join(workdir, "frontend", "**", "package.json"),
                recursive=True,
            )
        )
        found = any(os.path.isfile(p) for p in candidates)
        assert found, "frontend/package.json not found"

    def test_frontend_has_notification_component(self):
        """A notification-related React component file must exist."""
        patterns = [
            "Notification*.tsx",
            "Notification*.jsx",
            "notification*.tsx",
            "notification*.jsx",
            "*Notification*.tsx",
            "*notification*.tsx",
        ]
        found_files = []
        for pattern in patterns:
            found_files.extend(
                globmod.glob(
                    os.path.join(WORKDIR, "frontend", "**", pattern),
                    recursive=True,
                )
            )
        assert len(found_files) > 0, (
            "No notification component file found in frontend/ "
            "(expected a file matching *Notification*.tsx or similar)"
        )

    def test_frontend_has_preferences_component(self):
        """A preferences-related React component or page must exist."""
        patterns = [
            "Preference*.tsx",
            "Preference*.jsx",
            "preference*.tsx",
            "preference*.jsx",
            "*Preference*.tsx",
            "*preference*.tsx",
            "*Settings*.tsx",
            "*settings*.tsx",
        ]
        found_files = []
        for pattern in patterns:
            found_files.extend(
                globmod.glob(
                    os.path.join(WORKDIR, "frontend", "**", pattern),
                    recursive=True,
                )
            )
        assert len(found_files) > 0, (
            "No preferences/settings component found in frontend/ "
            "(expected a file matching *Preference*.tsx or *Settings*.tsx)"
        )

    def test_frontend_references_shared_types(self):
        """Frontend TypeScript files should import from shared types."""
        ts_files = globmod.glob(
            os.path.join(WORKDIR, "frontend", "**", "*.ts"), recursive=True
        ) + globmod.glob(
            os.path.join(WORKDIR, "frontend", "**", "*.tsx"), recursive=True
        )
        assert len(ts_files) > 0, "No TypeScript files found in frontend/"

        # Check if any frontend file references shared types.
        import_patterns = [
            "shared/types",
            "shared",
            "../shared",
            "../../shared",
            "NotificationType",
            "NotificationPriority",
            "WebSocketMessage",
        ]
        found_import = False
        for filepath in ts_files:
            try:
                with open(filepath, "r") as f:
                    content = f.read()
            except OSError:
                continue
            for pattern in import_patterns:
                if pattern in content:
                    found_import = True
                    break
            if found_import:
                break

        assert found_import, (
            "No frontend TypeScript file imports from shared types. "
            "Expected import references to shared/types or shared type names."
        )
