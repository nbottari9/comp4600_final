#!/bin/sh

uv run parallel_download.py 
./vectorize.sh ecr rag-data
