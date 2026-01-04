import os
from contextlib import asynccontextmanager

import torch
from ctransformers import AutoModelForCausalLM
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from .middleware import BadRequestTrackingMiddleware
from .prompt import compose_llama_prompt
from .schemas import ChatRequest

MODEL_PATH = "/models/llama-2-7b-chat.Q4_K_M.gguf"
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = "models/llama-2-7b-chat.Q4_K_M.gguf"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting application...")
    print("Loading model...")
    app.state.model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        model_type="llama",
        gpu_layers=50,
    )
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
async def chat(req: Request, request: ChatRequest):
    try:
        prompt = compose_llama_prompt(question=request.prompt)
        response = req.app.state.model(
            prompt,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            stop=["</s>"],
        )

        return {"response": response}

    except Exception as e:
        return JSONResponse(
            content={"error": "Unexpected error occured"},
            status_code=500,
        )

    finally:
        torch.cuda.empty_cache()
