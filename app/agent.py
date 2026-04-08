from app.db import run_query
from app.vector_loader import get_vector
from app.llm_calls import question_classification, generate_sql_new, generate_sql_followup, validate_sql

chat_state = {
    "last_question": None,
    "last_sql": None,
    "last_schema": None,
    "last_error": None
}

chat_history={}

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
    chat_state["last_error"] = error

    result=generate_response(sql_query,db_name)

    if db_name not in chat_history:
        chat_history[db_name] = []
    chat_history[db_name].append({"role": "user", "content": question})
    chat_history[db_name].append({"role": "agent", "content": result})

    if validate_sql(question, sql_query, result):
        return [
        {"role": "user", "content": question},
        {"role": "agent", "content": result}
    ]
    else:
        print("Validation failed, regenerating SQL...")
        return agent_pipeline(question, "Validation failed for the generated SQL. Please fix the SQL and try again.", db_name)
    # return result
    # return [
    #     {"role": "user", "content": question},
    #     {"role": "agent", "content": result}
    # ]