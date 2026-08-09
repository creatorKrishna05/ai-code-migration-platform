import pytest

from translator.response_cleaner import ResponseCleaner
from utils.exceptions import TranslationError


@pytest.fixture
def cleaner() -> ResponseCleaner:
    """Create a response cleaner."""
    return ResponseCleaner()


def test_clean_valid_cpp(cleaner: ResponseCleaner) -> None:
    """Accept valid C++ source."""
    response = """
#include <iostream>

int main() {
    std::cout << "hello";
    return 0;
}
"""

    result = cleaner.clean(response)

    assert result == response.strip()


def test_clean_removes_explanation(
    cleaner: ResponseCleaner,
) -> None:
    """Remove explanatory text after C++ source."""
    response = """#include <iostream>

int main() {
    return 0;
}

Explanation:
This program was translated from Python.
"""

    result = cleaner.clean(response)

    assert "int main()" in result
    assert "Explanation:" not in result
    assert "This program was translated" not in result


def test_clean_rejects_empty_response(
    cleaner: ResponseCleaner,
) -> None:
    """Reject an empty response."""
    with pytest.raises(
        TranslationError,
        match="Generated C\\+\\+ code is empty",
    ):
        cleaner.clean("   ")


def test_clean_rejects_invalid_response(
    cleaner: ResponseCleaner,
) -> None:
    """Reject a response that does not appear to be C++."""
    with pytest.raises(
        TranslationError,
        match="does not appear to contain valid C\\+\\+ code",
    ):
        cleaner.clean(
            "This is just an explanation."
        )