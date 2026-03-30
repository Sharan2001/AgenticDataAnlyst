from fastapi import FastAPI
from app.agent import agent_pipeline
from app.db import init_db

app = FastAPI()

init_db()

@app.get("/analyze")
def analyze(query: str):
    return agent_pipeline(query)