# supabase_client.py

from supabase import create_client
import logging
from icecream import ic

class SupabaseClient:

    def __init__(self, url:str, key:str):
        self.url = url
        self.key = key
        self.db = create_client(self.url, self.key)


    def insert(self, table_name:str, row:dict):
        try:
            return self.db.table(table_name).insert([row]).execute() 
        except Exception as e:
            logging.exception("Exception occurred")
    
    def get_system_prompt(self, table_name, name):
        try:
            prompt_data = self.db.table(table_name).select("*").eq("name", name).execute() 
            return prompt_data.data[0]['content']
        except Exception as e:
            logging.exception("Exception occurred")
    
    def insert_vector_row(self, row):
        try:
            return self.db.table("vdb").insert([row]).execute()
        except Exception as e:
            logging.exception("Exception occurred")
    
    def get_all_vectors_of_category(self, category):
        try:
            return self.db.table("vdb").select("*").eq("category", category).execute()
        except Exception as e:
            logging.exception("Exception occurred")

    def match_documents_knn_with_label(self, label, query_embedding, match_count):
        # Call the updated SQL function 'match_documents_knn_with_label'
        request = self.db.rpc('match_vdb_knn_with_label', {
            'query_embedding': query_embedding,
            'match_count': match_count,
            'label': label
        })
        # Execute the request and get the result
        result = request.execute()
        return result

class G2SupabaseClient:

    def __init__(self):
        self.url = "https://icuujyoacmcuuryqkpkn.supabase.co"
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImljdXVqeW9hY21jdXVyeXFrcGtuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5MTExNTYxMCwiZXhwIjoyMDA2NjkxNjEwfQ.UacmFvoe3eC4s0a9fhtAJQiKjBHo0Ut1P7xDIC5m_vo"
        self.db = create_client(self.url, self.key)


    def insert(self, table_name:str, row:dict):
        try:
            return self.db.table(table_name).insert([row]).execute() 
        except Exception as e:
            logging.exception("Exception occurred")
    
    def get_system_prompt(self, table_name, name):
        try:
            prompt_data = self.db.table(table_name).select("*").eq("id", name).execute() 
            return prompt_data.data[0]['system_prompt']
        except Exception as e:
            logging.exception("Exception occurred")
    
    def insert_vector_row(self, row):
        try:
            return self.db.table("vdb").insert([row]).execute()
        except Exception as e:
            logging.exception("Exception occurred")
    
    def get_all_vectors_of_category(self, category):
        try:
            return self.db.table("vdb").select("*").eq("category", category).execute()
        except Exception as e:
            logging.exception("Exception occurred")

    def match_documents_knn_with_label(self, label, query_embedding, match_count):
        # Call the updated SQL function 'match_documents_knn'
        request = self.db.rpc('match_vdb_knn_with_label', {
            'query_embedding': query_embedding,
            'match_count': match_count,
            'label': label
        })
        # Execute the request and get the result
        result = request.execute()
        return result

test = G2SupabaseClient()
askcole_classifier = test.get_system_prompt("bots_dev", "askcole_classifier")
askcole_responder = test.get_system_prompt("bots_dev", "askcole_responder")

def get_summarizer():
    askcole_summarizer = test.get_system_prompt("bots_dev", "askcole_summarizer")
    return askcole_summarizer

# #array of 1536 0.5's
# x = [0.5]*1536
# test = sb.match_documents_knn(x, 5)
# print(test)
                                       
