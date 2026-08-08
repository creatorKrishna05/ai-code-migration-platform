from __future__ import annotations

from config import DEFAULT_PROVIDER
from providers.base_provider import BaseProvider
from providers.groq_provider import GroqProvider
from providers.ollama_provider import OllamaProvider
from utils.exceptions import ConfigurationError


def create_provider(
    provider_name: str | None = None,
    model_name: str | None = None,
) -> BaseProvider:
    """
    Create and return the requested LLM provider.

    Args:
        provider_name:
            Optional provider name. If omitted, the configured
            default provider is used.
        model_name:
            Optional model override. Uses the provider default
            when omitted.

    Returns:
        Configured provider instance.

    Raises:
        ConfigurationError:
            If the requested provider is unsupported or empty.
    """
    selected_provider = (
        provider_name
        if provider_name is not None
        else DEFAULT_PROVIDER
    )

    if not selected_provider or not selected_provider.strip():
        raise ConfigurationError(
            "Provider name cannot be empty."
        )

    selected_provider = selected_provider.strip().lower()

    if selected_provider == "groq":
        return GroqProvider(
            model_name=model_name,
        )

    if selected_provider == "ollama":
        return OllamaProvider(
            model_name=model_name,
        )

    raise ConfigurationError(
        f"Unsupported provider: {selected_provider}"
    )