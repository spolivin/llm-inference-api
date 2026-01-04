import os
from uuid import uuid4

import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from .generate import generate_image
from .middleware import BadRequestTrackingMiddleware
from .schemas import GenerateRequest

TMP_PATH = "/tmp/sd_generated"
os.makedirs(TMP_PATH, exist_ok=True)

app = FastAPI(title="Stable Diffusion API")

app.add_middleware(BadRequestTrackingMiddleware)

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/generate")
async def generate(req: GenerateRequest):
    postfix = uuid4().hex[:6]
    gen_image_filename = os.path.join(TMP_PATH, f"generated_image_{postfix}.jpg")
    try:
        image = generate_image(
            req.prompt,
            req.steps,
            req.guidance,
            req.height,
            req.width,
        )
        image.save(gen_image_filename)

        return JSONResponse(
            content={
                "saved": os.path.exists(gen_image_filename),
                "image_name": f"generated_image_{postfix}.jpg",
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
    file_path = os.path.join(TMP_PATH, f"generated_image_{file_id}.jpg")

    if not os.path.exists(file_path):
        # 404 JSON response for curl or browser
        raise HTTPException(status_code=404)

    # File exists: stream it with proper headers
    return FileResponse(
        path=file_path,
        media_type="image/jpeg",
        filename=f"generated_image_{file_id}.jpg",
    )
