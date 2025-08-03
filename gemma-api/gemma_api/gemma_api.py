from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from .middleware import BadRequestTrackingMiddleware
from .pipeline import load_pipeline
from .schemas import ChatRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")
    print("Loading model...")
    app.state.pipe = load_pipeline()
    yield
    print("Application shutdown")


app = FastAPI(lifespan=lifespan)

app.add_middleware(BadRequestTrackingMiddleware)

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/generate")
async def chat(req: Request, request: ChatRequest):
    prompt = request.prompt
    messages = [
        {"role": "user", "content": prompt},
    ]
    try:
        output = req.app.state.pipe(
            messages,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            do_sample=True,
            top_p=0.95,
            top_k=50,
        )

        return {"response": output[0]["generated_text"][-1]["content"].strip()}

    except Exception as e:
        return JSONResponse(
            content={"error": "Unexpected error occured"},
            status_code=500,
        )

    finally:
        torch.cuda.empty_cache()
