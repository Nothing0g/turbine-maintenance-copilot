import pandas as pd
from turbine_copilot.quality import profile_telemetry

def test_quality_report_accepts_valid_rows():
    frame = pd.DataFrame({"timestamp": pd.to_datetime(["2026-01-01T00:00:00Z"]), "asset_id": ["A"], "temperature_c": [80.0], "vibration_mm_s": [1.0], "lubrication_flow_lpm": [12.0]})
    report = profile_telemetry(frame)
    assert report.passed is True
    assert report.row_count == 1

def test_quality_report_rejects_out_of_range_temperature():
    frame = pd.DataFrame({"timestamp": pd.to_datetime(["2026-01-01T00:00:00Z"]), "asset_id": ["A"], "temperature_c": [500.0], "vibration_mm_s": [1.0], "lubrication_flow_lpm": [12.0]})
    assert profile_telemetry(frame).passed is False
