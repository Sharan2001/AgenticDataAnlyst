import os
import time
import pandas as pd

CACHE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(CACHE_DIR, "..", "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "data_cache.parquet")
TTL_SECONDS = 300  

def is_cache_valid():
    if not os.path.exists(CACHE_FILE):
        return False
    
    last_modified = os.path.getmtime(CACHE_FILE)
    age = time.time() - last_modified
    return age < TTL_SECONDS

def load_cache():
    df = pd.read_parquet(CACHE_FILE)
    return df.to_string(index=False)

def save_cache(data):
    cleaned_data = []
    for point in data:
        if hasattr(point, "payload"):
            cleaned_data.append(point.payload)
        else:
            cleaned_data.append(point)
    if not cleaned_data:
        raise ValueError("No data to save")

    df = pd.DataFrame(cleaned_data)
    df.to_parquet(CACHE_FILE, index=False) 
    print("Cache saved to data_cache.parquet") 
