# app/data_loader.py
import pandas as pd
from app.cache import is_cache_valid, load_cache, save_cache
from app.loader import client,embed

# def get_relevant_schema(query,top_k=5):
#     search_result = client.query_points(
#         collection_name="sample2_schema_docs",
#         query=embed(query),
#         limit=top_k
#     )
#     if search_result:
#         #return [result.payload["text"] for result in search_result]
#         return search_result.points[0].payload["text"]
#     else:
#         return "No relevant schema found."
    
def get_relevant_schema(query, top_k=5):
    search_result = client.query_points(
        collection_name="sample2_schema_docs",
        query=embed(query),
        limit=top_k
    )

    if search_result and search_result.points:
        # Return a list of texts for all top-k results
        return [point.payload["text"] for point in search_result.points]
    else:
        return ["No relevant schema found."]

def get_vector(query):
    if is_cache_valid():
        print("Using cached parquet file")
        return load_cache()
    
    print("Fetching fresh data from Qdrant...")
    data = get_relevant_schema(query)
    print("Data fetched from Qdrant:", data)
    save_cache(data)
    
    return data