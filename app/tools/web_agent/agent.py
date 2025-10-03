# # agent.py

# from agents import Agent, Runner
# from dotenv import load_dotenv

# load_dotenv(override=True)

# # 1. Define the agent (or multiple agents or tools)
# agent = Agent(
#     name="Assistant",
#     instructions="You are a helpful assistant that responds to user prompts."
# )

# # 2. Optional: add tools, subagents, etc.

# # 3. Helper function to run the agent logic internally
# async def run_agent_internal(prompt: str) -> str:
#     """
#     Run the agent logic for a given prompt, return the final output string.
#     """
#     result = await Runner.run(agent, prompt)
#     return result.final_output

# agent.py

from agents import Agent, Runner, function_tool
from typing import Optional

# Suppose WebToolInput and WebToolOutput are defined somewhere or imported
# from your tool definitions / agents SDK
# For example:
from pydantic import BaseModel

class WebToolInput(BaseModel):
    query: str

class WebToolOutput(BaseModel):
    answer: Optional[str]
    sources: Optional[list[str]]

# Define the web sub-agent (handles web search queries)
web_agent = Agent(
    name="gpt-4o-mini",
    instructions="You are a web search agent. Answer queries using tools available.",
    tools=[],
    output_type=None
)

# Define the web_tool function, decorated as a tool
@function_tool(
    name_override="web_tool",
    description_override=(
        "Performs real-time web search using Tavily and related APIs. "
        "Returns a direct answer and a list of source URLs."
    )
)
async def web_tool(input: WebToolInput) -> WebToolOutput | None:
    try:
        result = await Runner.run(web_agent, input.query)
        output_obj = result.final_output
        # Assume output_obj is a dict with keys "answer", "sources"
        return WebToolOutput(
            answer=output_obj.get("answer", ""),
            sources=output_obj.get("sources", [])
        )
    except Exception as e:
        # You might want to log the error
        return None

# Now define the orchestrator agent that uses web_tool
orchestrator_agent = Agent(
    name="Orchestrator",
    instructions="You are the orchestrator. Use web_tool for factual queries.",
    tools=[web_tool],
    model="gpt-5-mini"  # or whichever model you use
)

# A helper to run orchestrator
async def run_orchestrator(prompt: str) -> str:
    result = await Runner.run(orchestrator_agent, prompt)
    return result.final_output
