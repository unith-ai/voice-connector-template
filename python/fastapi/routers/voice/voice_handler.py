import logging

import httpx
from fastapi import APIRouter
from fastapi import Header
from fastapi import HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

logger = logging.getLogger(__name__)

voice_router = APIRouter()


class TTSRequest(BaseModel):
    text: str


@voice_router.post("/tts/{voice}")
async def process_text_to_speech(
    voice: str,
    request: TTSRequest,
    unith_voice_x_api: str = Header(None, description="API Key for authentication"),
):
    # Validate the API key
    if unith_voice_x_api != "12345678":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    voice = voice
    text = request.text
    logger.info(f"Processing TTS for voice: {voice} with text: {text}")
    try:
        audio_data = b""
        # Return as a binary response with the correct content type
        return Response(
            content=audio_data,
            status_code=200,
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=speech.wav"},
        )
    except httpx.RequestError as exc:
        logger.error(f"Request error: {exc}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: {exc}")
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}")
