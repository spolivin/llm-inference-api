#!/bin/bash

curl -s \
  'http://localhost:8005/generate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "prompt": "Who are you? Be brief.",
  "max_new_tokens": 200,
  "temperature": 0.7
}'
