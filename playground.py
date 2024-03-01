from db import SupabaseClient
import os
from langchain.docstore.document import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings
from icecream import ic

loader = DirectoryLoader('docs/discovery')
documents = loader.load()
text_splitter = SemanticChunker(OpenAIEmbeddings())
docs = text_splitter.split_documents(documents)

### OpenAIEmbeddings
from openai import OpenAI
client = OpenAI()

def embed_query(text: str):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-large",
        dimensions = 1536
    )
    return response.data[0].embedding
##


##supabase
url = os.getenv("AK_SB_URL")
key = os.getenv("AK_SB_KEY")
sb = SupabaseClient(url, key)
##

for doc in docs:
    content = doc.page_content
    source = doc.metadata['source']
    path, source = os.path.split(source)

    embedding = embed_query(content)

    to_upload = {
        'content': content,
        'source': source,
        'embedding': embedding
    }

    try:
        test = sb.insert('vdb', to_upload)
        ic(test)

        embedding_id = test.data[0]['id']

        try:
            to_add_to_labels_table = {
                'vdb_id': embedding_id,
                'label': 'discovery'
            }
            test = sb.insert('label', to_add_to_labels_table)
        except:

            ic("Failed to add to labels table")

    except Exception as e:
        ic(e)

    

# CONNECTION_STRING = "postgresql+psycopg2://harrisonchase@localhost:5432/test3"

# COLLECTION_NAME = "state_of_the_union_test"

# db = PGVector.from_documents(
#     embedding=embeddings,
#     documents=docs,
#     collection_name=COLLECTION_NAME,
#     connection_string=CONNECTION_STRING,
