from dataclasses import dataclass
import pandas as pd

REQUIRED_COLUMNS = {"timestamp", "asset_id", "temperature_c", "vibration_mm_s", "lubrication_flow_lpm"}

@dataclass(frozen=True)
class QualityReport:
    passed: bool
    row_count: int
    missing_columns: tuple[str, ...]
    null_counts: dict[str, int]
    duplicate_timestamps: int
    unit_violations: int
    freshness_hours: float


def profile_telemetry(frame: pd.DataFrame, now: pd.Timestamp | None = None) -> QualityReport:
    missing = tuple(sorted(REQUIRED_COLUMNS - set(frame.columns)))
    if missing:
        return QualityReport(False, len(frame), missing, {}, 0, 0, float("inf"))
    timestamps = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    null_counts = {k: int(v) for k, v in frame.isna().sum().items() if v}
    duplicate_count = int(frame.duplicated(subset=["asset_id", "timestamp"]).sum())
    unit_violations = int(((frame["temperature_c"] < -80) | (frame["temperature_c"] > 250)).sum())
    ref = now or timestamps.max()
    freshness = float((ref - timestamps.max()).total_seconds() / 3600) if len(timestamps) else float("inf")
    passed = not missing and not null_counts and duplicate_count == 0 and unit_violations == 0
    return QualityReport(passed, len(frame), missing, null_counts, duplicate_count, unit_violations, freshness)
