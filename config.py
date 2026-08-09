"""
Central configuration for the AI Code Migration Platform.

Responsibilities:
- Load environment variables.
- Define project paths.
- Register supported providers and models.
- Store compiler, benchmark and translation settings.
- Create required runtime directories.

Design Principles:
- Single Responsibility Principle (SRP)
- Single Source of Truth (SSOT)
- Loose Coupling
- Production Ready
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

def get_secret(
    key: str,
    default: str = "",
) -> str:
    """
    Load configuration from environment variables
    with Streamlit secrets as fallback.
    """

    # First priority: .env / environment variables
    value = os.getenv(key)

    if value:
        return value

    # Second priority: Streamlit secrets
    try:
        import streamlit as st

        if key in st.secrets:
            return st.secrets[key]

    except Exception:
        pass

    return default

# =============================================================================
# Environment
# =============================================================================

load_dotenv()

# =============================================================================
# Application
# =============================================================================

APP_NAME: str = "AI Code Migration Platform"
APP_VERSION: str = "1.0.0"

# =============================================================================
# Project Paths
# =============================================================================

BASE_DIR: Path = Path(__file__).resolve().parent

OUTPUT_DIR: Path = BASE_DIR / "outputs"
TEMP_DIR: Path = BASE_DIR / "temp"
LOG_DIR: Path = BASE_DIR / "logs"
REPORT_DIR: Path = BASE_DIR / "reports"
HISTORY_DIR: Path = BASE_DIR / "history"

for directory in (
    OUTPUT_DIR,
    TEMP_DIR,
    LOG_DIR,
    REPORT_DIR,
    HISTORY_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)

# =============================================================================
# Environment Variables
# =============================================================================

GROQ_API_KEY: str = get_secret("GROQ_API_KEY")

OLLAMA_BASE_URL: str = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

# Future Provider Keys

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
XAI_API_KEY: str = os.getenv("XAI_API_KEY", "")

# =============================================================================
# Provider Configuration
# =============================================================================

DEFAULT_PROVIDER: str = get_secret(
    "DEFAULT_PROVIDER",
    "groq",
)

DEFAULT_MODEL: str = "openai/gpt-oss-120b"

PROVIDERS: dict[str, dict[str, bool]] = {
    "groq": {
        "enabled": True,
    },
    "ollama": {
        "enabled": True,
    },
    "openai": {
        "enabled": False,
    },
    "anthropic": {
        "enabled": False,
    },
    "google": {
        "enabled": False,
    },
    "xai": {
        "enabled": False,
    },
}

MODELS: dict[str, dict[str, str]] = {
    "groq": {
        "GPT OSS 120B": "openai/gpt-oss-120b",
        "Qwen 3.6 27B": "qwen/qwen3.6-27b",
        "Llama 3.3 70B": "llama-3.3-70b-versatile",
    },

    "ollama": {
        "Llama 3.2": "llama3.2",
        "Qwen 2.5 Coder": "qwen2.5-coder",
    },

    "openai": {
        "GPT-5": "gpt-5",
    },

    "anthropic": {
        "Claude Sonnet 4": "claude-sonnet-4",
    },

    "google": {
        "Gemini 2.5 Pro": "gemini-2.5-pro",
    },

    "xai": {
        "Grok 4": "grok-4",
    },
}

# =============================================================================
# Model Registry
# =============================================================================

MODELS: dict[str, dict[str, str]] = {
    "groq": {
        "GPT OSS 120B": "openai/gpt-oss-120b",
        "Qwen 3.6 27B": "qwen/qwen3.6-27b",
        "Llama 3.3 70B": "llama-3.3-70b-versatile",
    },

    "ollama": {
        "Llama 3.2": "llama3.2",
        "Qwen 2.5 Coder": "qwen2.5-coder",
    },

    "openai": {
        "GPT-5": "gpt-5",
    },

    "anthropic": {
        "Claude Sonnet 4": "claude-sonnet-4",
    },

    "google": {
        "Gemini 2.5 Pro": "gemini-2.5-pro",
    },

    "xai": {
        "Grok 4": "grok-4",
    },
}

# =============================================================================
# Compiler Configuration
# =============================================================================

CPP_COMPILER: str = "g++"

CPP_STANDARD: str = "c++20"

COMPILER_OPTIMIZATION: str = "-O3"

SQLITE_INCLUDE_DIR: Path = Path(
    os.environ.get(
        "SQLITE_INCLUDE_DIR",
        r"C:\Users\DELL\miniconda3\Library\include",
    )
)

SQLITE_LIBRARY_DIR: Path = Path(
    os.environ.get(
        "SQLITE_LIBRARY_DIR",
        r"C:\Users\DELL\miniconda3\Library\lib",
    )
)

COMPILER_FLAGS: list[str] = [
    COMPILER_OPTIMIZATION,
    f"-std={CPP_STANDARD}",
    f"-I{SQLITE_INCLUDE_DIR}",
    f"-L{SQLITE_LIBRARY_DIR}",
    
]

# =============================================================================
# Benchmark Configuration
# =============================================================================

BENCHMARK_RUNS: int = 5
BENCHMARK_WARMUP_RUNS: int = 1
EXECUTION_TIMEOUT_SECONDS: int = 10

# =============================================================================
# Translation Configuration
# =============================================================================

SOURCE_LANGUAGE: str = "Python"
TARGET_LANGUAGE: str = "Modern C++"

AUTO_FORMAT_OUTPUT: bool = True
SAVE_GENERATED_CODE: bool = True

# =============================================================================
# Supported Files
# =============================================================================

SUPPORTED_EXTENSIONS: tuple[str, ...] = (                                   
    ".py",
)

# =============================================================================
# Configuration Validation
# =============================================================================


def validate_configuration() -> None:
    """
    Validate application configuration.

    Raises:
        ValueError:
            If any critical configuration value is invalid.
    """
    if not DEFAULT_PROVIDER.strip():
        raise ValueError(
            "DEFAULT_PROVIDER cannot be empty."
        )

    if DEFAULT_PROVIDER not in PROVIDERS:
        raise ValueError(
            f"Default provider '{DEFAULT_PROVIDER}' "
            "is not registered."
        )

    provider_config = PROVIDERS[DEFAULT_PROVIDER]

    if not provider_config.get("enabled", False):
        raise ValueError(
            f"Default provider '{DEFAULT_PROVIDER}' "
            "is disabled."
        )

    provider_models = MODELS.get(DEFAULT_PROVIDER)

    if not provider_models:
        raise ValueError(
            f"No models registered for provider "
            f"'{DEFAULT_PROVIDER}'."
        )

    if DEFAULT_MODEL not in provider_models.values():
        raise ValueError(
            f"Default model '{DEFAULT_MODEL}' "
            f"is not registered for provider "
            f"'{DEFAULT_PROVIDER}'."
        )

    if not CPP_COMPILER.strip():
        raise ValueError(
            "CPP_COMPILER cannot be empty."
        )

    if not CPP_STANDARD.strip():
        raise ValueError(
            "CPP_STANDARD cannot be empty."
        )

    if not COMPILER_FLAGS:
        raise ValueError(
            "COMPILER_FLAGS cannot be empty."
        )

    if BENCHMARK_RUNS <= 0:
        raise ValueError(
            "BENCHMARK_RUNS must be greater than zero."
        )

    if BENCHMARK_WARMUP_RUNS < 0:
        raise ValueError(
            "BENCHMARK_WARMUP_RUNS cannot be negative."
        )

    if EXECUTION_TIMEOUT_SECONDS <= 0:
        raise ValueError(
            "EXECUTION_TIMEOUT_SECONDS must be greater than zero."
        )