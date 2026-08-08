from unittest.mock import Mock

import pytest

from translator.translator import Translator
from utils.exceptions import TranslationError, ValidationError


def create_mock_provider() -> Mock:
    """Create a mock LLM provider."""
    provider = Mock()
    provider.provider_name = "MockProvider"
    provider.model_name = "MockModel"
    return provider


def test_translator_initializes_with_provider() -> None:
    """Translator should accept a provider."""
    provider = create_mock_provider()

    translator = Translator(provider=provider)

    assert translator is not None


def test_translate_rejects_empty_source() -> None:
    """Reject empty source code."""
    provider = create_mock_provider()
    translator = Translator(provider=provider)

    with pytest.raises(
        ValidationError,
        match="Source code cannot be empty",
    ):
        translator.translate("   ")


def test_translate_generates_translation() -> None:
    """Generate translated C++ code."""
    provider = create_mock_provider()
    provider.generate.return_value = "int main() { return 0; }"

    translator = Translator(provider=provider)

    result = translator.translate(
        "print('hello')"
    )

    assert result == "int main() { return 0; }"
    provider.generate.assert_called_once()


def test_translate_builds_translation_prompts() -> None:
    """Translator should send prompts to the provider."""
    provider = create_mock_provider()
    provider.generate.return_value = "int main() { return 0; }"

    translator = Translator(provider=provider)

    translator.translate(
        "print('hello')"
    )

    args, _ = provider.generate.call_args

    assert args[0]
    assert args[1]


def test_translate_cleans_cpp_code_fence() -> None:
    """Remove C++ markdown code fences."""
    provider = create_mock_provider()
    provider.generate.return_value = (
        "```cpp\n"
        "int main() { return 0; }\n"
        "```"
    )

    translator = Translator(provider=provider)

    result = translator.translate(
        "print('hello')"
    )

    assert result == "int main() { return 0; }"


def test_translate_rejects_empty_provider_response() -> None:
    """Reject an empty provider response."""
    provider = create_mock_provider()
    provider.generate.return_value = "   "

    translator = Translator(provider=provider)

    with pytest.raises(
        TranslationError,
        match="Generated translation is empty",
    ):
        translator.translate(
            "print('hello')"
        )


def test_translate_rejects_response_empty_after_cleaning() -> None:
    """Reject a response that becomes empty after cleaning."""
    provider = create_mock_provider()
    provider.generate.return_value = "```cpp\n```"

    translator = Translator(provider=provider)

    with pytest.raises(
        TranslationError,
        match="Generated translation is empty after cleaning",
    ):
        translator.translate(
            "print('hello')"
        )


def test_translate_wraps_provider_error() -> None:
    """Wrap unexpected provider errors."""
    provider = create_mock_provider()
    provider.generate.side_effect = RuntimeError(
        "Provider unavailable"
    )

    translator = Translator(provider=provider)

    with pytest.raises(
        TranslationError,
        match="Code translation failed",
    ):
        translator.translate(
            "print('hello')"
        )


def test_translator_exposes_provider_name() -> None:
    """Translator should expose the active provider name."""
    provider = create_mock_provider()

    translator = Translator(provider=provider)

    assert translator.provider_name == "MockProvider"


def test_translator_exposes_model_name() -> None:
    """Translator should expose the active model name."""
    provider = create_mock_provider()

    translator = Translator(provider=provider)

    assert translator.model_name == "MockModel"