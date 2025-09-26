from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def root():
    """
    Health check endpoint for the BioChirp API.

    Returns a JSON object indicating that the API is up and running,
    along with the current version and server time.

    Returns:
        dict: A dictionary with the following keys:
            - "message": Health status message.
            - "version": API version string.
            - "time": Current server timestamp in ISO 8601 format.

    Example response:
        {
            "message": "BioChirp API is healthy",
            "version": "0.1.0",
            "time": "2025-09-25T16:05:17"
        }
    """
    return {
        "message": "BioChirp API is healthy",
        "version": "0.1.0",
        "time": datetime.now().isoformat(timespec="seconds"),
    }
