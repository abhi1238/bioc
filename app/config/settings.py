
from pydantic import AnyUrl
from pydantic_settings import BaseSettings
from typing import Dict

class Settings(BaseSettings):
    # map logical model name --> service URL
    EMBEDDER_ENDPOINTS: Dict[str, AnyUrl] = {
        "biolord":     "http://localhost:8006/embed",
        "scincl":      "http://localhost:8007/embed",
        "pubmedbert":  "http://localhost:8009/embed",
        "sapbert":     "http://localhost:8010/embed",
        "wikimedical": "http://localhost:8011/embed",
    }

    DB_MAPPING: Dict[str, str] = {
        "TTD": "Therapeutic Targets Database",
        "CTD": "Comparative Toxicogenomics Database",
        "HCDT": "Highly Confident Drug-Target Database",
    }

    REQUEST_TIMEOUT_SECS: float = 20.0
    MAX_RETRIES: int = 2

    class Config:
        env_nested_delimiter = "__"   # allows EMBEDDER_ENDPOINTS__biolord=...
        env_prefix = "BIOCHIRP_"
