#!/bin/bash

huggingface-cli download \
    TheBloke/Llama-2-7b-Chat-GGUF \
    llama-2-7b-chat.Q4_K_M.gguf \
    --local-dir ./models \
    --local-dir-use-symlinks False
