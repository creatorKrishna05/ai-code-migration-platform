from __future__ import annotations

import ast
from dataclasses import dataclass

from utils.exceptions import ValidationError


@dataclass(frozen=True)
class PythonAnalysis:
    """
    Represent structural analysis results for Python source code.
    """

    lines_of_code: int
    function_count: int
    class_count: int
    import_count: int
    loop_count: int
    conditional_count: int
    exception_count: int
    complexity: int


class PythonAnalyzer:
    """
    Analyze Python source code using the built-in AST module.
    """

    def analyze(
        self,
        source_code: str,
    ) -> PythonAnalysis:
        """
        Analyze Python source code.

        Args:
            source_code:
                Python source code.

        Returns:
            Structural Python code analysis.

        Raises:
            ValidationError:
                If source code is empty or invalid.
        """
        if not source_code.strip():
            raise ValidationError(
                "Source code cannot be empty."
            )

        try:
            tree = ast.parse(source_code)
        except SyntaxError as error:
            raise ValidationError(
                "Invalid Python source code."
            ) from error

        lines_of_code = self._count_lines(
            source_code
        )

        function_count = len(
            [
                node
                for node in ast.walk(tree)
                if isinstance(
                    node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                    ),
                )
            ]
        )

        class_count = len(
            [
                node
                for node in ast.walk(tree)
                if isinstance(
                    node,
                    ast.ClassDef,
                )
            ]
        )

        import_count = len(
            [
                node
                for node in ast.walk(tree)
                if isinstance(
                    node,
                    (
                        ast.Import,
                        ast.ImportFrom,
                    ),
                )
            ]
        )

        loop_count = len(
            [
                node
                for node in ast.walk(tree)
                if isinstance(
                    node,
                    (
                        ast.For,
                        ast.AsyncFor,
                        ast.While,
                    ),
                )
            ]
        )

        conditional_count = len(
            [
                node
                for node in ast.walk(tree)
                if isinstance(
                    node,
                    ast.If,
                )
            ]
        )

        exception_count = len(
            [
                node
                for node in ast.walk(tree)
                if isinstance(
                    node,
                    (
                        ast.Try,
                        ast.Raise,
                    ),
                )
            ]
        )

        complexity = (
            1
            + loop_count
            + conditional_count
            + exception_count
        )

        return PythonAnalysis(
            lines_of_code=lines_of_code,
            function_count=function_count,
            class_count=class_count,
            import_count=import_count,
            loop_count=loop_count,
            conditional_count=conditional_count,
            exception_count=exception_count,
            complexity=complexity,
        )

    @staticmethod
    def _count_lines(
        source_code: str,
    ) -> int:
        """
        Count non-empty source lines.

        Args:
            source_code:
                Python source code.

        Returns:
            Number of non-empty lines.
        """
        return sum(
            1
            for line in source_code.splitlines()
            if line.strip()
        )

