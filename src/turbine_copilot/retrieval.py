import re
from dataclasses import asdict
from pathlib import Path
from .schemas import Evidence

STOPWORDS = {"the", "and", "for", "with", "from", "this", "that", "what", "are", "when", "into", "should"}

def tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9-]+", text.lower()) if t not in STOPWORDS}

class EvidenceIndex:
    def __init__(self, records: list[dict]):
        self.records = records
        self.term_sets = [tokens(r["title"] + " " + r["excerpt"]) for r in records]

    @classmethod
    def from_markdown(cls, path: Path) -> "EvidenceIndex":
        records = []
        current = None
        for line in path.read_text().splitlines():
            if line.startswith("## "):
                if current:
                    records.append(current)
                current = {"evidence_id": line.split("|", 1)[0].replace("## ", "").strip(), "title": line.split("|", 1)[-1].strip(), "excerpt": ""}
            elif current and line.strip():
                current["excerpt"] += " " + line.strip()
        if current:
            records.append(current)
        return cls(records)

    def search(self, query: str, limit: int = 3) -> tuple[Evidence, ...]:
        q = tokens(query)
        scored = []
        for record, terms in zip(self.records, self.term_sets):
            overlap = len(q & terms)
            score = overlap / max(1, len(q))
            if score > 0:
                scored.append(Evidence(record["evidence_id"], record["title"], record["excerpt"].strip(), round(score, 3)))
        return tuple(sorted(scored, key=lambda x: (-x.score, x.evidence_id))[:limit])
