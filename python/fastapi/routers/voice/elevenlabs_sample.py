import io
import wave
import requests

def pcm_to_wav(pcm_data) -> bytes:
    """Convert PCM data to WAV format"""
    wav_io = io.BytesIO()
    with wave.open(wav_io, "wb") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(16000)  # 16kHz sample rate
        wav_file.writeframes(pcm_data)
    return wav_io.getvalue()

async def make_elevenlabs_tts_sample(voice_id: str, text: str) -> bytes:
    """
    Generate text-to-speech audio using Eleven Labs API for the specified voice.
    voice_id: The voice ID to use for TTS.
    text: The text to convert to speech.
    Returns the audio data as bytes in WAV format.
    """
    # voice_id follows this pattern: EXAVITQu4vr4xnSDxMaL

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=pcm_16000"

    headers = {
        "xi-api-key": "** [your provider api key] **",
        "content-type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2_5", # the model you want to use which is related to the voice id
        "voice_settings": {}, # optional
    }

    response = requests.post(
        url=url,
        headers=headers,
        json=payload,  # Automatically serializes to JSON
    )

    # Raise exception for any HTTP error status
    response.raise_for_status()

    # Return the binary response content
    return pcm_to_wav(response.content)
