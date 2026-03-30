from app.db import run_query
from app.vector_loader import get_vector
from app.loader import llm

def generate_sql(question, schema_context):
    prompt = f"""
    You are a data analyst.

    Relevant schema:
    {schema_context}

    Convert this question into SQL:
    {question}

    Only return SQL query. Do not include any explanations. The answer must be just the query. 
    Do not add ````sql` code block markers. I want a perfect and precise SQL query without any explanations or apologies.
    I want a perfect and precise SQL query without any explanations or apologies.
    It could be complex with multiple joins, but it should be correct and executable on the database with the above schema. 
    It might not involve joins, so dont simply make it complex unless it has to be.
    """

    # response = llm(prompt, max_new_tokens=150)
    # print("LLM response:", response)
    # return response[0]["generated_text"]
    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate SQL queries only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()


def agent_pipeline(query):
    schema_context = get_vector(query)

    sql = generate_sql(query, schema_context)
    print("Generated SQL:", sql)

    result = run_query(sql)

    return {
        "sql": sql,
        "result": result
    }