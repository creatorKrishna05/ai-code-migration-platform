from __future__ import annotations

from pathlib import Path

from config import MODELS, PROVIDERS
from utils.exceptions import ValidationError


class CLIValidationError(ValidationError):
    """
    Raised when CLI input validation fails.
    """


class CLIValidator:
    """
    Validate command-line interface inputs.
    """

    def validate_provider(
        self,
        provider: str,
    ) -> str:
        """
        Validate the selected LLM provider.

        Args:
            provider: Provider name supplied through the CLI.

        Returns:
            Validated provider name.

        Raises:
            CLIValidationError: If the provider is unsupported
                or disabled.
        """
        if not provider or not provider.strip():
            raise CLIValidationError(
                "Provider cannot be empty."
            )

        provider = provider.strip().lower()

        if provider not in MODELS:
            supported = ", ".join(
                sorted(MODELS.keys())
            )
            raise CLIValidationError(
                f"Unsupported provider '{provider}'. "
                f"Supported providers: {supported}."
            )

        provider_config = PROVIDERS.get(provider)

        if provider_config is None:
            raise CLIValidationError(
                f"Provider '{provider}' is not configured."
            )

        if not provider_config.get("enabled", False):
            raise CLIValidationError(
                f"Provider '{provider}' is currently disabled."
            )

        return provider

    def validate_model(
        self,
        provider: str,
        model: str,
    ) -> str:
        """
        Validate the selected model for a provider.

        Args:
            provider: Provider name.
            model: Model identifier or display name.

        Returns:
            Provider model identifier.

        Raises:
            CLIValidationError: If the model is not registered.
        """
        if not model or not model.strip():
            raise CLIValidationError(
                "Model cannot be empty."
            )

        provider = self.validate_provider(provider)
        model = model.strip()

        provider_models = MODELS[provider]

        if model in provider_models:
            return provider_models[model]

        if model in provider_models.values():
            return model

        available_models = ", ".join(
            sorted(provider_models.keys())
        )

        raise CLIValidationError(
            f"Model '{model}' is not available for "
            f"provider '{provider}'. "
            f"Available models: {available_models}."
        )

    def validate_source_path(
        self,
        source_path: str,
    ) -> Path:
        """
        Validate the Python source file path.

        Args:
            source_path: Path to the Python source file.

        Returns:
            Validated source file path.

        Raises:
            CLIValidationError: If the source path is invalid.
        """
        if not source_path or not source_path.strip():
            raise CLIValidationError(
                "Source file path cannot be empty."
            )

        path = Path(source_path.strip())

        if not path.exists():
            raise CLIValidationError(
                f"Source file does not exist: {path}"
            )

        if not path.is_file():
            raise CLIValidationError(
                f"Source path is not a file: {path}"
            )

        if path.suffix.lower() != ".py":
            raise CLIValidationError(
                f"Source file must have a .py extension: {path}"
            )

        return path

    def validate_output_path(
        self,
        output_path: str,
    ) -> Path:
        """
        Validate the generated C++ output path.

        Args:
            output_path: Output path supplied through the CLI.

        Returns:
            Validated output path.

        Raises:
            CLIValidationError: If the path is empty.
        """
        if not output_path or not output_path.strip():
            raise CLIValidationError(
                "Output path cannot be empty."
            )

        return Path(output_path.strip())

    def validate_benchmark_runs(
        self,
        benchmark_runs: int,
    ) -> int:
        """
        Validate the number of benchmark runs.

        Args:
            benchmark_runs: Number of benchmark iterations.

        Returns:
            Validated benchmark run count.

        Raises:
            CLIValidationError: If the value is not positive.
        """
        if benchmark_runs <= 0:
            raise CLIValidationError(
                "Benchmark runs must be greater than zero."
            )

        return benchmark_runs

    def validate_timeout(
        self,
        timeout: float,
    ) -> float:
        """
        Validate execution timeout.

        Args:
            timeout: Maximum execution time in seconds.

        Returns:
            Validated timeout.

        Raises:
            CLIValidationError: If the value is not positive.
        """
        if timeout <= 0:
            raise CLIValidationError(
                "Timeout must be greater than zero."
            )

        return timeout

    def validate_report_path(
        self,
        report_path: str | None,
    ) -> Path | None:
        """
        Validate the optional JSON report path.

        Args:
            report_path: Optional report output path.

        Returns:
            Validated report path or None.

        Raises:
            CLIValidationError: If the path is empty.
        """
        if report_path is None:
            return None

        if not report_path.strip():
            raise CLIValidationError(
                "Report path cannot be empty."
            )

        return Path(report_path.strip())