import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import nlu, schema, generate, validate, rank, execute

app = FastAPI(title="Talk-with-Database API", version="0.1.0")

# CORS - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(nlu.router, prefix="/nlu", tags=["nlu"]) 
app.include_router(schema.router, prefix="/schema", tags=["schema"]) 
app.include_router(generate.router, prefix="/generate", tags=["generate"]) 
app.include_router(validate.router, prefix="/validate", tags=["validate"]) 
app.include_router(rank.router, prefix="/rank", tags=["rank"]) 
app.include_router(execute.router, prefix="/execute", tags=["execute"]) 

@app.get("/")
def root():
    return {"message": "FastAPI service is running"}
