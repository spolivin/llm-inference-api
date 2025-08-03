#!/bin/bash

curl -s http://localhost:8025/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Привет, как дела?", "speaker": "kseniya"}' \
