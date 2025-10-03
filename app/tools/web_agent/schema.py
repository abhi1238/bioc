
from pydantic import BaseModel, Field
from typing import List, Optional, Union
class WebToolInput(BaseModel):
    query: str
    instructions: Optional[str] = None  # new field for dynamic system prompt


class WebToolOutput(BaseModel):
    # Field now contains ONLY the answer
    answer: str = Field(description="The final answer derived from the web search.")
