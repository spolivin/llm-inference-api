#!/bin/bash

curl -s http://localhost:8015/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A futuristic car in high quality", "steps": 150}' \
