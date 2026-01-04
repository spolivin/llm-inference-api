#!/bin/bash

curl -s http://localhost/api/v1/sd/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A futuristic car in high quality", "steps": 150}' \
