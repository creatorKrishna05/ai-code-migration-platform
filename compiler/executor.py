from __future__ import annotations

import subprocess
from pathlib import Path

from utils.exceptions import ExecutionError
from utils.logger import get_logger


class Executor:
    """
    Execute compiled C++ programs.
    """

    def __init__(self) -> None:
        """
        Initialize the executor.
        """
        self._logger = get_logger(__name__)

    def execute(
        self,
        executable_path: Path,
        timeout: int,
    ) -> str:
        """
        Execute a compiled C++ program.

        Args:
            executable_path:
                Path to the compiled executable.

        Returns:
            str:
                Standard output produced by the executable.

        Raises:
            ExecutionError:
                If program execution fails.
        """

        self._logger.info(
            "Executing compiled binary: %s",
            executable_path,
        )


        try:
            result = subprocess.run(
                [str(executable_path)],
                capture_output=True,
                text=True,
                check=False,
                shell=False,
                timeout=timeout,
            )

            self._logger.info(
                "Execution completed with return code: %d",
                result.returncode,
            )

            if result.returncode != 0:
                self._logger.error(
                    "Executable failed with return code: %d",
                    result.returncode,
                )

                error_message = (
                    result.stderr.strip()
                    or f"Executable terminated with exit code {result.returncode}."
                )

                raise ExecutionError(error_message)

            return result.stdout.strip()

        except subprocess.TimeoutExpired as error:
            self._logger.error(
                "Execution timed out after %s seconds.",
                timeout,
            )
            raise ExecutionError(
                f"Execution exceeded the timeout limit of {timeout} seconds."
            ) from error