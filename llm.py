from openai import OpenAI
import logging
import json
from icecream import ic
import streamlit as st
from dotenv import load_dotenv
import os
from utils import custom_phrases
load_dotenv()



#########INITIALIZE DBs #########
from db import SupabaseClient, askcole_classifier, askcole_responder, get_summarizer

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
        formatted_message = f"{message['role']}: {message['content']}\n\n"
        formatted_messages += formatted_message

    #classify
    classifier_prompt = askcole_classifier
    category = which_rag(classifier_prompt, messages, 'gpt-3.5-turbo')
    ic(category)
    custom_phrase = custom_phrases[category]

    #update 
    st.session_state.category = category

    #vectorize
    if st.session_state.previous_category == category or st.session_state.previous_category == "":
        v_query = embed_query(formatted_messages)
    else:
        v_query = embed_query(formatted_message)
        st.session_state.previous_category = category
        #now we need to summarize and replace the messages in the middle with the summary
        askcole_summarizer_prompt = get_summarizer()
        askcole_summarizer_prompt = askcole_summarizer_prompt.format(conversation = [f"Lead: {message['content']}\n\n" if message['role'].lower() == 'user' else f"Cole: {message['content']}\n\n" for message in messages[1:-1]])
        askcole_summarizer_prompt = [{'role': 'system', 'content': askcole_summarizer_prompt}]
        summarizer_response = generate_response(askcole_summarizer_prompt, 'gpt-4-turbo-preview', 500)
        ic(summarizer_response)
        messages = [messages[0], {'role': 'user', 'content': '[Original Conversation was long and ommitted. Summary:\n' + summarizer_response}, messages[-1]]
        st.session_state.messages = messages
        
    st.session_state.previous_category = category

    #perform similarity search 
    k_similar = sb.match_documents_knn_with_label(category, v_query, 6)
    k_similar = k_similar.data

    retrieved_chunks = ""
    for i, chunk in enumerate(k_similar):
        retrieved_chunks += f'Chunk {i}:\n' + chunk['content'] + "\n\n"

    #save in session state
    st.session_state.chunks = retrieved_chunks

    #generate cole response
    cole_prompt = askcole_responder
    cole_prompt = cole_prompt.format(RAG_results = retrieved_chunks, classifier_variable = custom_phrase)
    cole_prompt = {'role': 'system', 'content': cole_prompt}

    cole_response = generate_streaming_response([cole_prompt, *messages], 'gpt-4-turbo-preview', 350)

    for chunk in cole_response:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
