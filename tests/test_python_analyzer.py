from __future__ import annotations

import pytest

from analyzer.python_analyzer import (
    PythonAnalysis,
    PythonAnalyzer,
)
from utils.exceptions import ValidationError


@pytest.fixture
def analyzer() -> PythonAnalyzer:
    """Provide a PythonAnalyzer instance."""
    return PythonAnalyzer()


def test_analyze_basic_source(
    analyzer: PythonAnalyzer,
) -> None:
    """Test analysis of basic Python source."""
    source_code = """
x = 10
y = 20
result = x + y
"""

    result = analyzer.analyze(source_code)

    assert isinstance(result, PythonAnalysis)
    assert result.lines_of_code == 3
    assert result.function_count == 0
    assert result.class_count == 0
    assert result.import_count == 0
    assert result.loop_count == 0
    assert result.conditional_count == 0
    assert result.exception_count == 0
    assert result.complexity == 1


def test_analyze_functions_and_classes(
    analyzer: PythonAnalyzer,
) -> None:
    """Test function and class detection."""
    source_code = """
def first():
    pass


async def second():
    pass


class Example:
    def method(self):
        pass
"""

    result = analyzer.analyze(source_code)

    assert result.function_count == 3
    assert result.class_count == 1


def test_analyze_imports(
    analyzer: PythonAnalyzer,
) -> None:
    """Test import and from-import detection."""
    source_code = """
import os
import sys
from pathlib import Path
from typing import Optional
"""

    result = analyzer.analyze(source_code)

    assert result.import_count == 4


def test_analyze_loops(
    analyzer: PythonAnalyzer,
) -> None:
    """Test synchronous, asynchronous, and while loops."""
    source_code = """
for item in items:
    print(item)

while condition:
    condition = False


async def process():
    async for item in items:
        print(item)
"""

    result = analyzer.analyze(source_code)

    assert result.loop_count == 3


def test_analyze_conditionals(
    analyzer: PythonAnalyzer,
) -> None:
    """Test conditional statement detection."""
    source_code = """
if value > 10:
    result = 1
elif value > 5:
    result = 2
else:
    result = 3

if another_value:
    result += 1
"""

    result = analyzer.analyze(source_code)

    assert result.conditional_count == 3


def test_analyze_exceptions(
    analyzer: PythonAnalyzer,
) -> None:
    """Test try and raise detection."""
    source_code = """
try:
    result = 10 / value
except ZeroDivisionError:
    raise ValueError("Invalid value")
"""

    result = analyzer.analyze(source_code)

    assert result.exception_count == 2


def test_analyze_complexity(
    analyzer: PythonAnalyzer,
) -> None:
    """Test cyclomatic-style structural complexity."""
    source_code = """
def process(items):
    for item in items:
        if item > 10:
            try:
                print(item)
            except ValueError:
                raise RuntimeError("error")
"""

    result = analyzer.analyze(source_code)

    assert result.loop_count == 1
    assert result.conditional_count == 1
    assert result.exception_count == 2
    assert result.complexity == 5


def test_analyze_empty_source_raises_validation_error(
    analyzer: PythonAnalyzer,
) -> None:
    """Test that empty source raises ValidationError."""
    with pytest.raises(
        ValidationError,
        match="Source code cannot be empty.",
    ):
        analyzer.analyze("")


def test_analyze_whitespace_only_source_raises_validation_error(
    analyzer: PythonAnalyzer,
) -> None:
    """Test that whitespace-only source raises ValidationError."""
    with pytest.raises(
        ValidationError,
        match="Source code cannot be empty.",
    ):
        analyzer.analyze("   \n\t  \n")


def test_analyze_invalid_source_raises_validation_error(
    analyzer: PythonAnalyzer,
) -> None:
    """Test that invalid Python raises ValidationError."""
    source_code = """
def broken(
    print("invalid")
"""

    with pytest.raises(
        ValidationError,
        match="Invalid Python source code.",
    ):
        analyzer.analyze(source_code)


def test_analyze_counts_non_empty_lines_only(
    analyzer: PythonAnalyzer,
) -> None:
    """Test that blank lines are excluded from LOC."""
    source_code = """
import os

def hello():

    print("hello")


hello()
"""

    result = analyzer.analyze(source_code)

    assert result.lines_of_code == 4