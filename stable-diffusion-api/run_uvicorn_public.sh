#!/bin/bash

uvicorn stable_diffusion_api.main:app --host 0.0.0.0 --port 8015
