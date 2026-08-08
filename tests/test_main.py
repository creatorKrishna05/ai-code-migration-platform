from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import main


def test_main_success(monkeypatch) -> None:
    """Return zero when migration succeeds."""
    source_path = Path("example.py")

    args = SimpleNamespace(
        command="migrate",
        source=str(source_path),
        provider=None,
        model=None,
        output=None,
        benchmark_runs=None,
        timeout=None,
        report_json=False,
    )

    validator = Mock()
    validator.validate_provider.return_value = "groq"
    validator.validate_source_path.return_value = source_path

    pipeline = Mock()
    pipeline.run.return_value = {
        "overall_success": True,
    }

    monkeypatch.setattr(
        main,
        "parse_args",
        lambda: args,
    )
    monkeypatch.setattr(
        main,
        "CLIValidator",
        lambda: validator,
    )
    monkeypatch.setattr(
        main,
        "build_pipeline",
        lambda **kwargs: pipeline,
    )

    assert main.main() == 0

    validator.validate_provider.assert_called_once_with(
        "groq"
    )
    validator.validate_source_path.assert_called_once_with(
        str(source_path)
    )
    pipeline.run.assert_called_once_with(
        source_path
    )


def test_main_returns_two_for_cli_validation_error(
    monkeypatch,
) -> None:
    """Return exit code two for invalid CLI input."""
    args = SimpleNamespace(
        command="migrate",
        source="example.py",
        provider=None,
        model=None,
        output=None,
        benchmark_runs=None,
        timeout=None,
        report_json=False,
    )

    validator = Mock()
    validator.validate_provider.side_effect = (
        main.CLIValidationError(
            "Provider is invalid."
        )
    )

    monkeypatch.setattr(
        main,
        "parse_args",
        lambda: args,
    )
    monkeypatch.setattr(
        main,
        "CLIValidator",
        lambda: validator,
    )

    assert main.main() == 2


def test_main_returns_one_for_unexpected_error(
    monkeypatch,
) -> None:
    """Return exit code one for unexpected failures."""
    args = SimpleNamespace(
        command="migrate",
        source="example.py",
        provider=None,
        model=None,
        output=None,
        benchmark_runs=None,
        timeout=None,
        report_json=False,
    )

    validator = Mock()
    validator.validate_provider.side_effect = RuntimeError(
        "Unexpected failure."
    )

    monkeypatch.setattr(
        main,
        "parse_args",
        lambda: args,
    )
    monkeypatch.setattr(
        main,
        "CLIValidator",
        lambda: validator,
    )

    assert main.main() == 1


def test_main_passes_cli_options_to_pipeline(
    monkeypatch,
) -> None:
    """Pass optional CLI overrides to the pipeline."""
    source_path = Path("example.py")
    output_path = Path("custom_output")

    args = SimpleNamespace(
        command="migrate",
        source=str(source_path),
        provider="groq",
        model="Llama 3.3 70B",
        output=str(output_path),
        benchmark_runs=5,
        timeout=30,
        report_json=True,
    )

    validator = Mock()

    validator.validate_provider.return_value = "groq"
    validator.validate_model.return_value = (
        "llama-3.3-70b-versatile"
    )
    validator.validate_output_path.return_value = (
        output_path
    )
    validator.validate_benchmark_runs.return_value = 5
    validator.validate_timeout.return_value = 30
    validator.validate_source_path.return_value = source_path

    pipeline = Mock()
    pipeline.run.return_value = {
        "overall_success": True,
    }

    monkeypatch.setattr(
        main,
        "parse_args",
        lambda: args,
    )
    monkeypatch.setattr(
        main,
        "CLIValidator",
        lambda: validator,
    )
    monkeypatch.setattr(
        main,
        "build_pipeline",
        lambda **kwargs: pipeline,
    )

    assert main.main() == 0

    main.build_pipeline(
        provider_name="groq",
        model_name="llama-3.3-70b-versatile",
        output_directory=output_path,
        benchmark_runs=5,
        timeout=30,
        report_json=True,
    )

    pipeline.run.assert_called_once_with(
        source_path
    )