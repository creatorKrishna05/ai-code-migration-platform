from pathlib import Path
from unittest.mock import Mock

import pytest
import subprocess

from compiler.executor import Executor
from utils.exceptions import ExecutionError


def test_executor_initializes() -> None:
    """Executor should initialize successfully."""
    executor = Executor()

    assert executor is not None


def test_execute_returns_stdout(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Return stripped stdout from successful execution."""
    executable = tmp_path / "program.exe"
    executable.touch()

    result = Mock()
    result.returncode = 0
    result.stdout = "Hello World\n"
    result.stderr = ""

    mock_run = Mock(return_value=result)

    monkeypatch.setattr(
        "compiler.executor.subprocess.run",
        mock_run,
    )

    executor = Executor()

    output = executor.execute(
        executable,
        timeout=10,
    )

    assert output == "Hello World"
    mock_run.assert_called_once()


def test_execute_raises_on_nonzero_exit(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Raise ExecutionError when executable fails."""
    executable = tmp_path / "program.exe"

    result = Mock()
    result.returncode = 1
    result.stdout = ""
    result.stderr = "Runtime error"

    monkeypatch.setattr(
        "compiler.executor.subprocess.run",
        lambda *args, **kwargs: result,
    )

    executor = Executor()

    with pytest.raises(
        ExecutionError,
        match="Runtime error",
    ):
        executor.execute(
            executable,
            timeout=10,
        )


def test_execute_uses_exit_code_when_stderr_empty(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Use exit code when stderr is empty."""
    executable = tmp_path / "program.exe"

    result = Mock()
    result.returncode = 2
    result.stdout = ""
    result.stderr = ""

    monkeypatch.setattr(
        "compiler.executor.subprocess.run",
        lambda *args, **kwargs: result,
    )

    executor = Executor()

    with pytest.raises(
        ExecutionError,
        match="exit code 2",
    ):
        executor.execute(
            executable,
            timeout=10,
        )


def test_execute_handles_timeout(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Raise ExecutionError when execution times out."""
    executable = tmp_path / "program.exe"

    def timeout_run(*args, **kwargs):
        raise subprocess.TimeoutExpired(
            cmd=args[0],
            timeout=10,
        )

    monkeypatch.setattr(
        "compiler.executor.subprocess.run",
        timeout_run,
    )

    executor = Executor()

    with pytest.raises(
        ExecutionError,
        match="timeout limit of 10 seconds",
    ):
        executor.execute(
            executable,
            timeout=10,
        )


def test_execute_passes_timeout_to_subprocess(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Pass configured timeout to subprocess."""
    executable = tmp_path / "program.exe"

    result = Mock()
    result.returncode = 0
    result.stdout = ""
    result.stderr = ""

    mock_run = Mock(return_value=result)

    monkeypatch.setattr(
        "compiler.executor.subprocess.run",
        mock_run,
    )

    executor = Executor()

    executor.execute(
        executable,
        timeout=15,
    )

    kwargs = mock_run.call_args.kwargs

    assert kwargs["timeout"] == 15
    assert kwargs["shell"] is False
    assert kwargs["capture_output"] is True
    assert kwargs["text"] is True