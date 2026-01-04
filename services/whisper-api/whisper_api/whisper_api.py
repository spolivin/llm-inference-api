import os
import shutil
import tempfile
from contextlib import asynccontextmanager

import torch
import whisper
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from .middleware import BadRequestTrackingMiddleware

MODEL_PATH = "/models/small.pt"
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = "models/small.pt"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")
    print("Loading model...")
    app.state.model = whisper.load_model(MODEL_PATH)
    app.state.model.to("cuda")
    yield
    print("Application shutdown")


# Initializing a FastAPI application
app = FastAPI(lifespan=lifespan)


app.add_middleware(BadRequestTrackingMiddleware)

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/generate")
async def transcribe_audio(
    request: Request, file: UploadFile = File(...)
) -> dict[str, str]:
    """Endpoint for transcribing the loaded audio."""
    # Temporarily saving the uploaded audio file
    filename_suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=filename_suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # Transcribing the audio
        result = preprocess_audio(model=request.app.state.model, path=tmp_path)

        return {"audio_file": file.filename, "transcribed_text": result["text"]}

    except Exception as e:
        return JSONResponse(
            content={"error": "Unexpected error occured"},
            status_code=500,
        )

    finally:
        # Cleaning up the temp file after use
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        torch.cuda.empty_cache()


def preprocess_audio(model, path: str) -> dict[str, str | list]:
    """Conducts the audio transcription."""
    return model.transcribe(path)
