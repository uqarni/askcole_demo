from openai import OpenAI
import logging
import json
from icecream import ic
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()



#########INITIALIZE DBs #########
from db import SupabaseClient, askcole_classifier, askcole_responder

gp_sb_key = os.getenv("GP_SB_KEY")
gp_sb_url = os.getenv("GP_SB_URL")

ak_sb_key = os.getenv("AK_SB_KEY")
ak_sb_url = os.getenv("AK_SB_URL")

sb = SupabaseClient(ak_sb_url, ak_sb_key)


#########OPENAI API#########
openai = OpenAI(max_retries = 10)

def generate_response(messages, model, max_tokens = 200):
    try:
        response = openai.chat.completions.create(model=model, messages=messages, max_tokens=max_tokens, temperature=0)
        return response.choices[0].message.content
    except Exception as e:
        #always log exceptions
        logging.exception(f"Exception occurred: {e}")

    return False

def generate_streaming_response(messages, model, max_tokens = 200):
    try:
        response = openai.chat.completions.create(model=model, messages=messages, max_tokens=max_tokens, temperature=0, stream=True)
        for chunk in response:
            yield chunk
    except Exception as e:
        #always log exceptions
        logging.exception(f"Exception occurred: {e}")

    return False

def embed_query(text: str):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-large",
        encoding_format = 'float',
        dimensions = 1536
    )
    return response.data[0].embedding


tools=[
    {
        "type": "function",
        "function": 
        {
            "name": "classify_inquiry",
            "description": "This function needs as an input which category of knowledge base documentation the bot should reference to find the answer.",
            "parameters": 
            {
                "type": "object",
                "properties": 
                {
                    "topic":
                    {
                        "type": "string",
                        "enum": ["call_intro", "discovery", "transition", "pitching", "closing", "objection_handling"],
                        "description": "Select the category of knowledge base documentation the bot should reference to find the answer.",
                    },
                },
                "required": ["topic"]
            }

        }
    }
]

#messages has a system prompt as the first message
def which_rag(prompt, messages, model, tools = tools):
    
    system_prompt = {'role': 'system', 'content': prompt}
    messages = [system_prompt, *messages]
    try:
        response = openai.chat.completions.create(
            model=model, 
            messages=messages, 
            max_tokens=200, 
            temperature=0,
            tools = tools,
            tool_choice = {"type": "function", "function": {"name": "classify_inquiry"}}
            )
        return json.loads(response.choices[0].message.tool_calls[0].function.arguments)['topic']

    except Exception as e:
        #always log exceptions
        logging.exception(f"Exception occurred: {e}")

    return False

messages = [
    {'role': 'user', 'content': 'How can I intro my calls better?'}
]

def full_response(messages):
    formatted_messages = ""
    for message in messages:
        formatted_messages += f"{message['role']}: {message['content']}\n\n"

    #classify
    classifier_prompt = askcole_classifier
    category = which_rag(classifier_prompt, messages, 'gpt-3.5-turbo')
    ic(category)
    #st.session_state.category = category

    #vectorize
    v_query = embed_query(formatted_messages)

    #perform similarity search 
    k_similar = sb.match_documents_knn_with_label(category, v_query, 6)
    k_similar = k_similar.data

    retrieved_chunks = ""
    for i, chunk in enumerate(k_similar):
        retrieved_chunks += f'Chunk {i}:\n' + chunk['content'] + "\n\n"

    ic(retrieved_chunks)
    #save in session state
    #st.session_state.chunks = retrieved_chunks

    #generate cole response
    cole_prompt = askcole_responder
    cole_prompt = cole_prompt.format(RAG_results = retrieved_chunks, classifier_variable = "Use the snippets below to answer")
    cole_prompt = {'role': 'system', 'content': cole_prompt}

    cole_response = generate_streaming_response([cole_prompt, *messages], 'gpt-4-turbo-preview', 350)

    for chunk in cole_response:
        if chunk is not None:
            yield chunk.choices[0].delta.content
