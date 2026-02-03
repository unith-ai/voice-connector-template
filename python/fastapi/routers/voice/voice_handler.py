import logging

import httpx
from fastapi import APIRouter
from fastapi import Header
from fastapi import HTTPException
from fastapi.responses import Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from .elevenlabs_sample import make_elevenlabs_tts_sample
from .elevenlabs_streaming_sample import make_elevenlabs_stream_tts_sample

logger = logging.getLogger(__name__)

voice_router = APIRouter()


class TTSRequest(BaseModel):
    text: str


class StreamTTSRequest(BaseModel):
    text: str


@voice_router.post("/tts/{voice}")
async def process_text_to_speech(
    voice: str,
    request: TTSRequest,
    unith_voice_x_api: str = Header(None, description="API Key for authentication"),
):
    """
    Process text-to-speech audio using Eleven Labs API for the specified voice.
    voice: The voice ID to use for TTS.
    request: The TTSRequest object containing the text to convert.
    unith_voice_x_api: API key for authentication.
    Returns a Response with audio data.
    """
    # Validate the API key
    if unith_voice_x_api != "12345678":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    text = request.text
    logger.info(f"Processing TTS for voice: {voice} with text: {text}")
    try:
        audio_data: bytes = await make_elevenlabs_tts_sample(voice, request.text)
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


@voice_router.post("/stream-tts/{voice}")
async def stream_text_to_speech(
        voice: str,
        request: StreamTTSRequest,
        unith_voice_x_api: str = Header(None, description="API Key for authentication"),
):
    """
    Stream text-to-speech audio using Eleven Labs API streaming for the specified voice.
    voice: The voice ID to use for TTS.
    request: The TTSRequest object containing the text to convert.
    unith_voice_x_api: API key for authentication.
    Returns a StreamingResponse with audio data.
    """
    try:
        # Validate the API key
        if unith_voice_x_api != "12345678":
            raise HTTPException(status_code=401, detail="Invalid API Key")

        text = request.text
        logger.info(f"Starting streaming TTS for voice: {voice} with text: {text}")

        # Use our stream_tts generator function from tts.py
        audio_stream = make_elevenlabs_stream_tts_sample(
            voice_id=voice,
            text=request.text,
        )

        # Return streaming response
        return StreamingResponse(
            audio_stream,
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=speech.wav"},
        )

    except ValueError as exc:
        logger.error(f"Validation error: {exc}")
        raise HTTPException(status_code=400, detail=str(exc))
    except httpx.RequestError as exc:
        logger.error(f"Request error: {exc}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: {exc}")
    except httpx.HTTPStatusError as exc:
        logger.error(f"HTTP error: {exc}")
        status_code = exc.response.status_code if exc.response else 500
        raise HTTPException(status_code=status_code, detail=f"HTTP error: {exc}")
    except Exception as exc:
        logger.error(f"Unexpected error: {exc}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(exc)}")
