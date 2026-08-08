from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from utils.logger import get_logger
from utils.exceptions import ReportGenerationError

class ReportGenerator:
    """
    Generate standardized migration reports from evaluation results.
    """

    def __init__(self) -> None:
        """
        Initialize the report generator service.
        """
        self._logger = get_logger(__name__)


    def generate(
            self,
            evaluation: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Generate a standardized migration report.
                
        Args:
            evaluation:
                Aggregated evaluation results.

        Returns:
            Standardized migration report.
        """
        self._logger.info("Generating migration report.")

        try:
            report = dict(evaluation)

            report["generated_at"] = (
                datetime.now(UTC).isoformat()
            )

            self._logger.info("Migration report generated successfully.")

            return report

        except Exception as error:
            self._logger.exception(
                "Report generation failed."
            )

            raise ReportGenerationError(
                "Failed to generate migration report."
            ) from error

        