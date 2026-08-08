"""
Custom exceptions for the AI Code Migration Platform.

Responsibilities:
- Define application-specific exception classes.
- Provide a clear and extensible exception hierarchy.

Design Principles:
- Single Responsibility Principle (SRP)
- Loose Coupling
- Reusability
- Maintainability
"""

from __future__ import annotations


class AIPlatformError(Exception):
    """
    Base exception for all application-specific errors.
    """

    def __init__(self, message: str) -> None:
        """
        Initialize the exception.

        Args:
            message: Human-readable error message.
        """
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """
        Return the error message.

        Returns:
            Exception message.
        """
        return self.message


class ConfigurationError(AIPlatformError):
    """
    Raised when application configuration is invalid.
    """


class ProviderError(AIPlatformError):
    """
    Raised when an LLM provider fails.
    """


class TranslationError(AIPlatformError):
    """
    Raised when source code translation fails.
    """


class CompilationError(AIPlatformError):
    """
    Raised when generated C++ code fails to compile.
    """

class ExecutionError(AIPlatformError):
    """
    Raised when execution of a compiled program fails.
    """

class BenchmarkError(AIPlatformError):
    """
    Raised when benchmarking fails.
    """


class EvaluationError(AIPlatformError):
    """
    Raised when evaluation of generated code fails.
    """
    
class ReportGenerationError(AIPlatformError):
    """
    Raised when report generation fails.
    """

class ValidationError(AIPlatformError):
    """
    Raised when user input validation fails.
    """

