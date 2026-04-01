import sqlite3
import sqlparse

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
        doc = f"Table: {table}, Columns: {columns_str}"
        schema_docs.append(doc)
    
    conn.close()
    return schema_docs


def is_safe_query(sql: str) -> bool:
    # FORBIDDEN = ["drop", "delete", "update", "insert", "alter", "truncate"]
    # sql_lower = sql.lower()
    
    # if not sql_lower.strip().startswith("select"):
    #     return False
    
    # for word in FORBIDDEN:
    #     if word in sql_lower:
    #         return False
    # return True
    #sql = sql.lower()
    parsed = sqlparse.parse(sql)
    if not parsed:
        return False

    stmt = parsed[0]
    return stmt.get_type() == "SELECT"
    
    

def run_query(sql):
    db_file = "/Users/sharanshivram/Projects/Agents/Data Analyst/data/sample2.db"
    conn = sqlite3.connect(f"file:{db_file}?mode=ro", uri=True)  # your local DB file
    cursor = conn.cursor()
    if is_safe_query(sql):
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = {"columns": columns, "rows": rows}
            conn.close()  # close the connection
            return {
                'Success': True,
                'Data': result,
                'Error': None
            }
        except Exception as e:
            return {
                'Success': False,
                'Data': None,
                'Error': str(e)
            }
        
    else:
        return {
                'Success': False,
                'Data': None,
                'Error': "Unsafe query detected. Only SELECT statements are allowed."
            } 
