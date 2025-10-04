from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from pydantic import BaseModel, Extra, Field, constr, model_validator, ValidationError
# from pydantic import BaseModel, root_validator, ValidationError


class InterpreterInput(BaseModel):
    """
    Input for the interpreter agent.
    """
    query: str
    instructions: Optional[str] = None
    provider: Optional[Literal['openai', 'groq']] = None
    model: Optional[str] = None

    @model_validator(mode="after")
    def check_model_for_provider(self):
        if self.provider == 'openai':
            allowed = {"gpt-4o-mini", "gpt-5-mini"}
            if self.model is not None and self.model not in allowed:
                raise ValueError(f"For provider 'openai', model must be one of {allowed}.")
        elif self.provider == 'groq':
            allowed = {'llama-3.3-70b-versatile'}
            if self.model is not None and self.model not in allowed:
                raise ValueError(f"For provider 'groq', model must be one of {allowed}.")
        return self
    
class CommonFields(BaseModel):
    """All biomedical schema fields, used for input, query, and output stages."""
    drug_name: Optional[Union[str, List[str]]] = None
    target_name: Optional[Union[str, List[str]]] = None
    gene_name: Optional[Union[str, List[str]]] = None
    disease_name: Optional[Union[str, List[str]]] = None
    pathway_name: Optional[Union[str, List[str]]] = None
    biomarker_name: Optional[Union[str, List[str]]] = None
    drug_mechanism_of_action_on_target: Optional[Union[str, List[str]]] = None
    approval_status: Optional[Union[str, List[str]]] = None



class ParsedValue(CommonFields):
    """Fields extracted from user query after NER/LLM parsing."""
    class Config:
        extra = "forbid"
ParsedValue.model_rebuild()


class QueryInterpreterOutputGuardrail(BaseModel):
    """LLM-powered query interpreter output."""
    cleaned_query: str
    status: str
    route: str
    message_to_user: str
    suggestions: List[str]
    reasoning: str
    explanation: str
    parsed_value: ParsedValue

    class Config:
        extra = "forbid"

QueryInterpreterOutputGuardrail.model_rebuild()