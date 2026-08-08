from __future__ import annotations

from providers.base_provider import BaseProvider
from providers.provider_factory import create_provider
from utils.exceptions import (
    ValidationError,
    TranslationError,
)

from translator.prompt_builder import (
    build_translation_prompts,
)

from utils.logger import get_logger


class Translator:
    """
    Coordinate the complete code translation workflow.
    """

    def __init__(
        self,
        provider: BaseProvider | None = None,
    ) -> None:
        """
        Initialize the translator.

        Args:
            provider:
                Optional provider implementation.
                If not supplied, the configured provider
                is created automatically.
        """
        self._logger = get_logger(__name__)

        self._provider = (
            provider
            if provider is not None
            else create_provider()
        )

    @property
    def provider_name(self) -> str:
        """
        Return the active provider name.
        """
        return self._provider.provider_name


    @property
    def model_name(self) -> str:
        """
        Return the active model name.
        """
        return self._provider.model_name

    def translate(
        self,
        source_code: str,
    ) -> str:

        self._logger.info(
            "Starting code translation."
        )

        if not source_code.strip():
            self._logger.error(
                "Source code is empty."
            )

            raise ValidationError(
                "Source code cannot be empty."
            )

        system_prompt, user_prompt = build_translation_prompts(
            source_code
        )
        self._logger.info(
            "Sending translation request to %s.",
            self._provider.provider_name,
        )

        try:
            translation_result = self._provider.generate(
                system_prompt,
                user_prompt,
            )

        except TranslationError:
            raise
        
        except Exception as exc:
            self._logger.exception(
                "Translation failed during provider execution."
            )

            raise TranslationError(
                "Code translation failed."
            ) from exc
        
        if not translation_result.strip():
            self._logger.error(
                "Provider returned an empty translation."
            )

            raise TranslationError(
                "Generated translation is empty."
            )

        translation_result = (
            translation_result
            .replace("```cpp", "")
            .replace("```c++", "")
            .replace("```", "")
            .strip()
        )

        if not translation_result:
            self._logger.error(
                "Translation became empty after response cleaning."
            )

            raise TranslationError(
                "Generated translation is empty after cleaning."
            )

        self._logger.info(
            "Code translation completed successfully."
        )
        
        return translation_result


            