from fastapi import FastAPI
from app.agent import agent_pipeline

app = FastAPI()
@app.get("/analyze")
def analyze(query: str):
    return agent_pipeline(query,None)