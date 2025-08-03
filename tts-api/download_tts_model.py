import os

import torch

MODEL_PATH = "https://models.silero.ai/models/tts/ru/ru_v3.pt"
LOCAL_PATH = "models/tts_model_ru_v3.pt"

if not os.path.isfile(LOCAL_PATH):
    torch.hub.download_url_to_file(
        url=MODEL_PATH,
        dst=LOCAL_PATH,
    )
else:
    print(f"Model already loaded to '{LOCAL_PATH}'")
