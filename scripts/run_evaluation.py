import json
import statistics
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from turbine_copilot.service import CopilotService, diagnosis_dict

service = CopilotService()
rows = []
for asset in ["LP-BRG-02", "HP-BRG-01"]:
    result = diagnosis_dict(service.diagnosis(asset, 24))
    rows.append(result)
latencies = [r["latency_ms"] for r in rows]
report = {
    "dataset": {"rows": len(service.telemetry()), "assets": sorted(service.telemetry()["asset_id"].unique().tolist()), "synthetic": True, "seed": 42},
    "checks": {
        "quality_passed": service.quality()["passed"],
        "lp_bearing_review_required": rows[0]["human_review_required"],
        "healthy_asset_not_flagged": rows[1]["status"] == "normal",
        "evidence_retrieved_for_review": len(rows[0]["evidence"]) > 0,
        "structured_response_fields_present": all(k in rows[0] for k in ["status", "finding", "recommended_action", "evidence", "limitations"]),
    },
    "latency_ms": {"p50": round(statistics.median(latencies), 3), "p95_approx": round(max(latencies), 3)},
    "cases": rows,
    "limitations": ["Synthetic telemetry is not a plant failure benchmark.", "Thresholds require domain calibration.", "Lexical retrieval is a transparent baseline, not a production reranker."],
}
out = Path(__file__).resolve().parents[1] / "reports/evaluation.json"
out.write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
