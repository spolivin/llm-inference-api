#!/bin/bash

# Running `sh generate_image.sh` will output generated image ID that can be used as a parameter (11111 here)

curl -s -OJ http://localhost:8015/download/11111
