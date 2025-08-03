#!/bin/bash

uvicorn gemma_api.gemma_api:app --host 0.0.0.0 --port 8005
