#!/bin/bash

curl -s \
  'http://localhost:8012/generate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "prompt": "Is Moscow bigger than London in terms of population?",
  "max_new_tokens": 300,
  "temperature": 0.7
}'
