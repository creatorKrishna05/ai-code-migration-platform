from __future__ import annotations

import re

from utils.exceptions import TranslationError
from utils.logger import get_logger

class ResponseCleaner:
    """
    Clean and sanitize raw LLM responses before compilation.
    """

    def __init__(self) -> None:
        """
        Initialize the response cleaner.
        """
        self._logger = get_logger(__name__)

    def clean(
        self,
        response: str,
    ) -> str:
        """
        Return a sanitized C++ source code string.

        Args:
            response:
                Raw response returned by the LLM.

        Returns:
            Clean C++ source code.
        """

        self._logger.debug(
            "Cleaning LLM response."
        )
        
        response = self._remove_explanation(
            response
        )

        response = self._validate(
            response
        )

        return response

    def _remove_markdown(
            self,
            response: str,
    ) -> str:
        """
        Remove Markdown code fences
        from an LLM response.

        Args:
            response:
                Raw LLM response.

        Returns:
            Response without code fences.
        """

        self._logger.debug(
            "Removing Markdown code fences."
        )

        cleaned_response = (
            response
            .replace(
                "```cpp",
                "",
            )
            .replace(
                "```c++",
                "",
            )
            .replace(
                "```",
                "",
            )
        )

        return cleaned_response.strip()

    def _remove_thinking(
            self,
            response: str,
    ) -> str:
        """
        Remove reasoning blocks from 
        an LLM response.

        Args:
            response:
                Raw LLM response.

        Returns:
            Response without thinking blocks.
        """

        self._logger.debug(
            "Removing reasoning blocks."
        )

        cleaned_response = re.sub(
            r"<think>.*?</think>",
            "",
            response,
            flags=re.DOTALL,
        )

        return cleaned_response.strip()


    def _extract_cpp(
            self,
            response: str,
    ) -> str:
        """
        Extract C++ source code from
        an LLM response.

        Args:
            response:
                cleaned LLM response.

        Returns:
            Extracted C++ source code.
        """

        self._logger.debug(
            "Extracting C++ source code."
        )

        match = re.search(
            r"```(?:cpp|c\+\+)?(.*?)```",
            response,
            flags=re.DOTALL | re.IGNORECASE,
        )

        if match is not None:
            return match.group(1).strip()

        return response.strip()

    def _remove_explanation(
            self,
            response: str,
    ) -> str:
        """
        Remove explanatory text
        from an LLM response.

        Args:
            response:
                Extracted C++ source.

        Returns:
            Response without explanations.
        """

        self._logger.debug(
            "Removing explanatory text."
        )

        explanation_pattern = (
            r"\n\s*("
            r"Explanation|"
            r"Notes?|"
            r"Advantages?|"
            r"Summary|"
            r"Output|"
            r"This code|"
            r"The translated"
            r").*"
        )

        cleaned_response = re.sub(
            explanation_pattern,
            "",
            response,
            flags=re.IGNORECASE | re.DOTALL,
        )

        return cleaned_response.strip()


    def _validate(
        self,
        response: str,
    ) -> str:
        """
        Validate the cleaned C++ source code.

        Args:
            response:
                Cleaned response.

        Returns:
            Validated C++ source code.

        Raises:
            TranslationError:
                If the response does not
                appear to contain valid
                C++ code.
        """

        self._logger.debug(
            "Validating translated C++ code."
        )

        if not response.strip():
            raise TranslationError(
                "Generated C++ code is empty."
            )

        cpp_indicators = (
            "#include",
            "int main",
            "std::",
            "using namespace",
            "class",
            "template",
        )

        if not any(
            indicator in response
            for indicator in cpp_indicators
        ):
            raise TranslationError(
                "Generated response does not appear "
                "to contain valid C++ code."
            )

        self._logger.debug(
            "LLM response cleaned successfully."
        )

        return response