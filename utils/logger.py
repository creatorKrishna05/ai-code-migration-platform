"""
Central logging configuration for the AI Code Migration Platform.

Responsibilities:
- Configure application logging.
- Log messages to both console and file.
- Prevent duplicate logger creation.
- Provide reusable logger instances.

Design Principles:
- Single Responsibility Principle (SRP)
- Reusability
- Loose Coupling
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import LOG_DIR

# =============================================================================
# Logging Configuration
# =============================================================================

LOG_FILE: Path = LOG_DIR / "app.log"

LOG_LEVEL: int = logging.INFO

LOG_FORMAT: str = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger instance.

    Parameters
    ----------
    name : str
        Usually __name__ of the calling module.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    # -----------------------------------------------------------------
    # Console Handler
    # -----------------------------------------------------------------

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # -----------------------------------------------------------------
    # Rotating File Handler
    # -----------------------------------------------------------------

    file_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    # -----------------------------------------------------------------
    # Attach Handlers
    # -----------------------------------------------------------------

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger