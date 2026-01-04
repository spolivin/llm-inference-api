from diffusers import StableDiffusionPipeline

# Load the lightweight FLUX.1 Schnell model
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")

print(pipe)
