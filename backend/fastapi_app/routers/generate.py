from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from ..core.generator import get_generator

router = APIRouter()

class GenerateRequest(BaseModel):
    text: str
    schema: Dict[str, Any] | None = None
    db_type: str = "mysql"
    n_candidates: int | None = None

class GenerateResponse(BaseModel):
    candidates: List[str]
    provider: str

@router.post("/")
def generate(req: GenerateRequest):
    provider = os.getenv("GENERATOR_PROVIDER", "mixtral")
    n = req.n_candidates or int(os.getenv("GENERATOR_N_CANDIDATES", "5"))
    gen = get_generator(provider)
    schema_ctx = req.schema or {}
    prompt = build_prompt(req.text, schema_ctx, req.db_type)
    candidates = gen.generate(prompt, n=n)
    return GenerateResponse(candidates=candidates, provider=provider)


def build_prompt(user_text: str, schema: Dict[str, Any], db_type: str) -> str:
    schema_desc = []
    if db_type == "mysql":
        tables = schema.get("tables", [])
        columns = schema.get("columns", {})
        for t in tables[:10]:
            cols = ", ".join([c.get("name") if isinstance(c, dict) else str(c) for c in columns.get(t, [])])
            schema_desc.append(f"Table {t}({cols})")
    elif db_type == "mongodb":
        collections = schema.get("collections", [])
        for c in collections[:10]:
            schema_desc.append(f"Collection {c}")
    schema_str = "\n".join(schema_desc)
    system = (
        "You are a query generator. Follow the provided schema strictly. "
        "Output only the final query with no explanation."
    )
    return f"[SYSTEM]\n{system}\n[DB_TYPE]\n{db_type}\n[SCHEMA]\n{schema_str}\n[USER]\n{user_text}"
