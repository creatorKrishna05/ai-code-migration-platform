from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class BaseProvider(ABC):
    """
    Abstract base class for all LLM providers.

    Every provider implementation must expose:
    - Provider identification
    - Active model identification
    - Text generation capability
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Return the provider name.

        Returns:
            Human-readable provider name.
        """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Return the active model name.

        Returns:
            Model identifier.
        """

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a response from the language model.

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

        raise NotImplementedError