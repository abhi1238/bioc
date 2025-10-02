
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/embed")
async def embed_text(request: Request, body: dict):
    embedder_client = request.app.state.embedder_client
    result = embedder_client.embed(body["texts"])
    return {"embeddings": result}
