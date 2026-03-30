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
apiKey = os.getenv("OPENAI_API_KEY")
llm = OpenAI(api_key=apiKey)

# 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
def embed(text):
    return model.encode(text).tolist()