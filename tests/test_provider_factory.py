import pytest

from providers.groq_provider import GroqProvider
from providers.ollama_provider import OllamaProvider
from providers.provider_factory import create_provider
from utils.exceptions import ConfigurationError


def test_create_provider_uses_default_provider() -> None:
    """Create the configured default provider."""
    provider = create_provider()

    assert isinstance(provider, GroqProvider)


def test_create_groq_provider() -> None:
    """Create a Groq provider."""
    provider = create_provider(
        provider_name="groq",
    )

    assert isinstance(provider, GroqProvider)


def test_create_ollama_provider() -> None:
    """Create an Ollama provider."""
    provider = create_provider(
        provider_name="ollama",
    )

    assert isinstance(provider, OllamaProvider)


def test_create_provider_normalizes_name() -> None:
    """Normalize provider name before creation."""
    provider = create_provider(
        provider_name="  GROQ  ",
    )

    assert isinstance(provider, GroqProvider)


def test_create_provider_rejects_empty_name() -> None:
    """Reject an empty provider name."""
    with pytest.raises(
        ConfigurationError,
        match="Provider name cannot be empty",
    ):
        create_provider(
            provider_name="   ",
        )


def test_create_provider_rejects_unsupported_provider() -> None:
    """Reject an unsupported provider."""
    with pytest.raises(
        ConfigurationError,
        match="Unsupported provider",
    ):
        create_provider(
            provider_name="openai",
        )