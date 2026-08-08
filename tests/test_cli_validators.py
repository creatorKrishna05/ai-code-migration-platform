from pathlib import Path

import pytest

from cli.validators import CLIValidationError, CLIValidator


@pytest.fixture
def validator() -> CLIValidator:
    """Return a CLI validator instance."""
    return CLIValidator()


def test_validate_provider_success(
    validator: CLIValidator,
) -> None:
    """Validate an enabled provider."""
    assert validator.validate_provider("groq") == "groq"


def test_validate_provider_normalizes_input(
    validator: CLIValidator,
) -> None:
    """Normalize provider whitespace and casing."""
    assert validator.validate_provider("  GROQ  ") == "groq"


def test_validate_provider_rejects_empty(
    validator: CLIValidator,
) -> None:
    """Reject an empty provider."""
    with pytest.raises(
        CLIValidationError,
        match="Provider cannot be empty",
    ):
        validator.validate_provider("")


def test_validate_provider_rejects_unsupported(
    validator: CLIValidator,
) -> None:
    """Reject an unsupported provider."""
    with pytest.raises(
        CLIValidationError,
        match="Unsupported provider",
    ):
        validator.validate_provider("unknown")


def test_validate_provider_rejects_disabled(
    validator: CLIValidator,
) -> None:
    """Reject a disabled provider."""
    with pytest.raises(
        CLIValidationError,
        match="currently disabled",
    ):
        validator.validate_provider("openai")


def test_validate_model_accepts_display_name(
    validator: CLIValidator,
) -> None:
    """Resolve a model display name to its identifier."""
    assert (
        validator.validate_model(
            "groq",
            "Llama 3.3 70B",
        )
        == "llama-3.3-70b-versatile"
    )


def test_validate_model_accepts_model_identifier(
    validator: CLIValidator,
) -> None:
    """Accept a registered model identifier."""
    assert (
        validator.validate_model(
            "groq",
            "llama-3.3-70b-versatile",
        )
        == "llama-3.3-70b-versatile"
    )


def test_validate_model_rejects_unknown_model(
    validator: CLIValidator,
) -> None:
    """Reject a model not registered for the provider."""
    with pytest.raises(
        CLIValidationError,
        match="is not available",
    ):
        validator.validate_model(
            "groq",
            "unknown-model",
        )


def test_validate_model_rejects_empty_model(
    validator: CLIValidator,
) -> None:
    """Reject an empty model."""
    with pytest.raises(
        CLIValidationError,
        match="Model cannot be empty",
    ):
        validator.validate_model(
            "groq",
            "",
        )


def test_validate_output_path(
    validator: CLIValidator,
) -> None:
    """Validate and normalize an output path."""
    result = validator.validate_output_path(
        "  outputs  "
    )

    assert result == Path("outputs")


def test_validate_output_path_rejects_empty(
    validator: CLIValidator,
) -> None:
    """Reject an empty output path."""
    with pytest.raises(
        CLIValidationError,
        match="Output path cannot be empty",
    ):
        validator.validate_output_path("")


def test_validate_benchmark_runs_success(
    validator: CLIValidator,
) -> None:
    """Accept a positive benchmark run count."""
    assert validator.validate_benchmark_runs(5) == 5


def test_validate_benchmark_runs_rejects_zero(
    validator: CLIValidator,
) -> None:
    """Reject zero benchmark runs."""
    with pytest.raises(
        CLIValidationError,
        match="greater than zero",
    ):
        validator.validate_benchmark_runs(0)


def test_validate_benchmark_runs_rejects_negative(
    validator: CLIValidator,
) -> None:
    """Reject negative benchmark runs."""
    with pytest.raises(
        CLIValidationError,
        match="greater than zero",
    ):
        validator.validate_benchmark_runs(-1)


def test_validate_timeout_success(
    validator: CLIValidator,
) -> None:
    """Accept a positive timeout."""
    assert validator.validate_timeout(30) == 30


def test_validate_timeout_rejects_zero(
    validator: CLIValidator,
) -> None:
    """Reject zero timeout."""
    with pytest.raises(
        CLIValidationError,
        match="greater than zero",
    ):
        validator.validate_timeout(0)


def test_validate_timeout_rejects_negative(
    validator: CLIValidator,
) -> None:
    """Reject negative timeout."""
    with pytest.raises(
        CLIValidationError,
        match="greater than zero",
    ):
        validator.validate_timeout(-5)


def test_validate_source_path_success(
    validator: CLIValidator,
    tmp_path: Path,
) -> None:
    """Accept an existing Python source file."""
    source_file = tmp_path / "sample.py"
    source_file.write_text(
        "print(30)\n",
        encoding="utf-8",
    )

    result = validator.validate_source_path(
        str(source_file)
    )

    assert result == source_file


def test_validate_source_path_rejects_missing_file(
    validator: CLIValidator,
    tmp_path: Path,
) -> None:
    """Reject a source file that does not exist."""
    source_file = tmp_path / "missing.py"

    with pytest.raises(
        CLIValidationError,
        match="does not exist",
    ):
        validator.validate_source_path(
            str(source_file)
        )


def test_validate_source_path_rejects_directory(
    validator: CLIValidator,
    tmp_path: Path,
) -> None:
    """Reject a directory as a source file."""
    source_directory = tmp_path / "source"
    source_directory.mkdir()

    with pytest.raises(
        CLIValidationError,
        match="is not a file",
    ):
        validator.validate_source_path(
            str(source_directory)
        )


def test_validate_source_path_rejects_non_python_file(
    validator: CLIValidator,
    tmp_path: Path,
) -> None:
    """Reject a source file without a Python extension."""
    source_file = tmp_path / "sample.txt"
    source_file.write_text(
        "print(30)\n",
        encoding="utf-8",
    )

    with pytest.raises(
        CLIValidationError,
        match=r"\.py extension",
    ):
        validator.validate_source_path(
            str(source_file)
        )


def test_validate_report_path_none(
    validator: CLIValidator,
) -> None:
    """Allow an omitted report path."""
    assert validator.validate_report_path(None) is None


def test_validate_report_path_success(
    validator: CLIValidator,
) -> None:
    """Validate a report path."""
    result = validator.validate_report_path(
        "  report.json  "
    )

    assert result == Path("report.json")


def test_validate_report_path_rejects_empty(
    validator: CLIValidator,
) -> None:
    """Reject an empty report path."""
    with pytest.raises(
        CLIValidationError,
        match="Report path cannot be empty",
    ):
        validator.validate_report_path("   ")