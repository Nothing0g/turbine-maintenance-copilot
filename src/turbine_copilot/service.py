import json
import time
from pathlib import Path
import pandas as pd
from .anomaly import score_window
from .config import PROCESSED_DIR, RAW_DIR
from .quality import profile_telemetry
from .retrieval import EvidenceIndex
from .schemas import Diagnosis

class CopilotService:
    def __init__(self, telemetry_path: Path | None = None, evidence_path: Path | None = None):
        self.telemetry_path = telemetry_path or PROCESSED_DIR / "telemetry.csv"
        self.evidence_path = evidence_path or RAW_DIR / "maintenance_evidence.md"
        self.index = EvidenceIndex.from_markdown(self.evidence_path)

    def telemetry(self) -> pd.DataFrame:
        frame = pd.read_csv(self.telemetry_path, parse_dates=["timestamp"])
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        return frame

    def diagnosis(self, asset_id: str, hours: int = 24) -> Diagnosis:
        started = time.perf_counter()
        frame = self.telemetry()
        asset = frame[frame["asset_id"] == asset_id].sort_values("timestamp")
        if asset.empty:
            return Diagnosis(asset_id, "insufficient_data", "No telemetry was found for this asset.", "Do not make a maintenance decision; verify asset identity and historian connectivity.", 0.0, tuple(), ("asset_not_found",), True, _ms(started))
        end = asset["timestamp"].max()
        start = end - pd.Timedelta(hours=hours)
        window = asset[(asset["timestamp"] >= start) & (asset["timestamp"] <= end)]
        quality = profile_telemetry(window)
        if len(window) < 7 or not quality.passed:
            return Diagnosis(asset_id, "insufficient_data", "The requested telemetry window did not pass quality checks.", "Verify telemetry freshness, completeness, and units before interpreting the trend.", 0.1, tuple(), ("insufficient_or_invalid_telemetry",), True, _ms(started))
        score = score_window(window)
        query = "bearing temperature lubrication vibration inspection" if score["anomalous"] else "routine turbine bearing monitoring"
        evidence = self.index.search(query)
        if not score["anomalous"]:
            return Diagnosis(asset_id, "normal", "The latest observation is within the recent operating envelope.", "Continue routine monitoring and review the next scheduled inspection.", 0.76, evidence, tuple(), False, _ms(started))
        limitations = []
        if float(window["vibration_mm_s"].std()) < 0.01:
            limitations.append("Vibration variation was too small to independently confirm the temperature signal.")
        if not evidence:
            limitations.append("No matching procedure evidence was retrieved.")
        return Diagnosis(asset_id, "review_required", "The latest bearing-related telemetry is outside its recent operating envelope.", "Inspect lubrication flow and verify the temperature sensor before returning the asset to normal service.", 0.82 if evidence else 0.55, evidence, tuple(limitations), True, _ms(started))

    def quality(self) -> dict:
        report = profile_telemetry(self.telemetry())
        return {"passed": report.passed, "row_count": report.row_count, "missing_columns": report.missing_columns, "null_counts": report.null_counts, "duplicate_timestamps": report.duplicate_timestamps, "unit_violations": report.unit_violations, "freshness_hours": report.freshness_hours}

def _ms(started: float) -> float:
    return round((time.perf_counter() - started) * 1000, 3)

def diagnosis_dict(diagnosis: Diagnosis) -> dict:
    return {
        "asset_id": diagnosis.asset_id,
        "status": diagnosis.status,
        "finding": diagnosis.finding,
        "recommended_action": diagnosis.recommended_action,
        "confidence": diagnosis.confidence,
        "evidence": [{"evidence_id": e.evidence_id, "title": e.title, "excerpt": e.excerpt, "score": e.score} for e in diagnosis.evidence],
        "limitations": list(diagnosis.limitations),
        "human_review_required": diagnosis.human_review_required,
        "latency_ms": diagnosis.latency_ms,
    }
