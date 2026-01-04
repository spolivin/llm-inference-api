import torch

from .model import pipeline


def generate_image(
    prompt: str,
    steps: int = 40,
    guidance: float = 7.5,
    height: int = 512,
    width: int = 512,
):
    with torch.autocast("cuda"):
        result = pipeline(
            prompt,
            num_inference_steps=steps,
            guidance_scale=guidance,
            height=height,
            width=width,
        )
    return result.images[0]
