#!/bin/bash

# TO BE RUN WITH `source` command: "source setup_env.sh"

# Create a new conda environment
conda create -y -n api-venv python=3.10
conda activate api-venv

pip install -r requirements-all.txt
