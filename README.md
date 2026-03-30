# Agentic Data Analyst

This project provides a local setup for a Qdrant-based data ingestion and query system with Hugging Face integration. It allows you to store database schemas in Qdrant and test queries through a FastAPI interface.

---

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- Python 3.9+
- Git

---

## Setup Instructions
Follow these steps to get the project running:

## 1. Run Qdrant Locally
```bash
docker pull qdrant/qdrant
docker run -d -p 6333:6333 -p 6334:6334 -v "$PWD/qdrant_storage:/qdrant/storage" qdrant/qdrant
```

## 2. Setup Hugging Face
```bash
pip install huggingface_hub
huggingface-cli login
```

## 3. Create Project Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

## 4. Install Dependencies
```bash
pip install -r requirements.txt
# If you install new packages, update requirements.txt
pip freeze > requirements.txt
```

## 5. Export Your API Keys
```bash
export OPENAI_API_KEY="your_api_key_here"
```
# 6. Add Your Database Files
Place your database files in the `data` folder \

data analyst/ \
├── app/                \
├── cache/              \
├── data/               \              
└── requirements.txt \

# 7. Ingest Database Schemas into Qdrant
```bash
python app/ingest_schema.py
```
# 8. Run the App
```bash
uvicorn app.main:app --reload
```
# Open your browser at http://127.0.0.1:8000/docs and use the GET tab to test prompts

