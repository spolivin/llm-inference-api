#!/bin/bash

curl -s http://localhost/api/v1/tts/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Привет, как дела?", "speaker": "kseniya"}' \
