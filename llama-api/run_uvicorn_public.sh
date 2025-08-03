#!/bin/bash

uvicorn llama_api.llama_api:app --host 0.0.0.0 --port 8012
