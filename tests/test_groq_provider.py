from unittest.mock import Mock

import pytest

import providers.groq_provider as groq_module
from providers.groq_provider import GroqProvider
from utils.exceptions import ProviderError


def test_groq_provider_initializes(monkeypatch) -> None:
    """Initialize Groq provider successfully."""
    monkeypatch.setattr(
        groq_module,
        "GROQ_API_KEY",
        "test-api-key",
    )

    provider = GroqProvider()

    assert provider.provider_name == "Groq"
    assert provider.model_name == (
        "llama-3.3-70b-versatile"
    )


def test_groq_provider_accepts_custom_model(
    monkeypatch,
) -> None:
    """Accept a custom model identifier."""
    monkeypatch.setattr(
        groq_module,
        "GROQ_API_KEY",
        "test-api-key",
    )

    provider = GroqProvider(
        model_name="custom-model",
    )

    assert provider.model_name == "custom-model"


def test_groq_provider_rejects_missing_api_key(
    monkeypatch,
) -> None:
    """Reject a missing Groq API key."""
    monkeypatch.setattr(
        groq_module,
        "GROQ_API_KEY",
        "",
    )

    with pytest.raises(
        ProviderError,
        match="GROQ_API_KEY is not configured",
    ):
        GroqProvider()


def test_groq_provider_rejects_empty_model(
    monkeypatch,
) -> None:
    """Reject an empty model name."""
    monkeypatch.setattr(
        groq_module,
        "GROQ_API_KEY",
        "test-api-key",
    )

    with pytest.raises(
        ProviderError,
        match="Groq model name cannot be empty",
    ):
        GroqProvider(model_name="   ")


def test_groq_provider_generates_response(
    monkeypatch,
) -> None:
    """Generate a response successfully."""
    monkeypatch.setattr(
        groq_module,
        "GROQ_API_KEY",
        "test-api-key",
    )

    message = Mock()
    message.content = "Generated C++ code."

    response = Mock()
    response.choices = [Mock(message=message)]

    client = Mock()
    client.chat.completions.create.return_value = response

    monkeypatch.setattr(
        groq_module,
        "Groq",
        lambda api_key: client,
    )

    provider = GroqProvider()

    result = provider.generate(
        system_prompt="You are a translator.",
        user_prompt="Translate this Python code.",
    )

    assert result == "Generated C++ code."

    client.chat.completions.create.assert_called_once()


def test_groq_provider_rejects_empty_system_prompt(
    monkeypatch,
) -> None:
    """Reject an empty system prompt."""
    monkeypatch.setattr(
        groq_module,
        "GROQ_API_KEY",
        "test-api-key",
    )

    provider = GroqProvider()

    with pytest.raises(
        ProviderError,
        match="System prompt cannot be empty",
    ):
        provider.generate(
            system_prompt="   ",
            user_prompt="Translate this.",
        )


def test_groq_provider_rejects_empty_user_prompt(
    monkeypatch,
) -> None:
    """Reject an empty user prompt."""
    monkeypatch.setattr(
        groq_module,
        "GROQ_API_KEY",
        "test-api-key",
    )

    provider = GroqProvider()

    with pytest.raises(
        ProviderError,
        match="User prompt cannot be empty",
    ):
        provider.generate(
            system_prompt="Translate.",
            user_prompt="   ",
        )


def test_groq_provider_rejects_empty_choices(
    monkeypatch,
) -> None:
    """Reject a response without choices."""
    monkeypatch.setattr(
        groq_module,
        "GROQ_API_KEY",
        "test-api-key",
    )

    response = Mock()
    response.choices = []

    client = Mock()
    client.chat.completions.create.return_value = response

    monkeypatch.setattr(
        groq_module,
        "Groq",
        lambda api_key: client,
    )

    provider = GroqProvider()

    with pytest.raises(
        ProviderError,
        match="Groq returned an empty response",
    ):
        provider.generate(
            system_prompt="Translate.",
            user_prompt="Translate this.",
        )


def test_groq_provider_rejects_empty_content(
    monkeypatch,
) -> None:
    """Reject a response with empty content."""
    monkeypatch.setattr(
        groq_module,
        "GROQ_API_KEY",
        "test-api-key",
    )

    message = Mock()
    message.content = ""

    response = Mock()
    response.choices = [Mock(message=message)]

    client = Mock()
    client.chat.completions.create.return_value = response

    monkeypatch.setattr(
        groq_module,
        "Groq",
        lambda api_key: client,
    )

    provider = GroqProvider()

    with pytest.raises(
        ProviderError,
        match="Groq response content is empty",
    ):
        provider.generate(
            system_prompt="Translate.",
            user_prompt="Translate this.",
        )


def test_groq_provider_wraps_api_error(
    monkeypatch,
) -> None:
    """Wrap Groq API failures in ProviderError."""
    monkeypatch.setattr(
        groq_module,
        "GROQ_API_KEY",
        "test-api-key",
    )

    client = Mock()
    client.chat.completions.create.side_effect = (
        RuntimeError("API failure")
    )

    monkeypatch.setattr(
        groq_module,
        "Groq",
        lambda api_key: client,
    )

    provider = GroqProvider()

    with pytest.raises(
        ProviderError,
        match="Failed to generate response",
    ):
        provider.generate(
            system_prompt="Translate.",
            user_prompt="Translate this.",
        )