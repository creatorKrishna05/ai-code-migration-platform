from __future__ import annotations

import json
from pathlib import Path

from .leaderboard_entry import LeaderboardEntry


class LeaderboardStore:
    """
    Persist leaderboard entries to a JSON file.
    """

    def __init__(
        self,
        file_path: Path,
    ) -> None:

        """
        Initialize the leaderboard store.

        Args:
            file_path:
                Path to the leaderboard JSON file.
        """
        from utils.logger import get_logger
        
        self._logger = get_logger(__name__)
        self._file_path = file_path

    def save(
        self,
        entry: LeaderboardEntry,
    ) -> None:
        """
        Save a leaderboard entry.

        Args:
            entry:
                Leaderboard entry to persist.
        """
        try:
            entries = self.load()

            entries.append(entry)

            self._file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            data = [
                {
                    "provider_name": item.provider_name,
                    "model_name": item.model_name,
                    "source_file": item.source_file,
                    "benchmark_time": item.benchmark_time,
                    "execution_time": item.execution_time,
                    "overall_success": item.overall_success,
                    "created_at": item.created_at,
                }
                for item in entries
            ]

            self._file_path.write_text(
                json.dumps(
                    data,
                    indent=4,
                ),
                encoding="utf-8",
            )

            self._logger.info(
                "Leaderboard entry saved successfully."
            )

        except Exception as error:
            from utils.exceptions import AIPlatformError

            self._logger.exception(
                "Failed to save leaderboard entry."
            )

            raise AIPlatformError(
                "Failed to save leaderboard entry."
            ) from error

    def load(self) -> list[LeaderboardEntry]:
        """
        Load leaderboard entries from storage.

        Returns:
            List of stored leaderboard entries.
        """
        if not self._file_path.exists():
            return []

        try:
            data = json.loads(
                self._file_path.read_text(
                    encoding="utf-8"
                )
            )

            return [
                LeaderboardEntry(
                    provider_name=item["provider_name"],
                    model_name=item["model_name"],
                    source_file=item.get(
                        "source_file",
                        "unknown.py",
                    ),
                    benchmark_time=item["benchmark_time"],
                    execution_time=item["execution_time"],
                    overall_success=item["overall_success"],
                    created_at=item.get(
                        "created_at",
                        "",
                    ),

                )
                for item in data
            ]

        except Exception as error:
            from utils.exceptions import AIPlatformError

            self._logger.exception(
                "Failed to load leaderboard entries."
            )

            raise AIPlatformError(
                "Failed to load leaderboard entries."
            ) from error