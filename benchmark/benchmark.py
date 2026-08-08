from __future__ import annotations

import time
from pathlib import Path

from utils.logger import get_logger
from compiler.executor import Executor

class Benchmark:
    """
    Benchmark compiled executables.
    """

    def __init__(
        self,
        executor: Executor,
    ) -> None:
        """
        Initialize the benchmark service.
        """
        self._executor = executor
        self._logger = get_logger(__name__)

    def benchmark(
        self,
        executable_path: Path,
        timeout: int,
        runs: int = 5,
    ) -> tuple[str, float]:
        """
        Benchmark a compiled executable and measure its execution time.

        Args:
            executable_path:
                Path to the compiled executable.
            timeout:
                Maximum execution time in seconds.

        Returns:
            tuple[str, float]:
                Program output and execution time in seconds.

        Raises:
            ValueError:
                If runs is less than or equal to zero.
            ExecutionError:
                If executable execution fails.
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
        output = ""

        for _ in range(runs):
            start_time = time.perf_counter()
            
            output = self._executor.execute(
                executable_path=executable_path,
                timeout=timeout,
            )
            
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            
            execution_times.append(execution_time)

        average_execution_time = (
            sum(execution_times) / len(execution_times)
        )

        self._logger.info(
            "Average execution time over %d runs: %.6f seconds.",
            runs,
            average_execution_time,
        )

        return output, average_execution_time
