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
        #doc = f"Table: {table}, Columns: {columns_str}"
        doc = {table: columns}  # Store as dict for better structure
        schema_docs.append(doc)
    
    conn.close()
 
    return schema_docs

# # To check if sql query doesnst have unqualified columns in case of joins. Still WIP, need to handle edge cases and ensure it works correctly with various SQL syntax.
# def has_unqualified_columns(sql_query) -> bool:
#     sql_lower = sql_query.lower()

#     if " join " not in sql_lower:
#         return True

#     tokens = sql_query.replace(",", " ").split()

#     for token in tokens:
#         # skip SQL keywords
#         if token.lower() in {
#             "select", "from", "join", "on", "group", "by",
#             "sum", "count", "avg", "as", "order", "limit"
#         }:
#             print(f"Skipping SQL keyword")
#             continue

#         # detect column without table alias
#         if "." not in token and token.isidentifier():
#             return False

#     return True

def is_safe_query(sql_query) -> bool:
    FORBIDDEN = ["drop", "delete", "update", "insert", "alter", "truncate"]
    if not sql_query or not sql_query.strip():
        return False

    sql_query = sql_query.lower()
    if any(word in sql_query for word in FORBIDDEN):
        return False

    parsed = sqlparse.parse(sql_query)
    if not parsed or len(parsed) > 1:
        return False

    stmt = parsed[0]
    if stmt.get_type() != "SELECT":
        return False

    if ";" in sql_query.strip()[:-1]:
        return False

    # # Used when the function is fully implemented to check for unqualified columns in JOIN queries
    # if not has_unqualified_columns(sql_query):
    #     return False
    return True
    
    

def run_query(sql_query,db_name):
    db_file = f"/data/{db_name}.db"
    conn = sqlite3.connect(f"file:{db_file}?mode=ro", uri=True)  # your local DB file
    cursor = conn.cursor()
    response = {
        'Success': True,
        'Data': [],
        'Error': []
    }
    for query in sql_query:
        if is_safe_query(query):
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                result = {"columns": columns, "rows": rows}
                response['Success'] &= True
                response['Data'].append(result)
            except Exception as e:
                response['Success'] &= False
                response['Error'].append(str(e))
            
        else:
            response['Success'] &= False
            response['Error'].append("Unsafe query detected. Only SELECT statements are allowed or there are unqualified columns in a JOIN query.")
    conn.close()  # close the connection
    return response
