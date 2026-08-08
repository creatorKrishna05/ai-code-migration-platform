from leaderboard.leaderboard import Leaderboard
from leaderboard.leaderboard_entry import LeaderboardEntry


def test_add_entry() -> None:
    leaderboard = Leaderboard()

    entry = LeaderboardEntry(
        provider_name="groq",
        model_name="llama-3.3-70b-versatile",
        benchmark_time=0.167758,
        execution_time=0.167758,
        overall_success=True,
    )

    leaderboard.add(entry)

    rankings = leaderboard.get_rankings()

    assert len(rankings) == 1
    assert rankings[0] == entry


def test_successful_entries_rank_before_failed_entries() -> None:
    leaderboard = Leaderboard()

    failed_entry = LeaderboardEntry(
        provider_name="ollama",
        model_name="failed-model",
        benchmark_time=0.05,
        execution_time=0.05,
        overall_success=False,
    )

    successful_entry = LeaderboardEntry(
        provider_name="groq",
        model_name="llama-3.3-70b-versatile",
        benchmark_time=0.20,
        execution_time=0.20,
        overall_success=True,
    )

    leaderboard.add(failed_entry)
    leaderboard.add(successful_entry)

    rankings = leaderboard.get_rankings()

    assert rankings == [
        successful_entry,
        failed_entry,
    ]


def test_successful_entries_rank_by_benchmark_time() -> None:
    leaderboard = Leaderboard()

    slow_entry = LeaderboardEntry(
        provider_name="groq",
        model_name="slow-model",
        benchmark_time=0.30,
        execution_time=0.30,
        overall_success=True,
    )

    fast_entry = LeaderboardEntry(
        provider_name="groq",
        model_name="fast-model",
        benchmark_time=0.10,
        execution_time=0.10,
        overall_success=True,
    )

    leaderboard.add(slow_entry)
    leaderboard.add(fast_entry)

    rankings = leaderboard.get_rankings()

    assert rankings == [
        fast_entry,
        slow_entry,
    ]