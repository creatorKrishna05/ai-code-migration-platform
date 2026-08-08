from pathlib import Path
from unittest.mock import Mock

import pytest

from benchmark.benchmark import Benchmark


def test_benchmark_initializes() -> None:
    """Benchmark should initialize with an executor."""
    executor = Mock()

    benchmark = Benchmark(
        executor=executor,
    )

    assert benchmark is not None


def test_benchmark_rejects_zero_runs(
    tmp_path: Path,
) -> None:
    """Reject zero benchmark runs."""
    executor = Mock()

    benchmark = Benchmark(
        executor=executor,
    )

    with pytest.raises(
        ValueError,
        match="Benchmark runs must be greater than zero",
    ):
        benchmark.benchmark(
            executable_path=tmp_path / "program.exe",
            timeout=10,
            runs=0,
        )


def test_benchmark_rejects_negative_runs(
    tmp_path: Path,
) -> None:
    """Reject negative benchmark runs."""
    executor = Mock()

    benchmark = Benchmark(
        executor=executor,
    )

    with pytest.raises(
        ValueError,
        match="Benchmark runs must be greater than zero",
    ):
        benchmark.benchmark(
            executable_path=tmp_path / "program.exe",
            timeout=10,
            runs=-1,
        )


def test_benchmark_executes_requested_number_of_runs(
    tmp_path: Path,
) -> None:
    """Execute the program the requested number of times."""
    executor = Mock()
    executor.execute.return_value = "Hello"

    benchmark = Benchmark(
        executor=executor,
    )

    output, average_time = benchmark.benchmark(
        executable_path=tmp_path / "program.exe",
        timeout=10,
        runs=5,
    )

    assert output == "Hello"
    assert average_time >= 0
    assert executor.execute.call_count == 5


def test_benchmark_returns_average_execution_time(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Calculate and return the average execution time."""
    executor = Mock()
    executor.execute.return_value = "Result"

    benchmark = Benchmark(
        executor=executor,
    )

    timestamps = iter(
        [
            0.0, 0.1,
            1.0, 1.3,
            2.0, 2.2,
        ]
    )

    monkeypatch.setattr(
        "benchmark.benchmark.time.perf_counter",
        lambda: next(timestamps),
    )

    output, average_time = benchmark.benchmark(
        executable_path=tmp_path / "program.exe",
        timeout=10,
        runs=3,
    )

    assert output == "Result"
    assert average_time == pytest.approx(0.2)


def test_benchmark_passes_timeout_to_executor(
    tmp_path: Path,
) -> None:
    """Pass the configured timeout to the executor."""
    executor = Mock()
    executor.execute.return_value = "Output"

    benchmark = Benchmark(
        executor=executor,
    )

    benchmark.benchmark(
        executable_path=tmp_path / "program.exe",
        timeout=25,
        runs=3,
    )

    assert executor.execute.call_count == 3

    for call in executor.execute.call_args_list:
        assert call.kwargs["timeout"] == 25