from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class LeaderboardEntry:
    """
    Represent the measurable result of a migration run.
    """

    provider_name: str
    model_name: str
    benchmark_time: float
    execution_time: float
    overall_success: bool
    source_file: str = "unknown.py"
    created_at: str = (
        datetime.now(timezone.utc).isoformat()
    )