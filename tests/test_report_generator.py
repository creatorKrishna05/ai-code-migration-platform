from typing import Any

from report.report_generator import ReportGenerator


def test_report_generator_initializes() -> None:
    """Report generator should initialize successfully."""
    generator = ReportGenerator()

    assert generator is not None


def test_generate_preserves_evaluation_data() -> None:
    """Generated report should preserve evaluation results."""
    generator = ReportGenerator()

    evaluation: dict[str, Any] = {
        "translation_success": True,
        "compilation_success": True,
        "execution_success": True,
        "execution_time": 0.25,
        "benchmark_time": 0.20,
        "overall_success": True,
    }

    report = generator.generate(evaluation)

    for key, value in evaluation.items():
        assert report[key] == value


def test_generate_adds_generated_at() -> None:
    """Generated report should contain a timestamp."""
    generator = ReportGenerator()

    evaluation = {
        "overall_success": True,
    }

    report = generator.generate(evaluation)

    assert "generated_at" in report
    assert isinstance(report["generated_at"], str)
    assert report["generated_at"]


def test_generate_does_not_modify_original_evaluation() -> None:
    """Report generation should not mutate the input dictionary."""
    generator = ReportGenerator()

    evaluation = {
        "overall_success": True,
        "execution_time": 0.5,
    }

    original = dict(evaluation)

    generator.generate(evaluation)

    assert evaluation == original
    assert "generated_at" not in evaluation


def test_generate_returns_new_dictionary() -> None:
    """Generated report should be a new dictionary."""
    generator = ReportGenerator()

    evaluation = {
        "overall_success": True,
    }

    report = generator.generate(evaluation)

    assert report is not evaluation