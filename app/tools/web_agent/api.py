# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from agent import run_agent_internal  # import internal logic

# app = FastAPI()

# # Request schema
# class PromptRequest(BaseModel):
#     prompt: str

# # Response schema
# class AgentResponse(BaseModel):
#     output: str

# @app.post("/web_tool/", response_model=AgentResponse)
# async def run_agent(req: PromptRequest):
#     try:
#         output = await run_agent_internal(req.prompt)
#         return {"output": output}
#     except Exception as e:
#         # Log error if you have a logging system
#         raise HTTPException(status_code=500, detail=str(e))

# api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import run_orchestrator, WebToolInput, WebToolOutput  # import types if needed

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

class AgentResponse(BaseModel):
    output: str

@app.post("/chat/", response_model=AgentResponse)
async def chat(req: PromptRequest):
    try:
        output = await run_orchestrator(req.prompt)
        return {"output": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
