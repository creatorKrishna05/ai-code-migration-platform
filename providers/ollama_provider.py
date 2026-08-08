from __future__ import annotations

from typing import Optional

from ollama import Client

from config import (
    MODELS,
    OLLAMA_BASE_URL,
)
from providers.base_provider import BaseProvider
from utils.exceptions import (
    ProviderError,
    ValidationError,
)
from utils.logger import get_logger


class OllamaProvider(BaseProvider):
    """
    Ollama implementation of the BaseProvider interface.
    """

    def __init__(
        self,
        model_name: str | None = None,
    ) -> None:
        """
        Initialize the Ollama provider.

        Raises:
            ProviderError:
                If the Ollama configuration is invalid.
        """
        self._logger = get_logger(__name__)

        self._provider_name = "Ollama"

        self._model_name = (
            model_name.strip()
            if model_name is not None
            else next(
                iter(MODELS["ollama"].values())
            )
        )

        if not self._model_name:
            raise ProviderError(
                "Ollama model name cannot be empty."
            )

        if not OLLAMA_BASE_URL.strip():
            raise ProviderError(
                "OLLAMA_BASE_URL is not configured."
            )

        self._client = Client(
            host=OLLAMA_BASE_URL,
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
        Generate a response using the Ollama model.

        Args:
            system_prompt:
                Instructions that define the model behavior.

            user_prompt:
                User request sent to the model.

            temperature:
                Sampling temperature.

            max_tokens:
                Maximum number of tokens to generate.

        Returns:
            Model-generated response.
        """
        if not system_prompt.strip():
            raise ValidationError(
                "System prompt cannot be empty."
            )

        if not user_prompt.strip():
            raise ValidationError(
                "User prompt cannot be empty."
            )

        self._logger.info(
            "Generating response using %s model.",
            self._model_name,
        )

        try:
            response = self._client.chat(
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
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens,
                },
            )

        except Exception as exc:
            self._logger.exception(
                "Ollama generation failed."
            )

            raise ProviderError(
                "Failed to generate response from Ollama provider."
            ) from exc

        message = response.get("message")

        if message is None:
            raise ProviderError(
                "Ollama response does not contain a message."
            )

        content = message.get("content")

        if not content:
            raise ProviderError(
                "Ollama response content is empty."
            )

        self._logger.info(
            "Successfully generated response using %s.",
            self._model_name,
        )

        return content