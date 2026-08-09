from __future__ import annotations

import time
from pathlib import Path

from compiler.executor import Executor
from utils.logger import get_logger


class Benchmark:
    """Benchmark compiled executables."""

    def __init__(
        self,
        executor: Executor,
    ) -> None:
        """Initialize the benchmark service."""
        self._executor = executor
        self._logger = get_logger(__name__)

    def benchmark(
        self,
        executable_path: Path,
        timeout: int,
        runs: int = 5,
    ) -> tuple[str, float]:
        """
        Benchmark a compiled executable.

        Returns:
            Tuple containing:
            - program output
            - average execution time
        """

        if runs <= 0:
            self._logger.error(
                "Invalid benchmark runs: %d",
                runs,
            )
            raise ValueError(
                "Benchmark runs must be greater than zero."
            )

        self._logger.info(
            "Benchmarking executable: %s (%d runs).",
            executable_path,
            runs,
        )

        execution_times: list[float] = []
        program_output = ""

        for _ in range(runs):
            start_time = time.perf_counter()

            output = self._executor.execute(
                executable_path=executable_path,
                timeout=timeout,
            )

            end_time = time.perf_counter()

            execution_times.append(
                end_time - start_time
            )

            if not program_output:
                program_output = output

        average_execution_time = (
            sum(execution_times)
            / len(execution_times)
        )

        self._logger.info(
            "Average execution time over %d runs: %.6f seconds.",
            runs,
            average_execution_time,
        )

        return (
            program_output,
            average_execution_time,
        )