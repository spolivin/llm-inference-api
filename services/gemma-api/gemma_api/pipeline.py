import os

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    pipeline,
)

MODEL_NAME = "/models/gemma-2-2b-it"
if not os.path.exists(MODEL_NAME):
    MODEL_NAME = "models/gemma-2-2b-it"


def load_quantization_config():
    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )


def load_pipeline_components():
    bnb_config = load_quantization_config()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto",
        quantization_config=bnb_config,
    )
    return model, tokenizer


def load_pipeline():
    model, tokenizer = load_pipeline_components()
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    return pipe
