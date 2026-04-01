from app.cache import is_cache_valid, load_cache, save_cache
from app.loader import client,embed
from app.ingest_schema import store_schema_in_qdrant
from app.db import generate_schema_docs
from qdrant_client.models import Filter, FieldCondition, MatchAny

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

def get_relevant_schema(question, db_name, top_k=5):
    collection_name = f"{db_name}_schema_docs"
    if collection_name not in client.get_collections().collections:
        schema = generate_schema_docs(f"data/{db_name}.db")
        if store_schema_in_qdrant(schema, collection_name):
            print("Schema ingested successfully, retrying query...")
        else:
            return "Failed to ingest schema."

    # query_tokens = question.lower().split()
    # filter_conditions = [FieldCondition(key="columns", match=MatchAny(any=query_tokens))]

    search_result = client.query_points(
        collection_name=collection_name,
        query=embed(question),
        limit=top_k,
        #query_filter=Filter(must=filter_conditions)
    )
        
    if search_result and search_result.points:
        return [p.payload["text"] for p in search_result.points]
    else:
        return "No relevant schema found."


def get_vector(question, db_name):
    if is_cache_valid(db_name):
        print("Using cached parquet file")
        return load_cache(db_name)
    
    print("Fetching fresh data from Qdrant...")
    data = get_relevant_schema(question,db_name)
    print("Data fetched from Qdrant:", data)
    save_cache(data,db_name)
    
    return data