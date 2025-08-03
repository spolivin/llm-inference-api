import os

import whisper

WHISPER_MODEL_NAME = "small"
SAVE_DIR_NAME = "models"
SAVE_PATH = f"{SAVE_DIR_NAME}/{WHISPER_MODEL_NAME}.pt"

if not os.path.isfile(SAVE_PATH):
    _ = whisper.load_model(WHISPER_MODEL_NAME, download_root=f"./{SAVE_DIR_NAME}")
else:
    print(f"Model already loaded to '{SAVE_PATH}'")
