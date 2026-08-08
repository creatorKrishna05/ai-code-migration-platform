import pytest

import config


def test_validate_configuration_success() -> None:
    """Accept the current valid configuration."""
    config.validate_configuration()


def test_validate_configuration_rejects_invalid_provider(
    monkeypatch,
) -> None:
    """Reject an unregistered default provider."""
    monkeypatch.setattr(
        config,
        "DEFAULT_PROVIDER",
        "invalid-provider",
    )

    with pytest.raises(
        ValueError,
        match="is not registered",
    ):
        config.validate_configuration()


def test_validate_configuration_rejects_disabled_provider(
    monkeypatch,
) -> None:
    """Reject a disabled default provider."""
    monkeypatch.setattr(
        config,
        "DEFAULT_PROVIDER",
        "openai",
    )

    with pytest.raises(
        ValueError,
        match="is disabled",
    ):
        config.validate_configuration()


def test_validate_configuration_rejects_invalid_model(
    monkeypatch,
) -> None:
    """Reject an unregistered default model."""
    monkeypatch.setattr(
        config,
        "DEFAULT_MODEL",
        "invalid-model",
    )

    with pytest.raises(
        ValueError,
        match="is not registered",
    ):
        config.validate_configuration()


def test_validate_configuration_rejects_empty_compiler(
    monkeypatch,
) -> None:
    """Reject an empty C++ compiler."""
    monkeypatch.setattr(
        config,
        "CPP_COMPILER",
        "",
    )

    with pytest.raises(
        ValueError,
        match="CPP_COMPILER cannot be empty",
    ):
        config.validate_configuration()


def test_validate_configuration_rejects_invalid_benchmark_runs(
    monkeypatch,
) -> None:
    """Reject non-positive benchmark runs."""
    monkeypatch.setattr(
        config,
        "BENCHMARK_RUNS",
        0,
    )

    with pytest.raises(
        ValueError,
        match="BENCHMARK_RUNS must be greater than zero",
    ):
        config.validate_configuration()


def test_validate_configuration_rejects_negative_warmup_runs(
    monkeypatch,
) -> None:
    """Reject negative benchmark warmup runs."""
    monkeypatch.setattr(
        config,
        "BENCHMARK_WARMUP_RUNS",
        -1,
    )

    with pytest.raises(
        ValueError,
        match="BENCHMARK_WARMUP_RUNS cannot be negative",
    ):
        config.validate_configuration()


def test_validate_configuration_rejects_invalid_timeout(
    monkeypatch,
) -> None:
    """Reject non-positive execution timeout."""
    monkeypatch.setattr(
        config,
        "EXECUTION_TIMEOUT_SECONDS",
        0,
    )

    with pytest.raises(
        ValueError,
        match="EXECUTION_TIMEOUT_SECONDS must be greater than zero",
    ):
        config.validate_configuration()