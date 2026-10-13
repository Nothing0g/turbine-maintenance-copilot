from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "data/processed/telemetry.csv"
rng = np.random.default_rng(42)
end = pd.Timestamp("2026-08-31 12:00:00", tz="UTC")
times = pd.date_range(end=end, periods=72, freq="h")
rows = []
for asset, temp_base, vib_base in [("LP-BRG-02", 81.0, 1.7), ("HP-BRG-01", 76.0, 1.3)]:
    for i, ts in enumerate(times):
        temp = temp_base + rng.normal(0, 0.7)
        vib = vib_base + rng.normal(0, 0.08)
        flow = 12.0 + rng.normal(0, 0.15)
        if asset == "LP-BRG-02" and i >= 66:
            temp += (i - 65) * 1.8
            flow -= (i - 65) * 0.35
        rows.append({"timestamp": ts.isoformat(), "asset_id": asset, "temperature_c": round(temp, 3), "vibration_mm_s": round(vib, 3), "lubrication_flow_lpm": round(flow, 3)})
pd.DataFrame(rows).to_csv(out, index=False)
print(f"wrote {len(rows)} rows to {out}")
