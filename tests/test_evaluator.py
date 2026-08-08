import pytest

from evaluator.evaluator import Evaluator
from utils.exceptions import EvaluationError


def test_evaluator_initializes() -> None:
    """Evaluator should initialize successfully."""
    evaluator = Evaluator()

    assert evaluator is not None


def test_evaluate_returns_all_results() -> None:
    """Evaluation should contain all migration results."""
    evaluator = Evaluator()

    result = evaluator.evaluate(
        translation_success=True,
        compilation_success=True,
        execution_success=True,
        execution_time=0.25,
        benchmark_time=0.20,
    )

    assert result["translation_success"] is True
    assert result["compilation_success"] is True
    assert result["execution_success"] is True
    assert result["execution_time"] == 0.25
    assert result["benchmark_time"] == 0.20


def test_evaluate_marks_overall_success_when_all_succeed() -> None:
    """Overall success should be true when every stage succeeds."""
    evaluator = Evaluator()

    result = evaluator.evaluate(
        translation_success=True,
        compilation_success=True,
        execution_success=True,
        execution_time=0.1,
        benchmark_time=0.08,
    )

    assert result["overall_success"] is True


@pytest.mark.parametrize(
    "translation_success, compilation_success, execution_success",
    [
        (False, True, True),
        (True, False, True),
        (True, True, False),
        (False, False, False),
    ],
)
def test_evaluate_marks_overall_failure(
    translation_success: bool,
    compilation_success: bool,
    execution_success: bool,
) -> None:
    """Overall success should be false when any stage fails."""
    evaluator = Evaluator()

    result = evaluator.evaluate(
        translation_success=translation_success,
        compilation_success=compilation_success,
        execution_success=execution_success,
        execution_time=0.1,
        benchmark_time=0.08,
    )

    assert result["overall_success"] is False


def test_evaluate_preserves_execution_times() -> None:
    """Evaluation should preserve execution and benchmark times."""
    evaluator = Evaluator()

    result = evaluator.evaluate(
        translation_success=True,
        compilation_success=True,
        execution_success=True,
        execution_time=1.234567,
        benchmark_time=0.987654,
    )

    assert result["execution_time"] == 1.234567
    assert result["benchmark_time"] == 0.987654


def test_evaluate_returns_expected_keys() -> None:
    """Evaluation should return the expected result structure."""
    evaluator = Evaluator()

    result = evaluator.evaluate(
        translation_success=True,
        compilation_success=True,
        execution_success=True,
        execution_time=0.5,
        benchmark_time=0.4,
    )

    assert set(result.keys()) == {
        "translation_success",
        "compilation_success",
        "execution_success",
        "execution_time",
        "benchmark_time",
        "overall_success",
    }