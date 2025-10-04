

from pydantic import BaseModel, Field
from typing import List, Optional, Union

class ReadmeInput(BaseModel):
    query: str

class ReadmeOutput(BaseModel):
    # Field now contains ONLY the answer
    answer: str = Field(description="The final answer derived from the Readme.")
