from pathlib import Path
from unittest.mock import Mock

import pytest

from pipeline.migration_pipeline import MigrationPipeline
from utils.exceptions import ValidationError


@pytest.fixture
def source_file(tmp_path: Path) -> Path:
    """Create a temporary Python source file."""
    source = tmp_path / "example.py"
    source.write_text(
        "print('hello')",
        encoding="utf-8",
    )
    return source


@pytest.fixture
def pipeline_components(tmp_path: Path):
    """Create mocked pipeline dependencies."""
    workspace_manager = Mock()
    translator = Mock()
    analyzer = Mock()
    compiler = Mock()
    benchmark = Mock()
    evaluator = Mock()
    report_generator = Mock()
    output_manager = Mock()
    leaderboard = Mock()

    workspace = tmp_path / "workspace"
    workspace.mkdir()

    executable = workspace / "program.exe"
    executable.write_bytes(b"binary")

    workspace_manager.create_workspace.return_value = workspace

    translator.translate.return_value = (
        "int main() { return 0; }"
    )

    translator.provider_name = "MockProvider"
    translator.model_name = "MockModel"

    compiler.compile.return_value = executable

    benchmark.benchmark.return_value = (
        "hello",
        0.25,
    )

    evaluator.evaluate.return_value = {
        "translation_success": True,
        "compilation_success": True,
        "execution_success": True,
        "execution_time": 0.25,
        "benchmark_time": 0.25,
        "overall_success": True,
    }

    report_generator.generate.return_value = {
        "overall_success": True,
    }

    return {
        "workspace_manager": workspace_manager,
        "translator": translator,
        "analyzer": analyzer,
        "compiler": compiler,
        "benchmark": benchmark,
        "evaluator": evaluator,
        "report_generator": report_generator,
        "output_manager": output_manager,
        "leaderboard": leaderboard,
    }


def test_pipeline_initializes(
    pipeline_components,
) -> None:
    """Migration pipeline should initialize."""
    pipeline = MigrationPipeline(
        **pipeline_components,
    )

    assert pipeline is not None


def test_pipeline_runs_successfully(
    source_file: Path,
    pipeline_components,
) -> None:
    """Run the complete migration workflow."""
    pipeline = MigrationPipeline(
        **pipeline_components,
    )

    report = pipeline.run(source_file)

    assert report["overall_success"] is True
    assert report["program_output"] == "hello"


def test_pipeline_reads_source_code(
    source_file: Path,
    pipeline_components,
) -> None:
    """Pipeline should pass source code to translator."""
    pipeline = MigrationPipeline(
        **pipeline_components,
    )

    pipeline.run(source_file)

    pipeline_components["translator"].translate.assert_called_once_with(
        "print('hello')",
        pipeline_components["analyzer"].analyze.return_value,
    )


def test_pipeline_compiles_translated_code(
    source_file: Path,
    pipeline_components,
) -> None:
    """Pipeline should compile translated code."""
    pipeline = MigrationPipeline(
        **pipeline_components,
    )

    pipeline.run(source_file)

    pipeline_components["compiler"].compile.assert_called_once()


def test_pipeline_benchmarks_executable(
    source_file: Path,
    pipeline_components,
) -> None:
    """Pipeline should benchmark the compiled executable."""
    pipeline = MigrationPipeline(
        **pipeline_components,
        benchmark_runs=3,
        timeout=7,
    )

    pipeline.run(source_file)

    pipeline_components["benchmark"].benchmark.assert_called_once_with(
        executable_path=(
            pipeline_components["compiler"].compile.return_value
        ),
        runs=3,
        timeout=7,
    )


def test_pipeline_generates_report(
    source_file: Path,
    pipeline_components,
) -> None:
    """Pipeline should generate a migration report."""
    pipeline = MigrationPipeline(
        **pipeline_components,
    )

    pipeline.run(source_file)

    pipeline_components[
        "report_generator"
    ].generate.assert_called_once()


def test_pipeline_saves_source_and_executable(
    source_file: Path,
    pipeline_components,
) -> None:
    """Pipeline should save migration artifacts."""
    pipeline = MigrationPipeline(
        **pipeline_components,
    )

    pipeline.run(source_file)

    output_manager = pipeline_components["output_manager"]

    output_manager.save_source.assert_called_once_with(
        "int main() { return 0; }"
    )

    output_manager.save_executable.assert_called_once()


def test_pipeline_saves_json_report_when_enabled(
    source_file: Path,
    pipeline_components,
) -> None:
    """Pipeline should save JSON report when enabled."""
    pipeline = MigrationPipeline(
        **pipeline_components,
        report_json=True,
    )

    pipeline.run(source_file)

    pipeline_components[
        "output_manager"
    ].save_report.assert_called_once()


def test_pipeline_does_not_save_json_report_by_default(
    source_file: Path,
    pipeline_components,
) -> None:
    """Pipeline should not save JSON report by default."""
    pipeline = MigrationPipeline(
        **pipeline_components,
    )

    pipeline.run(source_file)

    pipeline_components[
        "output_manager"
    ].save_report.assert_not_called()


def test_pipeline_rejects_missing_source(
    tmp_path: Path,
    pipeline_components,
) -> None:
    """Reject a missing source file."""
    pipeline = MigrationPipeline(
        **pipeline_components,
    )

    missing_source = tmp_path / "missing.py"

    with pytest.raises(
        FileNotFoundError,
        match="Source file not found",
    ):
        pipeline.run(missing_source)


def test_pipeline_cleans_workspace_on_success(
    source_file: Path,
    pipeline_components,
) -> None:
    """Workspace should be cleaned after successful execution."""
    pipeline = MigrationPipeline(
        **pipeline_components,
    )

    pipeline.run(source_file)

    pipeline_components[
        "workspace_manager"
    ].cleanup.assert_called_once()


def test_pipeline_cleans_workspace_on_failure(
    source_file: Path,
    pipeline_components,
) -> None:
    """Workspace should be cleaned even when pipeline fails."""
    pipeline_components[
        "translator"
    ].translate.side_effect = RuntimeError(
        "Translation failed"
    )

    pipeline = MigrationPipeline(
        **pipeline_components,
    )

    with pytest.raises(RuntimeError):
        pipeline.run(source_file)

    pipeline_components[
        "workspace_manager"
    ].cleanup.assert_called_once()


def test_pipeline_adds_leaderboard_entry(
    source_file: Path,
    pipeline_components,
) -> None:
    """Pipeline should add migration results to the leaderboard."""
    pipeline = MigrationPipeline(
        **pipeline_components,
    )

    pipeline.run(source_file)

    leaderboard = pipeline_components["leaderboard"]

    leaderboard.add.assert_called_once()

    entry = leaderboard.add.call_args.args[0]

    assert entry.provider_name == "MockProvider"
    assert entry.model_name == "MockModel"
    assert entry.benchmark_time == 0.25
    assert entry.execution_time == 0.25
    assert entry.overall_success is True


def test_pipeline_rejects_empty_translation(
    source_file: Path,
    pipeline_components,
) -> None:
    """Reject empty generated C++ code."""
    pipeline_components[
        "translator"
    ].translate.return_value = ""

    pipeline = MigrationPipeline(
        **pipeline_components,
    )

    with pytest.raises(
        ValidationError,
        match="Generated C\\+\\+ code is empty",
    ):
        pipeline.run(source_file)

    pipeline_components[
        "compiler"
    ].compile.assert_not_called()


def test_pipeline_stops_after_compilation_failure(
    source_file: Path,
    pipeline_components,
) -> None:
    """Pipeline should stop when compilation fails."""
    pipeline_components[
        "compiler"
    ].compile.side_effect = RuntimeError(
        "Compilation failed"
    )

    pipeline = MigrationPipeline(
        **pipeline_components,
    )

    with pytest.raises(RuntimeError):
        pipeline.run(source_file)

    pipeline_components[
        "benchmark"
    ].benchmark.assert_not_called()

    pipeline_components[
        "workspace_manager"
    ].cleanup.assert_called_once()


def test_pipeline_stops_after_benchmark_failure(
    source_file: Path,
    pipeline_components,
) -> None:
    """Pipeline should stop when benchmarking fails."""
    pipeline_components[
        "benchmark"
    ].benchmark.side_effect = RuntimeError(
        "Execution failed"
    )

    pipeline = MigrationPipeline(
        **pipeline_components,
    )

    with pytest.raises(RuntimeError):
        pipeline.run(source_file)

    pipeline_components[
        "evaluator"
    ].evaluate.assert_not_called()

    pipeline_components[
        "report_generator"
    ].generate.assert_not_called()

    pipeline_components[
        "workspace_manager"
    ].cleanup.assert_called_once()