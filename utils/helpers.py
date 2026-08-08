"""
Reusable helper functions for the AI Code Migration Platform.

Responsibilities:
- File operations
- JSON operations
- Directory management
- Timestamp generation
- Filename utilities

Design Principles:
- Single Responsibility Principle (SRP)
- Don't Repeat Yourself (DRY)
- Single Source of Truth (SSOT)
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from utils.exceptions import FileOperationError
from utils.logger import get_logger

logger = get_logger(__name__)

# =============================================================================
# Constants
# =============================================================================

TIMESTAMP_FORMAT: str = "%Y%m%d_%H%M%S"


# =============================================================================
# Timestamp Utilities
# =============================================================================

def get_timestamp() -> str:
    """
    Return the current timestamp.

    Returns:
        Current timestamp in YYYYMMDD_HHMMSS format.
    """

    return datetime.now().strftime(TIMESTAMP_FORMAT)


# =============================================================================
# Directory Utilities
# =============================================================================

def ensure_directory(directory: Path) -> None:
    """
    Create the directory if it does not already exist.

    Args:
        directory: Directory path.

    Raises:
        ValidationError:
            If the directory cannot be created.
    """

    try:
        directory_exists = directory.exists()

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not directory_exists:
            logger.info(
                "Created directory: %s",
                directory,
            )

    except Exception as error:
        logger.exception(
            "Failed to create directory: %s",
            directory,
        )

        raise FileOperationError(
            f"Unable to create directory: {directory}"
        ) from error


# =============================================================================
# Filename Utilities
# =============================================================================

def sanitize_filename(filename: str) -> str:
    """
    Convert a filename into a filesystem-safe format.

    Args:
        filename: Original filename.

    Returns:
        Sanitized filename safe for most operating systems.
    """

    sanitized = re.sub(
        r'[\\/*?:"<>|]',
        "_",
        filename,
    )

    sanitized = re.sub(
        r"\s+",
        "_",
        sanitized,
    ).strip("_")

    if not sanitized:
        sanitized = "untitled"

    logger.debug(
        "Sanitized filename '%s' -> '%s'.",
        filename,
        sanitized,
    )

    return sanitized


def create_output_filename(
    prefix: str,
    extension: str,
) -> str:
    """
    Create a timestamped output filename.

    Args:
        prefix: File name prefix.
        extension: File extension.

    Returns:
        Timestamped output filename.
    """

    extension = extension.lstrip(".")

    safe_prefix = sanitize_filename(prefix)

    filename = (
        f"{safe_prefix}_"
        f"{get_timestamp()}."
        f"{extension}"
    )

    logger.debug(
        "Created output filename: %s",
        filename,
    )

    return filename


# =============================================================================
# File Utilities
# =============================================================================

def save_text_file(
    file_path: Path,
    content: str,
) -> None:
    """
    Save text content to a UTF-8 encoded file.

    Args:
        file_path: Destination file path.
        content: Text content to save.

    Raises:
        FileOperationError:
            If the file cannot be saved.
    """


    ensure_directory(file_path.parent)

    try:
        ensure_directory(file_path.parent)

        file_path.write_text(
                content,
            encoding="utf-8",
        )

        logger.info(
            "Saved text file: %s",
            file_path,
        )

    except Exception as error:
        logger.exception(
            "Failed to save text file: %s",
            file_path,
        )

        raise FileOperationError(
            f"Unable to save text file: {file_path}"
        ) from error


def read_text_file(
    file_path: Path,
) -> str:
    """
    Read text content from a UTF-8 encoded file.

    Args:
        file_path: Source file path.

    Returns:
        File contents as a string.

    Raises:
        FileOperationError:
            If the file cannot be read.
    """

    try:
        content = file_path.read_text(
            encoding="utf-8",
        )

        logger.info(
            "Read text file: %s",
            file_path,
        )

        return content

    except Exception as error:
        logger.exception(
            "Failed to read text file: %s",
            file_path,
        )

        raise FileOperationError(
            f"Unable to read text file: {file_path}"
        ) from error



# =============================================================================
# JSON Utilities
# =============================================================================

def save_json(
    file_path: Path,
    data: Any,
) -> None:
    """
    Save a Python object as a JSON file.

    Args:
        file_path: Destination JSON file.
        data: Python object to serialize.

    Raises:
        FileOperationError:
            If the JSON file cannot be saved.
    """


    try:
        ensure_directory(file_path.parent)


        with file_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        logger.info(
            "Saved JSON file: %s",
            file_path,
        )

    except Exception as error:
        logger.exception(
            "Failed to save JSON file: %s",
            file_path,
        )

        raise FileOperationError(
            f"Unable to save JSON file: {file_path}"
        ) from error


def load_json(
    file_path: Path,
) -> Any:
    """
    Load a JSON file.

    Args:
        file_path: Source JSON file.

    Returns:
        Deserialized Python object.

    Raises:
        FileOperationError:
            If the JSON file cannot be loaded.
    """

    try:
        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        logger.info(
            "Loaded JSON file: %s",
            file_path,
        )

        return data

    except Exception as error:
        logger.exception(
            "Failed to load JSON file: %s",
            file_path,
        )

        raise FileOperationError(
            f"Unable to load JSON file: {file_path}"
        ) from error