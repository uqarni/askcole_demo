from vdb import initialize_all_vdbs, find_examples
from fastapi import FastAPI, HTTPException
from typing import Optional

#initialize dbs
dbs = initialize_all_vdbs()

app = FastAPI()

#find examples
def find_examples(db, query, k=5):
    docs = db.similarity_search(query, k=k)

    examples = ""
    i = 1
    for doc in docs:
       examples += f'\n\nEXAMPLE {i}:\n' + doc.page_content
       i+=1
    return examples


# Replace 'YourDatabaseType' with the actual type of your db object
@app.get("/find-examples/")
async def find_examples_endpoint(db, query: str, k: Optional[int] = 5):
    try:
        db = dbs.get('db', None)
        if db:
            examples = find_examples(db, query, k)
            return {"examples": examples}
        return {"examples": ""}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        
#using uvicorn to run the app:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)