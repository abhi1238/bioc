

import json
import requests
from fastapi import FastAPI, HTTPException
from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from pydantic import model_validator, ValidationError 
import logging
import os

from app.tools.interpreter_agent.schema import ParsedValue, QueryInterpreterOutputGuardrail, InterpreterInput

from agents import function_tool

logger = logging.getLogger("uvicorn.error")

@function_tool(
    name_override="interpreter_tool",
    description_override=(
        "... (your description as above) ..."
    ),
)
async def interpreter_tool(input: InterpreterInput) -> QueryInterpreterOutputGuardrail | None:
    """
    Core biomedical query interpreter and router for BioChirp.
    Args:
        input (InterpreterInput): The user's query and agent context.
    Returns:
        QueryInterpreterOutputGuardrail or None if failed.
    """

    logger.info("[RUNNING] Interpreter tool")
    print("[RUNNING] Interpreter tool")

    BASE_URL = "http://192.168.22.20:8016"
    ENDPOINT = "/interpreter_tool/"
    URL = BASE_URL + ENDPOINT

    payload = {
        "query": input.query,
        "provider": input.provider,
        "model": input.model,
        "instructions": input.instructions,
    }

    try:
        response = requests.post(URL, json=payload, timeout=30)
        logger.info(f"[Interpreter tool] HTTP status: {response.status_code}")

        if response.status_code == 200:
            try:
                output = QueryInterpreterOutputGuardrail.model_validate(response.json())
                logger.info("[FINISHED] Interpreter tool - Success")
                logger.info(output)
                print(output)
                print("[FINISHED] Interpreter tool")
                return output
            except Exception as parse_exc:
                logger.error(f"Failed to parse response: {parse_exc}")
        else:
            logger.error(f"Interpreter tool HTTP error: {response.status_code} - {response.text}")

    except Exception as e:
        logger.exception("Interpreter tool failed with exception")

    print("Interpreter tool failed")
    return QueryInterpreterOutputGuardrail
