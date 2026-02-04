import logging
from typing import AsyncGenerator
import httpx

# Set up logging
logger = logging.getLogger(__name__)

async def stream_text_tts(
        voice_id, text
) -> AsyncGenerator[bytes, None]:
    # voice_id follows this pattern: EXAVITQu4vr4xnSDxMaL
    """
    Stream text-to-speech audio using Eleven Labs API for the specified voice.
    voice_id: The voice ID to use for TTS.
    text: The text to convert to speech.
    Returns an asynchronous generator yielding audio chunks.
    """

    if not text:
        raise ValueError("Text cannot be empty")

    if not voice_id:
        raise ValueError("Voice ID and model cannot be empty")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream?output_format=pcm_16000"

    # Create a client with the appropriate timeout for streaming
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            logger.info(f"Starting streaming request for voice {voice_id}")

            # Make a streaming request directly to ElevenLabs API
            async with client.stream(
                    method="POST",
                    url=url,
                    headers={
                        "xi-api-key": "** [your provider api key] **",
                        "content-type": "application/json",
                    },
                    json={"text": text, "model_id": "eleven_turbo_v2_5"}, # the model you want to use which is related to the voice id
            ) as response:
                # Check response status
                if response.status_code != 200:
                    error_text = await response.text()
                    logger.error(
                        f"ElevenLabs API error: {response.status_code} - {error_text}"
                    )
                    raise httpx.HTTPStatusError(
                        f"Stream request failed: {error_text}",
                        request=response.request,
                        response=response,
                    )

                # Stream the chunks asynchronously
                chunk_count = 0
                async for chunk in response.aiter_bytes(chunk_size=1024):
                    chunk_count += 1
                    logger.debug(
                        f"Streaming chunk {chunk_count}: {len(chunk)} bytes"
                    )
                    yield chunk

                logger.info(
                    f"Completed streaming {chunk_count} chunks for voice {voice_id}"
                )

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during streaming: {e}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error during streaming: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in streaming: {e}")
            raise

async def make_elevenlabs_stream_tts_sample(voice_id: str, text: str) -> AsyncGenerator[bytes, None]:
    """
    Stream text-to-speech audio using Eleven Labs API streaming for the specified voice.
    voice_id: The voice ID to use for TTS.
    text: The text to convert to speech.
    Returns an asynchronous generator yielding audio chunks.
    """
    async for chunk in stream_text_tts(
            voice_id, text
    ):
        yield chunk
