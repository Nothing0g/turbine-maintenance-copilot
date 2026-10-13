from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    title: str
    excerpt: str
    score: float

@dataclass(frozen=True)
class Diagnosis:
    asset_id: str
    status: Literal["normal", "review_required", "insufficient_data"]
    finding: str
    recommended_action: str
    confidence: float
    evidence: tuple[Evidence, ...]
    limitations: tuple[str, ...]
    human_review_required: bool
    latency_ms: float
