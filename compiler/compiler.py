from __future__ import annotations

import subprocess
import os

from pathlib import Path

from utils.exceptions import (
    CompilationError,
    ValidationError,
)

from utils.logger import get_logger
from config import (
    COMPILER_FLAGS,
    CPP_COMPILER,
)


class Compiler:
    """
    Compile generated C++ source code.
    """

    def __init__(self) -> None:
        """
        Initialize the compiler.
        """
        self._logger = get_logger(__name__)
        self._compiler = CPP_COMPILER
        self._compiler_flags = list(COMPILER_FLAGS)


    def compile(
        self,
        workspace_path: Path,
        cpp_code: str,
    ) -> Path:
        """
        Compile generated C++ source code.

        Args:
            workspace_path:
                Path to the workspace where compilation artifacts
                will be stored.

            cpp_code:
                Generated C++ source code.
        Returns:
            Path:
                Path to the compiled executable.       
        Raises:
            ValidationError:
                If the source code is empty.

            CompilationError:
                If compilation fails.

        """

        self._logger.info("Starting C++ compilation.")

        if not cpp_code.strip():
            self._logger.error("Generated C++ source code is empty.")
            raise ValidationError(
                "Generated C++ source code cannot be empty."
            )

        self._logger.debug(
            "Using workspace: %s",
            workspace_path,
        )
        source_file = workspace_path / "source.cpp"
        executable_name = (
            "program.exe"
            if os.name == "nt"
            else "program"
        )

        executable_file = (
            workspace_path / executable_name
        )

        try:
            source_file.write_text(
                cpp_code,
                encoding="utf-8",
            )

            self._logger.debug(
                "Generated C++ source written to: %s",
                source_file,
            )

        except OSError as error:
            self._logger.exception(
                "Failed to write generated C++ source."
            )
            raise CompilationError(
                "Failed to write generated C++ source."
            ) from error
          
        
        compile_command = [
            self._compiler,
            *self._compiler_flags,
            str(source_file),
            "-o",
            str(executable_file),
        ]

        self._logger.debug(
            "Compilation command: %s",
            compile_command,
        )

        try:
            result = subprocess.run(
                compile_command,
                capture_output=True,
                text=True,
                check=False,
            )

        except OSError as error:
            self._logger.exception(
                "Failed to invoke the C++ compiler."
            )

            raise CompilationError(
                "Failed to invoke the C++ compiler."
            ) from error
            
        self._logger.debug(
            "Compiler exited with return code: %d",
            result.returncode,
        )

        if result.stdout:
            self._logger.debug(
                "Compiler stdout:\n%s",
                result.stdout,
            )

        if result.stderr:
            self._logger.debug(
                "Compiler stderr:\n%s",
                result.stderr,
            )

        if result.returncode != 0:
            self._logger.error(
                "C++ compilation failed:\n%s",
                result.stderr,
            )

            raise CompilationError(
                f"Compilation failed:\n{result.stderr.strip()}"
            ) 

        self._logger.info(
            "C++ compilation completed successfully."
        )

        return executable_file