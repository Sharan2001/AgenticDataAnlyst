from app.db import run_query
from app.vector_loader import get_vector
from app.loader import llm
from app.texts import rules,output_format
import json

chat_state = {
    "last_question": None,
    "last_sql": None,
    "last_schema": None,
    "history": []
}
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
        Error from executing SQL: {chat_state['history'][-1]['error']}
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

def generate_response(sql_query,db_name):
    result = run_query(sql_query,db_name)
    if result['Success']:
        return {
            "result": [i for i in result['Data']]
        }
    else:
        return {
            "Error executing SQL": [i for i in result['Error']]
        }
    
        # Add regeneration logic here

        # print("Error executing SQL:", result['Error'])
        # print("Regenerating SQL...")
        # agent_pipeline(query, result['Error'])

def agent_pipeline(question,error,db_name):
    question_type = question_classification(question)

    if question_type == "NEW_QUESTION" or not chat_state["last_question"]:  
        print("New Question")
        schema_context = get_vector(question,db_name)
        print("Schema context fetched:", schema_context)
        chat_state["last_schema"] = schema_context
        response = generate_sql_new(question, schema_context)
    else:
        print("Follow-up Question")
        response = generate_sql_followup(question, chat_state)  

    sql_query = []
    for query in response['sql']:
        sql_query.append(query.strip().split(";")[0] + ";") # Ensure only one statement and ends with a semicolon
        chat_state["last_sql"] = sql_query
    
    chat_state["last_question"] = question
    chat_state["history"].append({"question": question, "sql": sql_query, "error": error})

    print("Intent:", response['intent'],"\n")
    print("Generated SQL:", sql_query,"\n")
    print("Explanation:", response['explanation'])

    return generate_response(sql_query,db_name)