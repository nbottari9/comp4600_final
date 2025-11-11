#!/bin/bash

ecr_repo="620339869704.dkr.ecr.us-east-1.amazonaws.com/gcp_ecr_repository"
html_files=$(ls ./html/*.html)
echo $html_files
mkdir output

# everyone else - local
# ramalama rag $html_files ./output/

# FOR ME AND NICO - mac
# ramalama --engine podman rag $html_files ./output/

# ecr
ramalama --engine podman rag $html_files $ecr_repo
