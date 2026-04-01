from app.db import run_query
from app.vector_loader import get_vector
from app.loader import llm

def generate_sql(question, schema_context,error):
    prompt = f"""
    You are a data analyst.

    Relevant schema:
    {schema_context}

    Convert this question into SQL:
    {question}

    Currently there is {error} errors(s).

    Only return SQL query. Do not include any explanations. The answer must be just the query. 
    It must only be a Select query. No other SQL commands are allowed. Do not include any comments in the SQL.
    Do not add ````sql` code block markers. I want a perfect and precise SQL query without any explanations or apologies.
    It could be complex with multiple joins, but it should be correct and executable on the database with the above schema. 
    It might not involve joins, so dont simply make it complex unless it has to be.
    If the question is ambiguoud just ask for clarification instead of making assumptions. Do not make any assumptions. If you dont know the answer, just say you dont know. Do not try to make up an answer.
    """

    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate SQL queries only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def generate_response(query):
    result = run_query(query)
    if result['Success']:
        return {
            "result": result['Data']
        }
    else:
        return {
            "Error executing SQL": result['Error']
         }
    
        # Add regeneration logic here

        # print("Error executing SQL:", result['Error'])
        # print("Regenerating SQL...")
        # agent_pipeline(query, result['Error'])

def agent_pipeline(query,error):
    schema_context = get_vector(query)

    sql = generate_sql(query, schema_context,error)
    sql = sql.strip().split(";")[0] + ";" # Ensure only one statement and ends with a semicolon
    print("Generated SQL:", sql)

    return generate_response(sql)