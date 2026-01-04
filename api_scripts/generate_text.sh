#!/bin/bash

curl -s \
  'http://localhost/api/v1/gemma/generate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "prompt": "Who are you? Be brief.",
  "max_new_tokens": 200,
  "temperature": 0.7
}'
