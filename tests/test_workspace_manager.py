from pathlib import Path

from workspace.workspace_manager import WorkspaceManager


def test_workspace_manager_initializes() -> None:
    """Workspace manager should initialize successfully."""
    manager = WorkspaceManager()

    assert manager is not None


def test_create_workspace_returns_existing_directory() -> None:
    """Create a temporary workspace."""
    manager = WorkspaceManager()

    workspace = manager.create_workspace()

    try:
        assert isinstance(workspace, Path)
        assert workspace.exists()
        assert workspace.is_dir()
    finally:
        manager.cleanup()


def test_create_workspace_reuses_existing_workspace() -> None:
    """Reuse the same workspace when called multiple times."""
    manager = WorkspaceManager()

    workspace_one = manager.create_workspace()
    workspace_two = manager.create_workspace()

    try:
        assert workspace_one == workspace_two
        assert workspace_one.exists()
    finally:
        manager.cleanup()


def test_cleanup_removes_workspace() -> None:
    """Cleanup should remove the temporary workspace."""
    manager = WorkspaceManager()

    workspace = manager.create_workspace()

    assert workspace.exists()

    manager.cleanup()

    assert not workspace.exists()


def test_cleanup_without_workspace_does_not_fail() -> None:
    """Cleanup should safely handle an absent workspace."""
    manager = WorkspaceManager()

    manager.cleanup()

    assert manager._workspace is None