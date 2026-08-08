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

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

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

DEFAULT_PROVIDER: str = "groq"
DEFAULT_MODEL: str = "llama-3.3-70b-versatile"

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

# =============================================================================
# Model Registry
# =============================================================================

MODELS: dict[str, dict[str, str]] = {
    "groq": {
        "Llama 3.3 70B": "llama-3.3-70b-versatile",
        "DeepSeek R1 Distill Llama 70B": "deepseek-r1-distill-llama-70b",
        "Qwen 3": "qwen/qwen3-32b",
    },
    "ollama": {
        "Llama 3.2": "llama3.2",
        "Qwen 2.5 Coder": "qwen2.5-coder",
    },
    # Future Providers
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

COMPILER_FLAGS: list[str] = [
    COMPILER_OPTIMIZATION,
    f"-std={CPP_STANDARD}",
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