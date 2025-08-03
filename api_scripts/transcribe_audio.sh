#!/bin/bash

curl -s \
  "http://localhost:8035/generate" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_audio.wav"
