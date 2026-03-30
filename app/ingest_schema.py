from app.loader import client,embed
from app.db import generate_schema_docs

collection_name = "sample2_schema_docs"

# schema_docs = [
#     "Table: sales, Columns: id, date, revenue, region. Contains company sales data."
# ]
schema = generate_schema_docs("/Users/sharanshivram/Projects/Agents/Data Analyst/data/sample2.db")

points = []

for i, doc in enumerate(schema):
    points.append({
        "id": i,
        "vector": embed(doc),
        "payload": {"text": doc}
    })
try:
    client.delete_collection(collection_name=collection_name)
except Exception:
    pass # ignore if collection doesn't exist
client.recreate_collection(
    collection_name=collection_name,
    vectors_config={"size": 384, "distance": "Cosine"}
)

client.upsert(collection_name=collection_name, points=points)

print("Schema stored in Qdrant")