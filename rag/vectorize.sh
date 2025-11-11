#!/bin/bash
html_files=$(ls ./html/*.html)
echo $html_files
mkdir output
# everyone else
ramalama rag $html_files ./output/
# FOR ME AND NICO
# ramalama --engine podman rag $html_files ./output/