
from agents import Agent, Runner, WebSearchTool, function_tool
import logging
import os
from app.tools.web_agent.schema import WebToolInput, WebToolOutput
from dotenv import load_dotenv
import requests
from IPython.display import display, JSON


load_dotenv(override=True)

logger = logging.getLogger("uvicorn.error")

@function_tool(
    name_override="web_tool",
    description_override="Performs real-time web search and returns a concise textual answer.",
)
async def web_tool(input: WebToolInput) -> WebToolOutput:
    """
    Runs a lightweight web-search agent and returns WebToolOutput(answer=str).
    """
    try:

        logger.info("[RUNNING] Web tool")
        print("[RUNNING] Web tool")

        BASE_URL = "http://192.168.22.20:8015"
        ENDPOINT = "/web_tool/" 
        URL = BASE_URL + ENDPOINT

        payload = {
        "query": input.query
        # "instructions": "Answer in one word and cite a reliable source."
        }

        # try:
        fo = requests.post(
            URL, 
            json=payload,
            # Set a reasonable timeout for external API calls (e.g., 30 seconds)
            timeout=30 
        ).json()

        print("[Web tool] outout", str(fo))

        #     # --- Process Response ---
        #     if response.status_code == 200:
        #         logger.info("\n Success! Web Agent executed.")
                
        #         # FastAPI returns a JSON response which requests.json() converts to a Python dict
        #         data = response.json()

        #         return WebToolOutput(answer=data.get("answer", "No answer found."))
            

        # except requests.Timeout:
        #     logger.error("Request to web tool timed out.")
        #     return WebToolOutput(answer="Web search timed out.")
        # except requests.RequestException as e:
        #     logger.error(f"Request to web tool failed: {e}")
        #     return WebToolOutput(answer="Web search failed due to a request error.")
        
        # except:
        #     logger.error(f"Request to web tool failed: {e}")
        #     return WebToolOutput(answer="Web search failed due to a request error.")

        # pc = require_ctx("prompt_var", prompt_var)
        # instructions = pc['GenericWebSearchAgent']

        # web_agent = Agent(
        #     name="WebAgent",
        #     model=os.getenv("WEB_AGENT_MODEL", "gpt-5-mini"),
        #     instructions=instructions,
        #     tools=[WebSearchTool()],
        #     output_type=WebToolOutput
        # )

        # result = await Runner.run(web_agent, input.query)
        # fo = getattr(result, "final_output", None)

        logger.info("[FINISHED] Web tool")
        print("[FINISHED] Web tool")

        # Normalize to WebToolOutput(answer=...)
        if isinstance(fo, WebToolOutput):
            return fo
        if isinstance(fo, dict):
            return WebToolOutput(answer=str(fo.get("answer", "")))
        return WebToolOutput(answer=str(fo) if fo is not None else "")


    except Exception:
        logger.exception("web_tool failed")
        print("web_tool failed")
        return WebToolOutput(answer="Web search failed.")
