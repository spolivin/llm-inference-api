#!/bin/bash

HF_TOKEN="${1}"

huggingface-cli login --token $HF_TOKEN
