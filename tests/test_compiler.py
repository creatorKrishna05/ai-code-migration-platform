from pathlib import Path
from unittest.mock import Mock

import pytest

from compiler.compiler import Compiler
from utils.exceptions import CompilationError, ValidationError


def create_compiler() -> Compiler:
    """Create a compiler instance for testing."""
    return Compiler()


def test_compiler_initializes() -> None:
    """Compiler should initialize successfully."""
    compiler = create_compiler()

    assert compiler is not None


def test_compile_rejects_empty_cpp_code(
    tmp_path: Path,
) -> None:
    """Reject empty generated C++ code."""
    compiler = create_compiler()

    with pytest.raises(
        ValidationError,
        match="Generated C\\+\\+ source code cannot be empty",
    ):
        compiler.compile(
            tmp_path,
            "   ",
        )


def test_compile_writes_source_file(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Generated C++ code should be written to source.cpp."""
    compiler = create_compiler()

    result = Mock()
    result.returncode = 0
    result.stdout = ""
    result.stderr = ""

    def fake_run(*args, **kwargs):
        return result

    monkeypatch.setattr(
        "compiler.compiler.subprocess.run",
        fake_run,
    )

    compiler.compile(
        tmp_path,
        "int main() { return 0; }",
    )

    source_file = tmp_path / "source.cpp"

    assert source_file.exists()
    assert source_file.read_text(
        encoding="utf-8"
    ) == "int main() { return 0; }"


def test_compile_success_returns_executable_path(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Successful compilation should return executable path."""
    compiler = create_compiler()

    result = Mock()
    result.returncode = 0
    result.stdout = ""
    result.stderr = ""

    monkeypatch.setattr(
        "compiler.compiler.subprocess.run",
        lambda *args, **kwargs: result,
    )

    executable = compiler.compile(
        tmp_path,
        "int main() { return 0; }",
    )

    assert executable == (
        tmp_path / "program.exe"
    )


def test_compile_invokes_compiler(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Compiler should invoke the configured C++ compiler."""
    compiler = create_compiler()

    result = Mock()
    result.returncode = 0
    result.stdout = ""
    result.stderr = ""

    mock_run = Mock(return_value=result)

    monkeypatch.setattr(
        "compiler.compiler.subprocess.run",
        mock_run,
    )

    compiler.compile(
        tmp_path,
        "int main() { return 0; }",
    )

    mock_run.assert_called_once()

    command = mock_run.call_args.args[0]

    assert command[0] == compiler._compiler
    assert "-o" in command
    assert str(tmp_path / "source.cpp") in command


def test_compile_wraps_compiler_invocation_error(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Wrap compiler invocation errors."""
    compiler = create_compiler()

    def failing_run(*args, **kwargs):
        raise OSError("Compiler not found")

    monkeypatch.setattr(
        "compiler.compiler.subprocess.run",
        failing_run,
    )

    with pytest.raises(
        CompilationError,
        match="Failed to invoke the C\\+\\+ compiler",
    ):
        compiler.compile(
            tmp_path,
            "int main() { return 0; }",
        )


def test_compile_rejects_compilation_failure(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Reject non-zero compiler return codes."""
    compiler = create_compiler()

    result = Mock()
    result.returncode = 1
    result.stdout = ""
    result.stderr = "syntax error"

    monkeypatch.setattr(
        "compiler.compiler.subprocess.run",
        lambda *args, **kwargs: result,
    )

    with pytest.raises(
        CompilationError,
        match="Compilation failed",
    ):
        compiler.compile(
            tmp_path,
            "invalid cpp code",
        )


def test_compile_handles_source_write_error(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Wrap source file write errors."""
    compiler = create_compiler()

    def failing_write(*args, **kwargs):
        raise OSError("Permission denied")

    monkeypatch.setattr(
        Path,
        "write_text",
        failing_write,
    )

    with pytest.raises(
        CompilationError,
        match="Failed to write generated C\\+\\+ source",
    ):
        compiler.compile(
            tmp_path,
            "int main() { return 0; }",
        )