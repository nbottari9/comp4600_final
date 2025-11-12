#!/bin/bash

ecr_link="620339869704.dkr.ecr.us-east-1.amazonaws.com/gcp_ecr_repository:latest"

mkdir -p output
html_files="./html/"
 
# if local directory, elif local directory Mac, else ECR 
if [ "$1" == "local" ]; then
    ramalama rag $html_files $2
elif [ "$1" == "local-mac" ]; then
    ramalama --engine podman rag $html_files $2
elif [ "$1" == "ECR" ]; then
    aws ecr get-login-password --region us-east-1 | ramalama login --username AWS --password-stdin 620339869704.dkr.ecr.us-east-1.amazonaws.com

    ramalama rag $html_files $2 && podman push $2 $ecr_link
else 
    echo "$0: Usage: $0 <MODE> <DIRECTORY/OCI-IMAGE>"
    exit 1
fi
