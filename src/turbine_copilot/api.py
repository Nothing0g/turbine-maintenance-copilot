from fastapi import FastAPI, HTTPException, Query
from .service import CopilotService, diagnosis_dict

app = FastAPI(title="Turbine Maintenance Intelligence Copilot", version="0.1.0")
service = CopilotService()

@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "turbine-maintenance-copilot"}

@app.get("/quality/telemetry")
def quality() -> dict:
    return service.quality()

@app.get("/assets/{asset_id}/diagnosis")
def diagnosis(asset_id: str, hours: int = Query(default=24, ge=1, le=168)) -> dict:
    if asset_id not in set(service.telemetry()["asset_id"]):
        raise HTTPException(status_code=404, detail="asset not found")
    return diagnosis_dict(service.diagnosis(asset_id, hours))
