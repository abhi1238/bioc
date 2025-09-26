
from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/embed")
async def embed_text(request: Request, body: dict):
    embedder_client = request.app.state.embedder_client
    # Call your embedding logic here
    result = embedder_client.embed(body["texts"])
    return {"embeddings": result}
