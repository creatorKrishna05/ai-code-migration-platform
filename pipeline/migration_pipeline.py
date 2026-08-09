from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from benchmark.benchmark import Benchmark
from compiler.compiler import Compiler
from evaluator.evaluator import Evaluator
from leaderboard.manager import Leaderboard
from leaderboard.leaderboard_entry import LeaderboardEntry
from outputs.output_manager import OutputManager
from report.report_generator import ReportGenerator
from translator.translator import Translator
from utils.logger import get_logger
from workspace.workspace_manager import WorkspaceManager
from analyzer.python_analyzer import PythonAnalyzer
from utils.exceptions import ValidationError

from config import (
    BENCHMARK_RUNS,
    EXECUTION_TIMEOUT_SECONDS,
)


class MigrationPipeline:
    """
    Orchestrate the complete AI code migration workflow.
    """

    def __init__(
        self,
        workspace_manager: WorkspaceManager,
        translator: Translator,
        analyzer: PythonAnalyzer,
        compiler: Compiler,
        benchmark: Benchmark,
        evaluator: Evaluator,
        report_generator: ReportGenerator,
        output_manager: OutputManager,
        leaderboard: Leaderboard | None = None,
        benchmark_runs: int = BENCHMARK_RUNS,
        timeout: int = EXECUTION_TIMEOUT_SECONDS,
        report_json: bool = False,
    ) -> None:
        """
        Initialize the migration pipeline.
        """
        self._logger = get_logger(__name__)

        self._workspace_manager = workspace_manager
        self._translator = translator
        self._analyzer = analyzer
        self._compiler = compiler
        self._benchmark = benchmark
        self._evaluator = evaluator
        self._report_generator = report_generator
        self._output_manager = output_manager
        self._leaderboard = leaderboard

        self._benchmark_runs = benchmark_runs
        self._timeout = timeout
        self._report_json = report_json

        self._logger.info(
            "Migration pipeline initialized."
        )

    def run(
        self,
        source_path: Path,
    ) -> dict[str, Any]:
        """
        Execute the complete AI migration workflow.

        Args:
            source_path:
                Path to the Python source project.

        Returns:
            Final migration report.
        """
        self._logger.info(
            "Starting migration pipeline."
        )

        try:
            if not source_path.is_file():
                raise FileNotFoundError(
                    f"Source file not found: {source_path}"
                )

            workspace = (
                self._workspace_manager.create_workspace()
            )

            source_code = source_path.read_text(
                encoding="utf-8"
            )

            analysis = self._analyzer.analyze(
                source_code
            )

            translated_code = (
                self._translator.translate(
                    source_code,
                    analysis,
                )
            )

            self._validate_translation(
                translated_code
            )

            executable_path = (
                self._compiler.compile(
                    workspace,
                    translated_code,
                )
            )

            benchmark_start = time.perf_counter()

            program_output, benchmark_time = (
                self._benchmark.benchmark(
                executable_path=executable_path,
                runs=self._benchmark_runs,
                timeout=self._timeout,
                )
            )

            execution_time = (
                time.perf_counter() - benchmark_start
            )

            evaluation = self._evaluator.evaluate(
                translation_success=True,
                compilation_success=True,
                execution_success=True,
                execution_time=execution_time,
                benchmark_time=benchmark_time,
                program_output=program_output,
            )

            report = (
                self._report_generator.generate(
                    evaluation
                )
            )

            report["program_output"] = program_output
            report["generated_code"] = translated_code
            
            self._output_manager.save_source(
                translated_code
            )

            self._output_manager.save_executable(
                executable_path
            )

            if self._report_json:
                self._output_manager.save_report(
                    report
                )

            self._update_leaderboard(
                evaluation,
                source_path,
            )

            self._logger.info(
                "Migration pipeline completed successfully."
            )

            return report

        except Exception:
            self._logger.exception(
                "Migration pipeline failed."
            )

            raise

        finally:
            self._workspace_manager.cleanup()


    def _validate_translation(
        self,
        translated_code: str,
    ) -> None:
        """
        Validate generated C++ source code.
        """
        if not translated_code.strip():
            raise ValidationError(
                "Generated C++ code is empty."
            )
        

    def _update_leaderboard(
        self,
        evaluation: dict[str, Any],
        source_path: Path,
    ) -> None:
        """
        Add the migration result to the leaderboard.

        Args:
            evaluation:
                Aggregated migration evaluation.
        """
        if self._leaderboard is None:
            return

        try:
            entry = LeaderboardEntry(
                provider_name=self._translator.provider_name,
                model_name=self._translator.model_name,
                source_file=source_path.name,
                
                benchmark_time=evaluation[
                    "benchmark_time"
                ],
                execution_time=evaluation[
                    "execution_time"
                ],
                overall_success=evaluation[
                    "overall_success"
                ],
            )

            self._leaderboard.add(entry)

            self._logger.info(
                "Migration result added to leaderboard."
            )

        except Exception:
            self._logger.exception(
                "Failed to update leaderboard."
            )