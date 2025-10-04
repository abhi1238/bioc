
from agents import Agent, Runner, WebSearchTool, function_tool
import logging
import os
from app.tools.web_agent.schema import WebToolInput, WebToolOutput
from dotenv import load_dotenv
import requests
from IPython.display import display, JSON


load_dotenv(override=True)

# logger = logging.getLogger("uvicorn.error")
def get_fallback_logger(name="biochirp.tmp"):
    """
    Return a logger instance for the given name, ensuring logging is always available.

    If no root logger handlers are set (e.g., the app is run as a standalone script or test),
    this function will automatically configure a basic console logger with INFO level.
    This ensures that logs are never lost, whether or not a global logging setup exists.

    Args:
        name (str): The name of the logger to retrieve. Use a module- or component-specific
                    string for easier log filtering. Defaults to "biochirp.tmp".

    Returns:
        logging.Logger: Configured logger instance, ready for use.

    Example:
        >>> from app.utils.logger import get_fallback_logger
        >>> logger = get_fallback_logger("biochirp.services")
        >>> logger.info("Logger is ready!")
    """
    logger = logging.getLogger(name)
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
    return logger

@function_tool(
    name_override="web_tool",
    description_override="Performs real-time web search and returns a concise textual answer.",
)
async def web_tool(input: WebToolInput) -> WebToolOutput:
    """
    Runs a lightweight web-search agent and returns WebToolOutput(answer=str).
    """
    try:

        logger = logging.getLogger("uvicorn.error")


        logger.info("[RUNNING] Web tool")
        print("[RUNNING] Web tool")

        BASE_URL = "http://192.168.22.20:8015"
        ENDPOINT = "/web_tool/" 
        URL = BASE_URL + ENDPOINT

        payload = {
        "query": input.query
        }

        # try:
        fo = requests.post(
            URL, 
            json=payload,
            # Set a reasonable timeout for external API calls (e.g., 30 seconds)
            timeout=30 
        ).json()

        print("[Web tool] outout", str(fo))

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
