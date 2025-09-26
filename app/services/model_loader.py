# import logging
from sentence_transformers import SentenceTransformer
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.utils.logger import get_fallback_logger
from app.config.model_config import BIOMEDICAL_MODELS


BIOMEDICAL_MODELS = [
    "FremyCompany/BioLORD-2023-S",
    "malteos/scincl",
    "pritamdeka/S-PubMedBERT-MS-MARCO",
    "cambridgeltl/SapBERT-from-PubMedBERT-fulltext",
    "nuvocare/WikiMedical_sent_biobert",
]


def preload_sentence_models(model_names=None, max_workers=5, logger=None):
    """
    Loads all requested sentence-transformer models in parallel and returns a cache dict.
    Accepts an optional logger. If none is provided, uses fallback logger.
    """
    if model_names is None:
        model_names = BIOMEDICAL_MODELS
    if logger is None:
        logger = get_fallback_logger()
    cache = {}
    errors = {}

    def load_model(name):
        try:
            logger.info(f"[Model] loading '{name}'...")
            model = SentenceTransformer(name)
            logger.info(f"[Model] loaded '{name}'.")
            return name, model, None
        except Exception as e:
            logger.exception(f"[Model] FAILED to load '{name}': {e}")
            return name, None, e

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_name = {executor.submit(load_model, name): name for name in model_names}
        for future in as_completed(future_to_name):
            name, model, error = future.result()
            if model is not None:
                cache[name] = model
            if error:
                errors[name] = error

    logger.info(f"[Model] preload complete ({len(cache)}/{len(model_names)}) loaded")
    if errors:
        logger.error(f"[Model] errors for: {list(errors.keys())}")
    return cache
