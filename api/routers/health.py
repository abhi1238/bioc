
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def root():
    return {
        "message": "BioChirp API is healthy",
        "version": "0.1.0",
        "time": datetime.now().isoformat(timespec="seconds"),
    }
