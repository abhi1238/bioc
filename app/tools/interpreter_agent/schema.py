from typing import Any, Dict, List, Literal, Optional, Tuple, Union
from pydantic import BaseModel, Extra, Field, constr, model_validator

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