# app/tools/interpreter_agent/agent.py

import json
import logging
from .schema import QueryInterpreterOutputGuardrail
from agents import (
    Agent,
    AgentOutputSchema,
    ModelSettings,
    OpenAIResponsesModel,
    Runner,
    WebSearchTool,
    function_tool,
)

PROMPT_PATH = "../../../resources/prompts/query_interpreter.md"
with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    prompt_content = f.read()

# Import your Runner, Agent, prompt_content, log_ui, etc.
# from your_core_module import Runner, Agent, prompt_content, log_ui

# --- This is your real tool code, unmodified! ---
async def interpreter(user_input: str) -> QueryInterpreterOutputGuardrail | None:
    # await log_ui(msg = "Running: *Interpreter ...*", tool = "interpreter")
    agent = Agent(
        name="DrugTargetQueryInterpreterAgent",
        model="gpt-5-mini",
        instructions=prompt_content,
        output_type=QueryInterpreterOutputGuardrail,
    )

    try:
        result = await Runner.run(agent, user_input)
        output_obj = result.final_output  # Should be a QueryInterpreterOutputGuardrail instance

        # (Optionally remove Chainlit-specific UI code if not running in Chainlit)
        pretty_json = json.dumps(output_obj.model_dump(exclude_none=True), indent=2, ensure_ascii=False)
        msg = (
            "<details><summary>Show full JSON</summary>\n\n"
            "```json\n" + pretty_json + "\n```\n</details>"
        )
        try:
            # logger.info("[Interpreter] Output: %s", msg)
            pass
        except Exception:
            # logger.info("[Interpreter] Output: %s", pretty_json)
            pass

        # await log_ui(msg = "Finished: *Interpreter ...*", tool = "interpreter")
        return output_obj

    except Exception as e:
        # logger.error("[QueryInterpreter] Exception: %s", e, exc_info=True)
        return None
