from unittest.mock import Mock

import pytest

import providers.ollama_provider as ollama_module
from providers.ollama_provider import OllamaProvider
from utils.exceptions import ProviderError, ValidationError


def test_ollama_provider_initializes(monkeypatch) -> None:
    """Initialize Ollama provider successfully."""
    monkeypatch.setattr(
        ollama_module,
        "OLLAMA_BASE_URL",
        "http://localhost:11434",
    )

    provider = OllamaProvider()

    assert provider.provider_name == "Ollama"
    assert provider.model_name == "llama3.2"


def test_ollama_provider_accepts_custom_model(
    monkeypatch,
) -> None:
    """Accept a custom model identifier."""
    monkeypatch.setattr(
        ollama_module,
        "OLLAMA_BASE_URL",
        "http://localhost:11434",
    )

    provider = OllamaProvider(
        model_name="qwen2.5-coder",
    )

    assert provider.model_name == "qwen2.5-coder"


def test_ollama_provider_rejects_empty_model(
    monkeypatch,
) -> None:
    """Reject an empty model name."""
    monkeypatch.setattr(
        ollama_module,
        "OLLAMA_BASE_URL",
        "http://localhost:11434",
    )

    with pytest.raises(
        ProviderError,
        match="Ollama model name cannot be empty",
    ):
        OllamaProvider(model_name="   ")


def test_ollama_provider_rejects_missing_base_url(
    monkeypatch,
) -> None:
    """Reject a missing Ollama base URL."""
    monkeypatch.setattr(
        ollama_module,
        "OLLAMA_BASE_URL",
        "",
    )

    with pytest.raises(
        ProviderError,
        match="OLLAMA_BASE_URL is not configured",
    ):
        OllamaProvider()


def test_ollama_provider_generates_response(
    monkeypatch,
) -> None:
    """Generate a response successfully."""
    monkeypatch.setattr(
        ollama_module,
        "OLLAMA_BASE_URL",
        "http://localhost:11434",
    )

    response = {
        "message": {
            "content": "Generated C++ code.",
        },
    }

    client = Mock()
    client.chat.return_value = response

    monkeypatch.setattr(
        ollama_module,
        "Client",
        lambda host: client,
    )

    provider = OllamaProvider()

    result = provider.generate(
        system_prompt="You are a translator.",
        user_prompt="Translate this Python code.",
    )

    assert result == "Generated C++ code."

    client.chat.assert_called_once()


def test_ollama_provider_rejects_empty_system_prompt(
    monkeypatch,
) -> None:
    """Reject an empty system prompt."""
    monkeypatch.setattr(
        ollama_module,
        "OLLAMA_BASE_URL",
        "http://localhost:11434",
    )

    provider = OllamaProvider()

    with pytest.raises(
        ValidationError,
        match="System prompt cannot be empty",
    ):
        provider.generate(
            system_prompt="   ",
            user_prompt="Translate this.",
        )


def test_ollama_provider_rejects_empty_user_prompt(
    monkeypatch,
) -> None:
    """Reject an empty user prompt."""
    monkeypatch.setattr(
        ollama_module,
        "OLLAMA_BASE_URL",
        "http://localhost:11434",
    )

    provider = OllamaProvider()

    with pytest.raises(
        ValidationError,
        match="User prompt cannot be empty",
    ):
        provider.generate(
            system_prompt="Translate.",
            user_prompt="   ",
        )


def test_ollama_provider_rejects_missing_message(
    monkeypatch,
) -> None:
    """Reject a response without a message."""
    monkeypatch.setattr(
        ollama_module,
        "OLLAMA_BASE_URL",
        "http://localhost:11434",
    )

    client = Mock()
    client.chat.return_value = {}

    monkeypatch.setattr(
        ollama_module,
        "Client",
        lambda host: client,
    )

    provider = OllamaProvider()

    with pytest.raises(
        ProviderError,
        match="does not contain a message",
    ):
        provider.generate(
            system_prompt="Translate.",
            user_prompt="Translate this.",
        )


def test_ollama_provider_rejects_empty_content(
    monkeypatch,
) -> None:
    """Reject a response with empty content."""
    monkeypatch.setattr(
        ollama_module,
        "OLLAMA_BASE_URL",
        "http://localhost:11434",
    )

    client = Mock()
    client.chat.return_value = {
        "message": {
            "content": "",
        },
    }

    monkeypatch.setattr(
        ollama_module,
        "Client",
        lambda host: client,
    )

    provider = OllamaProvider()

    with pytest.raises(
        ProviderError,
        match="Ollama response content is empty",
    ):
        provider.generate(
            system_prompt="Translate.",
            user_prompt="Translate this.",
        )


def test_ollama_provider_wraps_api_error(
    monkeypatch,
) -> None:
    """Wrap Ollama API failures in ProviderError."""
    monkeypatch.setattr(
        ollama_module,
        "OLLAMA_BASE_URL",
        "http://localhost:11434",
    )

    client = Mock()
    client.chat.side_effect = RuntimeError(
        "Connection failed"
    )

    monkeypatch.setattr(
        ollama_module,
        "Client",
        lambda host: client,
    )

    provider = OllamaProvider()

    with pytest.raises(
        ProviderError,
        match="Failed to generate response",
    ):
        provider.generate(
            system_prompt="Translate.",
            user_prompt="Translate this.",
        )