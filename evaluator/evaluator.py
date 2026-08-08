from __future__ import annotations

from typing import Any

from utils.exceptions import EvaluationError
from utils.logger import get_logger


class Evaluator:
    """
    Evaluate the overall AI code migration process by aggregating
    results from translation, compilation, execution, and benchmarking.
    """

    def __init__(self) -> None:
        """
        Initialize the evaluator service.
        """
        self._logger = get_logger(__name__)


    def evaluate(
            self,
            translation_success: bool,
            compilation_success: bool,
            execution_success: bool,
            execution_time: float,
            benchmark_time: float,
    ) -> dict[str, Any]:
        """       
        Aggregate migration results and produce a unified evaluation.

        Args:
            translation_success: Whether translation completed successfully.
            compilation_success: Whether compilation completed successfully.
            execution_success: Whether execution completed successfully.
            execution_time: Program execution time in seconds.
            benchmark_time: Average benchmark time in seconds.

        Returns:
            Dictionary containing the evaluation summary.
        """
        self._logger.info("Starting evaluation.")
        try:
            overall_success = (
                translation_success
                and compilation_success
                and execution_success
            )

            evaluation = {
                "translation_success": translation_success,
                "compilation_success": compilation_success,
                "execution_success": execution_success,
                "execution_time": execution_time,
                "benchmark_time": benchmark_time,
                "overall_success": overall_success,
            }

            self._logger.info("Evaluation completed successfully.")

            return evaluation

        except Exception as error:
            self._logger.exception("Evaluation failed.")

            raise EvaluationError(
                "Failed to evaluate migration results."
            ) from error
        