import pandas as pd
import numpy as np


def score_window(frame: pd.DataFrame, temperature_limit: float = 3.0, vibration_limit: float = 3.0) -> dict:
    """Score the final observation against the preceding operating envelope."""
    if frame.empty:
        return {"anomalous": False, "reason": "no_observations", "temperature_z": None, "vibration_z": None}
    ordered = frame.sort_values("timestamp").copy()
    baseline = ordered.iloc[:-1]
    current = ordered.iloc[-1]
    if len(baseline) < 6:
        return {"anomalous": False, "reason": "insufficient_baseline", "temperature_z": None, "vibration_z": None}

    def z(col: str) -> float:
        mean = float(baseline[col].mean())
        std = float(baseline[col].std(ddof=0))
        return 0.0 if std == 0 else float((current[col] - mean) / std)

    temp_z, vibration_z = z("temperature_c"), z("vibration_mm_s")
    return {
        "anomalous": abs(temp_z) >= temperature_limit or abs(vibration_z) >= vibration_limit,
        "reason": "threshold_exceeded" if abs(temp_z) >= temperature_limit or abs(vibration_z) >= vibration_limit else "within_envelope",
        "temperature_z": round(temp_z, 3),
        "vibration_z": round(vibration_z, 3),
        "observed_at": str(current["timestamp"]),
    }
