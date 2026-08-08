from __future__ import annotations

import tempfile
from pathlib import Path

from utils.logger import get_logger


class WorkspaceManager:
    """
    Manage temprory workspaces used during code migration.
    """

    def __init__(self) -> None:
        """
        Initialize the workspace manager.
        """

        self._logger = get_logger(__name__)
        self._workspace: tempfile.TemporaryDirectory[str] | None = None


    def create_workspace(
        self,
    ) -> Path:
        """
        Create a temporary workspace.

        Returns:
            Path:
                Path to the temporary workspace.

        """

        if self._workspace is not None:
            workspace_path = Path(self._workspace.name)

            self._logger.debug(
                "Using existing workspace: %s",
                workspace_path,
            )

            return workspace_path

        self._workspace = tempfile.TemporaryDirectory()
        workspace_path = Path(self._workspace.name)

        self._logger.info(
            "Created temporary workspace: %s",
            workspace_path,
        )

        return workspace_path

    def cleanup(
        self,
    ) -> None:
        """
        Clean up the temporary workspace.
        """
        if self._workspace is None:
            self._logger.debug(
                "No workspace to clean up."
            )
            return

        self._workspace.cleanup()

        self._logger.info(
            "Temporary workspace cleaned up successfully."
        )

        self._workspace = None