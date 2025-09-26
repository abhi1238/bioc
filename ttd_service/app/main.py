
# ttd_service/app/main.py

from fastapi import FastAPI, HTTPException
from .data_loader import return_preprocessed_ttd

app = FastAPI()
db = return_preprocessed_ttd()

@app.get("/tables")
def list_tables():
    return list(db.keys())

@app.get("/table/{table_name}")
def get_table(table_name: str):
    if table_name not in db:
        raise HTTPException(status_code=404, detail="Table not found")
    return db[table_name].to_dicts()
