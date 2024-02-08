from openai import OpenAI
import logging
import json
from icecream import ic

#########LANGCHAIN EXAMPLES PULLER #########
from db import SupabaseClient

sb = SupabaseClient()

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
            yield chunk.choices[0].delta.content
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
                        "enum": ["call_intro", "goal_first_or_problem_first", "objection_handling", "pitch", "skilled_questions", "unknown_or_NA"],
                        "description": "Select call_intro if it is about call introductions, goal_first_or_problem_first if about whether to talk about the goal first or the problem first, objection_handling if about how to handle objections, pitch if about how to pitch, skilled_questions if about specific questions, unknown_or_NA if none of the others.",
                    },
                },
                "required": ["topic"]
            }

        }
    }
]

#messages has a system prompt as the first message
def which_rag(messages, model, tools = tools):
    
    system_prompt = {'role': 'system', 'content': 'You are a salesperson talking to a customer. You are trying to figure out what to say next.'}
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
    {'role': 'system', 'content': 'You are a salesperson talking to a customer. You are trying to figure out what to say next.'},
    {'role': 'user', 'content': 'How can I intro my calls better?'}
]

def full_response(messages):
    #get messages
    # messages = ss.messages

    #pull last message
    query = messages[-1]['content']
    
    #classify
    #TODO 

    #vectorize
    v_query = embed_query(query)

    #perform similarity search 
    k_similar = sb.match_documents_knn(v_query, 4)
    k_similar = k_similar.data

    retrieved_chunks = ""
    for i, chunk in enumerate(k_similar):
        retrieved_chunks += f'Chunk {i}:\n' + chunk['content'] + "\n\n"

    ic(retrieved_chunks)
    #summarize
    #summarizer_prompt = sb.get_system_prompt('prompt', 'summarizer')
    summarizer_prompt = "Your job is to summarize the following chunks of information that was retrieved from out database. It probably has to do with objection handling on a sales call as a sales person. The user asked {query}. The following chunks were retrieved: {retrieved_chunks}. Just respond only with a summary, nothing else."
    summarizer_prompt = summarizer_prompt.format(query = query, retrieved_chunks = retrieved_chunks)
    summarizer_prompt = {'role': 'system', 'content': summarizer_prompt}

    summary = generate_response([summarizer_prompt, *messages], 'gpt-4-1106-preview', 500)
    #remember we might have to reload this or something
    ic(summary)

    #generate cole response
    cole_prompt = sb.get_system_prompt('prompt', 'askcole_objections')
    cole_prompt = cole_prompt.format(summary = summary)
    cole_prompt = {'role': 'system', 'content': cole_prompt}

    cole_response = generate_streaming_response([cole_prompt, *messages], 'gpt-4-1106-preview', 250)

    for chunk in cole_response:
        yield chunk

test = [{"role": "user", "content": "how do I handle financial objections"}]

# result = full_response(test)
# for i in result:
#     print(i)
