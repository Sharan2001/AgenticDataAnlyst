import os
from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.agent import agent_pipeline
from frontend import *
import time

app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
def home():
    return FileResponse("frontend/home.html")

UPLOAD_FOLDER = "data"
#os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload")
async def upload_db(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"message": "Uploaded successfully"}

@app.get("/list-dbs")
def list_dbs():
    return [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".db")]



@app.get("/analyze")
def analyze(question: str, db_name: str):
    db_name = db_name.replace(".db", "")
    start_time = time.perf_counter()
    result = agent_pipeline(question, None, db_name)
    end_time = time.perf_counter()
    print(f"Total execution time: {end_time - start_time:.2f} seconds","\n")
    #print("Final Result:", result)
    return result