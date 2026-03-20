# 🚀 LLM Inference API

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Prerequisites](#prerequisites)
5. [Quick Start](#quick-start)
6. [Usage](#usage)
7. [Development](#development)
8. [Security Considerations](#security-considerations)
9. [Performance Optimization](#performance-optimization)
10. [Troubleshooting](#troubleshooting)
11. [License](#license)

> A GPU-accelerated inference platform for deploying multiple AI models as microservices. Built with Docker, FastAPI, and Prometheus/Grafana monitoring.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This project provides a containerized infrastructure for running multiple AI/ML models with GPU acceleration. Each model runs as an independent microservice behind an NGINX reverse proxy, with built-in monitoring via Prometheus and Grafana.

| Model                                                                         | Capability                                   | Framework    |
| ----------------------------------------------------------------------------- | -------------------------------------------- | ------------ |
| [Whisper](https://github.com/openai/whisper)                                  | Automatic speech recognition & transcription | OpenAI       |
| [Stable Diffusion v1.4](https://huggingface.co/CompVis/stable-diffusion-v1-4) | Text-to-image generation                     | Hugging Face |
| [LLaMA 2 7B (Q4_K_M)](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF)   | Text generation & chat                       | Meta AI      |
| [Gemma 2 2B](https://huggingface.co/google/gemma-2-2b-it)                     | Text generation & instruction following      | Google       |
| [Silero TTS v3](https://github.com/snakers4/silero-models)                    | Russian text-to-speech synthesis             | Silero       |

## Architecture

```
┌─────────────┐
│   NGINX     │  ← Reverse Proxy (Port 80)
└──────┬──────┘
       │
       ├─────► Whisper API      (Port 8035)
       ├─────► Stable Diff API  (Port 8015)
       ├─────► LLaMA API        (Port 8012)
       ├─────► Gemma API        (Port 8005)
       └─────► TTS API          (Port 8025)

┌──────────────────────────────────┐
│   Monitoring Stack               │
│   • Prometheus (Port 8090)       │
│   • Grafana (Port 8034)          │
└──────────────────────────────────┘
```

**Key Design Decisions:**

- **Microservices Architecture**: Each model runs in isolation for independent updates and deployment
- **Shared Base Image**: Common dependencies cached in `Dockerfile.base` to reduce build time and storage
- **GPU Sharing**: All services share a single GPU through NVIDIA Container Toolkit
- **Non-root Containers**: Services run as unprivileged users for enhanced security
- **Makefile Orchestration**: Simplified commands for common operations

## Features

✅ **GPU Acceleration**: CUDA-optimized inference for all models

✅ **Containerized Deployment**: Docker Compose orchestration with a shared base image

✅ **Monitoring**: Prometheus metrics + Grafana dashboards

✅ **Security Hardening**: Rootless Docker support, non-root containers

✅ **Reverse Proxy**: NGINX routing and request proxying

✅ **Modular Design**: Easy to add/remove models independently

✅ **Optimized Builds**: Shared base image with dependency caching

## Prerequisites

### Hardware Requirements

- **GPU**: NVIDIA GPU with CUDA support (recommended: ≥16GB VRAM for all models)
- **RAM**: Minimum 16GB system memory
- **Storage**: ~50GB free disk space for models and containers

### Software Requirements

1. **Docker Engine** (≥20.10)
   - [Installation Guide for Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

2. **NVIDIA Container Toolkit**
   - Required for GPU access from containers
   - [Installation Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

3. **CUDA Drivers** (≥11.8)
   - Verify with: `nvidia-smi`

4. **Python 3.12+** (for setup scripts)

### Verify GPU Access

Check that Docker can access your GPU:

```bash
nvidia-smi
```

> Alternatively, run `python check_gpu.py` after installing `torch` into your environment.

📚 **Detailed GPU setup**: See [docs/GPU_SETUP.md](docs/GPU_SETUP.md)

## Quick Start

### 1. Clone and Configure

```bash
git clone https://github.com/spolivin/llm-inference-api.git
cd llm-inference-api

# Configure environment variables (Grafana credentials)
cp .env.example .env
```

### 2. Set Up Python Environment

**Option A: Using Python venv**

```bash
sudo apt-get update
sudo apt-get install python3.12-venv build-essential

python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-all.txt
```

**Option B: Using Conda**

```bash
source setup_env.sh
```

### 3. Download Model Weights

Authenticate with Hugging Face:

```bash
sh hf_login.sh
```

Download all models:

```bash
# LLaMA 2 7B (quantized)
cd services/llama-api && sh download_llama_weights.sh && cd ../..

# Gemma 2 2B
cd services/gemma-api && sh download_gemma_model.sh && cd ../..

# Stable Diffusion v1.4
cd services/stable-diffusion-api && python download_sd_model.py && cd ../..

# Silero TTS v3 (Russian)
cd services/tts-api && python download_tts_model.py && cd ../..

# Whisper (base model)
cd services/whisper-api && python download_whisper_model.py && cd ../..
```

Logout from Hugging Face (security best practice):

```bash
sh hf_logout.sh
```

### 4. Build and Launch

```bash
# Build shared base image (one-time operation)
make build-base

# Build all services
make build-services

# Start all services
make up-services
```

### 5. Verify Deployment

Check that all services are running:

```bash
make services
```

> Expected output: 8 containers running (5 models + NGINX + Prometheus + Grafana)

## Usage

Once deployed, access services through NGINX on `localhost` or your VM's public IP:

### API Endpoints

```bash
# Text Generation (LLaMA 2)
curl -X POST http://localhost/api/v1/llama/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing", "max_new_tokens": 100}'

# Text Generation (Gemma 2)
curl -X POST http://localhost/api/v1/gemma/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a Python function", "max_new_tokens": 150}'

# Image Generation (Stable Diffusion)
curl -X POST http://localhost/api/v1/sd/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a serene mountain landscape", "steps": 50}'

# Speech Recognition (Whisper)
curl -X POST http://localhost/api/v1/whisper/generate \
  -F "file=@audio.wav"

# Text-to-Speech (Silero - Russian)
curl -X POST http://localhost/api/v1/tts/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Привет, как дела?", "speaker": "kseniya"}'
```

> Note: Generating image and synthesizing audio as shown above generate files and save them in temporary directory. Consult [API scripts](./api_scripts/) directory on how to download the generated files locally.

### Monitoring

- **Prometheus**: http://localhost:8090
- **Grafana**: http://localhost:8034
  - Default credentials: See `.env` file
  - Pre-configured dashboards available

📊 **Monitoring Guide**: See [docs/MONITORING.md](docs/MONITORING.md)

## Development

### Useful Commands

```bash
# View running containers
make containers

# View service logs
docker compose logs -f

# Check open ports
make open-ports

# Rebuild a specific service
docker compose build <service-name>

# Stop all services
make down-services

# Clean up everything (containers, volumes, images)
docker compose down -v --rmi all
```

### Project Structure

```
llm-inference-api/
├── services/               # Individual model services
│   ├── whisper-api/
│   ├── stable-diffusion-api/
│   ├── llama-api/
│   ├── gemma-api/
│   └── tts-api/
├── nginx/                  # Reverse proxy configuration
├── prometheus/             # Metrics collection config
├── docs/                   # Additional documentation
├── Dockerfile.base         # Shared base image
├── docker-compose.yml      # Service orchestration
├── Makefile                # Build and deployment commands
└── requirements-*.txt      # Python dependencies
```

## Security Considerations

This project implements several security best practices:

1. **Non-root Containers**: All services run as unprivileged users (UID 1000)
2. **Rootless Docker Support**: Compatible with rootless Docker installations
3. **Token Management**: HF tokens cleared after model download
4. **Network Isolation**: Services communicate through internal Docker network
5. **Environment Variables**: Sensitive configs managed via `.env` file

🔒 **Security Details**:

- [Rootless Docker Setup](https://docs.docker.com/engine/security/rootless/)
- [NVIDIA Toolkit Rootless Mode](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#rootless-mode)

## Performance Optimization

### Memory Management

For systems with <16GB VRAM, consider:

- Running a subset of models
- Using smaller model variants
- Implementing model swapping (load/unload on demand)

### Build Optimization

The shared base image (`Dockerfile.base`) caches common dependencies:

- PyTorch + CUDA libraries
- FastAPI + Uvicorn
- HuggingFace Transformers

Benefits:

- Reduction in total build time
- Reduction in total image size
- Faster iterative development

## Troubleshooting

### GPU Not Detected

```bash
# Check NVIDIA drivers
nvidia-smi

# Verify Docker GPU access
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### Out of Memory Errors

- Lower `max_new_tokens` in generation requests
- Run fewer models simultaneously

### Port Conflicts

```bash
# Check which ports are in use
make open-ports
```

> Modify ports in docker-compose.yml if needed

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.
