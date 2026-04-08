from app.loader import llm
from app.texts import rules,output_format
import json

def question_classification(query):
    prompt = f"""
    Classify the query as:
    - NEW_QUESTION
    - FOLLOW_UP

    Query: {query}

    Answer only one word.
    """
    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You classify user queries into NEW_QUERY or FOLLOW_UP."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def generate_sql_new(question, schema_context):
    prompt = f"""You are a senior data analyst.

        Relevant schema: It is of the format [{{table_name: [column1, column2, column3...]}}]
        {schema_context}

        User query will be about analyzing the data in the database with the above schema. It could be about finding trends, making comparisons, looking up specific values or performing aggregations.

        User query: 
        {question}


        Rules:
        {rules}

        Output format:
        {output_format}
        """

    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate SQL queries only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return json.loads(response.choices[0].message.content.strip())

def generate_sql_followup(question, chat_state):
    prompt = f"""You are a senior data analyst.

        The user has already asked a question and you generated SQL for it. The user is now asking a follow-up question to fix the error/or make a modification to the previous question.
        Analyze the error(if any) and fix the SQL accordingly.

        Here is the previous question and the SQL you generated for it:
        Previous question: {chat_state['last_question']}
        Generated SQL: {chat_state['last_sql']}
        Error from executing SQL: {chat_state['last_error']}
        Relevant schema: {chat_state['last_schema']} - It is of the format [{{table_name: [column1, column2, column3...]}}]
        Now the user is asking this follow-up question:
        Follow-up question: {question}

        Rules:
        {rules}
        
        Output format:
        {output_format}
        """

    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You generate SQL queries only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return json.loads(response.choices[0].message.content.strip())

def validate_sql(question, sql, result_text):
    prompt = f"""
You are a data analyst.

Question:
{question}

SQL Query:
{sql}

Query Result:
{result_text}

Does this result correctly answer the question?

Answer ONLY in this format:
YES or NO
Do not give any explanations, just answer YES or NO.
If it is valid say YES, if not say NO.
"""

    response = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    output = response.choices[0].message.content

    if "YES" in output:
        return True
    else:
        return False
    