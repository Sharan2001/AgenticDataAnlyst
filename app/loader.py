from transformers import pipeline
from sentence_transformers import SentenceTransformer
import os
from openai import OpenAI
from qdrant_client import QdrantClient


client = QdrantClient(
    url="http://localhost:6333"
)

model = SentenceTransformer("all-MiniLM-L6-v2")
#llm = pipeline(task="text2text-generation", model="google/flan-t5-small")  # Using a smaller model for faster generation
apiKey = os.getenv("YOUR_OPENAI_API_KEY")
llm = OpenAI(api_key=apiKey)

def embed(text):
    return model.encode(text).tolist()