#!/bin/bash

# Running `sh generate_image.sh` will output generated image ID that can be used as a parameter (11111 here)

curl -s -OJ http://localhost/api/v1/sd/download/11111
