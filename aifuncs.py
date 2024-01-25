from openai import OpenAI
import os
import logging
import time
import json

#########LANGCHAIN EXAMPLES PULLER #########
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_experimental.text_splitter import SemanticChunker


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

def initialize_vdb(foldername):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to the .txt file, in this case, the book Meditations by Marcus Aurelius
    #txt_file_path = os.path.join(dir_path, 'meditations.txt')

    loader = DirectoryLoader(f'rag_docs/{foldername}')
    documents = loader.load()
    
    text_splitter = SemanticChunker(OpenAIEmbeddings())
    #text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, length_function = len, is_separator_regex = False)
    docs = text_splitter.split_documents(documents)
    
    #probably need to do retries here too
    embeddings = OpenAIEmbeddings()

    db = FAISS.from_documents(docs, embeddings)
    print(f'{foldername} db initialized')
    return db

def find_examples(db, query, k=5):
    docs = db.similarity_search(query, k=k)

    examples = ""
    i = 1
    for doc in docs:
       examples += f'\n\nEXAMPLE {i}:\n' + doc.page_content
       i+=1
    return examples

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

def colify(messages, suggestion):
    with open('prompts/cole_prompt.txt', 'r') as file:
        prompt = file.read()
    
    prompt = prompt.format(summary=suggestion)
    prompt = {'role': 'system', 'content': prompt}
    messages = [prompt, *messages]
    print('##')
    [print(message) for message in messages]
    print('##')
    response = generate_streaming_response(messages, "gpt-4-1106-preview", max_tokens=200)
    for chunk in response:
        yield chunk 


def initialize_all_vdbs():
    call_intro = initialize_vdb('call_intro')
    goal_first_or_problem_first = initialize_vdb('goal_first_or_problem_first')
    objection_handling = initialize_vdb('objection_handling')
    pitch = initialize_vdb('pitch')
    skilled_questions = None #initialize_vdb('skilled_questions')
    unknown_or_NA = None #initialize_vdb('unknown_or_NA')
    
    dbs = {
        "call_intro": call_intro,
        "goal_first_or_problem_first": goal_first_or_problem_first,
        "objection_handling": objection_handling,
        "pitch": pitch,
        "skilled_questions": skilled_questions,
        "unknown_or_NA": unknown_or_NA
    }

    return dbs

def generate_cole_response(messages, dbs, session_state, max_tokens = 200):
    '''messages are always promptless'''

    #classify inquiry
    topic = which_rag(messages, 'gpt-3.5-turbo')
    print('topic: ', topic)
    session_state["topic"] = topic

    #pull prompt
    with open('prompts/answer_prompt.txt', 'r') as file:
        answer_prompt = file.read()
        session_state["answer_prompt"] = answer_prompt

    #get appropriate examples from vector database
    if topic != 'unknown_or_NA' and topic != 'skilled_questions':
        db = dbs[topic]

        #do similarity search and get examples
        examples = find_examples(db, messages[-1]['content'])
        session_state["examples"] = examples

        #format custom system prompt
        answer_prompt = answer_prompt + examples
        answer_prompt = answer_prompt.format(incoming = messages[-1]['content'])

    custom_prompt = {"role": "system", "content": answer_prompt}

    #format messages for response generation
    llm_messages = [custom_prompt, *messages]

    #generate summary
    summary = generate_response(llm_messages, "gpt-3.5-turbo", max_tokens=600)
    print('got outbound message')
    session_state["summary"] = summary

    #Cole-ify
    outbound = colify(messages, summary)
    print('streaming colified response')

    for chunk in outbound:
        if chunk != None:
            yield chunk

messages = [
    {'role': 'system', 'content': 'You are a salesperson talking to a customer. You are trying to figure out what to say next.'},
    {'role': 'user', 'content': 'How can I intro my calls better?'}
]


# test = generate_streaming_response(messages, "gpt-3.5-turbo", max_tokens=200)
# for chunk in test:
#     print(chunk)