#!/bin/bash

# Running `sh synthesize_speech.sh` will output generated audio ID that can be used as a parameter (11111 here)

curl -s -OJ http://localhost/api/v1/tts/download/11111
