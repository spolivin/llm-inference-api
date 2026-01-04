#!/bin/bash

MODEL_ID="google/gemma-2-2b-it"
LOCAL_DIR="./models/gemma-2-2b-it"

echo "Downloading model: $MODEL_ID to $LOCAL_DIR"
huggingface-cli download $MODEL_ID \
  --local-dir $LOCAL_DIR \
  --local-dir-use-symlinks False

echo "Model saved to: $LOCAL_DIR"
