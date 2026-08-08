from __future__ import annotations

from pathlib import Path

from utils.logger import get_logger
import json
from typing import Any

class OutputManager:
    """
    Manage permanent migration output artifacts.
    """

    def __init__(
        self,
        output_directory: Path,
    ) -> None:
        """
        Initialize the output manager.

        Args:
            output_directory:
                Directory where migration artifacts
                will be stored.
        """
        self._logger = get_logger(__name__)
        self._output_directory = output_directory

        self._logger.info(
            "Output manager initialized with directory: %s",
            self._output_directory,
        )

    def save_source(
        self,
        cpp_code: str,
    ) -> Path:
        """
        Save generated C++ source code.

        Args:
            cpp_code:
                Generated C++ source code.

        Returns:
            Path:
                Path to the saved C++ source file.

        Raises:
            OSError:
                If the source file cannot be written.
        """
        if not cpp_code.strip():
            raise ValueError(
                "Generated C++ source code cannot be empty."
            )

        try:
            self._output_directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            source_path = (
                self._output_directory / "source.cpp"
            )

            source_path.write_text(
                cpp_code,
                encoding="utf-8",
        )

        except OSError as exc:
            self._logger.exception(
            "Failed to save generated C++ source."
            )
            raise

        self._logger.info(
            "Generated C++ source saved to: %s",
            source_path,
        )

        return source_path

    def save_executable(
        self,
        executable_path: Path,
    ) -> Path:
        """
        Save the compiled executable.

        Args:
            executable_path:
                Path to the compiled executable.

        Returns:
            Path:
                Path to the saved executable.

        Raises:
            FileNotFoundError:
                If the executable does not exist.

            OSError:
                If the executable cannot be copied.
        """
        if not executable_path.is_file():
            raise FileNotFoundError(
                f"Executable not found: {executable_path}"
            )

        try:
            self._output_directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            output_path = (
                self._output_directory
                / executable_path.name
            )

            output_path.write_bytes(
                executable_path.read_bytes()
            )

        except OSError:
            self._logger.exception(
                "Failed to save compiled executable."
            )
            raise

        self._logger.info(
            "Compiled executable saved to: %s",
            output_path,
        )

        return output_path


    def save_report(
        self,
        report: dict[str, Any],
    ) -> Path:
        """
        Save the migration report as JSON.

        Args:
            report:
                Migration report data.

        Returns:
            Path:
                Path to the saved JSON report.

        Raises:
            OSError:
                If the report cannot be written.

            TypeError:
                If the report contains non-serializable data.
        """
        if not report:
            raise ValueError(
                "Migration report cannot be empty."
            )

        try:
            self._output_directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            report_path = (
                self._output_directory / "report.json"
            )

            report_path.write_text(
                json.dumps(
                    report,
                    indent=4,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

        except (OSError, TypeError):
            self._logger.exception(
                "Failed to save migration report."
            )
            raise

        self._logger.info(
            "Migration report saved to: %s",
            report_path,
        )

        return report_path