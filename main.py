from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from zyphra import ZyphraClient, ZyphraError
import os
import base64

app = FastAPI()

ZYPHRA_API_KEY = "zsk-1c2f2f08c75789a27021eba05af4bc8397bd300f38e3850697ffd2ada5f10d2b"
if not ZYPHRA_API_KEY:
    raise Exception("ZYPHRA_API_KEY environment variable not set")

class TTSRequest(BaseModel):
    text: str
    speaking_rate: int = 15
    speaker_audio: str | None = None # Optional voice cloning

@app.post("/synthesize_voice/")
async def synthesize_voice(request: TTSRequest):
    try:
        async with ZyphraClient(api_key=ZYPHRA_API_KEY) as client: # Use AsyncClient for FastAPI
            audio_data = await client.audio.speech.create(
                text=request.text,
                speaking_rate=request.speaking_rate,
                speaker_audio=request.speaker_audio
            )
            return StreamingResponse(audio_data, media_type="audio/webm") # Stream audio data
    except ZyphraError as e:
        raise HTTPException(status_code=500, detail=f"Zyphra API Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
