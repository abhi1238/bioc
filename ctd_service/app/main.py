from fastapi import FastAPI, HTTPException
from data_loader import return_preprocessed_ctd

app = FastAPI(title="BioChirp CTD Service", version="1.0.0", description="API to serve preprocessed CTD Parquet tables")
db = return_preprocessed_ctd()

@app.get("/tables")
def list_tables():
    """
    List all available CTD table keys.
    """
    return list(db.keys())

@app.get("/table/{table_name}")
def get_table(table_name: str):
    """
    Return the full table (as a list of dicts) for the specified CTD table.
    """
    if table_name not in db:
        raise HTTPException(status_code=404, detail="Table not found")
    return db[table_name].to_dicts()
