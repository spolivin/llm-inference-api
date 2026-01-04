import os
from contextlib import asynccontextmanager
from uuid import uuid4

import soundfile as sf
import torch
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from .middleware import BadRequestTrackingMiddleware
from .schemas import TTSRequest

MODEL_PATH = "/models/tts_model_ru_v3.pt"
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = "models/tts_model_ru_v3.pt"

TMP_PATH = "/tmp/tts_generated"
os.makedirs(TMP_PATH, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")
    print("Loading model...")
    app.state.model = torch.package.PackageImporter(MODEL_PATH).load_pickle(
        "tts_models", "model"
    )
    app.state.model.to("cuda")
    yield
    print("Application shutdown")


# FastAPI app
app = FastAPI(lifespan=lifespan)


app.add_middleware(BadRequestTrackingMiddleware)

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/generate")
async def speak(req: TTSRequest, request: Request):
    postfix = uuid4().hex[:6]
    gen_audio_filename = os.path.join(TMP_PATH, f"generated_audio_{postfix}.wav")

    try:
        # Generate audio waveform
        audio = request.app.state.model.apply_tts(
            text=req.text, speaker=req.speaker, sample_rate=48000
        )

        sf.write(gen_audio_filename, audio, 48000)

        return JSONResponse(
            content={
                "saved": os.path.exists(gen_audio_filename),
                "audio_name": f"generated_audio_{postfix}.wav",
                "download_endpoint": f"/download/{postfix}",
            },
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(
            content={"error": "Unexpected error occured"},
            status_code=500,
        )

    finally:
        torch.cuda.empty_cache()


@app.get("/download/{file_id}")
async def download(file_id: str):
    file_path = os.path.join(TMP_PATH, f"generated_audio_{file_id}.wav")

    if not os.path.exists(file_path):
        # 404 JSON response for curl or browser
        raise HTTPException(status_code=404)

    # File exists: stream it with proper headers
    return FileResponse(
        path=file_path,
        media_type="audio/wav",
        filename=f"generated_audio_{file_id}.wav",
    )
