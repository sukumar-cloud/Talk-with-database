from __future__ import annotations
from typing import Dict, Any
from sqlglot import parse_one, exp
from .config import settings

BLOCKED = {"DROP", "TRUNCATE", "ALTER"}


def validate_query(query: str, db_type: str = "mysql") -> Dict[str, Any]:
    safety = {"valid_syntax": False, "blocked": False, "reasons": []}
    try:
        tree = parse_one(query, read=db_type)
        safety["valid_syntax"] = True
        # Block DDL
        if isinstance(tree, (exp.Drop, exp.Truncate, exp.Alter)):
            safety["blocked"] = True
            safety["reasons"].append("DDL is blocked")
        # Block DELETE/UPDATE without WHERE
        if isinstance(tree, exp.Delete) and not tree.args.get("where"):
            safety["blocked"] = True
            safety["reasons"].append("DELETE without WHERE is blocked")
        if isinstance(tree, exp.Update) and not tree.args.get("where"):
            safety["blocked"] = True
            safety["reasons"].append("UPDATE without WHERE is blocked")
        # Enforce LIMIT on SELECT
        if isinstance(tree, exp.Select):
            limit = tree.args.get("limit")
            if not limit:
                safety["reasons"].append("SELECT missing LIMIT; will cap at runtime")
    except Exception as e:
        safety["reasons"].append(f"parse_error: {e}")
    # Simple injection heuristics
    lower = query.lower()
    if "--" in lower or ";" in lower:
        safety["reasons"].append("multi-statement or inline comment detected")
    return safety
