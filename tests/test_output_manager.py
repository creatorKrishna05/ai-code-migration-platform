import json
from pathlib import Path

import pytest

from outputs.output_manager import OutputManager


def test_output_manager_initializes(
    tmp_path: Path,
) -> None:
    """Output manager should initialize successfully."""
    manager = OutputManager(tmp_path)

    assert manager is not None


def test_save_source_creates_cpp_file(
    tmp_path: Path,
) -> None:
    """Save generated C++ source code."""
    manager = OutputManager(tmp_path)

    cpp_code = "int main() { return 0; }"

    source_path = manager.save_source(cpp_code)

    assert source_path == tmp_path / "source.cpp"
    assert source_path.exists()
    assert source_path.read_text(
        encoding="utf-8"
    ) == cpp_code


def test_save_source_rejects_empty_code(
    tmp_path: Path,
) -> None:
    """Reject empty C++ source code."""
    manager = OutputManager(tmp_path)

    with pytest.raises(
        ValueError,
        match="Generated C\\+\\+ source code cannot be empty",
    ):
        manager.save_source("   ")


def test_save_executable_copies_file(
    tmp_path: Path,
) -> None:
    """Copy compiled executable to output directory."""
    executable = tmp_path / "build" / "program.exe"
    executable.parent.mkdir()

    executable.write_bytes(b"compiled-binary")

    output_directory = tmp_path / "outputs"

    manager = OutputManager(output_directory)

    output_path = manager.save_executable(executable)

    assert output_path == (
        output_directory / "program.exe"
    )
    assert output_path.exists()
    assert output_path.read_bytes() == b"compiled-binary"


def test_save_executable_rejects_missing_file(
    tmp_path: Path,
) -> None:
    """Reject a missing executable."""
    manager = OutputManager(tmp_path)

    executable = tmp_path / "missing.exe"

    with pytest.raises(
        FileNotFoundError,
        match="Executable not found",
    ):
        manager.save_executable(executable)


def test_save_report_creates_json_file(
    tmp_path: Path,
) -> None:
    """Save migration report as JSON."""
    manager = OutputManager(tmp_path)

    report = {
        "overall_success": True,
        "execution_time": 0.25,
        "benchmark_time": 0.20,
    }

    report_path = manager.save_report(report)

    assert report_path == tmp_path / "report.json"
    assert report_path.exists()

    saved_report = json.loads(
        report_path.read_text(
            encoding="utf-8"
        )
    )

    assert saved_report == report


def test_save_report_rejects_empty_report(
    tmp_path: Path,
) -> None:
    """Reject an empty migration report."""
    manager = OutputManager(tmp_path)

    with pytest.raises(
        ValueError,
        match="Migration report cannot be empty",
    ):
        manager.save_report({})


def test_save_report_rejects_non_serializable_data(
    tmp_path: Path,
) -> None:
    """Reject reports containing non-JSON-serializable data."""
    manager = OutputManager(tmp_path)

    report = {
        "timestamp": object(),
    }

    with pytest.raises(TypeError):
        manager.save_report(report)