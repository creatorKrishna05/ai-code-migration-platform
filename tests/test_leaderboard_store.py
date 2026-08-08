from pathlib import Path

import pytest

from leaderboard.leaderboard_entry import LeaderboardEntry
from leaderboard.leaderboard_store import LeaderboardStore
from utils.exceptions import AIPlatformError


def create_entry(
    model_name: str = "test-model",
    benchmark_time: float = 0.1,
) -> LeaderboardEntry:
    """Create a test leaderboard entry."""
    return LeaderboardEntry(
        provider_name="test-provider",
        model_name=model_name,
        benchmark_time=benchmark_time,
        execution_time=0.05,
        overall_success=True,
    )


def test_load_returns_empty_list_for_missing_file(
    tmp_path: Path,
) -> None:
    """Return an empty list when storage does not exist."""
    store = LeaderboardStore(
        tmp_path / "leaderboard.json"
    )

    assert store.load() == []


def test_save_and_load_entry(
    tmp_path: Path,
) -> None:
    """Persist and restore a leaderboard entry."""
    file_path = tmp_path / "leaderboard.json"
    store = LeaderboardStore(file_path)

    entry = create_entry()

    store.save(entry)

    entries = store.load()

    assert entries == [entry]


def test_save_multiple_entries(
    tmp_path: Path,
) -> None:
    """Persist multiple leaderboard entries."""
    file_path = tmp_path / "leaderboard.json"
    store = LeaderboardStore(file_path)

    first_entry = create_entry(
        model_name="model-one",
        benchmark_time=0.1,
    )

    second_entry = create_entry(
        model_name="model-two",
        benchmark_time=0.2,
    )

    store.save(first_entry)
    store.save(second_entry)

    entries = store.load()

    assert entries == [
        first_entry,
        second_entry,
    ]


def test_save_creates_parent_directory(
    tmp_path: Path,
) -> None:
    """Create the parent directory when it does not exist."""
    file_path = (
        tmp_path
        / "nested"
        / "leaderboard.json"
    )

    store = LeaderboardStore(file_path)

    store.save(create_entry())

    assert file_path.exists()


def test_load_raises_error_for_invalid_json(
    tmp_path: Path,
) -> None:
    """Raise an application error for corrupted JSON."""
    file_path = tmp_path / "leaderboard.json"

    file_path.write_text(
        "{invalid-json",
        encoding="utf-8",
    )

    store = LeaderboardStore(file_path)

    with pytest.raises(
        AIPlatformError,
        match="Failed to load leaderboard entries",
    ):
        store.load()