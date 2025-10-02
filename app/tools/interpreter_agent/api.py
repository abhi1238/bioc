# app/tools/interpreter_agent/api.py

from fastapi import FastAPI, HTTPException, Request
from agent import interpreter  # Use your actual agent path
from schema import QueryInterpreterOutputGuardrail  # Or real import
import asyncio

app = FastAPI(title="BioChirp Interpreter Agent", version="1.0")

@app.post("/interpret", response_model=QueryInterpreterOutputGuardrail)
async def interpret_endpoint(payload: dict):
    user_input = payload.get("user_input")
    if not user_input:
        raise HTTPException(status_code=400, detail="user_input required")
    try:
        # If you're already in an event loop (e.g., if run in async context), just call directly.
        result = await interpreter(user_input)
        if result is None:
            raise HTTPException(status_code=500, detail="Interpreter returned None")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interpreter failed: {e}")

@app.get("/health")
async def health():
    return {"status": "ok"}
