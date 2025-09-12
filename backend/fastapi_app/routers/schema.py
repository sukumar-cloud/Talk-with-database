from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List
import os
from sqlalchemy import create_engine, text
from pymongo import MongoClient

router = APIRouter()

class SchemaRequest(BaseModel):
    db_type: str | None = None
    db_uri: str | None = None

@router.post("/inspect")
def inspect_schema(req: SchemaRequest):
    db_type = req.db_type or os.getenv("DB_TYPE", "mysql")
    db_uri = req.db_uri or os.getenv("DB_URI")
    if db_type == "mysql":
        if not db_uri:
            return {"error": "DB_URI not set"}
        engine = create_engine(db_uri)
        with engine.connect() as conn:
            current_db = conn.execute(text("SELECT DATABASE()"))
            dbname = list(current_db)[0][0]
            tables = conn.execute(text(
                """
                SELECT TABLE_NAME FROM information_schema.tables
                WHERE table_schema = :db
                ORDER BY TABLE_NAME
                """
            ), {"db": dbname}).fetchall()
            table_names = [t[0] for t in tables]
            columns: Dict[str, List[Dict[str, Any]]] = {}
            for t in table_names:
                cols = conn.execute(text(
                    """
                    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
                    FROM information_schema.columns
                    WHERE table_schema = :db AND table_name = :t
                    ORDER BY ORDINAL_POSITION
                    """
                ), {"db": dbname, "t": t}).fetchall()
                columns[t] = [
                    {"name": c[0], "type": c[1], "nullable": c[2]} for c in cols
                ]
        return {"db": dbname, "tables": table_names, "columns": columns}
    elif db_type == "mongodb":
        mongo_uri = db_uri or os.getenv("MONGO_URI")
        client = MongoClient(mongo_uri)
        dbname = client.get_default_database().name if client.get_default_database() else "default"
        db = client[dbname]
        collections = db.list_collection_names()
        return {"db": dbname, "collections": collections}
    else:
        return {"error": f"Unsupported db_type: {db_type}"}
