
# # from fastapi import FastAPI, Request
# # from sentence_transformers import SentenceTransformer
# # import os
# # from app.utils.logger import get_fallback_logger

# # MODEL_NAME = os.environ.get("MODEL_NAME", "pritamdeka/S-PubMedBERT-MS-MARCO")
# # print(f"Loading model: {MODEL_NAME}")
# # model = SentenceTransformer(MODEL_NAME)

# # app = FastAPI()

# # @app.post("/embed")
# # async def embed(request: Request):
# #     data = await request.json()
# #     texts = data["texts"]
# #     embeddings = model.encode(texts).tolist()
# #     return {"embeddings": embeddings}

# #----------------------------------------------------
# from fastapi import FastAPI, Request
# from sentence_transformers import SentenceTransformer
# import os
# from app.utils.logger import get_fallback_logger

# def load_embedder_model(logger=None):
#     """
#     Loads a SentenceTransformer model using MODEL_NAME from environment.
#     Accepts an optional logger. If none is provided, uses fallback logger.
#     Returns: (model, logger)
#     """
#     if logger is None:
#         logger = get_fallback_logger("biochirp.embed_api")
#     model_name = os.environ.get("MODEL_NAME", "pritamdeka/S-PubMedBERT-MS-MARCO")
#     logger.info(f"Loading model: {model_name}")
#     model = SentenceTransformer(model_name)
#     return model, logger

# # At top level, allow logger to be injected or fallback:
# model, logger = load_embedder_model()

# app = FastAPI()

# @app.post("/embed")
# async def embed(request: Request, logger=logger):
#     """
#     Accepts a POST request with JSON payload: {"texts": [ ... ]}
#     Returns embeddings for the input texts.
#     Uses fallback logger if none provided.
#     """
#     try:
#         data = await request.json()
#         texts = data["texts"]
#         logger.info(f"Received {len(texts)} texts for embedding.")
#         embeddings = model.encode(texts).tolist()
#         logger.info("Successfully encoded texts.")
#         return {"embeddings": embeddings}
#     except Exception as e:
#         logger.exception(f"Failed to generate embeddings: {e}")
#         return {"error": str(e)}, 500


from fastapi import FastAPI, Request
from sentence_transformers import SentenceTransformer
import os

MODEL_NAME = os.environ.get("MODEL_NAME", "pritamdeka/S-PubMedBERT-MS-MARCO")
print(f"Loading model: {MODEL_NAME}", flush=True)
model = SentenceTransformer(MODEL_NAME)

app = FastAPI()

@app.post("/embed")
async def embed(request: Request):
    data = await request.json()
    texts = data["texts"]
    embeddings = model.encode(texts).tolist()
    return {"embeddings": embeddings}
