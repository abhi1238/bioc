

from fastapi import FastAPI
from .routers import health, ws
import os
from types import SimpleNamespace
from typing import (Any, Dict, List, Literal, Optional, Type, Union)
import time
from contextlib import asynccontextmanager, suppress
import logging
from dotenv import load_dotenv
from agents import Agent
from config.logging_setup import setup_logging_uvicorn_style
load_dotenv(override=True)

# logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
# Use uvicorn.error so logs appear under Uvicorn by default
# logger = logging.getLogger("uvicorn.error")

logger = setup_logging_uvicorn_style(loglevel="INFO", logfile="biochirp.log")



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load heavy resources at startup and attach to app.state; cleanup on shutdown."""
    t0 = time.perf_counter()
    pid = os.getpid()
    logger.info("[startup] PID=%s: initializing resources...", pid)

    # Safe defaults
    app.state.db_value: dict[str, Any] = {}
    app.state.embeddings: dict[str, Any] = {}
    app.state.model_cache: dict[str, Any] = {}
    app.state.prompt_content: dict[str, Any] = {}
    app.state.settings = SimpleNamespace(
        db_mapping={
            "TTD": "Therapeutic Targets Database",
            "CTD": "Comparative Toxicogenomics Database",
            "HCDT": "Highly Confident Drug-Target Database",
        }
    )

    # ---- DB Value
    # try:
    #     app.state.db_value = try_load_resource(DB_VALUE_PATH, "DB Value", loader_fn="pickle")
    #     n = len(app.state.db_value) if hasattr(app.state.db_value, "__len__") else "?"
    #     logger.info("[startup] PID=%s: DB Value loaded from %s (items=%s)", pid, DB_VALUE_PATH, n)
    # except Exception as e:
    #     logger.exception("[startup] PID=%s: DB Value load failed: %s", pid, e)

    # ---- Embeddings
    # try:
    #     t = time.perf_counter()
    #     app.state.embeddings = load_embeddings(base_dir="embeddings")
    #     dt = time.perf_counter() - t
    #     n = len(app.state.embeddings) if hasattr(app.state.embeddings, "__len__") else "?"
    #     logger.info("[startup] PID=%s: embeddings loaded (items=%s) in %.2fs", pid, n, dt)
    # except Exception as e:
    #     logger.exception("[startup] PID=%s: embeddings load failed: %s", pid, e)

    # ---- Sentence models
    try:
        t = time.perf_counter()
        app.state.model_cache = preload_sentence_models(BIOMEDICAL_MODELS)
        dt = time.perf_counter() - t
        logger.info("[startup] PID=%s: models preloaded %s in %.2fs", pid, BIOMEDICAL_MODELS, dt)
    except Exception as e:
        logger.exception("[startup] PID=%s: model preload failed: %s", pid, e)

    # # ---- Prompts
    # try:
    #     if not os.path.exists(PROMPT_PATH):
    #         raise FileNotFoundError(f"Prompt not found: {PROMPT_PATH}")
    #     prompt_dict = load_prompts(PROMPT_PATH)
    #     # prompt_dict = json.loads(subprocess.run(["docker", "run", "-v", f"{os.path.abspath(prompt_file)}:/app/prompts/prompt_agent.txt",
    #     #     "prompt-loader", "/app/prompts/prompt_agent.txt"], capture_output=True, text=True).stdout)
    #     app.state.prompt_content = prompt_dict
    #     logger.info(
    #         "[startup] PID=%s: Loaded %d prompts from %s. Available keys: %r",
    #         pid, len(prompt_dict), PROMPT_PATH, list(prompt_dict.keys())
    #     )
    # except Exception as e:
    #     logger.exception("[startup] PID=%s: prompt load failed: %s", pid, e)
    #     raise

    # app.state.agents = SimpleNamespace()
    # app.state.agents.orchestrator = Agent(
    #     name="Orchestrator",
    #     instructions=app.state.prompt_content.get("orchestrator", "Answer to user"),
    #     # tools=[readme, interpreter, web_tool, ttd, expand_and_match_db, ctd, hcdt, expand_synonyms],
    #     model=os.getenv("ORCH_MODEL", "gpt-5-mini"),
    # )
    logger.info("[startup] PID=%s: orchestrator agent ready", pid)

    logger.info("[startup] PID=%s: complete in %.2fs", pid, time.perf_counter() - t0)

    # --- Yield control to run the app ---
    try:
        yield
    finally:
        # ---- Shutdown/Cleanup ----
        try:
            logger.info("[shutdown] PID=%s: cleanup complete", pid)
        except Exception as e:
            logger.exception("[shutdown] PID=%s: cleanup error: %s", pid, e)



appc = FastAPI(lifespan=lifespan)
appc.include_router(health.router)
appc.include_router(ws.router)
