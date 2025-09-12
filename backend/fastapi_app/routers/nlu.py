from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

class NLURequest(BaseModel):
    text: str

class NLUResponse(BaseModel):
    intent: str
    entities: List[Dict[str, Any]]
    dependencies: List[Dict[str, Any]]

# Lightweight heuristic intent detection to avoid heavy downloads by default
INTENT_KEYWORDS = {
    "select": ["select", "show", "list", "find", "get", "fetch"],
    "insert": ["insert", "add", "create", "new", "append"],
    "update": ["update", "modify", "change", "set"],
    "delete": ["delete", "remove", "drop", "truncate"],
    "api_fetch": ["call api", "fetch api", "http", "curl"],
}

try:
    from transformers import pipeline
    _ner = pipeline("ner", grouped_entities=True)
except Exception:
    _ner = None

@router.post("/parse", response_model=NLUResponse)
def parse(req: NLURequest):
    text = req.text.lower()
    intent = "other"
    for k, words in INTENT_KEYWORDS.items():
        if any(w in text for w in words):
            intent = k
            break

    entities: List[Dict[str, Any]] = []
    if _ner:
        try:
            ents = _ner(req.text)
            for e in ents:
                entities.append({
                    "text": e.get("word"),
                    "label": e.get("entity_group"),
                    "score": e.get("score"),
                })
        except Exception:
            pass

    # Minimal dependency hints (rule-based for now)
    dependencies: List[Dict[str, Any]] = []
    preps = ["from", "into", "where", "join", "on", "group by", "order by"]
    for p in preps:
        if p in text:
            dependencies.append({"type": "clause", "value": p})

    return NLUResponse(intent=intent, entities=entities, dependencies=dependencies)
