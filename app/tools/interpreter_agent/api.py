from fastapi import FastAPI, HTTPException
from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from pydantic import model_validator, ValidationError 
import logging
import os
from schema import ParsedValue, QueryInterpreterOutputGuardrail, InterpreterInput
from dotenv import load_dotenv
from pathlib import Path
import uvicorn

from agents import Agent, Runner, WebSearchTool, function_tool
import requests
# from IPython.display import display, JSON
import traceback


load_dotenv(override=True)

md_file_path = "query_interpreter.md"

with open(md_file_path, "r", encoding="utf-8") as f:
    prompt_md = f.read()

InterpreterInput.model_rebuild()
ParsedValue.model_rebuild()
QueryInterpreterOutputGuardrail.model_rebuild()



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



app = FastAPI()

@app.get("/")
def root():
    return {"message": "Interpreter service tool is running"}



@app.post("/interpreter_tool/", response_model=QueryInterpreterOutputGuardrail)
async def run_interpreter(input_data: InterpreterInput, logger = None):


    if logger is None:
        logger = get_fallback_logger()

    try:
        # Use user-supplied instructions if present, else fallback to default
        system_prompt = input_data.instructions or prompt_md

        # Choose provider/model
        if input_data.provider == 'openai' or input_data.provider is None:
            if input_data.model is None:
                model_to_use = "gpt-5-mini"
                logger.info("No model specified; defaulting to 'gpt-5-mini'")
            else:
                model_to_use = input_data.model
                logger.info(f"Using model '{model_to_use}' for provider '{input_data.provider}'")

            interpreter_agent = Agent(
                name="DrugTargetQueryInterpreterAgent",
                model=model_to_use,
                instructions=system_prompt,
                tools=[WebSearchTool()],
                output_type=QueryInterpreterOutputGuardrail
            )
        else:
            logger.error(f"Provider '{input_data.provider}' is not supported.")
            raise HTTPException(status_code=400, detail=f"Unsupported provider: {input_data.provider}")

        # Run agent
        result = await Runner.run(interpreter_agent, input_data.query)
        logger.info(f"Interpreter Agent execution completed. Result: {str(result)}")

        fo = getattr(result, "final_output", None)
        if isinstance(fo, QueryInterpreterOutputGuardrail):
            # logger.info("Returning successful response.")
            return fo
        else:
            logger.error("Agent returned empty or invalid response.")
            raise HTTPException(status_code=500, detail="Agent returned empty or invalid response.")

    except ValidationError as ve:
        logger.error(f"Pydantic validation error: {ve.json()}")
        raise HTTPException(status_code=422, detail=ve.errors())
    except HTTPException as he:
        logger.error(f"HTTPException raised: {he.detail}")
        raise he
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"Agent execution failed: {str(e)}\n{tb}")
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")


