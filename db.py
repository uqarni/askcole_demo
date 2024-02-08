# supabase_client.py

from supabase import create_client
import logging

class SupabaseClient():

    def __init__(self):
        url: str = "https://izkwvhrffzveyuwodakn.supabase.co"
        key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6a3d2aHJmZnp2ZXl1d29kYWtuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNDczNDY4MywiZXhwIjoyMDIwMzEwNjgzfQ.5Jf2v0QzT3ip5mqbJPhOszFS3BxPoFguHhdddPaqYxI"
        self.db = create_client(url, key)


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

    def match_documents_knn(self, query_embedding, match_count):
        # Call the updated SQL function 'match_documents_knn'
        request = self.db.rpc('match_vdb_knn', {
            'query_embedding': query_embedding,
            'match_count': match_count
        })
        # Execute the request and get the result
        result = request.execute()
        return result


# sb = SupabaseClient()
# #array of 1536 0.5's
# x = [0.5]*1536
# test = sb.match_documents_knn(x, 5)
# print(test)
                                       
