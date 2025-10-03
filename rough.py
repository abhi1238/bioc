# # # from fastapi import FastAPI
# # # from pydantic import BaseModel
# # # from agents import Agent, Runner
# # # from dotenv import load_dotenv
# # # load_dotenv(override=True)

# # # from pydantic import BaseModel

# # # class RunAgentResponse(BaseModel):
# # #     output: str


# # # app = FastAPI()

# # # class PromptRequest(BaseModel):
# # #     prompt: str

# # # @app.post("/run_agent/")
# # # async def run_agent(request: PromptRequest):
# # #     agent = Agent(name="Assistant", instructions="You are a helpful assistant")
# # #     result = await Runner.run(agent, request.prompt)
# # #     return {"output": result.final_output}

# # from fastapi import FastAPI
# # from pydantic import BaseModel
# # from agents import Agent, Runner

# # app = FastAPI()

# # class PromptRequest(BaseModel):
# #     prompt: str

# # class RunAgentResponse(BaseModel):
# #     output: str

# # @app.post("/run_agent/", response_model=RunAgentResponse)
# # async def run_agent(request: PromptRequest):
# #     agent = Agent(name="Assistant", instructions="You are a helpful assistant")
# #     result = await Runner.run(agent, request.prompt)
# #     return {"output": result.final_output}

# # # from fastapi import FastAPI
# # # from pydantic import BaseModel
# # # import requests

# # # from agents import Agent, Runner, function_tool

# # # app = FastAPI()

# # # class PromptRequest(BaseModel):
# # #     prompt: str

# # # # --- Define sub-agents and their API endpoints in this app ---

# # # booking_agent = Agent(
# # #     name="Booking Agent",
# # #     instructions="You handle booking requests (flights, hotels, tickets, etc.)."
# # # )

# # # refund_agent = Agent(
# # #     name="Refund Agent",
# # #     instructions="You handle refund / cancellation requests."
# # # )

# # # @app.post("/booking/")
# # # async def booking_endpoint(req: PromptRequest):
# # #     result = await Runner.run(booking_agent, req.prompt)
# # #     return {"output": result.final_output}

# # # @app.post("/refund/")
# # # async def refund_endpoint(req: PromptRequest):
# # #     result = await Runner.run(refund_agent, req.prompt)
# # #     return {"output": result.final_output}

# # # # --- Define tools for orchestrator, which call those endpoints ---

# # # @function_tool
# # # def booking_expert(prompt: str) -> str:
# # #     """
# # #     Calls the booking sub-agent via HTTP.
# # #     """
# # #     url = "http://localhost:8000/booking/"  # adjust host/port if needed
# # #     resp = requests.post(url, json={"prompt": prompt})
# # #     resp.raise_for_status()
# # #     return resp.json()["output"]

# # # @function_tool
# # # def refund_expert(prompt: str) -> str:
# # #     """
# # #     Calls the refund sub-agent via HTTP.
# # #     """
# # #     url = "http://localhost:8000/refund/"
# # #     resp = requests.post(url, json={"prompt": prompt})
# # #     resp.raise_for_status()
# # #     return resp.json()["output"]

# # # # --- Orchestrator / customer-facing agent ---

# # # customer_facing_agent = Agent(
# # #     name="Customer-Facing Agent",
# # #     instructions=(
# # #         "You are the front-line agent talking to the user. "
# # #         "If the users request is about booking, call booking_expert. "
# # #         "If its about refunds, call refund_expert."
# # #     ),
# # #     tools=[booking_expert, refund_expert]
# # # )

# # # @app.post("/chat/")
# # # async def chat_endpoint(req: PromptRequest):
# # #     # This is the public endpoint for users to talk to the orchestrator
# # #     result = await Runner.run(customer_facing_agent, req.prompt)
# # #     return {"output": result.final_output}


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# from agents import Agent, Runner

# from dotenv import load_dotenv
# load_dotenv(override=True)

# app = FastAPI()

# class PromptRequest(BaseModel):
#     prompt: str

# class AgentResponse(BaseModel):
#     output: str

# # Prepare the agent (you can also create agent inside each request if preferred)
# agent = Agent(name="Assistant", instructions="Respond to user question.")

# @app.post("/web_tool/", response_model=AgentResponse)
# async def run_agent(req: PromptRequest):
#     try:
#         result = await Runner.run(agent, req.prompt)
#         return {"output": result.final_output}
#     except Exception as e:
#         # Handle errors: wrap or rethrow
#         raise HTTPException(status_code=500, detail=str(e))



# from fastapi import FastAPI
# from pydantic import BaseModel

# # 1. Define the Pydantic model for the request body
# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: bool | None = None

# app = FastAPI()

# @app.post("/items/")
# # 2. Declare the Pydantic model as the function parameter's type
# def create_item(item: Item):
#     # 'item' is now a validated Pydantic object
#     return item


# main.py
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}

@app.get("/")
def read_root():
    return {"Hello": "World"}