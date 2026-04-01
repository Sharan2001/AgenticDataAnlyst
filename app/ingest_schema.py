from app.loader import client,embed
from qdrant_client.http.models import PointStruct

def store_schema_in_qdrant(schema, collection_name):
    points = []

    for i,table_doc in enumerate(schema):
        table_name = list(table_doc.keys())[0]  # parse from doc or keep separately
        columns = table_doc[table_name] 
        #text_to_embed = f"Table: {table_name}, Columns: {columns}"  
        points.append(
            PointStruct(
                id=i,  # or just a unique int
                vector=embed(f"Table: {table_name}, Columns: {columns}"  ),
                payload={
                    "text": table_doc,
                    "table_name": table_name,
                    "columns": columns
                }
            )
        )
    # Check if collection exists, if yes delete and recreate to avoid duplicates. Needs better handling of versoning and updates in real implementation.
    try:
        client.delete_collection(collection_name=collection_name)
    except Exception:
        pass # ignore if collection doesn't exist

    try:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config={"size": 384, "distance": "Cosine"}
        )
    except Exception as e:
        print("Error creating collection:", e)
        return False
    
    client.upsert(collection_name=collection_name, points=points)
    print("Schema stored in Qdrant")
    return True