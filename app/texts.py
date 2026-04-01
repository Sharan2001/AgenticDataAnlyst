rules="""
        - Only use tables and columns from schema
        - Always generate valid SQLite SQL
        - Use proper JOINs where needed
        - Use only SELECT statements, no other SQL commands are allowed
        - Do not include any comments in the SQL
        - Use aliases for computed columns
        - Do not add sql code block markers like ```sql
        - Return only the SQL query without any explanations or apologies.
        - Do not hallucinate columns
        - ALWAYS use table aliases (e.g., c, o, p)
        - ALWAYS prefix columns with table aliases (e.g., c.customer_id)
        - NEVER use unqualified column names in JOIN queries
        - Always include LIMIT 100 unless aggregation
        - Always give column names when giving results, do not return unnamed columns, so its easier to read the results and debug if needed and create visualizations on top of it. For example, if im asking for a count of customers, return "SELECT COUNT(customer_id) AS customer_count FROM customers" instead of "SELECT COUNT(customer_id) FROM customers", or for a trend of sales by month, return "SELECT strftime('%Y-%m', order_date) AS month, SUM(sales) AS total_sales FROM orders GROUP BY month" instead of "SELECT strftime('%Y-%m', order_date), SUM(sales) FROM orders GROUP BY strftime('%Y-%m', order_date)"
        - Try to show as much data as possible. Use data from the user question, like if they say 2025, try to include that in the column name.
        - Always add ; at the end of the query so it can be executed directly
        - If there is no join possible due to lack of foreign keys, use subqueries instead, or generate multiple queries if needed, but try to generate a single query if possible.
"""

output_format = """
    Return ONLY JSON:
    {   
        "intent": "aggregation | trend | comparison | lookup",
        "sql": ["valid SQL query 1", "valid SQL query 2 if needed", ...], It must be a list of SQL queries, even if there is only one query. This is to allow for multiple queries if needed.
        "explanation": "Short explanation of the SQL query. I will use this for explanation of the results and for creating visualizations, so it should be concise and to the point, and not include any apologies or extraneous information."
    }
"""
