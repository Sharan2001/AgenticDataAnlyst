from fastapi import FastAPI
from app.agent import agent_pipeline
import time

app = FastAPI()
@app.get("/analyze")
def analyze(question: str, db_name: str):
    start_time = time.perf_counter()
    result = agent_pipeline(question, None, db_name)
    end_time = time.perf_counter()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
    return result