from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Union
import uvicorn
from agents import Agent, Runner, WebSearchTool 
from schema import WebToolInput, WebToolOutput
from dotenv import load_dotenv
load_dotenv(override=True)
from pathlib import Path


md_file_path = "web_tool_prompt.md"

with open(md_file_path, "r", encoding="utf-8") as f:
    prompt_md = f.read()

WebToolInput.model_rebuild()
WebToolOutput.model_rebuild()

app = FastAPI()

# Setup your agent


@app.get("/")
def root():
    return {"message": "Web service tool is running"}


@app.post("/web_tool/", response_model=WebToolOutput)
async def run_web_search(input_data: WebToolInput):
    try:

        # Use user-supplied instructions if present, else fallback to default
        system_prompt = input_data.instructions or prompt_md

        # Dynamically instantiate agent for this request
        web_agent = Agent(
            name="WebAgent",
            model="gpt-4o-mini",
            instructions=system_prompt,
            tools=[WebSearchTool()],
            output_type=WebToolOutput
        )

        result = await Runner.run(web_agent, input_data.query)
        fo = getattr(result, "final_output", None)

        if isinstance(fo, WebToolOutput):
            return fo
        elif isinstance(fo, dict):
            return WebToolOutput(
                answer=str(fo.get("answer", "No answer found."))
            )
        else:
            return WebToolOutput(
                answer=str(fo) if fo is not None else "Agent returned empty response."
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {e}")
