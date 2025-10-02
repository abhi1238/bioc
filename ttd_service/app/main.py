
# ttd_service/app/main.py

from fastapi import FastAPI, HTTPException
from app.ttd_data_loader import return_preprocessed_ttd

app = FastAPI(title="BioChirp TTD Service", version="1.0.0", description="API to serve preprocessed TTD Parquet tables")
db = return_preprocessed_ttd()

@app.get("/tables")
def list_tables():
    return list(db.keys())

@app.get("/table/{table_name}")
def get_table(table_name: str):
    if table_name not in db:
        raise HTTPException(status_code=404, detail="Table not found")
    return db[table_name].to_dicts()


