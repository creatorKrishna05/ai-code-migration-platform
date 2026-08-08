from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line argument parser.

    Returns:
        Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        prog="ai-code-migration",
        description=(
            "AI-powered platform for migrating "
            "Python code to modern C++."
        ),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    migrate_parser = subparsers.add_parser(
        "migrate",
        help="Migrate a Python source file to C++.",
    )

    migrate_parser.add_argument(
        "source",
        type=str,
        help="Path to the Python source file.",
    )

    migrate_parser.add_argument(
        "--provider",
        type=str,
        default=None,
        help="LLM provider to use for migration.",
    )

    migrate_parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="LLM model to use for migration.",
    )

    migrate_parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Directory for migration output artifacts.",
    )

    migrate_parser.add_argument(
        "--benchmark-runs",
        type=int,
        default=None,
        help="Number of benchmark runs to perform.",
    )

    migrate_parser.add_argument(
        "--timeout",
        type=int,
        default=None,
        help="Maximum execution time in seconds.",
    )

    migrate_parser.add_argument(
        "--report-json",
        action="store_true",
        help="Save the migration report as a JSON file.",
    )

    return parser


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed command-line arguments.
    """
    parser = build_parser()

    return parser.parse_args()