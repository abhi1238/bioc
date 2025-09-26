
# app/services/embedding_client.py

import requests
from typing import Dict, List
from app.config.settings import Settings

class EmbeddingClient:
    """
    Client for sending text(s) to multiple embedding servers (via HTTP POST).
    """
    def __init__(self, settings: Settings):
        self.endpoints: Dict[str, str] = settings.EMBEDDER_ENDPOINTS
        self.timeout: float = settings.REQUEST_TIMEOUT_SECS
        self.max_retries: int = settings.MAX_RETRIES

    def embed(self, text: str, models: List[str] = None) -> Dict[str, dict]:
        """
        Calls each embedding endpoint with the given text.
        :param text: The text string to embed.
        :param models: If provided, limit to these models (names in endpoints).
        :return: Dict of model name --> response or error dict.
        """
        results = {}
        target_models = models or self.endpoints.keys()
        for name in target_models:
            url = self.endpoints.get(name)
            if not url:
                results[name] = {"error": f"No endpoint configured for model '{name}'"}
                continue
            last_exc = None
            for attempt in range(self.max_retries + 1):
                try:
                    resp = requests.post(url, json={"texts": [text]}, timeout=self.timeout)
                    resp.raise_for_status()
                    results[name] = resp.json()
                    break  # success, exit retry loop
                except Exception as e:
                    last_exc = e
            else:
                results[name] = {"error": f"Failed after {self.max_retries+1} attempts: {last_exc}"}
        return results
