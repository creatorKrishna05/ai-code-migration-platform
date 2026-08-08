
from __future__ import annotations

import json
import tempfile
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

from config import OUTPUT_DIR
from config import DEFAULT_MODEL, DEFAULT_PROVIDER
from main import build_pipeline

from leaderboard.manager import Leaderboard
from leaderboard.leaderboard_store import LeaderboardStore


OLLAMA_MODELS = [
    "llama3.2:latest",
]

GROQ_MODELS = [
    "llama-3.3-70b-versatile",
]

st.set_page_config(
    page_title="AI Code Migration Platform",
    page_icon="🚀",
    layout="wide",
)


LEADERBOARD_PATH = Path(OUTPUT_DIR/"leaderboard.json")


def get_status_text(success: bool) -> str:
    """Return a human-readable status."""
    return "Success" if success else "Failed"


def get_status_icon(success: bool) -> str:
    """Return a status icon."""
    return "✅" if success else "❌"


def render_header() -> None:
    """Render the application header."""
    st.title("🚀 AI Code Migration Platform")

    st.markdown(
        "### Convert Python code into optimized Modern C++20"
    )

    st.caption(
        "AI-powered source migration, compilation, benchmarking "
        "and performance evaluation."
    )

    st.divider()


def render_configuration() -> tuple[str, str]:
    """Render migration configuration controls."""
    st.subheader("⚙️ Migration Configuration")

    left_column, right_column = st.columns(2)

    with left_column:
        provider = st.selectbox(
            "LLM Provider",
            options=["groq", "ollama"],
            index=(
                0
                if DEFAULT_PROVIDER == "groq"
                else 1
            ),
        )

    with right_column:
        if provider == "groq":
            model_options = GROQ_MODELS
        else:
            model_options = OLLAMA_MODELS

        default_model = (
            DEFAULT_MODEL
            if DEFAULT_MODEL in model_options
            else model_options[0]
        )

        model = st.selectbox(
            "Model",
            options=model_options,
            index=model_options.index(
                default_model
            ),
        )

    return provider, model


def render_source_upload():
    """Render Python source upload control."""
    st.subheader("📂 Source Code")

    uploaded_file = st.file_uploader(
        "Upload Python source file",
        type=["py"],
        help="Upload a Python .py file for migration.",
    )

    if uploaded_file is not None:
        st.success(
            f"Loaded: {uploaded_file.name}"
        )

    return uploaded_file


def render_migration_status(report: dict) -> None:
    """Render migration pipeline status."""
    st.subheader("📊 Migration Status")

    col1, col2, col3 = st.columns(3)

    translation_success = report["translation_success"]
    compilation_success = report["compilation_success"]
    execution_success = report["execution_success"]

    with col1:
        st.metric(
            "Translation",
            get_status_text(translation_success),
            delta=(
                get_status_icon(translation_success)
            ),
        )

    with col2:
        st.metric(
            "Compilation",
            get_status_text(compilation_success),
            delta=(
                get_status_icon(compilation_success)
            ),
        )

    with col3:
        st.metric(
            "Execution",
            get_status_text(execution_success),
            delta=(
                get_status_icon(execution_success)
            ),
        )


def render_provider_information(
    provider: str,
    model: str,
) -> None:
    """Render provider and model information."""
    st.subheader("🤖 AI Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Provider",
            provider.upper(),
        )

    with col2:
        st.metric(
            "Model",
            model,
        )


def render_performance(report: dict) -> None:
    """Render benchmark and execution metrics."""
    st.subheader("⚡ Performance")

    benchmark_time = report["benchmark_time"]
    execution_time = report["execution_time"]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Benchmark Time",
            f"{benchmark_time:.6f} sec",
        )

    with col2:
        st.metric(
            "Execution Time",
            f"{execution_time:.6f} sec",
        )


def render_program_output(report: dict) -> None:
    """Render migrated program output."""
    st.subheader("🖥️ Program Output")

    program_output = report.get(
        "program_output",
        "",
    )

    if program_output:
        st.code(
            program_output,
            language="text",
        )
    else:
        st.info(
            "The migrated program produced no output."
        )


def render_generated_code(report: dict) -> None:
    """Render generated C++ source code."""
    st.subheader("💻 Generated C++20 Code")

    generated_code = report.get(
        "generated_code",
        "",
    )

    if not generated_code:
        st.warning(
            "Generated C++ code is not available."
        )
        return

    st.code(
        generated_code,
        language="cpp",
    )

    st.download_button(
        label="⬇️ Download source.cpp",
        data=generated_code,
        file_name="source.cpp",
        mime="text/plain",
        width="stretch",
    )


def render_report_download(report: dict) -> None:
    """Render migration report download."""
    st.subheader("📄 Migration Report")

    report_json = json.dumps(
        report,
        indent=4,
        default=str,
    )

    st.download_button(
        label="⬇️ Download migration_report.json",
        data=report_json,
        file_name="migration_report.json",
        mime="application/json",
        width="stretch",
    )


def render_leaderboard() -> None:
    """Render the migration leaderboard."""
    st.subheader("🏆 Leaderboard")

    try:
        leaderboard = Leaderboard(
            store=LeaderboardStore(
                LEADERBOARD_PATH
            )
        )

        rankings = leaderboard.get_rankings()

        if not rankings:
            st.info(
                "No migration results available yet."
            )
            return

        rows = []

        for rank, entry in enumerate(
            rankings,
            start=1,
        ):
            rows.append(
                {
                    "Rank": rank,
                    "Provider": entry.provider_name,
                    "Model": entry.model_name,
                    "Benchmark (sec)": (
                        f"{entry.benchmark_time:.6f}"
                    ),
                    "Execution (sec)": (
                        f"{entry.execution_time:.6f}"
                    ),
                    "Status": (
                        "✅ Success"
                        if entry.overall_success
                        else "❌ Failed"
                    ),
                }
            )

        st.dataframe(
            rows,
            width="stretch",
            hide_index=True,
        )

    except Exception as exc:
        st.warning(
            f"Unable to load leaderboard: {exc}"
        )


def render_migration_results(
    report: dict,
    provider: str,
    model: str,
) -> None:
    """Render all migration results."""
    st.success(
        "Migration completed successfully! 🎉"
    )

    st.divider()

    render_provider_information(
        provider=provider,
        model=model,
    )

    render_migration_status(
        report
    )

    render_performance(
        report
    )

    st.divider()

    render_program_output(
        report
    )

    st.divider()

    render_generated_code(
        report
    )

    st.divider()

    render_report_download(
        report
    )

    st.divider()

    render_leaderboard()


def run_migration(
    uploaded_file,
    provider: str,
    model: str,
) -> dict:
    """Execute the migration pipeline."""
    temporary_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            suffix=".py",
            delete=False,
        ) as temporary_file:
            temporary_file.write(
                uploaded_file.getvalue()
            )

            temporary_path = Path(
                temporary_file.name
            )

        with st.spinner(
            "Running AI code migration..."
        ):
            pipeline = build_pipeline(
                provider_name=provider,
                model_name=model,
            )

            report = pipeline.run(
                temporary_path
            )

        return report

    finally:
        if temporary_path is not None:
            temporary_path.unlink(
                missing_ok=True
            )


def main() -> None:
    """Render the AI Code Migration Platform UI."""
    render_header()

    provider, model = render_configuration()

    st.divider()

    uploaded_file = render_source_upload()

    st.divider()

    migrate_clicked = st.button(
        "🚀 Migrate Code",
        type="primary",
        width="stretch",
    )

    if not migrate_clicked:
        render_leaderboard()
        return

    if uploaded_file is None:
        st.warning(
            "Please upload a Python source file first."
        )
        return

    try:
        report = run_migration(
            uploaded_file=uploaded_file,
            provider=provider,
            model=model,
        )

        render_migration_results(
            report=report,
            provider=provider,
            model=model,
        )

    except Exception as exc:
        st.error(
            f"Migration failed: {exc}"
        )


if __name__ == "__main__":
    main()
