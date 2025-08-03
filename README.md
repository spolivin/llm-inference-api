# LLM Inference API – Multi-Model GPU-Ready Deployment

1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Security considerations](#security-considerations)
5. [Monitoring system](#monitoring-system)
6. [Preparation of the environment](#preparation-of-the-environment-for-launch)
7. [Running services](#running-services)

## Overview

This project is a functional prototype built to explore multi-container deployment of ML inference APIs using large language models. It intentionally skips production features (like reverse proxy and autoscaling) to focus on clean modular design, *Docker*-based deployment and *GPU* provisioning.

It includes: 

* [*Whisper*](https://github.com/openai/whisper) for automatic speech recognition and transcription

* [*Stable Diffusion*](https://huggingface.co/CompVis/stable-diffusion-v1-4) for image generation

* [*LLaMA Q4_K_M*](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF) for text generation

* [*Gemma 2*](https://huggingface.co/google/gemma-2-2b-it) for text generation

* [*Silero RU V3*](https://github.com/snakers4/silero-models) for text-to-speech audio synthesis for Russian language

Each service is independently deployed using *FastAPI* and *Docker*, optimized for *GPU* inference. Additionally monitoring system using *Prometheus*/*Grafana* is added to keep track of the requests that services process.

## Features

* Supports multiple transformer-based models (*Hugging Face*)

* *GPU*-accelerated inference (*CUDA*-compatible)

* *Docker Compose* with modular containers

* Internal service communication over *HTTP*

* Optimized *Docker* images using shared base and caching layers

* Optionally supports *rootless Docker* for better isolation

## Requirements

### 1. *CUDA-compatible GPU*

In order to use the services efficiently, the local system should have access to *CUDA* drivers and *GPU*. Instructions on how to check the visibility/availability of *GPU* can be found 

Details: [*GPU* visibility check](./docs/GPU_SETUP.md)

### 2. *Docker Engine* 

Each service is launched in a separate *Docker* container all of which are orchestrated using *Docker Compose*. Hence, it is necessary to have *Docker* installed on the system.

Details: [Docker installation for Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

### 3. *NVIDIA Container Toolkit*

Since the inference is conducted using *GPU*, containers should have access to the system's GPU. This requires *NVIDIA Container Toolkit* to be installed.

Details: [NVIDIA Container Toolkit Installation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

### 4. *~16 GB VRAM*

In order that all models could be fit on a single *GPU*, it is recommendable that the *GPU* be equipped with at least 16GB of *VRAM*.

## Security considerations

1. Containers are configured to run under a *non-root* user to prevent privilege escalation and align with container hardening best practices.

2. This project also was built using *rootless Docker* to ensure containers do not run with root privileges, improving deployment security and isolating services from the host system. In this connection *NVIDIA Container Toolkit* has also been configured to run in *rootless mode*.

Details:

[Rootless Docker Configuration](https://docs.docker.com/engine/security/rootless/)

[Configuring NVIDIA Container Toolkit for rootless mode](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#rootless-mode)

## Monitoring system

In order to be able to keep track of key metrics and the state of the requests to the APIs, the monitoring system has been embedded. More information about monitoring can be consulted [here](./docs/MONITORING.md).

## Preparation of the environment for launch

### Cloning the repository

First, we clone the project locally and set up the environment:

```bash
# Cloning the repo
git clone https://github.com/spolivin/llm-inference-api.git
cd llm-inference-api

# Copying example environment and configuring
cp .env.example .env
```
> **NOTE:** File `.env.example` contains only credentials for *Grafana* which can be configured with new username and password after copying.

### Configuring virtual environment

Next, we need to set up a virtual environment so that the next steps could be executed without problems.

#### Python

```bash
sudo apt-get update
sudo apt-get install python3.12-venv

python3.12 -m venv .venv
source .venv/bin/activate

pip install -r requirements-all.txt
```

> **NOTE:** During libraries installation there can appear `subprocess-exited-with-error` error connected to the fact that installing some libraries requires compiling code in *C/C++*. The best way to avoid this error is to install the required compilies (such as `gcc` or `g++`) and other needed tools via `sudo apt install build-essential`.

#### Conda

```bash
source setup_env.sh
```
> **NOTE:** Before running this command one needs to make sure that *Conda* is installed via `which conda` command. In case of its absence, it it necessary to follow [Conda installation guidelines ](https://docs.conda.io/projects/conda/en/stable/user-guide/install/linux.html) for local installation on Ubuntu.

### Loading models locally

The next step is to load all models that we are about to deploy locally. Before that, we need to log in to Hugging Face, since some models will be pulled from HF Hub:

```bash
sh hf_login.sh <YOUR-HF-TOKEN>
```

#### 1. LLaMA model (text generation)

```bash
cd llama-api
sh download_llama_weights.sh
cd ..
```

#### 2. Gemma model (text generation)

```bash
cd gemma-api
sh download_gemma_model.sh
cd ..
```

#### 3. Stable Diffusion model (image generation)
```bash
cd stable-diffusion-api
python download_sd_model.py
cd ..
```

#### 4. Silero TTS model (text-to-speech)
```bash
cd tts-api
python download_tts_model.py
cd ..
```

#### 5. Whisper model (audio transcription to text)
```bash
cd whisper-api
python download_whisper_model.py
cd ..
```

After loading all models it is necessary to log out of Hugging Face to avoid the token getting leaked into containers during build stage:

```bash
sh hf_logout.sh
```

## Running services

In order to save memory and re-use cached layers, the system is based on shared base image which we need to firstly build:

```bash
# Building a common image for re-use across images
make build-base
```

After successfully building the base image, we can go on and build the main services and launch them:

```bash
# Building services with deployed models
make build-services

# Launching the system
make up-services
```

One can check if all services (including Prometheus and Grafana) are up and running:

```bash
make services
```
> **NOTE:** One can optionally check the opened ports via `make open-ports` or `make containers` to make sure that all services are running

Services can be stopped and deleted in this way:

```bash
make down-services
```
