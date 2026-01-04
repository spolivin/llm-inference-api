import torch
from diffusers import StableDiffusionPipeline


def load_pipeline():
    pipe = StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        torch_dtype=torch.float16,
        local_files_only=True,
    ).to("cuda")

    return pipe


pipeline = load_pipeline()
