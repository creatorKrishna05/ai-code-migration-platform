from __future__ import annotations

import sys
from pathlib import Path

from cli.arguments import parse_args
from cli.validators import CLIValidationError, CLIValidator
from config import DEFAULT_PROVIDER, MODELS
from utils.exceptions import AIPlatformError
from utils.logger import get_logger


logger = get_logger(__name__)


def build_pipeline(
    provider_name: str | None = None,
    model_name: str | None = None,
    output_directory: Path | None = None,
    benchmark_runs: int | None = None,
    timeout: int | None = None,
    report_json: bool = False,
):
    """
    Build and wire all application services.
    """

    from analyzer.python_analyzer import PythonAnalyzer
    from benchmark.benchmark import Benchmark
    from compiler.compiler import Compiler
    from compiler.executor import Executor
    from config import (
        BENCHMARK_RUNS,
        EXECUTION_TIMEOUT_SECONDS,
    )
    from evaluator.evaluator import Evaluator
    from leaderboard.leaderboard_store import LeaderboardStore
    from leaderboard.manager import Leaderboard
    from outputs.output_manager import OutputManager
    from pipeline.migration_pipeline import MigrationPipeline
    from providers.provider_factory import create_provider
    from report.report_generator import ReportGenerator
    from translator.translator import Translator
    from workspace.workspace_manager import WorkspaceManager

    logger.info(
        "Building application dependencies."
    )

    workspace_manager = WorkspaceManager()

    provider = create_provider(
        provider_name=(
            provider_name
            if provider_name
            else DEFAULT_PROVIDER
        ),
        model_name=model_name,
    )

    translator = Translator(
        provider=provider,
    )

    analyzer = PythonAnalyzer()

    compiler = Compiler()

    executor = Executor()

    benchmark = Benchmark(
        executor=executor,
    )

    evaluator = Evaluator()

    report_generator = ReportGenerator()

    output_manager = OutputManager(
        output_directory=(
            output_directory
            if output_directory is not None
            else Path("outputs")
        )
    )

    leaderboard_store = LeaderboardStore(
        Path("outputs/leaderboard.json")
    )

    leaderboard = Leaderboard(
        store=leaderboard_store
    )

    pipeline = MigrationPipeline(
        workspace_manager=workspace_manager,
        translator=translator,
        analyzer=analyzer,
        compiler=compiler,
        benchmark=benchmark,
        evaluator=evaluator,
        report_generator=report_generator,
        output_manager=output_manager,
        leaderboard=leaderboard,
        benchmark_runs=(
            benchmark_runs
            if benchmark_runs is not None
            else BENCHMARK_RUNS
        ),
        timeout=(
            timeout
            if timeout is not None
            else EXECUTION_TIMEOUT_SECONDS
        ),
        report_json=report_json,
    )

    logger.info(
        "Application dependencies created successfully."
    )

    return pipeline


def main() -> int:
    """
    Application entry point.

    Returns:
        Process exit code.
    """
    try:
        logger.info(
            "Starting AI Code Migration Platform."
        )

        args = parse_args()

        if args.command != "migrate":
            raise ValueError(
                f"Unsupported command: {args.command}"
            )

        validator = CLIValidator()

        provider_name = validator.validate_provider(
            args.provider
            if args.provider is not None
            else DEFAULT_PROVIDER
        )

        model_name = None

        if args.model is not None:
            model_name = validator.validate_model(
                provider_name,
                args.model,
            )

        output_directory = None

        if args.output is not None:
            output_directory = (
                validator.validate_output_path(
                    args.output
                )
            )

        benchmark_runs = None

        if args.benchmark_runs is not None:
            benchmark_runs = (
                validator.validate_benchmark_runs(
                    args.benchmark_runs
                )
            )

        timeout = None

        if args.timeout is not None:
            timeout = validator.validate_timeout(
                args.timeout
            )

        source_path = validator.validate_source_path(
            args.source
        )

        pipeline = build_pipeline(
            provider_name=provider_name,
            model_name=model_name,
            output_directory=output_directory,
            benchmark_runs=benchmark_runs,
            timeout=timeout,
            report_json=args.report_json,
        )

        report = pipeline.run(source_path)

        logger.info(
            "Migration completed successfully."
        )

        print()
        print("Migration completed successfully.")
        print()

        print(f"Provider: {provider_name}")

        display_model = (
            model_name
            if model_name is not None
            else next(
                iter(MODELS[provider_name].values())
            )
        )

        print(f"Model: {display_model}")

        print(
            "Translation: "
            f"{'SUCCESS' if report.get('translation_success') else 'FAILED'}"
        )

        print(
            "Compilation: "
            f"{'SUCCESS' if report.get('compilation_success') else 'FAILED'}"
        )

        print(
            "Execution: "
            f"{'SUCCESS' if report.get('execution_success') else 'FAILED'}"
        )

        print(
            f"Benchmark: "
            f"{report.get('benchmark_time', 0):.6f} seconds"
        )

        print(
            f"Output: {report.get('program_output', '')}"
        )

        print()

        print("Generated files:")
        print("  outputs/source.cpp")
        print("  outputs/program.exe")

        if args.report_json:
            print("  outputs/report.json")

        print()

        return 0

    except CLIValidationError as exc:
        logger.error(
            "Invalid CLI input: %s",
            exc,
        )

        print(
            f"Error: Invalid CLI input: {exc}",
            file=sys.stderr,
        )

        return 2

    except AIPlatformError as exc:
        logger.error(
            "Migration failed: %s",
            exc,
        )

        print(
            f"Error: Migration failed: {exc}",
            file=sys.stderr,
        )

        return 1

    except Exception as exc:
        logger.exception(
            "Application failed: %s",
            exc,
        )

        print(
            "Error: Migration failed. "
            "Check the application logs for details.",
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":
    sys.exit(main())