from __future__ import annotations

from typing import Optional

from groq import Groq

from config import (
    GROQ_API_KEY,
    MODELS,
)

print(
    "GROQ PROVIDER IMPORT KEY:",
    GROQ_API_KEY[:10],
    len(GROQ_API_KEY),
)
from providers.base_provider import BaseProvider
from utils.logger import get_logger
from utils.exceptions import ProviderError


class GroqProvider(BaseProvider):
    """
    Groq implementation of the BaseProvider interface.
    """

    def __init__(
        self,
        model_name: str | None = None,
    ) -> None:
        """
        Initialize the Groq provider.

        Raises:
            ProviderError:
                If the Groq API key or model name is invalid.
        """
        self._logger = get_logger(__name__)

        self._provider_name = "Groq"

        if not GROQ_API_KEY.strip():
            raise ProviderError(
                "GROQ_API_KEY is not configured."
            )

        self._model_name = (
            model_name.strip()
            if model_name is not None
            else next(
                iter(MODELS["groq"].values())
            )
        )

        if not self._model_name:
            raise ProviderError(
                "Groq model name cannot be empty."
            )

        self._logger.info(
            "Groq key prefix: %s | length: %s",
            GROQ_API_KEY[:10],
            len(GROQ_API_KEY),
        )

        self._client = Groq(
            api_key=GROQ_API_KEY,
        )

        self._logger.info(
            "Initialized %s provider with model '%s'.",
            self._provider_name,
            self._model_name,
        )

    @property
    def provider_name(self) -> str:
        """
        Return the provider name.

        Returns:
            Human-readable provider name.
        """
        return self._provider_name

    @property
    def model_name(self) -> str:
        """
        Return the active model name.

        Returns:
            Active model identifier.
        """
        return self._model_name

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a response using the Groq model.
        """
        if not system_prompt.strip():
            raise ProviderError("System prompt cannot be empty.")

        if not user_prompt.strip():
            raise ProviderError("User prompt cannot be empty.")

        self._logger.info(
            "Generating response using %s model.",
            self._model_name,
        )

        try:
            response = self._client.chat.completions.create(
                model=self._model_name,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=temperature,
                max_completion_tokens=max_tokens,
            )
        except Exception as exc:
            self._logger.exception(
                "Groq generation failed."
            )

            raise ProviderError(
                "Failed to generate response from Groq provider."
            ) from exc

        if not response.choices:
            raise ProviderError(
                "Groq returned an empty response."
            )

        content = response.choices[0].message.content

        if not content:
            raise ProviderError(
                "Groq response content is empty."
            )

        self._logger.info(
            "Successfully generated response using %s.",
            self._model_name,
        )

        return content