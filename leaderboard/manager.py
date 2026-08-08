from __future__ import annotations
from .leaderboard_store import LeaderboardStore
from .leaderboard_entry import LeaderboardEntry

class Leaderboard:
    """
    Manage and rank migration performance entries.
    """

    def __init__(
        self,
        store: LeaderboardStore | None = None,
    ) -> None:
        """
        Initialize the leaderboard.

        Args:
            store:
                Optional persistence store.
        """
        self._entries: list[LeaderboardEntry] = []
        self._store = store

        if self._store is not None:
            self._entries = self._store.load()

    def add(
        self,
        entry: LeaderboardEntry,
    ) -> None:
        """
        Add a migration result to the leaderboard.

        Args:
            entry:
                Migration result to add.
        """
        self._entries.append(entry)

        if self._store is not None:
            self._store.save(entry)

    def get_rankings(
        self,
    ) -> list[LeaderboardEntry]:
        """
        Return migration results ranked by performance.

        Successful migrations are ranked before failed migrations.
        Among successful migrations, lower benchmark time ranks higher.

        Returns:
            Ranked leaderboard entries.
        """
        return sorted(
            self._entries,
            key=lambda entry: (
                not entry.overall_success,
                entry.benchmark_time,
            ),
        )