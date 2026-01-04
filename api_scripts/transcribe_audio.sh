#!/bin/bash

curl -s \
  "http://localhost/api/v1/whisper/generate" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_audio.wav"
