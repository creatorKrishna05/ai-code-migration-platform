import pytest

from cli.arguments import build_parser


def test_migrate_command_with_defaults() -> None:
    """Parse the minimum valid migrate command."""
    parser = build_parser()

    args = parser.parse_args(
        ["migrate", "example.py"]
    )

    assert args.command == "migrate"
    assert args.source == "example.py"
    assert args.provider is None
    assert args.model is None
    assert args.output is None
    assert args.benchmark_runs is None
    assert args.timeout is None
    assert args.report_json is False


def test_migrate_command_with_all_options() -> None:
    """Parse migrate command with all CLI options."""
    parser = build_parser()

    args = parser.parse_args(
        [
            "migrate",
            "example.py",
            "--provider",
            "groq",
            "--model",
            "llama-3.3-70b-versatile",
            "--output",
            "custom_output",
            "--benchmark-runs",
            "10",
            "--timeout",
            "30",
            "--report-json",
        ]
    )

    assert args.command == "migrate"
    assert args.source == "example.py"
    assert args.provider == "groq"
    assert args.model == "llama-3.3-70b-versatile"
    assert args.output == "custom_output"
    assert args.benchmark_runs == 10
    assert args.timeout == 30
    assert args.report_json is True


def test_provider_accepts_groq() -> None:
    """Accept Groq as a CLI provider."""
    parser = build_parser()

    args = parser.parse_args(
        [
            "migrate",
            "example.py",
            "--provider",
            "groq",
        ]
    )

    assert args.provider == "groq"


def test_provider_accepts_ollama() -> None:
    """Accept Ollama as a CLI provider."""
    parser = build_parser()

    args = parser.parse_args(
        [
            "migrate",
            "example.py",
            "--provider",
            "ollama",
        ]
    )

    assert args.provider == "ollama"


def test_benchmark_runs_is_integer() -> None:
    """Parse benchmark runs as an integer."""
    parser = build_parser()

    args = parser.parse_args(
        [
            "migrate",
            "example.py",
            "--benchmark-runs",
            "5",
        ]
    )

    assert args.benchmark_runs == 5
    assert isinstance(args.benchmark_runs, int)


def test_benchmark_runs_rejects_non_integer() -> None:
    """Reject a non-integer benchmark run value."""
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "migrate",
                "example.py",
                "--benchmark-runs",
                "abc",
            ]
        )


def test_timeout_is_integer() -> None:
    """Parse timeout as an integer."""
    parser = build_parser()

    args = parser.parse_args(
        [
            "migrate",
            "example.py",
            "--timeout",
            "30",
        ]
    )

    assert args.timeout == 30
    assert isinstance(args.timeout, int)


def test_timeout_rejects_non_integer() -> None:
    """Reject a non-integer timeout value."""
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "migrate",
                "example.py",
                "--timeout",
                "abc",
            ]
        )


def test_report_json_flag() -> None:
    """Enable JSON report generation."""
    parser = build_parser()

    args = parser.parse_args(
        [
            "migrate",
            "example.py",
            "--report-json",
        ]
    )

    assert args.report_json is True


def test_report_json_defaults_to_false() -> None:
    """Keep JSON reporting disabled by default."""
    parser = build_parser()

    args = parser.parse_args(
        [
            "migrate",
            "example.py",
        ]
    )

    assert args.report_json is False


def test_source_is_required() -> None:
    """Require a source file argument."""
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["migrate"])


def test_command_is_required() -> None:
    """Require a CLI command."""
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args([])