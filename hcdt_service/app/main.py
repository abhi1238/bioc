
from fastapi import FastAPI, HTTPException
from hcdt_data_loader import return_preprocessed_hcdt

app = FastAPI(title="BioChirp HCDT Service", version="1.0.0", description="API to serve preprocessed HCDT Parquet tables")
db = return_preprocessed_hcdt()

@app.get("/")
async def read_root():
    return {"message": "Hello from CTD"}

@app.get("/tables")
def list_tables():
    """
    List all available HCDT table keys.
    """
    return list(db.keys())

@app.get("/table/{table_name}")
def get_table(table_name: str):
    """
    Return the full table (as a list of dicts) for the specified HCDT table.
    """
    if table_name not in db:
        raise HTTPException(status_code=404, detail="Table not found")
    return db[table_name].to_dicts()
