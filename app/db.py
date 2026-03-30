import sqlite3

conn = sqlite3.connect("data/sample.db")

def init_db():
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        date TEXT,
        revenue REAL,
        region TEXT
    )
    """)

    cursor.execute("""
    INSERT INTO sales (date, revenue, region) VALUES
    ('2024-01-01', 1000, 'North'),
    ('2024-02-01', 1500, 'South'),
    ('2024-03-01', 2000, 'North')
    """)

    conn.commit()

def generate_schema_docs(db_path: str) -> list[str]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    schema_docs = []
    
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [col[1] for col in cursor.fetchall()]  # col[1] is the column name
        columns_str = ", ".join(columns)
        # Optional: you can add your own descriptions for tables
        doc = f"Table: {table}, Columns: {columns_str}"
        schema_docs.append(doc)
    
    conn.close()
    return schema_docs

def run_query(sql):
    # create a new connection for this request
    conn = sqlite3.connect("/Users/sharanshivram/Projects/Agents/Data Analyst/data/sample2.db")  # your local DB file
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()  # close the connection
    return result
